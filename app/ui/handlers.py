"""Event handlers for the Gradio interface."""

import logging
import re
import shutil
import unicodedata
from collections.abc import Iterator
from pathlib import Path

import gradio as gr
from PIL import Image

from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image
from app.services.image_validator import validate_image_file

logger = logging.getLogger(__name__)

_MAX_DOWNLOAD_NAME_LENGTH = 80
_WINDOWS_RESERVED_NAMES = {
    "aux",
    "com1",
    "com2",
    "com3",
    "com4",
    "con",
    "lpt1",
    "lpt2",
    "lpt3",
    "nul",
    "prn",
}


def _normalize_download_name(product_name: str) -> str:
    """Return a safe, concise filename stem from a product name."""
    normalized = unicodedata.normalize("NFKD", product_name)
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    normalized = normalized[:_MAX_DOWNLOAD_NAME_LENGTH].rstrip("-")

    if not normalized or normalized in _WINDOWS_RESERVED_NAMES:
        return "generated-image"
    return normalized


def _image_extension(image_path: Path) -> str:
    """Return an extension matching the image format stored in the file."""
    with Image.open(image_path) as image:
        image_format = image.format

    if not image_format:
        raise ValueError("Generated image has no recognized format.")

    preferred_extensions = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }
    if image_format in preferred_extensions:
        return preferred_extensions[image_format]

    for extension, registered_format in Image.registered_extensions().items():
        if registered_format == image_format:
            return extension.lower()

    raise ValueError(f"Unsupported generated image format: {image_format}")


def _prepare_download_file(image_path: str, product_name: str) -> str:
    """Create a named byte-for-byte copy for the Gradio download."""
    source_path = Path(image_path)
    filename = f"{_normalize_download_name(product_name)}{_image_extension(source_path)}"
    download_path = source_path.with_name(filename)

    if download_path != source_path:
        shutil.copyfile(source_path, download_path)
    return str(download_path)


def _image_details(image_path: str, aspect_radio: str) -> str:
    """Return user-facing image metadata without failing the generation flow."""
    try:
        with Image.open(image_path) as image:
            dimensions = f"{image.width} x {image.height}px"
            image_format = image.format or "Image"
            return f"Format: **{aspect_radio}** | {image_format} | {dimensions}"
    except (OSError, ValueError):
        return f"Format: **{aspect_radio}**"


def generate_creative(
    product_name: str,
    description: str,
    category: str,
    style: str,
    primary_color: str,
    secondary_color: str,
    aspect_radio: str,
) -> Iterator[tuple[dict, dict, dict, dict, dict, dict, dict]]:
    """Generate a creative while exposing clear UI states to Gradio."""
    yield (
        gr.update(value=None, visible=False),
        gr.update(value=None, visible=False),
        gr.update(value=None, visible=False),
        gr.update(value=None, visible=False),
        gr.update(visible=True),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )

    try:
        request = GenerateRequest(
            product_name=product_name,
            description=description,
            category=category,
            style=style,
            primary_color=primary_color,
            secondary_color=secondary_color,
            aspect_radio=aspect_radio,
        )
        image_path, _prompt = generator_product_image(request)
        validate_image_file(Path(image_path))
        download_path = _prepare_download_file(image_path, product_name)

        yield (
            gr.update(value=image_path, visible=True),
            gr.update(value=download_path, visible=True),
            gr.update(
                value=(
                    "### Your creative is ready\n\n"
                    f"{_image_details(image_path, aspect_radio)} | "
                    "Use the download button to save the full-resolution image."
                ),
                visible=True,
            ),
            gr.update(value=None, visible=False),
            gr.update(visible=False),
            gr.update(interactive=True),
            gr.update(interactive=True),
        )
    except Exception:
        logger.exception("Creative generation failed")
        yield (
            gr.update(value=None, visible=False),
            gr.update(value=None, visible=False),
            gr.update(
                value=(
                    "### We couldn't generate that creative\n\n"
                    "Please review the product details and try again. "
                    "Your form is still available."
                ),
                visible=True,
            ),
            gr.update(value=None, visible=False),
            gr.update(visible=False),
            gr.update(interactive=True),
            gr.update(interactive=True),
        )
