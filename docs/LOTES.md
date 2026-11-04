# Lotes de iconos — Etapa 5

El catálogo maestro es `icons.json`. Cada activity se marca `verified` solo si pertenece a la lista de apps que el usuario confirmó en el teléfono; las demás quedan `estimated`.

## Lote 1 — 20 aplicaciones

Maps, Gmail, Drive, Photos, Calendar, YouTube Music, Facebook, Messenger, Telegram, Snapchat, X, Pinterest, Reddit, Netflix, Disney+, HBO Max, Crunchyroll, Twitch, ChatGPT, Claude.

## Lote 2 — 20 aplicaciones

Aniyomi, Mihon, Brave, CapCut, Gemini, DeepSeek, Duolingo, Excel, WPS Office, Files de Google, Kodi, VLC, Stremio, Shazam, Picsart, Weverse, Roblox, Termux, AnkiDroid, WeChat.

## Lote 3 — 28 de 30 aplicaciones solicitadas

Memrise, Drops, HelloTalk, Falou, Ling, LingQ, LangReactor, Reelang, Write Greek, Moon+ Reader, ReadEra, Lector de PDF, LNReader, Shosetsu, bilibili, CloudStream, Inkaplay, Lark Player, MXL TV, Xuper, Rave, Mnet Plus, Songstats, Soundcharts, SportzX, GeeSports, Lean Remote, LGRemote.

No se añadieron Cuestionario (`com.idea.questionnaire`) ni FM (`com.funbase.xradio`): sus paquetes no aparecen en el catálogo de dispositivos ni en el `appfilter.xml` de `main`. No se inventaron entradas ni activities.

Brave y CloudStream están marcadas `verified` porque figuran en la lista de apps verificadas por el usuario. Las otras 26 activities permanecen `estimated`.

## Reutilización de componentes

Los 28 componentes del lote 3 ya existían en el `appfilter.xml` anterior. Se conservan sus componentes y activities, y `icons.json` pasa a ser la fuente de autoridad para que el generador actualice cada drawable al PNG de Etapa 5, sin duplicar componentes.

La hoja de contacto se genera desde los diez PNG de Etapa 1, cinco PNG del dock y todos los PNG del catálogo. El generador de Etapa 1, sus diez PNG aprobados, el dock, los widgets, los lotes 1 y 2 y `docs/ESTILO.md` permanecen protegidos.
