"""Application entry point for the Gradio interface."""

import gradio as gr

from app.ui.components import (
    build_header,
    build_product_configuration,
    build_result_panel,
)
from app.ui.handlers import generate_creative
from app.ui.styles import CSS, THEME


def create_demo() -> gr.Blocks:
    """Build and wire the AI Product Studio interface."""
    with gr.Blocks(title="AI Product Studio") as demo:
        with gr.Column(elem_classes="studio-shell"):
            build_header()

            with gr.Row(elem_classes="studio-grid"):
                form_components = build_product_configuration()
                result_components = build_result_panel()

            (
                product_name,
                description,
                category,
                style,
                primary_color,
                secondary_color,
                aspect_ratio,
                generate_button,
            ) = form_components
            (
                empty_state,
                image_output,
                download_output,
                status_output,
                regenerate_button,
            ) = result_components
            generation_inputs = [
                product_name,
                description,
                category,
                style,
                primary_color,
                secondary_color,
                aspect_ratio,
            ]

            generate_button.click(
                fn=generate_creative,
                inputs=generation_inputs,
                outputs=[
                    image_output,
                    download_output,
                    status_output,
                    empty_state,
                ],
                show_progress="full",
            )
            regenerate_button.click(
                fn=generate_creative,
                inputs=generation_inputs,
                outputs=[
                    image_output,
                    download_output,
                    status_output,
                    empty_state,
                ],
                show_progress="full",
            )

    return demo


demo = create_demo()

__all__ = ["CSS", "THEME", "create_demo", "demo", "generate_creative"]
