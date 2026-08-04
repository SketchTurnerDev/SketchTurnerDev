import sys
import requests
from PIL import Image, ImageDraw, ImageFont

USERNAME = "SketchTurnerDev"
MAX_STARS = 50

X_PASTE_START = 577
Y_PASTE_START = 155

TEXT_X = 705
TEXT_Y = 710

FONT_FILE = "VT323-Regular.ttf"
FONT_SIZE = 65

try:
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url).json()
    total_stars = sum(
        repo['stargazers_count']
        for repo in response
        if isinstance(repo, dict) and not repo.get('fork', False)
    )
except Exception:
    total_stars = 0

progress_ratio = min(total_stars / MAX_STARS, 1.0)

try:
    with Image.open("empty.png").convert("RGBA") as empty_img, \
         Image.open("full.png").convert("RGBA") as patch_img:

        patch_width = patch_img.width
        patch_height = patch_img.height

        fill_height = int(patch_height * progress_ratio)

        if fill_height > 0:
            crop_box = (0, patch_height - fill_height, patch_width, patch_height)
            active_patch = patch_img.crop(crop_box)
            paste_y = Y_PASTE_START + (patch_height - fill_height)
            empty_img.paste(active_patch, (X_PASTE_START, paste_y), active_patch)

        draw = ImageDraw.Draw(empty_img)
        
        try:
            font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
        except IOError:
            font = ImageFont.load_default()

        text_color = (30, 30, 30, 255)
        stars_text = f"STARS {total_stars}/{MAX_STARS}"
        
        draw.text((TEXT_X, TEXT_Y), stars_text, fill=text_color, font=font)

        empty_img.save("status.png")

except FileNotFoundError:
    sys.exit(1)
