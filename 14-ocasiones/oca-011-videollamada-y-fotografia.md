---
id: OCA-011
titulo: Videollamada y fotografía
familia: OCA
resumen: "La cámara muestrea la imagen en píxeles y la comprime: rayas finas, espigas y cuadros pequeños crean moiré, el blanco puro se quema y el rojo saturado se corre; ganan los lisos de tono medio."
etiquetas: [videollamada, camara, fotografia, moire, color, teletrabajo]
evidencia: T
vigencia: duradera
formalidad: [2, 4]
relacionadas: [COL-008, COL-006, OCA-013, OCA-003, OCA-004, CUE-007, FUN-006, ASE-004, SAS-009, COL-007]
terminos: [moire, aliasing, frecuencia-de-nyquist, submuestreo-de-croma, exposicion-automatica]
fuentes:
  - "Rick Wicklin — Moiré patterns: Or why you shouldn't wear a striped shirt on a video (The DO Loop, SAS Blogs, 5 junio 2023). https://blogs.sas.com/content/iml/2023/06/05/moire-patterns.html"
  - "Adobe — Anti-aliasing (adobe.com/creativecloud/photography/discover/anti-aliasing.html)"
  - "University of Toronto Mississauga — Tips on what to wear to broadcast interviews (utm.utoronto.ca)"
  - "Columbia School of Social Work — What to wear on camera (PDF)"
  - "Comunidad Zoom — hilo 'Striped Shirt is Vibrating' (community.zoom.com), testimonios de usuarios"
  - "ITU-T H.264 / ISO/IEC 14496-10 (perfiles Main y High, formato de croma 4:2:0)"
actualizado: 2026-11-25
---

# Videollamada y fotografía

> La cámara muestrea la imagen en píxeles y la comprime: rayas finas, espigas y cuadros pequeños crean moiré, el blanco puro se quema y el rojo saturado se corre; ganan los lisos de tono medio.

## Qué es / idea central

Una cámara no ve como el ojo: convierte la escena en una rejilla de píxeles, ajusta la exposición automáticamente y comprime la señal. Tres fenómenos técnicos explican casi todos los problemas de ropa ante cámara:

1. **Moiré y aliasing**. Si el patrón de la tela tiene un periodo cercano o inferior al doble del tamaño del píxel (el límite de la **frecuencia de Nyquist**), la cámara no puede representarlo y genera un patrón falso: ondas, bandas o arcoíris que además "vibran" cuando uno se mueve. Eso es el **aliasing**; el **moiré** es su forma visible, la interferencia entre dos rejillas (la tela y el sensor). Muchas cámaras modernas omiten el filtro óptico antialiasing para ganar nitidez, lo que favorece el efecto [T].
2. **Exposición automática**. La cámara ajusta el brillo para que el promedio de la imagen sea medio. Una camisa blanca grande "engaña" al sistema: o la camisa se **quema** (pierde textura, se ve como mancha blanca) o la cara queda oscura [T].
3. **Compresión y submuestreo de croma**. El vídeo de videollamada suele codificarse en H.264 o similar con **submuestreo de croma** 4:2:0: el color se guarda a un cuarto de la resolución del brillo. Los colores muy saturados (rojo, naranja, magenta) pierden bordes y parecen "correrse"; los detalles finos se convierten en bloques cuando hay poco ancho de banda [T].

**Estimación propia** (orden de magnitud, no medición): con plano de medio cuerpo, el ancho visible ronda 70–90 cm. A 1280 píxeles de ancho (720p) cada píxel cubre ~0,6–0,7 mm de tela; con conexión mala la videollamada baja a 640 píxeles (~1,2–1,4 mm por píxel). Patrones con periodo inferior a ~3 mm (raya fina de camisa, *pinpoint* con color, espiguilla pequeña, *pied-de-poule* menudo, pana fina) caen en zona de riesgo.

## Cómo aplicarlo

| Elemento | Problemático | Seguro |
|---|---|---|
| Patrón | Raya fina y muy contrastada, espiga (*herringbone*) pequeña, pata de gallo pequeña, cuadro vichy menudo, pana fina, punto de rayas finas | Lisos; textura sin contraste (oxford liso, punto liso); patrones grandes (cuadro > 1–2 cm) |
| Color de camisa | Blanco puro brillante en planos cortos; negro absoluto (pierde detalle y se funde con fondos oscuros) | Celeste, azul medio, gris medio, crudo, rosa pálido |
| Color saturado | Rojo y naranja intensos, verde croma si se usa fondo virtual | Azules, verdes y burdeos apagados |
| Tejidos | Seda o satén brillante, estambre muy liso bajo luz fuerte (brilla) | Tejidos mates |
| Accesorios | Metales que reflejan, gafas con reflejo | Gafas con antirreflejante, reloj mate ([[ACC-004]]) |

Consejos operativos:
- **Prueba previa**: vista previa de la propia cámara, moviéndose, con la luz real de la llamada.
- **Contraste con el fondo**: si el fondo es blanco, evitar camisa blanca; si es oscuro, evitar negro.
- **Fondo virtual**: no llevar el color del croma; el pelo y los bordes con poco contraste "parpadean".
- **Ajustes**: reducir la nitidez del software de la cámara o desactivar modos "HD" agresivos ha reducido el moiré a algunos usuarios (testimonios en la comunidad de Zoom; no es una solución universal).
- **Luz frontal suave**, cámara a la altura de los ojos: corrige más que cambiar de camisa.

## Errores frecuentes

- Estrenar una camisa de raya fina el día de la videoentrevista ([[OCA-003]]).
- Camisa blanca, fondo blanco y ventana detrás: silueta oscura.
- Corbata de microdibujo muy contrastada: es lo que antes vibra.
- Pensar que una cámara 4K elimina el problema: la llamada se transmite a menor resolución.

## Matices y excepciones

- **Fotografía fija de alta resolución** (retrato profesional) tolera mejor patrones finos, pero el moiré sigue apareciendo al reducir la imagen para web.
- **Colorimetría personal** ([[CUE-007]]): los tonos cercanos a la cara afectan más en cámara que en persona porque la cámara exagera el contraste.
- **Televisión y escenario** tienen además iluminación fuerte; ver [[OCA-013]].
- **Discrepancia**: algunas guías de emisoras aceptan rojo y blanco "en poca cantidad"; las más estrictas los prohíben. La causa técnica es real, la tolerancia depende de la cámara.

## Preguntas que resuelve

- ¿Por qué mi camisa de rayas hace ondas en Zoom?
- ¿Qué color de camisa queda mejor en videollamada?
- ¿Puedo llevar camisa blanca en una videoentrevista?
- ¿Qué ropa evito en una foto de perfil profesional?
- ¿Por qué la americana de espiga se ve rara en vídeo?

## Fuentes

- Rick Wicklin, SAS Blogs (2023): explicación del moiré como interferencia de rejillas.
- Adobe, *Anti-aliasing*: filtro óptico de paso bajo y aliasing en ropa.
- Guías de vestuario para televisión de University of Toronto Mississauga y Columbia School of Social Work.
- Comunidad Zoom: soluciones de usuarios (anecdóticas).
- Norma ITU-T H.264: perfiles Main y High trabajan con croma 4:2:0, el formato habitual en videoconferencia.
