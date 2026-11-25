# Convenciones del sistema ASESOR

Sistema de conocimiento en español sobre moda y estilo masculino. Las **fichas** (`NN-familia/*.md`) son la fuente de verdad; todo lo demás (`00-indice/`, `datos/`) se genera con `herramientas/`.

## Familias e identificadores

| Prefijo | Carpeta | Contenido |
|---|---|---|
| FUN | 01-fundamentos | Principios: ajuste, proporción, formalidad, coherencia, sprezzatura |
| COL | 02-color-y-patron | Teoría del color aplicada, combinaciones, mezcla de estampados |
| MIT | 03-reglas-y-mitos | Reglas clásicas: origen, vigencia y cuándo romperlas |
| CUE | 04-cuerpo | Morfología, rostro, colorimetría personal, tallas |
| AJU | 05-ajuste-y-sastreria | Cómo debe quedar cada prenda, diagnóstico de arrugas, arreglos, medidas |
| SAS | 06-prendas-formales | Traje, americana, camisa de vestir, pantalón de vestir, corbata… |
| CAS | 07-prendas-informales | Vaqueros, chinos, camisetas, polos, punto, sobrecamisas… |
| EXT | 08-prendas-exteriores | Abrigos, chaquetas, gabardinas, parkas |
| CAL | 09-calzado | Tipos, construcción, combinaciones, cuidado específico |
| ACC | 10-accesorios | Reloj, cinturón, calcetines, gafas, sombreros, bolsos, joyería |
| TEJ | 11-tejidos-y-construccion | Fibras, tejidos, gramajes, construcción y señales de calidad |
| CUI | 12-cuidado | Lavado, planchado, almacenaje, reparación |
| COD | 13-codigos-de-vestimenta | Etiqueta, dress codes, protocolo (incluido el español) |
| OCA | 14-ocasiones | Bodas, entrevistas, oficina, viajes, clima, eventos |
| EST | 15-estilos | Estéticas y tradiciones (británico, napolitano, Ivy, workwear…) |
| ARM | 16-armario | Cápsula, prioridades de compra, presupuesto, fórmulas de outfit |
| ASE | 17-arreglo-personal | Pelo, barba, piel, fragancia |

ID = `PREFIJO-NNN` (tres dígitos). Nombre de fichero = `prefijo-nnn-slug.md` en minúsculas, p. ej. `fun-001-el-ajuste-primero.md`.

## Front matter (YAML, obligatorio)

```yaml
---
id: FUN-001
titulo: El ajuste es lo primero
familia: FUN
resumen: Una línea (máx. ~200 caracteres) con la idea central.
etiquetas: [ajuste, proporcion]        # minúsculas, sin tildes, con guiones
evidencia: T                            # ver niveles abajo
vigencia: atemporal                     # atemporal | duradera | tendencia
formalidad: [1, 5]                      # rango 1–5 al que aplica; [] si no aplica
relacionadas: [AJU-001, SAS-001]        # IDs existentes o previstos
terminos: [drop, canvas]                # términos que la ficha define (alimentan el glosario)
fuentes:
  - "Autor o institución — Título (año). URL si existe"
actualizado: 2026-11-25
---
```

### Niveles de evidencia (`evidencia`)

| Nivel | Significado |
|---|---|
| N | **Norma**: protocolo o código escrito por una autoridad (Debrett's, Casa Real, invitaciones formales, normas ISO/EN de tallas y cuidado). |
| T | **Técnica**: consenso de sastrería, fabricación o textil; verificable en manuales de oficio y fabricantes. |
| E | **Empírica**: respaldada por estudios publicados (percepción, psicología de la vestimenta, colorimetría). Citar el estudio. |
| C | **Consenso editorial**: coincidencia de varias fuentes de referencia (libros clásicos, prensa especializada), sin norma ni estudio. |
| O | **Opinión / gusto**: criterio estético razonado o tendencia; debe decirse como tal. |

Una ficha toma el nivel de su afirmación **central**; si mezcla niveles, marcarlos en línea con `[N]`, `[T]`, `[E]`, `[C]`, `[O]`.

### Formalidad (escala 1–5)

1 = ropa de estar en casa / deporte · 2 = casual · 3 = smart casual · 4 = business / traje de calle · 5 = etiqueta (chaqué, esmoquin, frac).

## Cuerpo de la ficha (secciones en este orden)

```
# {titulo}

> {resumen}

## Qué es / idea central
## Cómo aplicarlo            (reglas concretas, medidas, números cuando existan)
## Errores frecuentes
## Matices y excepciones      (clima, cuerpo, país, edad, contexto)
## Preguntas que resuelve     (3–6 preguntas tal como las haría un usuario)
## Fuentes                    (lista; síntesis propia, nunca texto copiado)
```

Se pueden añadir tablas y subsecciones dentro de esas secciones. Longitud orientativa: 300–900 palabras.

## Reglas de redacción

1. **Síntesis propia**: nunca copiar ni traducir literalmente textos con derechos; citar la fuente.
2. **Concreción**: medidas en cm, gramajes en g/m², números cuando existan. "Queda bien" no es una regla; "la manga deja ver 1–1,5 cm de camisa" sí.
3. **Explicar el porqué** de cada regla (función, historia, percepción) para poder razonar excepciones.
4. **Sin marcas** salvo cuando la marca *es* el conocimiento (p. ej. Goodyear como sistema, Barbour como origen del waxed jacket). Nada de publicidad.
5. **Inclusivo en cuerpo, edad y presupuesto**: las recomendaciones no presuponen un cuerpo "ideal".
6. **Tendencias** con `vigencia: tendencia` y fecha; nunca mezclar tendencia con principio.
7. **Contexto español y europeo** por defecto (tallas EU, clima peninsular, protocolo español), señalando diferencias con EE. UU./Reino Unido/Italia.

## Referencias cruzadas y catálogo

- En el cuerpo, enlazar otras fichas con `[[ID]]`, p. ej. `ver [[AJU-001]]`. En `relacionadas`, solo IDs.
- Todo ID debe existir en `herramientas/catalogo.yaml` (el plan de fichas). El título de la ficha debe coincidir con el del catálogo.
- Para añadir una ficha nueva: línea en el catálogo → fichero → `python3 herramientas/generar_indices.py` → `python3 herramientas/validar.py`.
