# ProjektAiMiloszNowackiJozefBaryza
    1. Opis rzeczywistego problemu
Celem projektu jest rozwiązanie problemu polegającego, na identyfikacji z fizycznych zdjęć wartości rezystancji rezystorów THT. W praktyce technicy często muszą odczytywać kolory na małych elementach - co może prowadzić do pomyłek. System komputerowy pozwala zautomatyzować ten proces i zwiększyć tempo i wygodę pracy. Projekt opiera się na metodach wizji komputerowej (Computer Vision), w szczególności operacjach segmentacji kolorów i przetwarzaniu konturów - będących elementami klasyfikacji wizualnej.
Dane wejściowe:
Zdjęcia rezystorów (np. z kamery, telefonu, katalogów) zawierające 4/5-paskowe oznaczenia kolorowe.
Dane wyjściowe:
Wartość rezystancji w ohmach oraz lista rozpoznanych kolorów.

    2. State of art
Poniżej przedstawiamy przegląd trzech różnych podejść do automatycznego rozpoznawania pasków na rezystorach:
    A) Rozpoznawanie koloru na podstawie segmentacji HSV + OpenCV 
    • Zalety: szybkie, nie wymaga trenowania modelu
    • Wady: wrażliwe na oświetlenie, tło, obrót
    • Narzędzia: OpenCV, filtry konturów, kolory w przestrzeni HSV
    B) Klasyfikacja obrazu rezystora przez model CNN (np. ResNet)
    • Zalety: odporność na tło, zmienność formy
    • Wady: wymaga dużej bazy danych i etykiet
    • Narzędzia: TensorFlow / PyTorch, CNN, transfer learning
    C) Rozpoznawanie kolorów z pomocą OCR rozszerzonego (np. Vision Transformers na segmentowanych obrazach)
    • Zalety: wysoka precyzja przy dobrze przygotowanych danych
    • Wady: złożoność, duży koszt obliczeniowy
    • Narzędzia: ViT, U-Net do segmentacji + klasyfikator

    3. Wybrana koncepcja:
W projekcie zastosowano podejście oparte na bibliotece OpenCV. Kolory są rozpoznawane za pomocą masek HSV, a paski wykrywane poprzez analizę konturów. Dzięki sortowaniu po współrzędnych X możliwe jest ustalenie kolejności pasków i obliczenie wartości rezystancji.
Dane wejściowe:
Obrazy rezystorów z bazy danych Kaggle (Resistors Starter)
https://www.kaggle.com/code/seanerfan/resistors-starter

Dane wyjściowe:
CSV zawierający: nazwę pliku, wykryte kolory pasków, obliczoną wartość rezystancji.
Forma danych:
    • Kolory rozpoznawane są przez dopasowanie do zdefiniowanych przedziałów HSV.
    • Rezystancja obliczana na podstawie wzoru:  wartość = (cyfra1)(cyfra2) * 10^cyfra3
Procedura testowania:
Dla każdego obrazu:
    • Ładowanie zdjęcia
    • Segmentacja kolorów
    • Filtracja konturów
    • Identyfikacja maksymalnie 5 pasków
    • Obliczenie wartości
    • Zapis do wyniki.csv
Potrzebne elementy do wdrożenia w realnym świecie:
    • Dobre oświetlenie
    • Kamera lub aparat
    • Komputer z Pythonem + OpenCV

    4. Proof of concept
Skrypt test_resistors.py przetwarza obrazy z podfolderów w resistors Wykrywa paski, rozpoznaje kolory i zapisuje dane do pliku CSV. Niestety tak jak napisane powyżej , problemy z tego typu rozwiązaniem powoduje światło, tło i obrót czego w wymienionej bazie danych doświadczamy non stop czego wynikiem jest niska skuteczność , aby wartość rezystora została podana poprawnie wszystkie paski muszą zostać odczytane dokładnie i żaden element tła bądź obudowy nie może zostać  wychwycony. Najczęściej kolory są dobrze odczytywane w poprawnej kolejnosci jednak pomiędzy nie zostaje dodany kolor obudowy/bądź ciemny kolor tj czarny/szary/brązowy co powoduje błędny pomiar 
