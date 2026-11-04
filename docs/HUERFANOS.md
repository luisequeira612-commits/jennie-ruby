# Recursos heredados y huérfanos — Etapa 5

## Lote 3

Los 28 componentes de las aplicaciones incluidas ya existían en el `appfilter.xml` de `main`. Sus identificadores drawable heredados coinciden con los nuevos nombres del catálogo de Etapa 5:

| Aplicación | Drawable heredado reutilizado |
|---|---|
| Memrise | `ruby_memrise` |
| Drops | `ruby_drops` |
| HelloTalk | `ruby_hellotalk` |
| Falou | `ruby_falou` |
| Ling | `ruby_ling` |
| LingQ | `ruby_lingq` |
| LangReactor | `ruby_langreactor` |
| Reelang | `ruby_reelang` |
| Write Greek | `ruby_write_greek` |
| Moon+ Reader | `ruby_moon_reader` |
| ReadEra | `ruby_readera` |
| Lector de PDF | `ruby_lector_de_pdf` |
| LNReader | `ruby_lnreader` |
| Shosetsu | `ruby_shosetsu` |
| bilibili | `ruby_bilibili` |
| CloudStream | `ruby_cloudstream` |
| Inkaplay | `ruby_inkaplay` |
| Lark Player | `ruby_lark_player` |
| MXL TV | `ruby_mxl_tv` |
| Xuper | `ruby_xuper` |
| Rave | `ruby_rave` |
| Mnet Plus | `ruby_mnet_plus` |
| Songstats | `ruby_songstats` |
| Soundcharts | `ruby_soundcharts` |
| SportzX | `ruby_sportzx` |
| GeeSports | `ruby_geesports` |
| Lean Remote | `ruby_lean_remote` |
| LGRemote | `ruby_lgremote` |

Estos nombres se reutilizan para los nuevos PNG; no se crean componentes duplicados. La sincronización de Nova se ejecuta desde `device-app-catalog.tsv` más `icons.json`.

## Archivos vectoriales huérfanos confirmados

Ningún archivo vectorial antiguo separado pudo confirmarse en las rutas fuente consultadas. Por eso no se declara ni se borra ningún vector como huérfano. La tabla anterior registra los nombres heredados del appfilter, no afirma que exista un archivo XML independiente con cada nombre.

## Paquetes no encontrados

- Cuestionario — `com.idea.questionnaire`
- FM — `com.funbase.xradio`

No se generaron entradas para estos dos paquetes.
