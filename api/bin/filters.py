from PIL import Image, ImageFilter
import io


async def apply_filter(file: object, filter: str) -> object:
    image = Image.open(file)
    image = image.filter(eval(f"ImageFilter.{filter.upper()}"))

    file = io.BytesIO()
    image.save(file, format="JPEG")
    file.seek(0)

    return file
