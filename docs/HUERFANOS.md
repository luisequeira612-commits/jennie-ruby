# Recursos heredados y huérfanos — Etapa 5

## Lote 3 — 28 componentes reutilizados

| Aplicación | Drawable |
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

## Lote 4 — 25 componentes reutilizados

| Aplicación | Drawable |
|---|---|
| rednote | `ruby_rednote` |
| NGL | `ruby_ngl` |
| Zangi | `ruby_zangi` |
| Labalabi For WhatsApp | `ruby_labalabi_for_whatsapp` |
| SocialAut | `ruby_socialaut` |
| Sticker.ly | `ruby_sticker_ly` |
| StickerVibe | `ruby_stickervibe` |
| Reface | `ruby_reface` |
| Viggle AI | `ruby_viggle_ai` |
| HoYoLAB | `ruby_hoyolab` |
| MCPEDL | `ruby_mcpedl` |
| MU Fan | `ruby_mu_fan` |
| Duskwood | `ruby_duskwood` |
| Blackjack Trainer | `ruby_blackjack_trainer` |
| AHA Games | `ruby_aha_games` |
| Meu Tarot | `ruby_meu_tarot` |
| Windy | `ruby_windy` |
| Moovit | `ruby_moovit` |
| Google Earth | `ruby_google_earth` |
| DeepStateMap | `ruby_deepstatemap` |
| PedidosYa | `ruby_pedidosya` |
| Mi Claro | `ruby_mi_claro` |
| Mi Tigo | `ruby_mi_tigo` |
| Tor Browser | `ruby_tor_browser` |
| Urban VPN | `ruby_urban_vpn` |

## Paquetes pendientes

- Palm Store — `com.transsnet.store`
- TECNO ID — `tech.palm.id`
- Hola — `com.talpa.hibrowser`

No aparecen en `device-app-catalog.tsv` ni en `appfilter.xml`; no se inventaron activities ni se crearon componentes.

## Vectores heredados sustituidos durante el build (93)

La inspección del árbol de `app/src/main/res/drawable-nodpi` en esta rama encontró los 93 XML siguientes, uno por cada drawable de `icons.json`. Son recursos vectoriales heredados que el renderizador sustituye por PNG durante el build: `tools/render_stage5_batch1.py` elimina del **workspace de CI** el XML de cada drawable antes de compilar. Esta limpieza no borra los archivos versionados de GitHub; se documentan aquí para conservar su trazabilidad.

`ruby_maps.xml`, `ruby_gmail.xml`, `ruby_drive.xml`, `ruby_fotos.xml`, `ruby_calendario.xml`, `ruby_youtube_music.xml`, `ruby_facebook.xml`, `ruby_messenger.xml`, `ruby_telegram.xml`, `ruby_snapchat.xml`, `ruby_x.xml`, `ruby_pinterest.xml`, `ruby_reddit.xml`, `ruby_netflix.xml`, `ruby_disney.xml`, `ruby_hbo_max.xml`, `ruby_crunchyroll.xml`, `ruby_twitch.xml`, `ruby_chatgpt.xml`, `ruby_claude.xml`, `ruby_aniyomi.xml`, `ruby_mihon.xml`, `ruby_brave.xml`, `ruby_capcut.xml`, `ruby_gemini.xml`, `ruby_deepseek.xml`, `ruby_duolingo.xml`, `ruby_excel.xml`, `ruby_wps_office.xml`, `ruby_files_de_google.xml`, `ruby_kodi.xml`, `ruby_vlc.xml`, `ruby_stremio.xml`, `ruby_shazam.xml`, `ruby_picsart.xml`, `ruby_weverse.xml`, `ruby_roblox.xml`, `ruby_termux.xml`, `ruby_ankidroid.xml`, `ruby_wechat.xml`, `ruby_memrise.xml`, `ruby_drops.xml`, `ruby_hellotalk.xml`, `ruby_falou.xml`, `ruby_ling.xml`, `ruby_lingq.xml`, `ruby_langreactor.xml`, `ruby_reelang.xml`, `ruby_write_greek.xml`, `ruby_moon_reader.xml`, `ruby_readera.xml`, `ruby_lector_de_pdf.xml`, `ruby_lnreader.xml`, `ruby_shosetsu.xml`, `ruby_bilibili.xml`, `ruby_cloudstream.xml`, `ruby_inkaplay.xml`, `ruby_lark_player.xml`, `ruby_mxl_tv.xml`, `ruby_xuper.xml`, `ruby_rave.xml`, `ruby_mnet_plus.xml`, `ruby_songstats.xml`, `ruby_soundcharts.xml`, `ruby_sportzx.xml`, `ruby_geesports.xml`, `ruby_lean_remote.xml`, `ruby_lgremote.xml`, `ruby_rednote.xml`, `ruby_ngl.xml`, `ruby_zangi.xml`, `ruby_labalabi_for_whatsapp.xml`, `ruby_socialaut.xml`, `ruby_sticker_ly.xml`, `ruby_stickervibe.xml`, `ruby_reface.xml`, `ruby_viggle_ai.xml`, `ruby_hoyolab.xml`, `ruby_mcpedl.xml`, `ruby_mu_fan.xml`, `ruby_duskwood.xml`, `ruby_blackjack_trainer.xml`, `ruby_aha_games.xml`, `ruby_meu_tarot.xml`, `ruby_windy.xml`, `ruby_moovit.xml`, `ruby_google_earth.xml`, `ruby_deepstatemap.xml`, `ruby_pedidosya.xml`, `ruby_mi_claro.xml`, `ruby_mi_tigo.xml`, `ruby_tor_browser.xml`, `ruby_urban_vpn.xml`

## Estado de conservación

No se elimina ningún vector del repositorio. Los 93 XML anteriores permanecen versionados; únicamente se retiran del workspace temporal de CI para que los PNG generados ocupen esos mismos nombres de recurso en el APK.
