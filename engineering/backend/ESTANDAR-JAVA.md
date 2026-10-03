# Estándar Java

El perfil y el POM del repositorio determinan Java y framework; no forzar JDK 21
en servicios que requieren otra versión. Mantener Checkstyle corporativo también
en tests. Para clases nuevas respeta la cabecera y atribución que ya exija el
repositorio. No inventes una organización, autor o aviso de copyright.

Pruebas: AAA comentado/separado, @DisplayName, nombres en inglés, assertions de
valor/estado y excepciones verificadas por tipo y código/mensaje. Mockito solo
en pruebas unitarias donde corresponde. Matchers tipados, sin @Disabled ni
lenient para ocultar deficiencias. Respeta utilitarios del repo. No impone tres
pruebas de referencia si no existen; registra las disponibles.

No amplía exclusiones de JaCoCo o Checkstyle para pasar. Clases generadas se
tratan según política corporativa; no edita su cabecera manualmente. Un código
de error controlado es parte de comportamiento, no un valor libre a inventar.
