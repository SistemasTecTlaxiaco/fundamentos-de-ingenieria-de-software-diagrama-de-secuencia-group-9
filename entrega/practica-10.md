# Entrega · Práctica 10

<!--
Plantilla de entrega. Llenen cada sección con la información de su módulo.
- No cambien los títulos: el robot los usa para encontrar cada parte.
- Todo lo que está entre estos símbolos de comentario NO cuenta como contenido.
- Si prefieren entregar en PDF, exporten este mismo documento como entrega/practica-10.pdf
  y borren este archivo .md (el robot revisa el .md si existen los dos).
- Se esperan al menos 4 imágenes: dominio, 2 secuencias y arquitectura.
- El repositorio es público: no escriban teléfonos, correos ni CURP, ni suban la
  firma escaneada de nadie. En la minuta usen el cargo o rol de cada persona.
-->

**Equipo:**
**Módulo del Hub:**
**Organización:**

## 1. Conceptos del dominio

<!-- Cada concepto, de dónde sale (BPMN, entrevista o DRS) y cómo lo nombra la organización.
Ejemplo:  | Bodega | BPMN mejorado, actividad "guardar la miel" | Así le dicen en la cooperativa | -->

| Concepto | De dónde sale | Cómo lo dice la organización |
|---|---|---|
|  |  |  |

## 2. Atributos y asociaciones del dominio

<!-- Atributos sin tipos y sin operaciones. Cada asociación leída como oración con multiplicidad.
Ejemplo:  Un Socio realiza 0..* Entregas; cada Entrega se guarda en 1 Bodega.
Inserten la imagen del modelo de dominio. -->

## 3. Escenarios

<!-- Por cada diagrama de secuencia: caso de uso (CU-01…), y si es flujo principal o alterno. -->

| Diagrama | Caso de uso | Escenario |
|---|---|---|
|  |  |  |

## 4. Diagramas de secuencia

<!-- Inserten cada diagrama y digan cuál es la frontera, el control y las entidades. -->

## 5. Fragmentos

<!-- Qué fragmento usaron (alt, opt o loop), su condición de guarda y de qué flujo alterno sale.
Ejemplo:  alt [kilos ≤ 0] / [else], flujo alterno 3a de CU-01. -->

## 6. Consistencia con el diagrama de clases

<!-- Cada mensaje y la operación de la clase que lo recibe.
Ejemplo:  :Control → :Inventario · sumar(kilos) existe en la clase Inventario. -->

| Mensaje | Clase que lo recibe | ¿Existe la operación? |
|---|---|---|
|  |  |  |

## 7. Integración de negocio y requisitos

<!-- Cómo se conectan BPMN mejorado → DRS (RF, RNF, RD) → casos de uso → dominio → secuencias.
Expliquen por qué el orden de los mensajes sigue al BPMN. -->

## 8. Modelo de arquitectura

<!-- Inserten el diagrama de paquetes con las cuatro capas: Presentación, Aplicación / API,
Dominio e Integración. Digan qué clase va en cada capa y qué es real y qué es simulado. -->

## 9. Validación con la organización

<!-- Fecha, minuta de la presentación (con cargos, no datos personales), qué preguntaron,
si aprobaron el modelo y qué cambió después. -->

## 10. Revisión cruzada

<!-- Equipo revisor, observaciones con la lista de consistencia, qué hicieron con cada una,
y quién hizo y revisó cada pull request. -->

| Observación del equipo revisor | Qué hicimos |
|---|---|
|  |  |
