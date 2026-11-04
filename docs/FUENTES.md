# Fuentes tipográficas — JENNIE RUBY, Etapa 2

Las tres familias se descargan durante GitHub Actions desde el repositorio oficial `google/fonts`, fijado a la revisión inmutable:

`2fe1e8c6b137fb13041a7cfca6fdcd8a910ea4dc`

Todas se distribuyen bajo SIL Open Font License (OFL). El workflow descarga también los tres textos de licencia y los incorpora al APK en `assets/fonts/licenses/`. No se necesita una cuenta, suscripción ni servicio externo de pago.

| Uso | Familia | Archivo | Motivo |
|---|---|---|---|
| Hora del reloj | Playfair Display | `playfair_display.ttf` | Serif de alto contraste, elegante y apropiada para cifras grandes de display. |
| Fecha y texto BLACKPINK | Cormorant Garamond | `cormorant_garamond.ttf` | Serif refinada, de trazos finos y proporciones delicadas para texto secundario. |
| Firma | Allura | `allura.ttf` | Caligrafía manuscrita fluida, con apariencia de firma sin los adornos excesivos de una script más recargada. |

## Origen oficial y licencias

- [Playfair Display — Google Fonts](https://github.com/google/fonts/tree/main/ofl/playfairdisplay)
- [Cormorant Garamond — Google Fonts](https://github.com/google/fonts/tree/main/ofl/cormorantgaramond)
- [Allura — Google Fonts](https://github.com/google/fonts/tree/main/ofl/allura)

Los nombres de archivo y las licencias se validan durante el build. Si falta una fuente o un texto OFL, el workflow falla antes de compilar el APK.

## Reproducibilidad

El script `tools/download_widget_fonts.sh` descarga las fuentes y licencias usando la revisión fijada arriba. Las fuentes se generan en `app/src/main/res/font/` antes de que Gradle compile; no se descargan en el teléfono ni durante el uso de los widgets.

Los PNG de vista previa del selector se generan por `tools/generate_widget_previews.py` a partir de esas mismas fuentes. Son simulaciones estáticas para el selector y para inspección del artefacto de CI; el widget real es el layout Android RemoteViews y debe revisarse en el Tecno Pova 4.
