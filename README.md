# Praia do Dia

App para elegir playa en Rio cada día: **https://manuelros99-png.github.io/praia-do-dia-data/**

- GitHub Actions baja el pronóstico de mar y clima frente a Copacabana (Open-Meteo) y la lluvia por hora de Meteored, lo guarda en `forecast.json` y calcula la recomendación del día en `summary.txt`. Corre del 20 al 30 de noviembre.
- `index.html` es la app (se genera con `build_site.py` desde la versión de Claude) y lee `forecast.json`.
- Una rutina de Claude carga los datos en la versión de Claude y manda el aviso de la mañana al celular.
