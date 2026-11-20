// Calcula la recomendación del día con la misma lógica de la app (index.html)
// y la imprime en una línea para el aviso del celular. Uso: node recommend.js [forecast.json] [YYYY-MM-DD]
const fs = require("fs"), vm = require("vm"), path = require("path");
const dir = __dirname;
const html = fs.readFileSync(path.join(dir, "index.html"), "utf8");
const code = html.match(/<script>([\s\S]*)<\/script>/)[1].replace(/\nboot\(\);\s*$/, "\n");
const data = JSON.parse(fs.readFileSync(process.argv[2] || path.join(dir, "forecast.json"), "utf8"));
const ctx = { console, Intl, Date, Math, JSON, document: { querySelector: () => null }, window: {}, sessionStorage: { getItem: () => null } };
vm.createContext(ctx);
vm.runInContext(code + "\nthis.__api = { evaluate, rainProb, series, HOURS, WD, rioToday, set: d => { DATA = d; } };", ctx);
const api = ctx.__api; api.set(data);
const day = process.argv[3] || api.rioToday();
const ranked = api.evaluate(day);
if (!ranked.length) { console.log("Praia do Dia: no hay pronóstico para hoy."); process.exit(0); }
const c = ranked.find(r => r.b.group === "copa"), i = ranked.find(r => r.b.group === "ipa");
const [top, alt] = [c, i].filter(Boolean).sort((a, b) => b.score - a.score);
const w = data.weather, wi = api.series(w, day);
let bm = { p: 0, h: 9 };
for (const h of api.HOURS) if (wi[h] != null) { const p = api.rainProb(day, h, w.precipitation_probability[wi[h]]); if (p > bm.p) bm = { p, h }; }
const x = top.best.mid;
const name = r => r.b.group === "copa" ? `Copacabana ${r.b.short}` : (r.b.short === "Arpoador" ? "Arpoador" : `Ipanema ${r.b.short}`);
let msg = `Hoy: ${name(top)} de ${top.best.from} a ${top.best.to} h (${top.score}/100), olas ${x.hb.toFixed(1).replace(".", ",")} m.`;
if (alt) msg += ` Plan B: ${name(alt)} (${alt.score}).`;
msg += bm.p >= 10 ? ` Lluvia: hasta ${bm.p}% a las ${bm.h} h.` : " Sin lluvia de día.";
const outside = ranked.find(r => !r.b.group);
if (outside && outside.score > top.score) msg += ` Ojo: ${outside.b.name} rinde más (${outside.score}).`;
if (x.hb > 1.2) msg += " Mar grande: solo frente a guardavidas.";
console.log(msg);
