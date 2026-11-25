"""Utilidades compartidas: lectura de catálogo y fichas."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent

CARPETAS = {
    "FUN": "01-fundamentos",
    "COL": "02-color-y-patron",
    "MIT": "03-reglas-y-mitos",
    "CUE": "04-cuerpo",
    "AJU": "05-ajuste-y-sastreria",
    "SAS": "06-prendas-formales",
    "CAS": "07-prendas-informales",
    "EXT": "08-prendas-exteriores",
    "CAL": "09-calzado",
    "ACC": "10-accesorios",
    "TEJ": "11-tejidos-y-construccion",
    "CUI": "12-cuidado",
    "COD": "13-codigos-de-vestimenta",
    "OCA": "14-ocasiones",
    "EST": "15-estilos",
    "ARM": "16-armario",
    "ASE": "17-arreglo-personal",
}

NOMBRES = {
    "FUN": "Fundamentos",
    "COL": "Color y patrón",
    "MIT": "Reglas y mitos",
    "CUE": "Cuerpo",
    "AJU": "Ajuste y sastrería",
    "SAS": "Prendas formales",
    "CAS": "Prendas informales",
    "EXT": "Prendas exteriores",
    "CAL": "Calzado",
    "ACC": "Accesorios",
    "TEJ": "Tejidos y construcción",
    "CUI": "Cuidado",
    "COD": "Códigos de vestimenta",
    "OCA": "Ocasiones",
    "EST": "Estilos",
    "ARM": "Armario",
    "ASE": "Arreglo personal",
}

EVIDENCIA = {
    "N": "Norma",
    "T": "Técnica",
    "E": "Empírica",
    "C": "Consenso editorial",
    "O": "Opinión / gusto",
}
VIGENCIA = {"atemporal", "duradera", "tendencia"}
SECCIONES = [
    "Qué es / idea central",
    "Cómo aplicarlo",
    "Errores frecuentes",
    "Matices y excepciones",
    "Preguntas que resuelve",
    "Fuentes",
]
CAMPOS = [
    "id", "titulo", "familia", "resumen", "etiquetas", "evidencia", "vigencia",
    "formalidad", "relacionadas", "terminos", "fuentes", "actualizado",
]
RE_ENLACE = re.compile(r"\[\[([A-Z]{3}-\d{3})\]\]")
RE_FM = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def catalogo() -> dict[str, str]:
    datos = yaml.safe_load((RAIZ / "herramientas" / "catalogo.yaml").read_text(encoding="utf-8"))
    out = {}
    for fam, fichas in datos.items():
        for num, titulo in fichas.items():
            out[f"{fam}-{int(num):03d}"] = titulo
    return out


def ficheros_ficha():
    for fam, carpeta in CARPETAS.items():
        d = RAIZ / carpeta
        if d.is_dir():
            yield from sorted(d.glob("*.md"))


def leer(ruta: Path):
    """Devuelve (front_matter: dict, cuerpo: str) o lanza ValueError."""
    texto = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = RE_FM.match(texto)
    if not m:
        raise ValueError("sin front matter YAML delimitado por ---")
    fm = yaml.safe_load(m.group(1)) or {}
    if not isinstance(fm, dict):
        raise ValueError("front matter no es un mapa")
    return fm, m.group(2)


def fichas():
    """Lista de dicts con fm + cuerpo + ruta, ignorando las ilegibles."""
    res = []
    for r in ficheros_ficha():
        try:
            fm, cuerpo = leer(r)
        except Exception:  # el validador informa del error
            continue
        fm = dict(fm)
        fm["_ruta"] = r
        fm["_cuerpo"] = cuerpo
        res.append(fm)
    return res


def rel(ruta: Path) -> str:
    return ruta.relative_to(RAIZ).as_posix()
