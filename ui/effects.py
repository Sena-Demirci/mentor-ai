from PIL import Image, ImageDraw


def create_ai_gradient(width, height):

    image = Image.new(
        "RGB",
        (width, height),
        "#1A1B24"
    )

    draw = ImageDraw.Draw(image)

    for i in range(height):

        ratio = i / height

        r = int(26 - ratio * 6)
        g = int(27 - ratio * 6)
        b = int(36 - ratio * 8)

        draw.line(
            (0, i, width, i),
            fill=(r, g, b)
        )

    return image