from gradio_client import Client

SPACE_ID = "alebcdev/ai-product-studio-space"

class ImageGenerator:
    def __init__(self):
        self.client = Client(SPACE_ID)

    def generate(self, prompt: str, aspect_radio: str):
        result = self.client.predict(
            prompt=prompt,
            aspect_radio=aspect_radio,
            api_name="/generate_image"
        )

        return result