
import pytest

from app.schemas import GenerateRequest
from app.services.prompt_builder import build_prompt, STYLE_DESCRIPTIONS


@pytest.fixture
def valid_request():
    return GenerateRequest(
        product_name="Coffee",
        description="Premium roasted coffee beans",
        category="Food & Beverage",
        style="Minimalist",
        primary_color="Black",
        secondary_color="Gold",
    )


def test_build_prompt_returns_non_empty_string(valid_request):
    prompt = build_prompt(valid_request)

    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_prompt_includes_product_information(valid_request):
    prompt = build_prompt(valid_request)

    assert "Coffee" in prompt
    assert "Premium roasted coffee beans" in prompt
    assert "Food & Beverage" in prompt


def test_prompt_includes_selected_colors(valid_request):
    prompt = build_prompt(valid_request)

    assert "Primary color: Black" in prompt
    assert "Secondary color: Gold" in prompt


@pytest.mark.parametrize(
    ("style", "expected_description"),
    [
        (
            "Minimalist",
            "clean minimalist composition, simple background, elegant lighting",
        ),
        (
            "Luxury",
            "premium luxury advertising, sophisticated lighting, elegant composition",
        ),
        (
            "Creative",
            "bold creative advertising, vibrant composition, artistic presentation",
        ),
        (
            "Natural",
            "organic natural advertising, soft daylight, earthy atmosphere",
        ),
    ],
)
def test_prompt_includes_correct_style(valid_request, style, expected_description):
    valid_request.style = style

    prompt = build_prompt(valid_request)

    assert expected_description in prompt


def test_prompt_includes_general_advertising_instructions(valid_request):
    prompt = build_prompt(valid_request)

    assert "High quality advertising photography" in prompt
    assert "balanced composition" in prompt
    assert "professional studio lighting" in prompt
    assert "visually appealing product presentation" in prompt


def test_prompt_excludes_text_watermarks_and_logos(valid_request):
    prompt = build_prompt(valid_request)

    assert "No text" in prompt
    assert "no watermark" in prompt
    assert "no logo" in prompt
