## Tabela funkcjonalności

| Funkcjonalność                     | Opis                                                                 |
|------------------------------------|----------------------------------------------------------------------|
| **Ekran startowy (Wybór trudności)** | Przycisk EASY (5 bomb), MEDIUM (15 bomb), HARD (25 bomb)              |
| **Generowanie planszy gry**         | Losowe rozmieszczenie bomb, obliczanie liczb wokół bomb               |
| **Obsługa kliknięć myszy**          | LPM: odkrywanie pola, PPM: oznaczanie pola flagą                      |
| **Flood fill (rozszerzanie pustych pól)** | Automatyczne odkrywanie sąsiednich pustych pól                        |
| **Wyświetlanie stanu planszy**      | Zakryte pola (zielone), odkryte (niebieskie), liczby, flagi (obrazek) |
| **Warunki wygranej**                | Oznaczenie wszystkich bomb flagami + odkrycie pozostałych pól         |
| **Warunki przegranej**              | Kliknięcie w bombę kończy grę (ekran GAME OVER)                       |
| **Licznik flag**                    | Wyświetlanie liczby umieszczonych flag na planszy                     |
| **Przycisk RESET**                  | Restart gry, powrót do wyboru trudności                               |
| **Rysowanie siatki (Grid)**         | Białe linie rozdzielające pola planszy                                |
| **Płynność rozgrywki (FPS 30)**     | Stała pętla gry z limitem 30 klatek na sekundę                        |
| **Centrowanie planszy**             | Automatyczne ustawienie planszy w środku okna                         |
| **Modularna struktura kodu**        | Oddzielne funkcje do logiki, rysowania i obsługi zdarzeń              |