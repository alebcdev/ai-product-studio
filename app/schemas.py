from typing import Literal

from pydantic import BaseModel, Field, field_validator

class GenerateRequest(BaseModel):
    product_name: str = Field(
        min_length=2,
        max_length=80
    )

    description: str = Field(
        min_length=5,
        max_length=300
    )

    @field_validator("product_name", "description", mode="before")
    @classmethod
    def strip_text(cls, value: object) -> object:
        if not isinstance(value, str):
            return value

        value = value.strip()
        if not value:
            raise ValueError("must not be empty or contain only whitespace")
        return value


    category: Literal[
        "Food & Beverage",
        "Beauty & Skincare",
        "Technology",
        "Fashion",
        "Home & Lifestyle"
    ]    

    style: Literal[
        "Minimalist",
        "Luxury",
        "Creative",
        "Natural"
    ]

    primary_color: Literal[
        "Black", "White", "Beige", "Brown", "Green",
        "Blue", "Pink", "Red", "Gold"
    ]

    secondary_color: Literal[
        "Black", "White", "Beige", "Brown", "Green",
        "Blue", "Pink", "Red", "Gold"
    ]

    aspect_radio: Literal[
        "1:1",
        "4:5",
        "16:9"
    ] = "1:1"