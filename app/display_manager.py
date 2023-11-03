from PIL import Image, ImageDraw, ImageFont
import ST7789 as ST7789

class DisplayManager:
    def __init__(self):
        self.display = ST7789.ST7789(
            height=240,
            width=240,
            rotation=90,
            port=0,
            cs=ST7789.BG_SPI_CS_FRONT,
            dc=9,
            backlight=19,
            spi_speed_hz=80 * 1000 * 1000
        )
        self.display.begin()

    def display_message(self, message):
        image = Image.new("RGB", (self.display.width, self.display.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font_size = 20
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

        # Calculate width and height of the text to be centered
        w, h = draw.textsize(message, font=font)
        draw.text(((240 - w) / 2, (240 - h) / 2), message, font=font, fill=(0, 0, 0))

        self.display.display(image)

    def clear_display(self):
        self.display.clear()
