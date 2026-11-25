# ASESOR — Conocimiento de moda y estilo masculino

Base de conocimiento en español, investigada y con fuentes, para consultar dudas de estilo masculino con cualquier IA (o leyéndola directamente).

## Uso

- **Con una IA**: abre esta carpeta en el agente (Claude Code, Cursor, Copilot, etc.) y pide la consulta; el agente debe empezar por `AGENTS.md`. En Claude, `SKILL.md` la expone como skill.
- **Personalizar**: rellena `18-consulta/perfil.md`; el asesor lo usa para no preguntar lo mismo cada vez.
- **Leer a mano**: empieza por `00-indice/mapa.md` (todas las fichas con resumen) o `00-indice/preguntas.md` (preguntas → ficha).

## Estructura

```
AGENTS.md              entrada y protocolo del asesor (reglas R1–R10)
SKILL.md               envoltorio de skill para Claude
CONVENCIONES.md        esquema de las fichas, niveles de evidencia, formalidad
00-indice/             GENERADO: mapa, glosario, etiquetas, preguntas, evidencia, formalidad, fuentes, relaciones
01-fundamentos/ … 17-arreglo-personal/   fichas (fuente de verdad)
18-consulta/           enrutador, cuestionario, perfil, plantilla de respuesta
datos/fichas.json      GENERADO: todas las fichas en JSON (para herramientas o RAG)
herramientas/          catalogo.yaml (plan de fichas), generar_indices.py, validar.py
```

## Mantenimiento

```bash
python3 herramientas/generar_indices.py     # regenera 00-indice/ y datos/
python3 herramientas/validar.py --estricto  # esquema, IDs, enlaces, secciones y fichas pendientes
```

Para añadir una ficha: línea en `herramientas/catalogo.yaml` → fichero en la carpeta de su familia siguiendo `CONVENCIONES.md` → generar → validar. Las fichas con `vigencia: tendencia` (ver `00-indice/evidencia.md`) deben revisarse cada temporada.

Requisitos: Python 3 con PyYAML (`pip install pyyaml`).

## Estado de verificación (2026-11-25)

- 210 fichas escritas por 9 investigadores en paralelo y revisadas después por 5 auditorías cruzadas por tema (etiqueta y protocolo; ajuste y medidas; color, calzado, estudios y salud; tejidos y cuidado; estilos, armario y ocasiones). Cada cifra compartida tiene una **ficha dueña** a la que remiten las demás (p. ej. gramajes → TEJ-011, hora del chaqué → COD-004, precios de arreglos → AJU-006, solapa → SAS-002, puño visible → MIT-006).
- Limitaciones conocidas:
  - Los libros clásicos (Flusser, Roetzel, Boyer, Amies, Antongiavanni, *Take Ivy*) se citan como obras de referencia, no se releyeron página a página.
  - Permanent Style y Debrett's no se pudieron abrir directamente; lo que se les atribuye viene de resúmenes y fuentes secundarias.
  - Precios en € y varias medidas finas son orientativos y están marcados así; revisarlos cada año.
  - Los usos de protocolo de la Casa Real se apoyan en prensa: no hay norma escrita publicada.
  - Clima: normales AEMET 1981–2010.
  - `EST-015` (tendencias) caduca: revisar cada temporada.
- Fichas sugeridas y aún no escritas: `herramientas/propuestas.md`.
