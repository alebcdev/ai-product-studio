"""Event handlers for the Gradio interface."""

import logging
from collections.abc import Iterator
from pathlib import Path

import gradio as gr
from PIL import Image

from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image
from app.services.image_validator import validate_image_file

logger = logging.getLogger(__name__)


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

        yield (
            gr.update(value=image_path, visible=True),
            gr.update(value=image_path, visible=True),
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
