# Saper Game  (Pygame)

Interaktywna implementacja klasycznego Sapera napisana w Pythonie z wykorzystaniem biblioteki **Pygame**. Gra działa w stałym oknie 800×650 px, obsługuje trzy poziomy trudności i mierzy czas każdej rozgrywki.

---

## Wymagania

| Narzędzie  | Wersja  |
| ---------- |---------|
| **Python** | ≥ 3.12  |
| **Pygame** | ≥ 2.6.1 |

---

## Instalacja zależności

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python app.py
```

## Sterowanie

- **Lewy przycisk myszy (LPM)** - odsłonięcie pola.

- **Prawy przycisk myszy (PPM)** – postawienie / zdjęcie flagi.

- **Kliknięcie RESET** – restart bieżącej rozgrywki.

## Tabela funkcjonalności

| Funkcjonalność                            | Opis                                                                                      |
| ----------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Ekran startowy (Wybór trudności)**      | Przyciski **EASY** (7 bomb), **MEDIUM** (20 bomb), **HARD** (50 bomb)                     |
| **Generowanie planszy gry**               | Losowe rozmieszczenie bomb, obliczanie liczb sąsiadujących pól                            |
| **Bezpieczne pierwsze kliknięcie**        | Pole wskazane jako pierwsze nigdy nie zawiera bomby                                       |
| **Obsługa kliknięć myszy**                | LPM – odkrywanie, PPM – flaga                                                             |
| **Flood-fill (rozszerzanie pustych pól)** | Automatyczne odsłanianie sąsiadujących pustych pól                                        |
| **Wyświetlanie stanu planszy**            | Zakryte (zieleń), odkryte (niebieski), liczby (kolory), flagi (ikonka)                    |
| **Warunki wygranej**                      | Oznaczenie wszystkich bomb flagami + odsłonięcie pozostałych pól → ekran „GAME WON!!!”    |
| **Warunki przegranej**                    | Kliknięcie w bombę → ekran „GAME OVER”                                                    |
| **Licznik flag**                          | Informacja "FLAG PLACED: x/y" nad planszą                                                 |
| **Stoper + Najlepszy czas**               | Bieżący czas od pierwszego ruchu oraz najlepszy czas dla danego poziomu (w obrębie sesji) |
| **Przycisk RESET**                        | Restart rozgrywki i powrót do ekranu wyboru trudności                                     |
