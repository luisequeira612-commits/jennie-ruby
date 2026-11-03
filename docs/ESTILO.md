# Estilo visual — JENNIE RUBY

> Referencia técnica del generador de la Etapa 1. Los valores de esta página se transcriben del código de producción del generador; no son una reconstrucción visual ni una propuesta para modificar los iconos.

## Fuente de verdad

- Generador: `tools/render_ruby_stage1_icons.py`
- Vectores de origen: `tools/ruby_icon_sources/ruby_*.xml`
- Recursos generados: `app/src/main/res/drawable-nodpi/ruby_*.png`
- Workflow: `.github/workflows/android-build.yml`
- Mapeo de Nova: `app/src/main/res/xml/appfilter.xml`
- Rama donde se documentó esta versión: `stage-1/final-glass-camera-gallery` (PR #74).

El workflow instala Pillow y CairoSVG en el runner de GitHub Actions. El generador rasteriza las formas vectoriales y crea diez PNG RGBA de 192 × 192 px. Pillow y CairoSVG son dependencias de compilación: no se empaquetan en el APK. Los diez PNG se comprueban en CI y se guardan en `drawable-nodpi`.

## Geometría de la base

| Propiedad | Valor del generador |
|---|---:|
| Lienzo | 192 × 192 px |
| Squircle | `(13, 13, 179, 179)` |
| Tamaño declarado | 166 × 166 px |
| Porcentaje del lienzo | 86,46 % |
| Radio de esquinas | 43 px |
| Máscara | Rectángulo redondeado, aplicado también al fondo |

La máscara del squircle define la superficie visible. Las esquinas exteriores del PNG permanecen transparentes.

## Sombra

- Color: negro (`#000000`).
- Máscara: la misma forma squircle.
- Desenfoque: `GaussianBlur(radius=8)`.
- Desplazamiento de composición: `(0, +4)` px.
- Opacidad: 46 % (multiplicador `0.46` sobre el alfa de la máscara desenfocada).

## Fondo y degradado localizado

- Base: `#080304` en la parte superior y también en la inferior; el gradiente vertical base es, por tanto, constante.
- Tinte de vino: `#2A0A10`.
- El tinte se compone como una capa alfa localizada hacia la esquina inferior derecha.
- Intensidad máxima de la mezcla: 38 % (`0.38`).
- La intensidad depende de las coordenadas normalizadas desde x=82 e y=88 y usa exponente 1.10. No es una división plana ni un segundo panel.
- La capa final de fondo queda recortada por la máscara squircle.

## Glifo

- El color se aplica mediante un degradado vertical: arriba `#E0334B`, abajo `#8E0B20`.
- El generador obtiene la máscara de los paths de los vectores fuente; para Cámara, Instagram y Galería construye máscaras específicas con Pillow.
- El resplandor usa el color superior del glifo (`#E0334B`), desenfoque de 2,2 px y alfa del 16 %.
- La geometría y el tamaño visible dependen de cada aplicación. No existe en el código un porcentaje de escala común para los diez glifos, así que no se debe documentar ni imponer uno.

### Máscaras especiales

- Cámara: cuerpo redondeado, saliente superior, lente y flash; dibujados mediante rectángulos redondeados y elipses.
- Instagram: contorno cuadrado redondeado, aro central y punto superior derecho.
- Galería: cinco pétalos elípticos y hueco central.

Los otros siete glifos se derivan de los paths de sus vectores fuente, conservando las sustracciones de las zonas negras/huecas.

## Borde y bisel

- Borde exterior: `#7A1624`, 3 px, siguiendo el squircle.
- Bisel superior: `#C23A4B`, arco superior de 3 px.
- El bisel se suaviza con `GaussianBlur(radius=1.2)`.
- Alfa máximo del bisel: 60 %.
- El bisel se desvanece horizontalmente en los extremos y hacia abajo.

## Reflejo de vidrio

- Color: `#FFEEF2`.
- Alfa máximo: 9 %.
- Concentrado en el 35 % superior del lienzo.
- Atenuación horizontal hacia ambos bordes.
- Desenfoque: 7 px.
- Se recorta con la máscara squircle.
- No dibuja un contorno curvo duro: es un lavado de luz suave.

## Paleta registrada

| Uso | HEX |
|---|---|
| Superficie casi negra | `#080304` |
| Tinte borgoña | `#2A0A10` |
| Borde rubí oscuro | `#7A1624` |
| Bisel rubí | `#C23A4B` |
| Rojo rubí auxiliar | `#C8102E` |
| Glifo, parte superior | `#E0334B` |
| Glifo, parte inferior | `#8E0B20` |
| Reflejo | `#FFEEF2` |

## Límites y protección de la Etapa 1

- Este documento describe únicamente el acabado de los diez iconos de la cuadrícula principal.
- No autoriza cambios de forma, color, escala, sombra ni acabado en los iconos aprobados.
- El fondo de pantalla, los widgets, el dock y el widget de música pertenecen a etapas separadas.
- Las hojas de contacto son salidas generadas por el script de CI para inspección; no sustituyen la comprobación en el Tecno Pova 4 con Nova Launcher.
- El workflow falla si falta un recurso generado, si el PNG no es RGBA de 192 × 192 px o si sus esquinas no conservan transparencia.

## Etapa 3 — iconos del dock

Los cuatro iconos de aplicación del dock (Teléfono, Contactos, Mensajes y Chrome) se rasterizan llamando a la función `render()` del generador protegido de Etapa 1. No mantienen una copia paralela de colores, geometría, sombra, bisel ni reflejo. El archivo `tools/render_ruby_stage1_icons.py` debe conservar su Git blob SHA-1 histórico `7eae0f7904744e190d520d9e9fe4ad131414d815`.

El cajón de aplicaciones es la excepción circular solicitada: superficie `#080304`, borde `#7A1624`, bisel superior `#C23A4B` y nueve puntos 3 × 3 en rosa pálido/gris claro. Conserva el lienzo RGBA de 192 × 192 px y las esquinas transparentes.

Los nombres públicos usados por Nova se declaran como alias en `app/src/main/res/values/drawable.xml`; sus PNG de arte terminan en `_art`. El generador de `appfilter.xml` valida que cada alias apunte a un recurso existente en `drawable-nodpi`.

La hoja de contacto de Etapa 3 se genera desde los quince PNG reales (diez originales más cinco del dock), a 2000 × 1350 px. No es una maqueta.
