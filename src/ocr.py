from PIL import Image
import pytesseract as pt

# Tesseract 실행 경로 필요 시 설정
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image_path):
    try:
        image = Image.open(image_path)
        image = image.convert('L')
        text = pt.image_to_string(image, lang='eng', config='--oem 1 --psm 6')
        return text.strip()
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""
