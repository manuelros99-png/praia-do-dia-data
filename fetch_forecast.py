#!/usr/bin/env python3
"""Baja el pronóstico de mar y clima para la Zona Sul de Rio y lo deja en forecast.json.

Fuente: Open-Meteo (gratis, sin clave). Guarda hoy + 2 días, más la lluvia de ayer
(para avisar si el agua puede estar contaminada después de lluvias).
Uso: python3 fetch_forecast.py [salida.json]
"""
import json, sys, urllib.request, datetime

LAT, LON = -22.99, -43.19  # frente a Copacabana/Arpoador
TZ = "America/Sao_Paulo"

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

marine = get(
    "https://marine-api.open-meteo.com/v1/marine"
    f"?latitude={LAT}&longitude={LON}&timezone={TZ}&forecast_days=3"
    "&hourly=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_direction,"
    "wind_wave_height,sea_level_height_msl,sea_surface_temperature"
)
weather = get(
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude=-22.985&longitude=-43.19&timezone={TZ}&forecast_days=3&past_days=1"
    "&wind_speed_unit=kmh"
    "&hourly=temperature_2m,precipitation_probability,precipitation,cloud_cover,"
    "wind_speed_10m,wind_direction_10m,wind_gusts_10m,uv_index"
    "&daily=sunrise,sunset,precipitation_sum"
)

def r1(xs):
    return [None if x is None else round(x, 2) for x in xs]

mh, wh = marine["hourly"], weather["hourly"]
out = {
    "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="minutes"),
    "source": "Open-Meteo (marine + forecast)",
    "marine": {"time": mh["time"], **{k: r1(v) for k, v in mh.items() if k != "time"}},
    "weather": {"time": wh["time"], **{k: r1(v) for k, v in wh.items() if k != "time"}},
    "daily": weather["daily"],
}
path = sys.argv[1] if len(sys.argv) > 1 else "forecast.json"
with open(path, "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(f"ok {path} {len(json.dumps(out))} bytes, marine {len(mh['time'])}h, weather {len(wh['time'])}h")
