"""Genera 00-indice/*.md y datos/*.json a partir de las fichas (fuente de verdad).

Uso: python3 herramientas/generar_indices.py
No edites a mano lo que este script escribe: se sobrescribe.
"""
from __future__ import annotations

import json
import unicodedata
from collections import defaultdict

from comun import CARPETAS, EVIDENCIA, NOMBRES, RAIZ, RE_ENLACE, catalogo, fichas, rel

AVISO = "<!-- GENERADO por herramientas/generar_indices.py · no editar a mano -->\n\n"
IDX = RAIZ / "00-indice"
DATOS = RAIZ / "datos"


def enlace(f, desde="00-indice"):
    return f"[{f['id']} · {f['titulo']}](../{rel(f['_ruta'])})"


def clave_orden(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn")


def escribir(nombre: str, texto: str):
    (IDX / nombre).write_text(AVISO + texto, encoding="utf-8")


def main():
    IDX.mkdir(exist_ok=True)
    DATOS.mkdir(exist_ok=True)
    cat = catalogo()
    fs = sorted(fichas(), key=lambda f: f["id"])
    por_id = {f["id"]: f for f in fs}

    # Relaciones entrantes (relacionadas + enlaces [[ID]] en el cuerpo)
    salientes = {}
    entrantes = defaultdict(set)
    for f in fs:
        s = set(f.get("relacionadas") or []) | set(RE_ENLACE.findall(f["_cuerpo"]))
        s.discard(f["id"])
        salientes[f["id"]] = sorted(s)
        for d in s:
            entrantes[d].add(f["id"])

    # mapa.md
    L = ["# Mapa del sistema ASESOR\n",
         f"{len(fs)} fichas escritas de {len(cat)} planificadas.\n",
         "Evidencia: " + " · ".join(f"**{k}** {v}" for k, v in EVIDENCIA.items()) + ". "
         "Formalidad 1 (casa) → 5 (etiqueta).\n"]
    for fam, carpeta in CARPETAS.items():
        ids = [i for i in cat if i.startswith(fam)]
        hechas = [i for i in ids if i in por_id]
        L.append(f"\n## {fam} · {NOMBRES[fam]} ({len(hechas)}/{len(ids)})\n")
        L.append("| ID | Ficha | Evid. | Formal. | Resumen |\n|---|---|---|---|---|")
        for i in ids:
            if i in por_id:
                f = por_id[i]
                fo = f.get("formalidad") or []
                fo_s = f"{fo[0]}–{fo[1]}" if fo else "—"
                res = str(f.get("resumen", "")).replace("|", "\\|")
                L.append(f"| {i} | [{f['titulo']}](../{rel(f['_ruta'])}) | {f.get('evidencia')} | {fo_s} | {res} |")
            else:
                L.append(f"| {i} | {cat[i]} | — | — | *pendiente* |")
    escribir("mapa.md", "\n".join(L) + "\n")

    # etiquetas.md
    et = defaultdict(list)
    for f in fs:
        for t in f.get("etiquetas") or []:
            et[str(t)].append(f)
    L = ["# Índice por etiquetas\n"]
    for t in sorted(et, key=clave_orden):
        L.append(f"- **{t}**: " + ", ".join(f"[{f['id']}](../{rel(f['_ruta'])})" for f in et[t]))
    escribir("etiquetas.md", "\n".join(L) + "\n")

    # glosario.md
    gl = defaultdict(list)
    for f in fs:
        for t in f.get("terminos") or []:
            gl[str(t)].append(f)
    L = ["# Glosario (término → ficha que lo define)\n",
         "La definición está en la ficha enlazada.\n"]
    letra = None
    for t in sorted(gl, key=clave_orden):
        ini = clave_orden(t)[:1].upper()
        if ini != letra:
            letra = ini
            L.append(f"\n## {letra}\n")
        L.append(f"- **{t}** — " + ", ".join(enlace(f) for f in gl[t]))
    escribir("glosario.md", "\n".join(L) + "\n")

    # formalidad.md
    L = ["# Fichas por nivel de formalidad\n",
         "1 casa/deporte · 2 casual · 3 smart casual · 4 business/traje · 5 etiqueta\n"]
    for n in range(1, 6):
        sel = [f for f in fs if (fo := f.get("formalidad")) and fo[0] <= n <= fo[1]]
        L.append(f"\n## Nivel {n} ({len(sel)})\n")
        L.append(", ".join(f"[{f['id']}](../{rel(f['_ruta'])})" for f in sel) or "—")
    escribir("formalidad.md", "\n".join(L) + "\n")

    # evidencia.md
    L = ["# Fichas por nivel de evidencia\n"]
    for k, v in EVIDENCIA.items():
        sel = [f for f in fs if f.get("evidencia") == k]
        L.append(f"\n## {k} · {v} ({len(sel)})\n")
        L += [f"- {enlace(f)}" for f in sel]
    tend = [f for f in fs if f.get("vigencia") == "tendencia"]
    L.append(f"\n## Vigencia «tendencia» — revisar periódicamente ({len(tend)})\n")
    L += [f"- {enlace(f)} (actualizado {f.get('actualizado')})" for f in tend]
    escribir("evidencia.md", "\n".join(L) + "\n")

    # fuentes.md
    fu = defaultdict(list)
    for f in fs:
        for s in f.get("fuentes") or []:
            fu[str(s).strip()].append(f["id"])
    L = ["# Fuentes citadas\n", f"{len(fu)} fuentes distintas, ordenadas por número de fichas que las citan.\n"]
    for s, ids in sorted(fu.items(), key=lambda kv: (-len(kv[1]), clave_orden(kv[0]))):
        L.append(f"- {s} — *{', '.join(ids)}*")
    escribir("fuentes.md", "\n".join(L) + "\n")

    # relaciones.md
    L = ["# Relaciones entre fichas\n", "Salientes = la ficha remite a · Entrantes = la citan.\n",
         "| Ficha | Remite a | La citan |\n|---|---|---|"]
    for f in fs:
        L.append(f"| [{f['id']}](../{rel(f['_ruta'])}) | {', '.join(salientes[f['id']]) or '—'} | "
                 f"{', '.join(sorted(entrantes[f['id']])) or '—'} |")
    huerfanas = [f["id"] for f in fs if not entrantes[f["id"]]]
    L.append(f"\nFichas sin enlaces entrantes ({len(huerfanas)}): {', '.join(huerfanas) or 'ninguna'}")
    escribir("relaciones.md", "\n".join(L) + "\n")

    # preguntas.md — todas las preguntas que resuelve cada ficha
    L = ["# Preguntas frecuentes → ficha\n", "Búsqueda rápida: localiza una pregunta parecida a la tuya.\n"]
    for fam in CARPETAS:
        sel = [f for f in fs if f["id"].startswith(fam)]
        if not sel:
            continue
        L.append(f"\n## {NOMBRES[fam]}\n")
        for f in sel:
            cuerpo = f["_cuerpo"]
            ini = cuerpo.find("## Preguntas que resuelve")
            if ini < 0:
                continue
            fin = cuerpo.find("\n## ", ini + 5)
            for linea in cuerpo[ini:fin].splitlines()[1:]:
                linea = linea.strip()
                if linea.startswith(("- ", "* ")):
                    L.append(f"- {linea[2:]} → [{f['id']}](../{rel(f['_ruta'])})")
    escribir("preguntas.md", "\n".join(L) + "\n")

    # datos/fichas.json
    out = []
    for f in fs:
        d = {k: v for k, v in f.items() if not k.startswith("_")}
        d["actualizado"] = str(d.get("actualizado"))
        d["ruta"] = rel(f["_ruta"])
        d["enlaza_a"] = salientes[f["id"]]
        d["citada_por"] = sorted(entrantes[f["id"]])
        out.append(d)
    (DATOS / "fichas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Índices regenerados: {len(fs)} fichas, {len(gl)} términos, {len(et)} etiquetas, {len(fu)} fuentes.")


if __name__ == "__main__":
    main()
