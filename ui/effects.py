from PIL import Image, ImageDraw


def create_ai_gradient(width, height):

    image = Image.new("RGBA", (width, height), (31, 33, 40, 255))

    pixels = image.load()

    for y in range(height):
        for x in range(width):

            distance = (x + y) / (width + height)

            alpha = int((1 - distance) * 35)

            alpha = max(0, min(alpha, 35))

            pixels[x, y] = (255, 255, 255, alpha)

    return image