from app.schemas import GenerateRequest

STYELE_DESCRIPTIONS = {
    "Minimalist": "clean minimalist composition, simple background, elegant lighting",
    "Luxury": "premium luxury advertising, sophisticated lighting, elegant composition",
    "Creative": "bold creative advertising, vibrant composition, artistic presentation",
    "Natural": "organic natural advertising, soft daylight, earthy atmosphere"    
}

def build_prompt(data: GenerateRequest) -> str:
    style_description = STYELE_DESCRIPTIONS[data.style]

    prompt = (
        f"Professional commercial product photography of {data.product_name}. "
        f"{data.description}. "
        f"Product category: {data.category}. "
        f"Visual style: {style_description}. "
        f"Primary color: {data.primary_color}. "
        f"Secondary color: {data.secondary_color}. "
        "High quality advertising photography, balanced composition, "
        "professional studio lighting, visually appealing product presentation. "
        "No text, no watermark, no logo."
    )

    return prompt