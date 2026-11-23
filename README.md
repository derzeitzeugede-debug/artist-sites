# Demo-Websites (Version 2)

- `jah-mason/index.html`, `lutan-fyah/index.html`: fertige Demo-Seiten, je eine Datei. Zum Ansehen im Browser öffnen (braucht Internet, weil Fotos, Cover und Hörproben online geladen werden).
- `template/`: Vorlage. Neuen Artist in `artists.json` eintragen, `python3 build.py` ausführen. Alte Version: `template-v1.html`.

## Was drin ist
- Vollbild-Hero mit Live-Foto, "Play latest"-Button
- Laufband mit den Labels, auf denen der Artist veröffentlicht hat
- "Hear the records": Tracklist mit 12 Hörproben, drehende Platte, Kauf-Button pro Track
- Fester Player unten (Play/Pause, vor/zurück, Fortschritt, "Buy this record")
- Vinyl-Shop-Raster mit Cover, Vorhören beim Drüberfahren, Kauf-Link
- Biografie mit Foto und Eckdaten, Foto-Galerie, Booking-Bereich mit Foto, Footer mit Bildnachweisen

## Quellen und Rechte
- Fotos: Wikimedia Commons, frei lizenziert (CC0 bzw. CC BY-SA). Nachweis steht im Footer, das ist bei CC BY-SA Pflicht.
- Hörproben und Cover: direkt von buyreggae.com (`/sounds/<id/10000>/<id>A.mp3`, `/images/product/P<id>.jpg`). Für den Live-Betrieb sollte buyreggae das absegnen.
- Schrift: Anton + Inter (Google Fonts).
