from typing import Literal
from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    product_name: str = Field(
        min_length=2,
        max_length=80
    )

    description: str = Field(
        min_length=5,
        max_length=300
    )


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