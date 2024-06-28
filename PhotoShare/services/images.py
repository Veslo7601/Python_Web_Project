import re


async def extract_url_from_img_tag(img: str) -> str:
    match = re.search(r'src="([^"]+)"', img)
    if not match:
        return "Not found"

    return match.group(1)

