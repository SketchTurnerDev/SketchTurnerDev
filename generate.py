import os
import requests
from PIL import Image

USERNAME = "SketchTurnerDev"
MAX_STARS = 50

X_PASTE_START = 577
Y_PASTE_START = 155

try:
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url).json()
    total_stars = sum(repo['stargazers_count'] for repo in response if isinstance(repo, dict) and not repo.get('fork', False))
except Exception as e:
    total_stars = 0

progress = min(total_stars / MAX_STARS, 1.0)

try:
    empty_img = Image.open("empty.png").convert("RGBA")
    patch_img = Image.open("full.png").convert("RGBA")
except FileNotFoundError:
    exit()

patch_width = patch_img.width
patch_height = patch_img.height

fill_height = int(patch_height * progress)

if fill_height > 0:
    crop_box = (0, patch_height - fill_height, patch_width, patch_height)
    active_patch = patch_img.crop(crop_box)
    
    paste_y = Y_PASTE_START + (patch_height - fill_height)
    
    empty_img.paste(active_patch, (X_PASTE_START, paste_y), active_patch)

empty_img.save("status.png")
