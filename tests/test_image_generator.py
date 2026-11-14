
from pathlib import Path
from unittest.mock import Mock

import pytest
from pydantic import SecretStr

from app.config import settings
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


def test_create_client_without_token_passes_none_to_client(monkeypatch):
    client_factory = Mock(return_value=Mock())
    monkeypatch.setattr("app.services.image_generator.Client", client_factory)
    monkeypatch.setattr(settings, "hf_token", None)

    ImageGenerator._create_client()

    client_factory.assert_called_once_with(
        settings.hf_space_id,
        token=None,
        httpx_kwargs={"timeout": settings.hf_timeout_seconds},
    )


def test_create_client_passes_secret_token_value(monkeypatch):
    client_factory = Mock(return_value=Mock())
    monkeypatch.setattr("app.services.image_generator.Client", client_factory)
    monkeypatch.setattr(settings, "hf_token", SecretStr("test-token"))

    ImageGenerator._create_client()

    client_factory.assert_called_once_with(
        settings.hf_space_id,
        token="test-token",
        httpx_kwargs={"timeout": settings.hf_timeout_seconds},
    )


def test_connection_error_does_not_expose_token_in_message_or_logs(
    monkeypatch, caplog
):
    secret_token = "test-token"

    def mock_client(*args, **kwargs):
        raise RuntimeError("Connection failed")

    monkeypatch.setattr("app.services.image_generator.Client", mock_client)
    monkeypatch.setattr(settings, "hf_token", SecretStr(secret_token))

    with caplog.at_level("ERROR"):
        with pytest.raises(ImageGenerationError) as error:
            ImageGenerator._create_client()

    assert secret_token not in str(error.value)
    assert secret_token not in caplog.text


def test_generation_error_does_not_expose_provider_details():
    client = Mock()
    client.predict.side_effect = RuntimeError("provider internals")
    generator = ImageGenerator(client=client)

    with pytest.raises(ImageGenerationError) as error:
        generator.generate(prompt="Test prompt", aspect_radio="1:1")

    assert str(error.value) == "The image provider failed to generate the image."
