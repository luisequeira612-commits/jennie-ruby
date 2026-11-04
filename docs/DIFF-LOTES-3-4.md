# Diff resumido antes de aplicar — lotes 3 y 4

- `icons.json`: 68 → 93 registros; se corrigieron los glifos solicitados del lote 3 y se añadieron 25 apps del lote 4.
- `app/src/main/res/xml/appfilter.xml`: no requiere nuevos componentes; los 25 paquetes del lote 4 ya tenían mappings y activities. `tools/generate_appfilter.py` vuelve a comprobar que los drawables apuntan al catálogo.
- `app/src/main/res/xml/drawable.xml` y `app/src/main/assets/drawable.xml`: selector actualizado a 93 entradas, conservando un solo registro por drawable.
- `app/src/main/res/values/drawable.xml`: sin cambios; conserva alias de recursos del dock.
- `applicationId` sin cambios; `versionCode 15`, `versionName 0.9.5`.
- No se modifican recursos congelados ni lotes 1 y 2.

## Actividades y estado

# Activities — Lotes 3 y 4

## Lote 3

| App | Tipo declarado | Activity | Estado |
|---|---|---|---|
| Memrise | marca | com.memrise.android.memrisecompanion.ui.activity.LauncherActivity | estimated |
| Drops | marca | com.languagedrops.drops.international.MainActivity | estimated |
| HelloTalk | marca | com.hellotalk.lib.main.launch.ui.LaunchActivity | estimated |
| Falou | genérico | com.moymer.falou.flow.onboarding.LauncherActivity | estimated |
| Ling | monograma | com.simyasolutions.ling.SplashActivity | estimated |
| LingQ | monograma | com.lingq.ui.MainActivity | estimated |
| LangReactor | genérico | org.chromium.webapk.shell_apk.h2o.H2OOpaqueMainActivity | estimated |
| Reelang | genérico | com.reelang.pt.MainActivity | estimated |
| Write Greek | monograma | com.jernung.writeit.android.MainActivity | estimated |
| Moon+ Reader | marca | com.flyersoft.moonreader.ActivityMain | estimated |
| ReadEra | monograma | com.readera.MainActivity | estimated |
| Lector de PDF | genérico | pdf.pdfreader.viewer.editor.free.ReaderLauncherBridgeActivity | estimated |
| LNReader | genérico | com.rajarsheechatterjee.LNReader.MainActivity | estimated |
| Shosetsu | monograma | app.shosetsu.android.activity.MainActivity | estimated |
| bilibili | marca | tv.danmaku.bili.MainActivityV2 | estimated |
| CloudStream | genérico | com.lagradost.cloudstream3.ui.account.AccountSelectActivity | verified |
| Inkaplay | monograma | com.inkamedia.inkaplay.presentation.main_activity.MainActivity | estimated |
| Lark Player | marca | com.dywx.larkplayer.main.MainActivity | estimated |
| MXL TV | genérico | tv.mxliptv.app.activities.InitActivity | estimated |
| Xuper | monograma | com.mobile.brasiltv.activity.SplashAty | estimated |
| Rave | marca | com.wemesh.android.rearch.RaveActivity | estimated |
| Mnet Plus | marca | world.mnetplus.MainActivity | estimated |
| Songstats | genérico | com.trackstats.MainActivity | estimated |
| Soundcharts | genérico | com.soundcharts.app.MainActivity | estimated |
| SportzX | genérico | com.sportzx.live.activities.SplashActivity | estimated |
| GeeSports | genérico | com.live.geesports.activities.SplashActivity | estimated |
| Lean Remote | genérico | co.leanremote.universalremotecontrol.remotecontrol.SplashActivity | estimated |
| LGRemote | genérico | com.nwt.lgremote.ui.MainActivity | estimated |

## Lote 4

| App | Tipo declarado | Activity | Estado |
|---|---|---|---|
| rednote | genérico | com.xingin.xhs.index.v2.IndexActivityV2 | estimated |
| NGL | genérico | com.nglreactnative.MainActivity | estimated |
| Zangi | genérico | com.beint.project.MainActivity | estimated |
| Labalabi For WhatsApp | genérico | cliker.whatsapp.SettingActivity | estimated |
| SocialAut | genérico | com.avilap.socialaut.MainActivity | estimated |
| Sticker.ly | genérico | com.snowcorp.stickerly.android.LauncherEntryActivity | estimated |
| StickerVibe | genérico | com.zhiqiaos.sticker.activity.SplashActivity | estimated |
| Reface | genérico | video.reface.app.start.MainActivity | estimated |
| Viggle AI | genérico | com.warpengine.viggle.MainActivity | estimated |
| HoYoLAB | genérico | com.mihoyo.hoyolab.splash.splash.HoYoSplashActivity | estimated |
| MCPEDL | genérico | com.overwolf.mcpedl.MainActivity | estimated |
| MU Fan | genérico | com.choicely.sdk.activity.splash.SplashActivity | estimated |
| Duskwood | genérico | com.unity3d.player.UnityPlayerActivity | estimated |
| Blackjack Trainer | genérico | com.blackjacktrainer.MainActivity | verified |
| AHA Games | genérico | net.bat.store.DefaultIconAliasActivity | verified |
| Meu Tarot | genérico | com.nowallsanalytics.tarot_guide.MainActivity | estimated |
| Windy | genérico | com.windyty.android.Standard | estimated |
| Moovit | genérico | com.moovit.app.home.HomeActivity | estimated |
| Google Earth | genérico | com.google.android.apps.earth.flutter.EarthFlutterActivity | estimated |
| DeepStateMap | genérico | ua.com.deepstatemap.MainActivity | estimated |
| PedidosYa | genérico | com.pedidosya.main.access.initialization.SplashActivity | estimated |
| Mi Claro | genérico | com.claro.app.view.SplashKTVC | estimated |
| Mi Tigo | genérico | ni.telefonica.mimovistar.MainActivity | estimated |
| Tor Browser | genérico | org.torproject.torbrowser.App | estimated |
| Urban VPN | genérico | com.urbanvpn.android.ui.payment.PaymentActivity | estimated |
