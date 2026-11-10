from app.schemas import GenerateRequest
from app.services.prompt_builder import build_prompt
from app.services.image_generator import ImageGenerator

def generator_product_image(data: GenerateRequest) -> tuple[str, str]:
    """
    Generate a product advertising image.

    Returns:
        tuple: (image_path, generated_prompt)
    """
    
    prompt = build_prompt(data)
    generator = ImageGenerator()

    image_path = generator.generate(
        prompt=prompt,
        aspect_radio=data.aspect_radio
    )

    return image_path, prompt