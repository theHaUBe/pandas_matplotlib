# 📊 Analiza Imion w USA i Polsce (1880–2024)

## Opis projektu  
Celem projektu było praktyczne utrwalenie umiejętności w zakresie przetwarzania i wizualizacji danych tabelarycznych oraz analizy trendów w nadawaniu imion w Stanach Zjednoczonych i Polsce.  

Dane amerykańskie pochodziły z bazy **Social Security Administration**:  
➡️ [https://www.ssa.gov/oact/babynames/names.zip](https://www.ssa.gov/oact/babynames/names.zip)  
Dane polskie pochodziły z bazy **imiona_pl**:  
➡️ [https://chmura.put.poznan.pl/s/foC9qaKz7B8cQBK](https://chmura.put.poznan.pl/s/foC9qaKz7B8cQBK)

Projekt został w całości zrealizowany w języku **Python**, z wykorzystaniem bibliotek:
- `pandas`
- `matplotlib`
- `sqlite3`
- `os`

## 🔍 Zakres zrealizowanych prac

### 1. Wczytanie danych  
Zostały wczytane wszystkie pliki z katalogu `./data/names`, zawierające dane o imionach nadawanych w USA w latach **1880–2024**.  
Pliki CSV zostały scalone w jeden zbiór danych, w którym każdemu rekordowi przypisano rok nadania imienia.

### 2. Liczba unikalnych imion  
Została określona całkowita liczba unikalnych imion nadanych w badanym okresie.  
Dodatkowo dokonano podziału na imiona męskie i żeńskie oraz porównano ich liczność.

### 3. Normalizacja częstości występowania  
Dla każdego imienia obliczono jego **popularność względną**, będącą stosunkiem liczby nadań do całkowitej liczby urodzeń danej płci w danym roku.  
W wyniku tego procesu powstały kolumny `frequency_male` oraz `frequency_female`.

### 4. Analiza liczby urodzeń i proporcji płci  
Zostały wygenerowane dwa wykresy:
- całkowitej liczby urodzeń w każdym roku,  
- stosunku liczby narodzin dziewczynek do chłopców.  

Na wykresie oznaczono lata, w których różnica między płciami była najmniejsza oraz największa.

### 5. Ranking najpopularniejszych imion  
Na podstawie średniej popularności w całym okresie czasu wyznaczono **1000 najpopularniejszych imion** dla każdej płci.

### 6. Analiza trendów wybranych imion  
Dla dwóch imion (najpopularniejszego żeńskiego oraz drugiego najpopularniejszego męskiego) przedstawiono zmiany liczby nadań oraz ich popularności w czasie.  
Na wykresie wyróżniono wartości dla lat **1934**, **1980** i **2024**.

### 7. Analiza różnorodności imion  
Został wykreślony wykres udziału imion z rankingu **Top 1000** w całkowitej liczbie urodzeń w każdym roku.  
Określono rok o największej różnicy różnorodności między płciami oraz przedstawiono wnioski dotyczące ewolucji trendów w nadawaniu imion.

### 8. Zmiana rozkładu ostatnich liter imion męskich  
Przeanalizowano zmiany popularności ostatnich liter imion męskich w latach **1900**, **1975** i **2024**.  
Dane zostały znormalizowane względem liczby urodzeń.  
Zidentyfikowano litery o największym wzroście i spadku popularności oraz przedstawiono ich przebieg w czasie.

### 9. Zmiana konotacji płci imion  
Zostały zidentyfikowane imiona występujące u obu płci.  
Porównano dwa okresy — **1880–1920** oraz **2000–2024** — i wyłoniono dwa imiona:
- które przeszło z typowo męskiego na żeńskie,  
- które przeszło z typowo żeńskiego na męskie.  

Dla tych imion przedstawiono przebieg zmiany konotacji płciowej w czasie.

### 10. Analiza imion w Polsce (2000–2024)  
Zostały wczytane dane z bazy **imiona_pl** i przekształcone do formatu zgodnego z amerykańskim zbiorem.  
Przeprowadzono:
- analizę **Top 200** najpopularniejszych imion w Polsce,  
- porównanie trendów w latach **2000**, **2013** i **2024**,  
- analizę liter końcowych imion,  
- identyfikację liter o największych zmianach popularności.  

## 🧩 Wnioski  
- Liczba unikalnych imion systematycznie rosła, co świadczy o wzroście różnorodności imion.  
- Różnorodność imion żeńskich była większa niż męskich przez cały okres analizy.  
- Wzrosła popularność imion o końcówkach miękkich, np. „a”, „n”.  
- Część imion zmieniła konotację płciową, co można wiązać ze zmianami społecznymi i kulturowymi.  
- W Polsce obserwowane są podobne tendencje jak w USA, choć o mniejszej dynamice zmian.

