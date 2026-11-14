from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app.services.image_generator import ImageGenerationError


def validate_image_file(path: Path) -> str:
    if not path.is_file():
        raise ImageGenerationError("The provider returned an unavailable image.")

    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image_format = image.format
    except (
        FileNotFoundError,
        IsADirectoryError,
        PermissionError,
        OSError,
        UnidentifiedImageError,
    ) as error:
        raise ImageGenerationError(
            "The provider returned an invalid image file."
        ) from error

    media_type = Image.MIME.get(image_format, "")
    if not image_format or not media_type.startswith("image/"):
        raise ImageGenerationError("The provider returned an invalid image file.")

    return media_type
