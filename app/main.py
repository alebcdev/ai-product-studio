import logging
import mimetypes
from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
import gradio as gr
from PIL import Image

from app.config import settings
from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image
from app.services.image_generator import ImageGenerationError
from app.ui.interface import CSS, THEME, demo

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="API for generating AI-powered product advertising creatives.",
    version=settings.app_version,
    debug=settings.debug
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "provider": "remote",
    }

@app.post("/generate")
async def generate_image(data: GenerateRequest, request: Request):
    started_at = perf_counter()
    try:
        image_path, _prompt = await run_in_threadpool(generator_product_image, data)
        path = Path(image_path)
        with Image.open(path) as image:
            image_format = image.format
        media_type = (
            Image.MIME.get(image_format, "")
            if image_format
            else mimetypes.guess_type(path.name)[0]
        )
        if not media_type or not media_type.startswith("image/"):
            raise ImageGenerationError("The provider returned a non-image file.")

        return FileResponse(
            path=path,
            media_type=media_type,
            filename=path.name,
        )
    except ImageGenerationError as error:
        logger.warning("Image request failed: %s", error)
        raise HTTPException(
            status_code=502, detail="The image provider is currently unavailable."
        ) from error
    except Exception as error:
        logger.exception("Unexpected image request failure")
        raise HTTPException(
            status_code=500, detail="The image could not be generated."
        ) from error
    finally:
        logger.info(
            "Image request completed in %.3fs from %s",
            perf_counter() - started_at,
            request.client.host if request.client else "unknown",
        )


app = gr.mount_gradio_app(
    app,
    demo,
    path="/",
    theme=THEME,
    css=CSS
)
