
import pytest
from unittest.mock import Mock
from pathlib import Path

from app.services.image_generator import (
    ImageGenerator,
    ImageGenerationError,
    _extract_path,
)


# --------------------------------------------------
# Tests for _extract_path
# --------------------------------------------------

def test_extract_path_from_string(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.touch()

    result = _extract_path(str(image_path))

    assert result == image_path


def test_extract_path_from_mapping(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.touch()

    result = _extract_path({"path": str(image_path)})

    assert result == image_path


def test_extract_path_from_nested_sequence(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.touch()

    result = _extract_path([None, {"name": str(image_path)}])

    assert result == image_path


def test_extract_path_rejects_unsupported_response():
    with pytest.raises(ImageGenerationError, match="unsupported image response"):
        _extract_path({"url": "https://example.com/image.png"})


# --------------------------------------------------
# Tests for ImageGenerator initialization
# --------------------------------------------------

def test_image_generator_rejects_invalid_concurrency_limit():
    with pytest.raises(ValueError, match="greater than zero"):
        ImageGenerator(client=Mock(), concurrency_limit=0)


# --------------------------------------------------
# Tests for image generation
# --------------------------------------------------

def test_generate_returns_valid_image_path(tmp_path):
    image_path = tmp_path / "generated_image.png"
    image_path.touch()

    client = Mock()
    client.predict.return_value = str(image_path)

    generator = ImageGenerator(client=client)

    result = generator.generate(
        prompt="Professional product photography",
        aspect_radio="4:5",
    )

    assert result == str(image_path)

    client.predict.assert_called_once_with(
        prompt="Professional product photography",
        aspect_radio="4:5",
        api_name="/generate_image",
    )


def test_generate_handles_provider_errors():
    client = Mock()
    client.predict.side_effect = RuntimeError("Connection failed")

    generator = ImageGenerator(client=client)

    with pytest.raises(
        ImageGenerationError,
        match="failed to generate the image",
    ):
        generator.generate(
            prompt="Test prompt",
            aspect_radio="1:1",
        )


def test_generate_rejects_unsupported_response():
    client = Mock()
    client.predict.return_value = {"url": "https://example.com/image.png"}

    generator = ImageGenerator(client=client)

    with pytest.raises(
        ImageGenerationError,
        match="unsupported image response",
    ):
        generator.generate(
            prompt="Test prompt",
            aspect_radio="1:1",
        )


def test_generate_rejects_nonexistent_image_file(tmp_path):
    image_path = tmp_path / "missing_image.png"

    client = Mock()
    client.predict.return_value = str(image_path)

    generator = ImageGenerator(client=client)

    with pytest.raises(
        ImageGenerationError,
        match="unavailable image",
    ):
        generator.generate(
            prompt="Test prompt",
            aspect_radio="1:1",
        )


def test_create_client_wraps_connection_errors(monkeypatch):
    def mock_client(*args, **kwargs):
        raise RuntimeError("Connection failed")

    monkeypatch.setattr(
        "app.services.image_generator.Client",
        mock_client,
    )

    with pytest.raises(
        ImageGenerationError,
        match="currently unavailable",
    ):
        ImageGenerator._create_client()
