[README.md](https://github.com/user-attachments/files/34426748/README.md)
# API-Cocktail-Finder

Das Programm fragt [TheCocktailDB-API](https://www.thecocktaildb.com/api.php) ab und zeigt Cocktail-Rezepte in einer grafischen Oberfläche an.

## Funktionen

- Cocktails nach Namen suchen (z. B. `margarita`, `mojito` oder `martini`)
- Suchergebnisse in einer Liste anzeigen
- Name, Kategorie, Alkoholstatus und Glasart anzeigen
- Zutaten und Mengen ausgeben
- Zubereitungsanleitung anzeigen (Deutsch, falls vorhanden, sonst Englisch)
- Cocktailbild laden
- Fehler bei Netzwerkproblemen und ungültigen Eingaben behandeln

## Voraussetzungen

- Python 3
- Internetverbindung
- Tkinter (bei den meisten Python-Installationen bereits enthalten)

## Installation

1. Dieses Repository herunterladen oder klonen.
2. Im Projektordner ein Terminal öffnen.
3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

4. Programm starten:

   ```bash
   python main.py
   ```

## Verwendete API

Die Anwendung verwendet den Such-Endpunkt:

```text
https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita
```

Der Suchbegriff wird als Query-Parameter `s` übergeben. In Python geschieht das mit:

```python
requests.get(API_URL, params={"s": search_term}, timeout=TIMEOUT)
```

Die Antwort wird mit `response.json()` in Python-Daten umgewandelt. Das oberste JSON-Objekt enthält den Schlüssel `drinks`. Dieser enthält eine Liste mit Cocktail-Objekten oder den Wert `null`, wenn nichts gefunden wurde.


## Hinweise

- Die API benötigt für diesen öffentlichen Test-Endpunkt keinen persönlichen API-Key.
- Die Verfügbarkeit und Inhalte der API können sich ändern.
- Die Cocktailbilder werden zur Laufzeit aus dem Internet geladen.
- `Pillow` wird zum Anzeigen und Verkleinern der Bilder verwendet.
- `Tkinter` ist Teil der Python-Standardbibliothek und wird nicht in `requirements.txt` installiert.
