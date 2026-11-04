# Firma de APKs de desarrollo

El workflow instala un keystore de depuración estable antes de ejecutar `gradle assembleDebug`. Así, las APKs futuras de GitHub Actions conservan el mismo certificado y Android puede instalarlas como actualizaciones unas sobre otras.

- Keystore: `tools/signing/jennie-ruby-debug.keystore.b64`
- Alias: `androiddebugkey`
- Tipo: JKS, solo para builds debug personales.
- No usar para Play Store, publicación comercial ni una versión release.
- La clave está en el repositorio público y, por tanto, no es un secreto ni ofrece seguridad de firma de producción.

## Transición desde la versión 0.5.0

La APK 0.5.0 generada por el workflow anterior usó el keystore temporal del runner. Se comprobó que su huella SHA-256 es distinta de la nueva identidad estable. No es posible recuperar la clave privada anterior desde el certificado incluido en aquella APK.

Por ello, si 0.5.0 está instalada, hay que desinstalar JENNIE RUBY una sola vez antes de instalar la primera APK firmada con la nueva identidad estable. Después de esa transición, las siguientes APKs debug del workflow conservarán la misma firma y podrán instalarse como actualizaciones normales.

La desinstalación puede quitar el paquete de iconos de la selección de Nova y eliminar los widgets colocados; después de instalar, vuelve a seleccionar JENNIE RUBY en Nova y añade los widgets nuevos. El fondo de pantalla configurado por Android normalmente permanece, pero la app debe volver a estar instalada para administrar sus recursos.
