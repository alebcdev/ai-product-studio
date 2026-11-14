from unittest.mock import MagicMock

import pytest

from app.services.image_generator import ImageGenerationError
from app.services.image_validator import validate_image_file


def test_validate_image_file_returns_media_type(tmp_path):
    from PIL import Image

    image_path = tmp_path / "image.png"
    Image.new("RGB", (10, 10)).save(image_path)

    assert validate_image_file(image_path) == "image/png"


@pytest.mark.parametrize(
    "path_factory",
    [
        lambda tmp_path: tmp_path / "missing.png",
        lambda tmp_path: _write_invalid_file(tmp_path),
    ],
)
def test_validate_image_file_rejects_invalid_files(tmp_path, path_factory):
    with pytest.raises(ImageGenerationError):
        validate_image_file(path_factory(tmp_path))


def _write_invalid_file(tmp_path):
    path = tmp_path / "invalid.png"
    path.write_bytes(b"not an image")
    return path


def test_validate_image_file_rejects_unknown_format(monkeypatch, tmp_path):
    image_path = tmp_path / "image.bin"
    image_path.touch()
    opened_image = MagicMock()
    opened_image.format = "UNKNOWN"
    opened_image.__enter__.return_value = opened_image
    monkeypatch.setattr(
        "app.services.image_validator.Image.open",
        lambda path: opened_image,
    )

    with pytest.raises(ImageGenerationError, match="invalid image file"):
        validate_image_file(image_path)
