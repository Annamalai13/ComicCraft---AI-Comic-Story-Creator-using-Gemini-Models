import os
import re
import uuid
import warnings
import io
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()


def sanitize_filename(prompt: str) -> str:
    """Sanitizes an image prompt string into a valid, safe filename prefix."""
    clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', prompt)
    clean = clean.replace(' ', '_').lower()
    return clean[:30]


def generate_image(image_prompt: str) -> str:
    """
    Generates a comic panel image using Pollinations.ai (free, no key needed).
    Falls back to Gemini image models if available, then Pillow placeholder.
    Saves to static/panels/ and returns '/static/panels/<filename>.png'.
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "panels")
    os.makedirs(output_dir, exist_ok=True)

    sanitized_prompt = sanitize_filename(image_prompt)
    unique_id = uuid.uuid4().hex[:8]
    filename = f"panel_{sanitized_prompt}_{unique_id}.png"
    filepath = os.path.join(output_dir, filename)
    relative_path = f"/static/panels/{filename}"

    # --- Primary: Pollinations.ai (free, no API key) ---
    try:
        encoded_prompt = urllib.parse.quote(image_prompt)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width=512&height=512&model=flux&nologo=true&seed={uuid.uuid4().int % 999999}"
        )
        print(f"[INFO] Generating image via Pollinations.ai...")
        req = urllib.request.Request(url, headers={"User-Agent": "ComicCraft/1.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            image_data = response.read()
        img = Image.open(io.BytesIO(image_data))
        img = img.convert("RGB")
        img.save(filepath)
        print(f"[SUCCESS] Pollinations image saved: {filepath}")
        return relative_path
    except Exception as e:
        print(f"[WARNING] Pollinations.ai failed ({e}). Trying Gemini image models...")

    # --- Secondary: Gemini image models (requires API key + quota) ---
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        image_models = [
            "models/gemini-2.5-flash-image",
            "models/gemini-3.1-flash-image",
            "models/gemini-3.1-flash-lite-image",
        ]
        try:
            import base64
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import google.generativeai as genai
                genai.configure(api_key=api_key)

            for model_name in image_models:
                try:
                    print(f"[INFO] Trying Gemini model: {model_name}")
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(
                            image_prompt,
                            generation_config={"response_modalities": ["IMAGE", "TEXT"]}
                        )
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                            image_data = base64.b64decode(part.inline_data.data)
                            img = Image.open(io.BytesIO(image_data))
                            img.save(filepath)
                            print(f"[SUCCESS] Gemini image saved using {model_name}")
                            return relative_path
                except Exception as e:
                    print(f"[INFO] {model_name} failed: {e}")
                    continue
        except Exception as e:
            print(f"[WARNING] Gemini image generation failed: {e}")

    # --- Fallback: Pillow placeholder ---
    print("[WARNING] All image sources failed. Using Pillow placeholder.")
    return _generate_fallback_image(image_prompt, filepath, relative_path)


def _generate_fallback_image(prompt: str, filepath: str, relative_path: str) -> str:
    """Generates a styled comic panel placeholder using PIL."""
    width, height = 512, 512
    img = Image.new('RGB', (width, height), color=(245, 242, 235))
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, width - 10, height - 10], outline=(20, 20, 20), width=6)
    draw.rectangle([18, 18, width - 18, height - 18], outline=(200, 50, 50), width=2)

    for y in range(25, height - 25, 4):
        color_val = max(180, 240 - int(y / 3))
        draw.line([(25, y), (width - 25, y)], fill=(color_val, color_val + 5, color_val + 15))

    draw.rectangle([40, height // 2 - 60, width - 40, height // 2 + 60],
                   fill=(255, 255, 255), outline=(0, 0, 0), width=3)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text((width // 2 - 60, height // 2 - 40), "COMIC PANEL ARTWORK", fill=(0, 0, 0), font=font)

    words = prompt.split()
    lines, current_line = [], []
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 35:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    y_offset = height // 2 - 10
    for line in lines[:3]:
        draw.text((50, y_offset), line, fill=(50, 50, 50), font=font)
        y_offset += 18

    img.save(filepath)
    print(f"[FALLBACK] Placeholder image saved: {filepath}")
    return relative_path
