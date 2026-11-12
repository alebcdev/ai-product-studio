import pytest
from pydantic import ValidationError

from app.schemas import GenerateRequest


@pytest.fixture
def valid_payload():
    return {
        "product_name": "Coffee",
        "description": "Premium roasted coffee beans",
        "category": "Food & Beverage",
        "style": "Minimalist",
        "primary_color": "Black",
        "secondary_color": "Gold",
    }


def test_valid_request_is_accepted(valid_payload):
    request = GenerateRequest(**valid_payload)

    assert request.product_name == "Coffee"
    assert request.description == "Premium roasted coffee beans"


def test_text_fields_are_stripped(valid_payload):
    valid_payload["product_name"] = "  Coffee  "
    valid_payload["description"] = "  Premium roasted coffee beans  "

    request = GenerateRequest(**valid_payload)

    assert request.product_name == "Coffee"
    assert request.description == "Premium roasted coffee beans"


@pytest.mark.parametrize(
    "field",
    ["product_name", "description"],
)
def test_empty_text_fields_are_rejected(valid_payload, field):
    valid_payload[field] = "   "

    with pytest.raises(ValidationError):
        GenerateRequest(**valid_payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("product_name", "A"),
        ("product_name", "C" * 81),
        ("description", "Test"),
        ("description", "D" * 301),
    ],
)
def test_invalid_text_lengths_are_rejected(valid_payload, field, value):
    valid_payload[field] = value

    with pytest.raises(ValidationError):
        GenerateRequest(**valid_payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("category", "Electronics"),
        ("style", "Vintage"),
        ("primary_color", "Purple"),
        ("secondary_color", "Orange"),
        ("aspect_radio", "3:2"),
    ],
)
def test_invalid_options_are_rejected(valid_payload, field, value):
    valid_payload[field] = value

    with pytest.raises(ValidationError):
        GenerateRequest(**valid_payload)


def test_default_aspect_radio_is_square(valid_payload):
    request = GenerateRequest(**valid_payload)

    assert request.aspect_radio == "1:1"


@pytest.mark.parametrize(
    "aspect_radio",
    ["1:1", "4:5", "16:9"],
)
def test_supported_aspect_ratios_are_accepted(valid_payload, aspect_radio):
    valid_payload["aspect_radio"] = aspect_radio

    request = GenerateRequest(**valid_payload)

    assert request.aspect_radio == aspect_radio
