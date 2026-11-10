from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import gradio as gr

from app.config import settings
from app.schemas import GenerateRequest
from app.services.generation_service import generator_product_image
from app.ui.interface import demo

app = FastAPI(
    title=settings.app_name,
    description="API for generating AI-powered product advertising creatives.",
    version=settings.app_version,
    debug=settings.debug
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/generate")
def generate_image(data: GenerateRequest):
    try:
        image_path, prompt = generator_product_image(data)

        return FileResponse(
            path=image_path,
            media_type="image/webp",
            filename="ai-product-studio.webp",
            headers={
                "X-Generated-Prompt": prompt
            }
        )

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Image generation failed: {str(error)}"
        )


app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)
