from __future__ import annotations

import logging
import os
from collections.abc import Mapping, Sequence
from functools import lru_cache
from pathlib import Path
from threading import BoundedSemaphore

from gradio_client import Client

from app.config import settings

logger = logging.getLogger(__name__)


class ImageGenerationError(RuntimeError):
    """Raised when the remote image generation cannot produce a valid image."""


def _extract_path(result: object) -> Path:
    if isinstance(result, (str, os.PathLike)):
        return Path(result)
    if isinstance(result, Mapping):
        for key in ("path", "name"):
            value = result.get(key)
            if isinstance(value, (str, os.PathLike)):
                return Path(value)
    if isinstance(result, Sequence) and not isinstance(result, (str, bytes, bytearray)):
        for item in result:
            try:
                return _extract_path(item)
            except ImageGenerationError:
                continue
    raise ImageGenerationError("The provider returned an unsupported image response.")

class ImageGenerator:
    def __init__(
        self,
        client: object | None = None,
        concurrency_limit: int | None = None,
    ):
        self.client = client if client is not None else self._create_client()
        limit = (
            concurrency_limit
            if concurrency_limit is not None
            else settings.hf_concurrency_limit
        )
        if limit < 1:
            raise ValueError("concurrency_limit must be greater than zero")
        self._semaphore = BoundedSemaphore(limit)

    @staticmethod
    def _create_client() -> Client:
        try:
            token = settings.hf_token.get_secret_value() if settings.hf_token else None
            return Client(
                settings.hf_space_id,
                token=token,
                httpx_kwargs={"timeout": settings.hf_timeout_seconds},
            )
        except Exception as error:
            logger.exception("Unable to connect to the Hugging Face Space")
            raise ImageGenerationError(
                "The image provider is currently unavailable."
            ) from error

    def generate(self, prompt: str, aspect_radio: str) -> str:
        try:
            with self._semaphore:
                result = self.client.predict(
                    prompt=prompt,
                    aspect_radio=aspect_radio,
                    api_name="/generate_image",
                )
        except Exception as error:
            logger.exception("Hugging Face image generation failed")
            raise ImageGenerationError(
                "The image provider failed to generate the image."
            ) from error

        image_path = _extract_path(result)
        if not image_path.is_file():
            raise ImageGenerationError("The provider returned an unavailable image.")
        return str(image_path)


@lru_cache(maxsize=1)
def get_image_generator() -> ImageGenerator:
    """Create one lazy generator so importing the application does not connect."""
    return ImageGenerator()