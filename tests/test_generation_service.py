
import pytest
from unittest.mock import Mock

from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image
from app.services.prompt_builder import build_prompt


@pytest.fixture
def valid_request():
    return GenerateRequest(
        product_name="Coffee",
        description="Premium roasted coffee beans",
        category="Food & Beverage",
        style="Minimalist",
        primary_color="Black",
        secondary_color="Gold",
        aspect_radio="4:5",
    )


def test_generator_product_image_builds_prompt(valid_request):
    generator = Mock()
    generator.generate.return_value = "generated_image.webp"

    generator_product_image(valid_request, generator)

    expected_prompt = build_prompt(valid_request)

    generator.generate.assert_called_once_with(
        prompt=expected_prompt,
        aspect_radio="4:5",
    )


def test_generator_product_image_returns_path_and_prompt(valid_request):
    generator = Mock()
    generator.generate.return_value = "generated_image.webp"

    image_path, prompt = generator_product_image(valid_request, generator)

    assert image_path == "generated_image.webp"
    assert prompt == build_prompt(valid_request)


def test_generator_product_image_uses_default_generator(
    valid_request, monkeypatch
):
    generator = Mock()
    generator.generate.return_value = "generated_image.webp"

    monkeypatch.setattr(
        "app.services.generation_service.get_image_generator",
        lambda: generator,
    )

    image_path, prompt = generator_product_image(valid_request)

    assert image_path == "generated_image.webp"
    assert prompt == build_prompt(valid_request)

    generator.generate.assert_called_once_with(
        prompt=prompt,
        aspect_radio="4:5",
    )


def test_generator_product_image_propagates_generation_errors(valid_request):
    generator = Mock()
    generator.generate.side_effect = RuntimeError("Generation failed")

    with pytest.raises(RuntimeError, match="Generation failed"):
        generator_product_image(valid_request, generator)
