
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.security.rate_limiter import RateLimiter
from app.services.image_generator import ImageGenerationError


@pytest.fixture(autouse=True)
def reset_rate_limiter(monkeypatch):
    limiter = RateLimiter(max_requests=5, window_seconds=600)
    monkeypatch.setattr("app.main.rate_limiter", limiter)


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


def test_generate_endpoint_handles_missing_image(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "missing_image.png"

    def mock_generator(data):
        return str(image_path), "Test prompt"

    monkeypatch.setattr("app.main.generator_product_image", mock_generator)

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The image provider is currently unavailable."
    }


def test_generate_endpoint_handles_corrupt_image(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "corrupt_image.png"
    image_path.write_bytes(b"not a valid image")

    def mock_generator(data):
        return str(image_path), "Test prompt"

    monkeypatch.setattr("app.main.generator_product_image", mock_generator)

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The image provider is currently unavailable."
    }


def test_generate_endpoint_rejects_non_image_file(
    client, valid_payload, monkeypatch, tmp_path
):
    file_path = tmp_path / "response.png"
    file_path.write_text("not an image")

    def mock_generator(data):
        return str(file_path), "Test prompt"

    monkeypatch.setattr("app.main.generator_product_image", mock_generator)

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The image provider is currently unavailable."
    }


def test_generate_endpoint_rejects_unrecognized_image_format(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "image.bin"
    image_path.touch()
    opened_image = MagicMock()
    opened_image.format = "UNKNOWN"
    opened_image.__enter__.return_value = opened_image
    monkeypatch.setattr(
        "app.services.image_validator.Image.open",
        lambda path: opened_image,
    )

    def mock_generator(data):
        return str(image_path), "Test prompt"

    monkeypatch.setattr("app.main.generator_product_image", mock_generator)

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The image provider is currently unavailable."
    }


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


def test_generate_endpoint_allows_requests_up_to_limit(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "generated_image.png"
    Image.new("RGB", (100, 100)).save(image_path)
    generator = MagicMock(return_value=(str(image_path), "Test prompt"))
    monkeypatch.setattr("app.main.generator_product_image", generator)

    responses = [
        client.post("/generate", json=valid_payload)
        for _ in range(5)
    ]

    assert all(response.status_code == 200 for response in responses)
    assert generator.call_count == 5


def test_generate_endpoint_rejects_request_after_limit(
    client, valid_payload, monkeypatch, tmp_path
):
    image_path = tmp_path / "generated_image.png"
    Image.new("RGB", (100, 100)).save(image_path)
    generator = MagicMock(return_value=(str(image_path), "Test prompt"))
    monkeypatch.setattr("app.main.generator_product_image", generator)

    for _ in range(5):
        assert client.post("/generate", json=valid_payload).status_code == 200

    response = client.post("/generate", json=valid_payload)

    assert response.status_code == 429
    assert response.headers["retry-after"].isdigit()
    assert generator.call_count == 5


def test_rate_limiter_allows_requests_after_window_expires():
    current_time = [0.0]
    limiter = RateLimiter(
        max_requests=1,
        window_seconds=10,
        clock=lambda: current_time[0],
    )

    assert limiter.check("client")[0] is True
    assert limiter.check("client")[0] is False
    current_time[0] = 10.0
    assert limiter.check("client")[0] is True


def test_rate_limiter_keeps_clients_independent():
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=lambda: 0.0)

    assert limiter.check("client-a")[0] is True
    assert limiter.check("client-a")[0] is False
    assert limiter.check("client-b")[0] is True


def test_invalid_requests_do_not_consume_rate_limit(
    client, valid_payload, monkeypatch, tmp_path
):
    valid_payload["style"] = "Vintage"

    for _ in range(5):
        assert client.post("/generate", json=valid_payload).status_code == 422

    image_path = tmp_path / "generated_image.png"
    Image.new("RGB", (100, 100)).save(image_path)
    monkeypatch.setattr(
        "app.main.generator_product_image",
        MagicMock(return_value=(str(image_path), "Test prompt")),
    )
    valid_payload["style"] = "Minimalist"
    assert client.post("/generate", json=valid_payload).status_code == 200
