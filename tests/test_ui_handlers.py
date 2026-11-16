from pathlib import Path

from PIL import Image

from app.ui.handlers import generate_creative


def _updates(monkeypatch, tmp_path, generator):
    image_path = Path(tmp_path) / "generated.png"
    Image.new("RGB", (10, 10)).save(image_path)
    monkeypatch.setattr("app.ui.handlers.generator_product_image", generator)
    return list(
        generate_creative(
            "Coffee",
            "Roasted coffee",
            "Food & Beverage",
            "Minimalist",
            "Black",
            "Beige",
            "1:1",
        )
    )


def test_generate_creative_shows_and_hides_loading_state(
    monkeypatch, tmp_path
):
    updates = _updates(
        monkeypatch,
        tmp_path,
        lambda request: (str(Path(tmp_path) / "generated.png"), "prompt"),
    )

    assert updates[0][4]["visible"] is True
    assert updates[0][5]["interactive"] is False
    assert updates[1][4]["visible"] is False
    assert updates[1][5]["interactive"] is True
    assert updates[1][6]["interactive"] is True


def test_generate_creative_hides_loading_state_after_error(monkeypatch):
    def fail(_request):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr("app.ui.handlers.generator_product_image", fail)
    updates = list(
        generate_creative(
            "Coffee",
            "Roasted coffee",
            "Food & Beverage",
            "Minimalist",
            "Black",
            "Beige",
            "1:1",
        )
    )

    assert updates[1][4]["visible"] is False
    assert updates[1][5]["interactive"] is True
    assert updates[1][2]["visible"] is True
