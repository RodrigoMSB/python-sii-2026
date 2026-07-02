# Pista Nivel 1 — Orientación 🧭

> *Destapa solo lo que necesites. Pedir un mapa no es perderse; es navegar.*

Esta pista **no trae código**. Trae el orden de batalla y tres preguntas-brújula.

## El orden de batalla

El Arenario es el pipeline completo del curso, en cadena. Hazlo por etapas y
prueba cada una antes de seguir:

1. **Depurar el censo** (`censo_anual.csv`) — como en el **Lab 05**: homogeneizar,
   deduplicar, filtrar códigos, imputar faltantes, apartar el outlier de consenso.
   → obtienes el **censo depurado**.
2. **Cargar las otras fuentes** — como en el **Lab 04**: el Excel de dos hojas, el
   JSON de multas, la BD de contribuyentes.
3. **Combinar** — como en el **Lab 06**: apila las dos hojas de pagos, agrupa por
   código, y **cruza** censo × pagos × multas × giro con `merge`.
4. **Calcular** — el **saldo** de cada uno (`deuda + multas − pagado`) y de ahí
   todo lo demás (rubro, tramo, al día vs moroso).
5. **Agregar** — como en el **Lab 06**: totales por rubro, tramos, pivote.
6. **Graficar e informar** — como en el **Lab 06**: dos PNG (Agg) y el informe con
   la sección de **hallazgos**.

Cada etapa la aprendiste en un lab. El capstone no pide nada nuevo: pide juntarlo.

## Tres preguntas-brújula

Antes de destapar más pistas, respóndete estas (el verificador te ayuda a
confirmarlas sin revelar el cómo):

1. **¿Cuántas filas debe tener tu censo depurado?** Corre tu depuración y mira. El
   verificador te dirá si el número es el correcto — eso te orienta sin destapar
   nada más.
2. **¿Por dónde entra la deuda "no informada"?** El censo trae faltantes escritos de
   más de una forma. Si tu columna de deuda quedó como texto, revisa cómo le dices
   a pandas qué cuenta como "vacío" (mira bien los tres marcadores del censo).
3. **¿El saldo puede ser negativo?** Sí. Y no es un bug: es un **hallazgo**. Cuando
   te aparezca, no lo escondas — el examen premia que lo detectes y lo expliques.

## Si te trabas

- Etapa por etapa, no todo de una. Un `print(df.shape)` después de cada paso vale
  oro.
- Si una etapa no cuadra, vuelve al lab que la enseñó (arriba dice cuál).
- ¿Aún trabado? La **Pista Nivel 2** trae el plan de ataque con pseudocódigo.
