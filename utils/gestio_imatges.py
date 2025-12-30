from PIL import Image, ImageOps
import os

def generar_miniatura(ruta_original, ruta_miniatura, max_costat=200):
    try:
        img = Image.open(ruta_original).convert("RGB")
        img = ImageOps.exif_transpose(img)

        img.thumbnail((max_costat, max_costat), Image.LANCZOS)

        # Fons quadrat blanc (com el fons web)
        mida_final = (max_costat, max_costat)
        fons = Image.new("RGB", mida_final, (255, 255, 255))

        x = (max_costat - img.width) // 2
        y = (max_costat - img.height) // 2
        fons.paste(img, (x, y))

        os.makedirs(os.path.dirname(ruta_miniatura), exist_ok=True)
        fons.save(ruta_miniatura)

        return True

    except Exception as e:
        print(f"❌ Error generant miniatura: {e}")
        return False
