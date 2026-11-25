"""Valida las fichas contra CONVENCIONES.md y el catálogo.

Uso:
  python herramientas/validar.py                 # todo el sistema
  python herramientas/validar.py --familia CAL   # solo una familia (las referencias se comprueban igual)
  python herramientas/validar.py --estricto      # además exige que existan todas las fichas del catálogo

Sale con código 1 si hay errores. Los avisos no hacen fallar.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys

from comun import (CAMPOS, CARPETAS, EVIDENCIA, RE_ENLACE, SECCIONES, VIGENCIA,
                   catalogo, ficheros_ficha, leer, rel)

RE_SLUG = re.compile(r"^([a-z]{3})-(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
RE_ETIQ = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RE_H2 = re.compile(r"^## (.+?)\s*$", re.M)


def sin_codigo(texto: str) -> str:
    return re.sub(r"```.*?```", "", texto, flags=re.S)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--familia")
    ap.add_argument("--estricto", action="store_true")
    a = ap.parse_args()

    cat = catalogo()
    errores: list[str] = []
    avisos: list[str] = []
    vistos: dict[str, str] = {}

    for ruta in ficheros_ficha():
        r = rel(ruta)
        fam_carpeta = next(f for f, c in CARPETAS.items() if ruta.parent.name == c)
        if a.familia and fam_carpeta != a.familia:
            continue
        E = lambda m: errores.append(f"{r}: {m}")  # noqa: E731
        W = lambda m: avisos.append(f"{r}: {m}")  # noqa: E731

        m = RE_SLUG.match(ruta.name)
        if not m:
            E("nombre de fichero no cumple prefijo-nnn-slug.md")
            continue
        try:
            fm, cuerpo = leer(ruta)
        except Exception as ex:  # noqa: BLE001
            E(f"front matter ilegible: {ex}")
            continue

        for c in CAMPOS:
            if c not in fm:
                E(f"falta el campo '{c}'")
        extra = set(fm) - set(CAMPOS)
        if extra:
            W(f"campos no previstos: {sorted(extra)}")

        fid = str(fm.get("id", ""))
        esperado = f"{m.group(1).upper()}-{m.group(2)}"
        if fid != esperado:
            E(f"id '{fid}' no coincide con el fichero ({esperado})")
        if fid in vistos:
            E(f"id duplicado con {vistos[fid]}")
        vistos[fid] = r
        if fid not in cat:
            E(f"id '{fid}' no está en herramientas/catalogo.yaml")
        if fm.get("familia") != fam_carpeta or not fid.startswith(fam_carpeta):
            E(f"familia '{fm.get('familia')}' no corresponde a la carpeta {ruta.parent.name}")
        if fm.get("evidencia") not in EVIDENCIA:
            E(f"evidencia '{fm.get('evidencia')}' no es N/T/E/C/O")
        if fm.get("vigencia") not in VIGENCIA:
            E(f"vigencia '{fm.get('vigencia')}' no válida")

        resumen = str(fm.get("resumen", "")).strip()
        if len(resumen) > 260:
            W(f"resumen largo ({len(resumen)} caracteres)")

        fo = fm.get("formalidad")
        if not isinstance(fo, list) or (fo and (len(fo) != 2 or not all(isinstance(x, int) and 1 <= x <= 5 for x in fo) or fo[0] > fo[1])):
            E(f"formalidad debe ser [] o [min, max] con enteros 1–5: {fo}")

        for campo in ("etiquetas", "relacionadas", "terminos", "fuentes"):
            if not isinstance(fm.get(campo, []), list):
                E(f"'{campo}' debe ser una lista")
        for t in fm.get("etiquetas") or []:
            if not RE_ETIQ.match(str(t)):
                E(f"etiqueta no normalizada: '{t}'")
        if not fm.get("fuentes"):
            E("sin fuentes")
        for rid in fm.get("relacionadas") or []:
            if rid not in cat:
                E(f"relacionada desconocida: {rid}")
            if rid == fid:
                W("se relaciona consigo misma")
        if not isinstance(fm.get("actualizado"), (dt.date, str)):
            E("actualizado debe ser fecha AAAA-MM-DD")

        texto = sin_codigo(cuerpo)
        h1 = re.search(r"^# (.+?)\s*$", texto, re.M)
        if not h1:
            E("falta el título H1")
        elif h1.group(1) != fm.get("titulo"):
            W(f"H1 '{h1.group(1)}' distinto del titulo '{fm.get('titulo')}'")
        if fid in cat and fm.get("titulo") != cat[fid]:
            W(f"titulo distinto del catálogo ('{cat[fid]}')")
        if not re.search(r"^> .+", texto, re.M):
            E("falta la cita de resumen (> ...)")

        h2 = [h for h in RE_H2.findall(texto)]
        pos = []
        for s in SECCIONES:
            if s not in h2:
                E(f"falta la sección '## {s}'")
            else:
                pos.append(h2.index(s))
        if pos != sorted(pos):
            E("secciones obligatorias fuera de orden")

        for ref in RE_ENLACE.findall(texto):
            if ref not in cat:
                E(f"enlace a ficha inexistente [[{ref}]]")

        palabras = len(re.findall(r"\w+", texto))
        if palabras < 250:
            W(f"corta ({palabras} palabras)")
        elif palabras > 1400:
            W(f"larga ({palabras} palabras)")

    # Documentos de consulta: sus [[ID]] también deben existir (y, con --estricto, estar escritos)
    from comun import RAIZ
    for doc in [RAIZ / "AGENTS.md", RAIZ / "SKILL.md", RAIZ / "README.md", *sorted((RAIZ / "18-consulta").glob("*.md"))]:
        if not doc.exists():
            continue
        for ref in RE_ENLACE.findall(doc.read_text(encoding="utf-8")):
            if ref not in cat:
                errores.append(f"{rel(doc)}: enlace a ficha inexistente [[{ref}]]")

    if a.estricto:
        for cid in cat:
            if (not a.familia or cid.startswith(a.familia)) and cid not in vistos:
                errores.append(f"catálogo: falta la ficha {cid} ({cat[cid]})")

    for w in avisos:
        print("AVISO ", w)
    for e in errores:
        print("ERROR ", e)
    print(f"\n{len(vistos)} fichas revisadas · {len(errores)} errores · {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
