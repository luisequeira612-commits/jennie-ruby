# Auditoría de cobertura — preparación del lote 5

Fecha: 2026-11-04  
Base auditada: `main` en `a577356e1299ba917932d46bcc3e35f7648d2172`  
Rama de trabajo: `stage-5/batch-5-catalog-audit`

## Resultado

El catálogo del dispositivo contiene **146 aplicaciones**. `icons.json` registra **93 aplicaciones** en el renderizador Stage 5. Las otras **53 no están ausentes del paquete**: todas tienen entrada exacta en `appfilter.xml` (paquete, activity y drawable) y todas resuelven a un recurso existente o generado por CI.

| Tipo de recurso | Cantidad | Tratamiento |
|---|---:|---|
| Vectores heredados en `drawable-nodpi` | 39 | Candidatos para una futura migración visual; no se modifican en esta auditoría |
| PNG de Stage 1 generados en CI | 10 | Congelados; no incluir en lotes nuevos |
| Alias de los cuatro iconos del dock generados en CI | 4 | Congelados; no incluir en lotes nuevos |
| **Total fuera de `icons.json`** | **53** | **0 recursos ausentes** |

Los alias del dock están declarados en `app/src/main/res/values/drawable.xml` y apuntan a los PNG generados por `tools/render_ruby_dock_icons.py`. Los diez recursos Stage 1 se generan con el renderer protegido y se verifican por hash en CI.

## Los 39 vectores heredados candidatos

Estos componentes ya están mapeados y tienen vector XML. No se han agregado a `icons.json` ni se ha cambiado su arte en esta rama.

| Aplicación | Drawable existente |
|---|---|
| Acode | `ruby_acode` |
| Administrador de archivos | `ruby_administrador_de_archivos` |
| AnkuLua | `ruby_ankulua` |
| App Manager | `ruby_app_manager` |
| Asistente | `ruby_asistente` |
| Autenticador | `ruby_autenticador` |
| Calculadora | `ruby_calculadora` |
| Carlcare | `ruby_carlcare` |
| Clima | `ruby_clima` |
| Creador de atajos | `ruby_creador_de_atajos` |
| Cx Explorador de Archivos | `ruby_cx_explorador_de_archivos` |
| Escáner inteligente | `ruby_escaner_inteligente` |
| EX Explorador de Archivos | `ruby_ex_explorador_de_archivos` |
| Flud | `ruby_flud` |
| Grabadora de sonido | `ruby_grabadora_de_sonido` |
| iAdb | `ruby_iadb` |
| Kit de herramientas de SIM | `ruby_kit_de_herramientas_de_sim` |
| Kustom Widget | `ruby_kustom_widget` |
| MarkClear | `ruby_markclear` |
| Mobile Cloner | `ruby_mobile_cloner` |
| MT Manager | `ruby_mt_manager` |
| MT Manager+ | `ruby_mt_manager_plus` |
| My Health | `ruby_my_health` |
| MYTECNO | `ruby_mytecno` |
| Notas | `ruby_notas` |
| Nova Launcher | `ruby_nova_launcher` |
| Phone Master | `ruby_phone_master` |
| PhotoRecovery | `ruby_photorecovery` |
| QuickEdit | `ruby_quickedit` |
| RAR | `ruby_rar` |
| Reloj | `ruby_reloj` |
| Reproductor Visha | `ruby_reproductor_visha` |
| Shizuku | `ruby_shizuku` |
| Smart Panel | `ruby_smart_panel` |
| Stella TV | `ruby_stella_tv` |
| TrebEdit | `ruby_trebedit` |
| webOS Dev Manager | `ruby_webos_dev_manager` |
| WeZone | `ruby_wezone` |
| ZArchiver | `ruby_zarchiver` |

## Exclusiones protegidas

- Los diez PNG y el generador Stage 1 permanecen fuera de alcance.
- Los cuatro iconos principales del dock y sus aliases permanecen fuera de alcance.
- No se modifica `appfilter.xml`, `icons.json`, `device-app-catalog.tsv`, los widgets, fondos ni lotes aprobados.
- No se cambia `applicationId`, `versionCode` ni `versionName`: este commit es únicamente documental y no genera una versión de la app.

## Paquetes no confirmados

Palm Store (`com.transsnet.store`), TECNO ID (`tech.palm.id`) y Hola (`com.talpa.hibrowser`) siguen fuera del catálogo y de `appfilter.xml`. No se inventan activities ni componentes para ellos.

## Decisión pendiente para el siguiente lote

El inventario comprobado permite definir el próximo lote únicamente a partir de los 39 vectores heredados anteriores. Esta auditoría no los convierte automáticamente en un lote aprobado: todavía hay que fijar el tamaño y el orden del lote antes de reemplazar arte. No se ha generado ni cambiado ningún icono en esta rama.
