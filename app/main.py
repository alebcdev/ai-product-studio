import logging
from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
import gradio as gr

from app.config import settings
from app.schemas import GenerateRequest
from app.security.rate_limiter import RateLimiter
from app.services.generation_service import generator_product_image
from app.services.image_generator import ImageGenerationError
from app.services.image_validator import validate_image_file
from app.ui.interface import CSS, THEME, demo

logger = logging.getLogger(__name__)

rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)


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
    client_id = request.client.host if request.client else "unknown-client"
    allowed, retry_after = rate_limiter.check(client_id)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )

    started_at = perf_counter()
    try:
        image_path, _prompt = await run_in_threadpool(generator_product_image, data)
        path = Path(image_path)
        media_type = validate_image_file(path)

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
            "Image generation request completed in %.3fs",
            perf_counter() - started_at,
        )


app = gr.mount_gradio_app(
    app,
    demo,
    path="/",
    theme=THEME,
    css=CSS
)
