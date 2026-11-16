# AI Product Studio

**Turn product ideas into AI-generated advertising visuals.**

AI Product Studio is a web application that helps small businesses create product advertising images using generative AI. Users can describe a product, choose its category, visual style, colors and aspect ratio, and generate a custom advertising visual.

**Live Demo:** [Try AI Product Studio](https://ai-product-studio-hfsi.onrender.com/)

---

## Overview

AI Product Studio was developed as a portfolio project to explore the practical application of generative AI, Python backend development and user-focused product design.

The application combines a Gradio interface with a FastAPI backend and connects to a Hugging Face Space running FLUX.1-schnell for image generation.

The main goal was to build a complete AI-powered application, from user input and prompt construction to image generation, validation and download.

## Features

- **AI Image Generation:** Generate product advertising visuals using FLUX.1-schnell.
- **Product Customization:** Define the product name, description and category.
- **Visual Direction:** Choose between Minimalist, Luxury, Creative and Natural styles.
- **Color Selection:** Customize primary and secondary colors.
- **Aspect Ratios:** Generate images in 1:1, 4:5 and 16:9 formats.
- **Loading Feedback:** Visual loading state while the image is being generated.
- **Image Preview and Download:** Preview the generated image and download it using a filename based on the product name.
- **Input Validation:** Validate incoming data using Pydantic.
- **Error Handling:** Handle provider failures and invalid image responses.
- **Rate Limiting:** Limit API requests to help prevent excessive usage.

## Tech Stack

| Area | Technologies |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Frontend | Gradio |
| AI Model | FLUX.1-schnell |
| AI Infrastructure | Hugging Face Spaces |
| AI Integration | Gradio Client |
| Data Validation | Pydantic |
| Image Processing | Pillow |
| Configuration | Pydantic Settings |
| Testing | Pytest |
| Deployment | Render |

## Architecture

The application follows a modular structure, separating the user interface, API, business logic and AI integration.

```text
User
  |
  v
Gradio Interface
  |
  v
FastAPI Backend
  |
  v
Input Validation
  |
  v
Prompt Builder
  |
  v
Generation Service
  |
  v
Hugging Face Space
  |
  v
FLUX.1-schnell
  |
  v
Image Validation
  |
  v
Preview and Download
```

### Project Structure

```text
ai-product-studio/
│
├── app/
│   ├── security/
│   │   └── rate_limiter.py
│   │
│   ├── services/
│   │   ├── generation_service.py
│   │   ├── image_generator.py
│   │   ├── image_validator.py
│   │   └── prompt_builder.py
│   │
│   ├── ui/
│   │   ├── components.py
│   │   ├── handlers.py
│   │   ├── interface.py
│   │   ├── options.py
│   │   └── styles.py
│   │
│   ├── config.py
│   ├── main.py
│   └── schemas.py
│
├── tests/
│
├── .gitignore
└── requirements.txt
```

## How It Works

1. The user enters the product name and description.
2. The user selects the product category, advertising style, colors and aspect ratio.
3. The backend validates the input.
4. The prompt builder creates a structured prompt based on the selected options.
5. The generation service sends the request to the Hugging Face Space.
6. FLUX.1-schnell generates the advertising image.
7. The application validates the returned image and makes it available for preview and download.

## Getting Started

### Prerequisites

- Python 3.10 or higher.
- Git.
- A Hugging Face account if you want to configure your own Space or token.

### 1. Clone the repository

```bash
git clone https://github.com/alebcdev/ai-product-studio.git
cd ai-product-studio
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DEBUG=false
HF_SPACE_ID=alebcdev/ai-product-studio-space

# Optional: only configure a token if your Hugging Face setup requires it.
HF_TOKEN=

HF_CONCURRENCY_LIMIT=2
HF_TIMEOUT_SECONDS=120

RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=600
```

**Security note:** Never commit your `.env` file or expose your Hugging Face access token.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open the application at:

`http://127.0.0.1:8000/`

The FastAPI documentation is available at:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/generate` | Generate a product advertising image |
| GET | `/docs` | Interactive API documentation |

### Generate Image

Example request:

```json
{
  "product_name": "Organic Coffee",
  "description": "Premium organic coffee beans with a rich aroma",
  "category": "Food & Beverage",
  "style": "Minimalist",
  "primary_color": "Brown",
  "secondary_color": "Beige",
  "aspect_radio": "1:1"
}
```

The API returns the generated image as a file response.

## Testing

The project includes automated tests using Pytest to validate application behaviour and important components.

Run the test suite with:

```bash
python -m pytest -v
```

## Security and Reliability

Several measures were implemented to improve application reliability:

- Input validation with Pydantic.
- Image file validation using Pillow.
- Centralized error handling for image generation failures.
- Configurable request timeouts and provider concurrency.
- In-memory rate limiting using a sliding time window.
- Environment-based configuration and protected secret handling.
- Logging of generation request duration and unexpected failures.

**Rate limiting note:** The current implementation uses in-memory storage. Limits are local to each application process and reset when the application restarts. It is designed as a lightweight protection mechanism rather than a distributed rate-limiting solution.

## Limitations

- Image generation depends on the availability and performance of the external Hugging Face Space.
- Generation time may vary depending on provider capacity and queue availability.
- The application does not guarantee real-time generation progress percentages.
- Rate limiting is process-local and is not shared across multiple application instances.
- Public demo availability may depend on the hosting provider's service limits and availability.

## What I Learned

Building AI Product Studio helped me gain practical experience in:

- Building and structuring Python applications.
- Developing REST APIs with FastAPI.
- Integrating external generative AI services.
- Designing and improving user interfaces with Gradio.
- Building dynamic prompts for generative AI.
- Validating data and handling errors.
- Implementing basic API security measures.
- Writing automated tests with Pytest.
- Managing configuration and environment variables.
- Deploying an end-to-end AI application.

## About Me

I'm a **Junior Data Analyst with a growing focus on Artificial Intelligence and Python development**.

I created AI Product Studio as a hands-on project to expand my technical skills beyond data analysis and explore how AI can be integrated into practical applications.

I'm particularly interested in the intersection of data, Python, AI and building useful products.

**GitHub:** [@alebcdev](https://github.com/alebcdev)

---

*Built as a personal portfolio project to explore applied generative AI and AI-powered product development.*