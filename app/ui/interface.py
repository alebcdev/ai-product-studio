import gradio as gr

from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image

CATEGORIES = [
    "Food & Beverage",
    "Beauty & Skincare",
    "Technology",
    "Fashion",
    "Home & Lifestyle"
]

STYLES = [
    "Minimalist",
    "Luxury",
    "Creative",
    "Natural"
]

COLORS = [
    "Black",
    "White",
    "Beige",
    "Brown",
    "Green",
    "Blue",
    "Pink",
    "Red",
    "Gold"
]

ASPECT_RATIOS = ["1:1", "4:5", "16:9"]

def generate_creative(
    product_name,
    description,
    category,
    style,
    primary_color,
    secondary_color,
    aspect_radio
):
    try:
        data = GenerateRequest(
            product_name=product_name,
            description=description,
            category=category,
            style=style,
            primary_color=primary_color,
            secondary_color=secondary_color,
            aspect_radio=aspect_radio
        )

        image_path, prompt = generator_product_image(data)

        return (
            image_path,
            image_path,
            f"Image generated successfully.\n\nPrompt: {prompt}"
        )

    except Exception as error:
        return (
            None,
            None,
            f"**Error:** {error}"
        )

with gr.Blocks(title="AI Product Studio") as demo:
    gr.Markdown(
                """
        # AI Product Studio

        ### Create AI-powered advertising visuals for your products.

        Describe your product, choose a visual style and generate
        a professional advertising image.
        """
    )

    with gr.Row():
        with gr.Column():
            product_name = gr.Textbox(
                label="Product name",
                placeholder="e.g. Premium Coffee",
                max_lines=1
            )

            description = gr.Textbox(
                label="Product description",
                placeholder="Describe your product...",
                lines=3
            )

            category = gr.Dropdown(
                choices=CATEGORIES,
                label="Product category",
                value="Food & Beverage"
            )

            style = gr.Radio(
                choices=STYLES,
                label="Advertising style",
                value="Minimalist"
            )

            primary_color = gr.Dropdown(
                choices=COLORS,
                label="Primary color",
                value="Black"
            )

            secondary_color = gr.Dropdown(
                choices=COLORS,
                label="Secondary color",
                value="Beige"
            )

            aspect_ratio = gr.Radio(
                choices=ASPECT_RATIOS,
                label="Image format",
                value="1:1"
            )

            generate_button = gr.Button(
                "Generate advertising image",
                variant="primary"
            )

        with gr.Column():
            
            image_output = gr.Image(
                label="Generated advertising image",
                type="filepath"
            )

            download_output = gr.File(
                label="Download your image"
            )

    status_output = gr.Markdown()
    generate_button.click(
        fn=generate_creative,
        inputs=[
            product_name,
            description,
            category,
            style,
            primary_color,
            secondary_color,
            aspect_ratio
        ],
        outputs=[
            image_output,
            download_output,
            status_output
        ]
    )

