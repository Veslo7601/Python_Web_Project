import re

import cloudinary

from PhotoShare.database.models import User


async def extract_url_from_img_tag(img: str) -> str:
    match = re.search(r'src="([^"]+)"', img)
    if not match:
        return "Not found"

    return match.group(1)


async def build_transform_url(user: User, width: int, height: int, crop: str, filter: str):

    public_id = f"users/{user.email}"
    transformations = [
        {"width": width, "height": height, "crop": crop},
        {"effect": filter}
    ]

    tag_url = cloudinary.CloudinaryImage(public_id).image(transformation=transformations)
    url = await extract_url_from_img_tag(tag_url)

    return url



