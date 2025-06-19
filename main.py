import cv2 as cv
import numpy as np
import os
import csv

# ==========================
# Parametry i konfiguracja
# ==========================
image_dir = "resistors"
csv_path = "wyniki.csv"

color_ranges = {
    'BLACK': ([0, 0, 0], [180, 255, 50]),
    'BROWN': ([10, 100, 20], [20, 255, 200]),
    'RED': ([0, 50, 50], [10, 255, 255]),
    'ORANGE': ([10, 100, 100], [25, 255, 255]),
    'YELLOW': ([25, 100, 100], [35, 255, 255]),
    'GREEN': ([35, 50, 50], [85, 255, 255]),
    'BLUE': ([85, 50, 50], [130, 255, 255]),
    'VIOLET': ([130, 50, 50], [160, 255, 255]),
    'GRAY': ([0, 0, 40], [180, 50, 150]),
    'WHITE': ([0, 0, 200], [180, 30, 255])
}

# ==========================
# Funkcje pomocnicze
# ==========================
def deskew(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)
    if lines is None:
        return img
    angles = [np.degrees(np.arctan2(y2 - y1, x2 - x1)) for [[x1, y1, x2, y2]] in lines]
    angle = np.median(angles)
    (h, w) = img.shape[:2]
    M = cv.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv.warpAffine(img, M, (w, h), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REPLICATE)

def findBands(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    bands = []
    for color, (lower, upper) in color_ranges.items():
        mask = cv.inRange(hsv, np.array(lower), np.array(upper))
        mask = cv.medianBlur(mask, 5)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if not validContour(cnt):
                continue
            x, y, w, h = cv.boundingRect(cnt)
            bands.append((x, y, x + w, y + h, color))
    bands.sort()  # sort by x
    return bands[:5]  # maksymalnie 5

def validContour(cont):
    min_area = 100
    if cv.contourArea(cont) < min_area:
        return False
    x, y, w, h = cv.boundingRect(cont)
    if h < 5 or w / float(h) > 0.6:
        return False
    return True

def calculateResistance(bands):
    if len(bands) < 3:
        return None
    try:
        color_order = [b[4] for b in bands]
        digits = {'BLACK': 0, 'BROWN': 1, 'RED': 2, 'ORANGE': 3, 'YELLOW': 4, 'GREEN': 5,
                  'BLUE': 6, 'VIOLET': 7, 'GRAY': 8, 'WHITE': 9}
        mults = digits.copy()
        val = digits[color_order[0]] * 10 + digits[color_order[1]]
        val *= 10 ** mults[color_order[2]]
        return val
    except Exception:
        return None

# ==========================
# Główna pętla programu
# ==========================
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Plik", "Kolory", "Rezystancja"])

    for fname in os.listdir(image_dir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        path = os.path.join(image_dir, fname)
        img = cv.imread(path)
        if img is None:
            continue

        print(f"➡️ Przetwarzanie: {fname}")
        img = deskew(img)
        bands = findBands(img)
        color_list = [b[4] for b in bands][:5]
        resistance = calculateResistance(bands)

        if resistance:
            print(f"📄 {fname}: {color_list} -> {resistance} Ω")
            writer.writerow([fname, "-".join(color_list), resistance])
        else:
            print(f"📄 {fname}: {color_list} -> BRAK Ω")
            writer.writerow([fname, "-".join(color_list), "BRAK"])

print("\n✅ Przetwarzanie zakonczone. Dane zapisane do pliku CSV.")

