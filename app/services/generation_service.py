from app.schemas import GenerateRequest
from app.services.prompt_builder import build_prompt
from app.services.image_generator import ImageGenerator, get_image_generator

def generator_product_image(
    data: GenerateRequest,
    generator: ImageGenerator | None = None,
) -> tuple[str, str]:
    """
    Generate a product advertising image.

    Returns:
        tuple: (image_path, generated_prompt)
    """
    
    prompt = build_prompt(data)
    image_generator = generator or get_image_generator()

    image_path = image_generator.generate(
        prompt=prompt,
        aspect_radio=data.aspect_radio
    )

    return image_path, prompt