#!/usr/bin/env python3
"""Lee de Meteored Brasil la probabilidad de lluvia por hora en Rio de Janeiro.

Agrega al JSON del pronóstico el campo `meteored`:
  {"url": ..., "days": {"2026-11-20": {"9": {"p": 10, "mm": 0.0}, ...}}}
Uso: python3 fetch_meteored.py forecast.json
Una sola consulta por día, para uso personal. Si la página cambia y no se puede leer, no toca el JSON.
"""
import html, json, re, sys, urllib.request, datetime

URL = "https://www.meteored.com.br/rio-de-janeiro_rio-de-janeiro-l12987-xhoras.htm"
MESES = {m: i for i, m in enumerate(["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
                                     "agosto", "setembro", "outubro", "novembro", "dezembro"], 1)}

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
txt = re.sub(r"\s+", " ", txt)

day_re = re.compile(r"(?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)[^,]{0,8}, (\d{1,2}) de (\w+)")
hour_re = re.compile(r"(\d{2}):00 -?\d+° .{0,200}? Chuva (\d+)% ([\d.,]+) mm")
today = datetime.date.today()
days = {}
heads = list(day_re.finditer(txt))
for i, h in enumerate(heads):
    mes = MESES.get(h.group(2).lower())
    if not mes:
        continue
    year = today.year + (1 if mes < today.month - 6 else 0)
    key = f"{year}-{mes:02d}-{int(h.group(1)):02d}"
    chunk = txt[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(txt)]
    for m in hour_re.finditer(chunk):
        days.setdefault(key, {})[str(int(m.group(1)))] = {"p": int(m.group(2)), "mm": float(m.group(3).replace(",", "."))}

days = {k: v for k, v in days.items() if len(v) >= 6}
if not days:
    sys.exit("meteored: no pude leer la página, dejo el JSON como estaba")
path = sys.argv[1]
data = json.load(open(path))
data["meteored"] = {"url": URL.replace("-xhoras", ""), "hourlyUrl": URL, "days": days}
json.dump(data, open(path, "w"), separators=(",", ":"))
print("meteored ok", {k: len(v) for k, v in days.items()})
