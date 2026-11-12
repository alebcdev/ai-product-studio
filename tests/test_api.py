
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services.image_generator import ImageGenerationError


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_payload():
    return {
        "product_name": "Coffee",
        "description": "Premium roasted coffee beans",
        "category": "Food & Beverage",
        "style": "Minimalist",
        "primary_color": "Black",
        "secondary_color": "Gold",
        "aspect_radio": "4:5",
    }


def test_health_endpoint_returns_healthy_status(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "provider": "remote",
    }


def test_generate_endpoint_returns_image(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "generated_image.png"
    Image.new("RGB", (100, 100)).save(image_path)

    def mock_generator(data):
        return str(image_path), "Test prompt"

    monkeypatch.setattr(
        "app.main.generator_product_image",
        mock_generator,
    )

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert "attachment" in response.headers["content-disposition"]
    assert response.content == image_path.read_bytes()


def test_generate_endpoint_rejects_invalid_data(client, valid_payload):
    valid_payload["style"] = "Vintage"

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 422


def test_generate_endpoint_handles_provider_errors(
    client, valid_payload, monkeypatch
):
    def mock_generator(data):
        raise ImageGenerationError("Provider unavailable")

    monkeypatch.setattr(
        "app.main.generator_product_image",
        mock_generator,
    )

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The image provider is currently unavailable."
    }


def test_generate_endpoint_handles_unexpected_errors(
    client, valid_payload, monkeypatch
):
    def mock_generator(data):
        raise RuntimeError("Unexpected internal error")

    monkeypatch.setattr(
        "app.main.generator_product_image",
        mock_generator,
    )

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 500
    assert response.json() == {
        "detail": "The image could not be generated."
    }
