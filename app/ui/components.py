"""Reusable Gradio component builders for the product studio UI."""

import gradio as gr

from app.ui.options import ASPECT_RATIOS, CATEGORIES, COLORS, STYLES
from app.ui.styles import EMPTY_STATE


def build_header() -> gr.HTML:
    return gr.HTML(
        """
        <header class="studio-header">
            <div class="studio-eyebrow">
                <span class="studio-mark">✦</span>
                AI creative workspace
            </div>
            <h1>AI Product Studio</h1>
            <p>Turn product details into polished advertising visuals in seconds.</p>
        </header>
        """
    )


def build_product_configuration() -> tuple:
    with gr.Column(scale=5, elem_classes="studio-panel"):
        gr.Markdown("### Product configuration")
        gr.Markdown(
            "Define the product and visual direction for your creative.",
            elem_classes="panel-intro",
        )

        gr.Markdown(
            "#### 01 &nbsp; Product information\n"
            "Tell us what you are promoting.",
            elem_classes="section-heading",
        )
        product_name = gr.Textbox(
            label="Product name",
            placeholder="e.g. Premium Coffee",
            max_lines=1,
        )
        description = gr.Textbox(
            label="Product description",
            placeholder="Describe your product, its benefits and audience...",
            lines=2,
        )
        category = gr.Dropdown(
            choices=CATEGORIES,
            label="Product category",
            value="Food & Beverage",
        )

        gr.Markdown(
            "#### 02 &nbsp; Visual identity\n"
            "Choose the look and feel of the image.",
            elem_classes="section-heading",
        )
        style = gr.Radio(
            choices=STYLES,
            label="Advertising style",
            value="Minimalist",
            elem_classes="centered-options",
        )
        with gr.Row(elem_classes="form-row"):
            primary_color = gr.Dropdown(
                choices=COLORS,
                label="Primary color",
                value="Black",
                scale=1,
            )
            secondary_color = gr.Dropdown(
                choices=COLORS,
                label="Secondary color",
                value="Beige",
                scale=1,
            )

        gr.Markdown(
            "#### 03 &nbsp; Output settings\n"
            "Set the composition for your final creative.",
            elem_classes="section-heading",
        )
        aspect_ratio = gr.Radio(
            choices=ASPECT_RATIOS,
            label="Image format",
            value="1:1",
            elem_classes="centered-options",
        )
        generate_button = gr.Button(
            "Generate advertising image",
            variant="primary",
            elem_classes="generate-button",
        )

    return (
        product_name,
        description,
        category,
        style,
        primary_color,
        secondary_color,
        aspect_ratio,
        generate_button,
    )


def build_result_panel() -> tuple:
    with gr.Column(
        scale=6,
        elem_classes=["studio-panel", "result-panel"],
    ):
        with gr.Row(elem_classes="result-heading"):
            gr.Markdown("### Generated creative")
            gr.HTML('<span class="result-badge">AI powered</span>')

        empty_state = gr.HTML(EMPTY_STATE)
        image_output = gr.Image(
            label="Generated advertising image",
            type="filepath",
            show_label=False,
            elem_classes="result-image",
            visible=False,
        )
        download_output = gr.DownloadButton(
            label="Download image",
            value=None,
            elem_classes="download-output",
            visible=False,
        )
        status_output = gr.Markdown(elem_classes="status-output", visible=False)
        regenerate_button = gr.Button(
            "Generate another version",
            variant="secondary",
            elem_classes="regenerate-button",
        )

    return (
        empty_state,
        image_output,
        download_output,
        status_output,
        regenerate_button,
    )
