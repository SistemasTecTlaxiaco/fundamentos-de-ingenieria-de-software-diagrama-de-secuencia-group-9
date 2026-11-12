# Rúbrica · Práctica 10 · Modelo de dominio y diagramas de secuencia

Fundamentos de Ingeniería de Software (SCC-1007) · Unidad 4 · Modelo de análisis (Sprint 4) · TecNM Campus Tlaxiaco · Docente: José Alfredo Román Cruz · Versión 2, noviembre de 2026

> **Competencia:** elabora el modelo de análisis proyectado en la representación técnica del sistema utilizando la notación orientada a objetos.

**Evidencia:** Dominio, secuencias y arquitectura que integran el negocio (Unidad 2) y los requisitos (Unidad 3) en una sola representación, validados con la organización.  
**Valor:** 30 puntos (30 % de la unidad) · 10 criterios de 3 puntos · por equipo eduScrum, entrega por pull request.

## Qué se entrega

- Un documento integrador en `entrega/`: PDF, Word (.docx) o Markdown, **con el nombre que quieran** y con la portada que quieran.
- Al menos 4 imágenes (dominio, 2 secuencias y arquitectura): dentro del documento o como PNG en `docs/analisis/`.
- El mismo proyecto de Architect de la Práctica 9 en `modelo/`, con los diagramas nuevos y el diagrama de clases actualizado.
- La minuta y la aprobación de la organización: dentro del documento o como archivo en `docs/`.

El formato es libre: pueden usar la portada del TecNM, ordenar las secciones a su manera y ponerles sus propios títulos. Lo que se califica es que **cada criterio tenga evidencia** en el documento o en el repositorio.

## Requisitos mínimos para ser evaluado

Si falta alguno, la práctica se devuelve sin calificar para que el equipo la corrija antes de la fecha límite.

1. La entrega está **en el repositorio del equipo y entró por pull request**. Un archivo enviado por correo o adjunto en un issue no cuenta.
2. El **.qea abre** y contiene el modelo de dominio y al menos un diagrama de secuencia del módulo del propio equipo.
3. **Sin datos personales**: ni teléfonos, ni correos, ni CURP, ni firmas escaneadas. A las personas de la organización se les nombra por su cargo, rol o apodo, no por su nombre completo. El repositorio es público.

## Cómo se usa

- Cada criterio vale **3 puntos**. Se elige el nivel que mejor describe el trabajo; si queda entre dos, se asigna el inferior.
- Escala: **Excelente 3.0 · Notable 2.6 · Bueno 2.3 · Suficiente 2.1 · Insuficiente 0**.
- La columna *Indicador* liga cada criterio con los indicadores de alcance A–F de la instrumentación didáctica.
- La calificación es por equipo. Con los pull requests e *Insights › Contributors* el docente puede ajustar el criterio de trabajo en equipo de quien no aportó.

### Cómo leer el comentario del robot

El robot revisa cada pull request y busca la evidencia de cada criterio **sin importar el nombre del archivo ni los títulos**. No califica.

| Marca | Qué significa | ¿Bloquea la fusión? |
|---|---|---|
| ✅ Encontrado | Hay una sección con la evidencia que pide el criterio | No |
| ⚠️ Revisar | Hay evidencia, pero no donde se esperaba; el docente la confirma | No |
| ❌ No encontrado | No hay evidencia del criterio. Ese criterio no puede quedar en Excelente, salvo que el docente la encuentre | No |
| ⛔ Corregir | Falta el documento o el diagrama, o hay datos personales | **Sí** |
| ⏳ Al final | Criterio que se califica al cerrar la práctica (el 9) | No |

El robot confirma que la información **existe**; esta rúbrica juzga si está **bien**. Una entrega puede salir toda en ✅ y quedar en Bueno.

## Rúbrica analítica

### 1. Conceptos del dominio

3 puntos · Indicador A, E

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Los conceptos salen del BPMN mejorado, de las entrevistas y del DRS, y se nombran como los dice la organización. No hay clases de software: ni pantallas, ni controladores, ni base de datos. |
| Notable | 2.6 | Conceptos pertinentes y con el vocabulario de la organización; falta un concepto que aparece en el BPMN o sobra uno. |
| Bueno | 2.3 | Conceptos pertinentes, pero varios usan nombres técnicos del software en lugar de los de la organización. |
| Suficiente | 2.1 | Copia del diagrama de clases de la Práctica 9, o incluye clases de software (Pantalla, Controlador, BaseDeDatos). |
| Insuficiente | 0 | Sin modelo de dominio, o conceptos sin relación con la organización del equipo. |

### 2. Atributos y asociaciones del dominio

3 puntos · Indicador C, E

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Atributos conceptuales sin tipos, sin operaciones y sin visibilidad. Cada asociación tiene nombre y multiplicidad en los dos extremos y se puede leer en voz alta como una regla de la organización. |
| Notable | 2.6 | Atributos y asociaciones correctos; una multiplicidad no está confirmada con la organización. |
| Bueno | 2.3 | Varias asociaciones sin nombre o con multiplicidad en un solo extremo. |
| Suficiente | 2.1 | Incluye operaciones, tipos o visibilidad, como si fuera un diagrama de diseño. |
| Insuficiente | 0 | Conceptos aislados, sin atributos ni asociaciones. |

### 3. Escenarios tomados de los casos de uso

3 puntos · Indicador D

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Al menos dos diagramas de secuencia, uno por escenario. Cada uno indica su caso de uso y traduce paso por paso la especificación (flujo principal y un flujo alterno importante). |
| Notable | 2.6 | Dos diagramas ligados a sus casos de uso; un paso de la especificación no aparece como mensaje. |
| Bueno | 2.3 | Dos diagramas, pero uno no corresponde a ningún caso de uso especificado. |
| Suficiente | 2.1 | Un solo diagrama, o uno que mezcla varios casos de uso y se vuelve ilegible. |
| Insuficiente | 0 | Sin diagramas de secuencia. |

### 4. Estructura de la secuencia

3 puntos · Indicador D

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Líneas de vida de actor, frontera, control y entidad. El actor solo habla con la frontera. Mensajes en orden de arriba abajo, con parámetros; respuestas punteadas y activación donde un objeto trabaja. |
| Notable | 2.6 | Estructura correcta; faltan respuestas o barras de activación en algún tramo. |
| Bueno | 2.3 | Mensajes en orden, pero el actor habla directo con las entidades o falta la clase control. |
| Suficiente | 2.1 | Mensajes sin nombre o sin orden claro; flechas que no indican quién pide qué. |
| Insuficiente | 0 | El diagrama no es de secuencia (es de actividades o de flujo). |

### 5. Fragmentos combinados

3 puntos · Indicador C

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Usa alt, opt o loop donde el caso lo pide, con su condición de guarda entre corchetes ([kilos ≤ 0], [else]). Cada fragmento corresponde a un flujo alterno de la especificación. |
| Notable | 2.6 | Fragmento correcto; una condición de guarda es vaga o falta [else]. |
| Bueno | 2.3 | Fragmento con el operador equivocado (opt donde se necesitaba alt) o sin guarda. |
| Suficiente | 2.1 | Alternativas dibujadas como mensajes sueltos o con notas, sin fragmento. |
| Insuficiente | 0 | Ningún fragmento en ningún diagrama. |

### 6. Consistencia con el diagrama de clases

3 puntos · Indicador D

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Cada línea de vida de entidad es una clase del dominio o del diagrama de clases, y cada mensaje que recibe existe como operación en su clase. El diagrama de clases de la Práctica 9 se actualizó con las operaciones que faltaban. |
| Notable | 2.6 | Consistente; una o dos operaciones faltan en el diagrama de clases. |
| Bueno | 2.3 | Varios mensajes no existen como operaciones y el diagrama de clases no se actualizó. |
| Suficiente | 2.1 | Líneas de vida que no corresponden a ninguna clase del modelo. |
| Insuficiente | 0 | Sin relación entre las secuencias y el diagrama de clases. |

### 7. Integración de negocio y requisitos

3 puntos · Indicador A, B

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | El orden de los mensajes coincide con el BPMN mejorado de la Unidad 2 y cada elemento conserva su requisito de origen (RF, RNF o RD). El documento integrador une BPMN, DRS, casos de uso, dominio y secuencias con una trazabilidad clara. |
| Notable | 2.6 | Documento integrador completo; una parte no cita su requisito de origen. |
| Bueno | 2.3 | Documento integrador que junta los modelos sin explicar cómo se relacionan. |
| Suficiente | 2.1 | Documento con modelos sueltos, o que contradice al BPMN o al DRS. |
| Insuficiente | 0 | Sin documento integrador. |

### 8. Modelo de arquitectura en UML

3 puntos · Indicador E

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Diagrama de paquetes con las cuatro capas (Presentación, Aplicación/API, Dominio, Integración). Las dependencias apuntan solo hacia abajo, cada clase está en su capa y se marca qué es real y qué es simulado. |
| Notable | 2.6 | Capas y dependencias correctas; falta marcar lo real y lo simulado. |
| Bueno | 2.3 | Capas presentes, pero alguna dependencia sube o salta capas sin justificar. |
| Suficiente | 2.1 | Capas dibujadas como cajas sin dependencias ni clases asignadas. |
| Insuficiente | 0 | Sin modelo de arquitectura. |

### 9. Presentación y validación con la organización

3 puntos · Indicador A, F

> ⏳ **Se califica al final**, después de presentar el modelo a la organización (fecha, minuta con cargos, aprobación y cambios). El robot lo muestra como «Al final» y no lo marca como faltante mientras tanto.

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Presentación de diez minutos en las palabras de la organización, cerrando con preguntas de validación. Sus respuestas quedan en una minuta (con cargos, no datos personales), los cambios se incorporan al modelo y su aprobación queda registrada. |
| Notable | 2.6 | Presentación clara y aprobación registrada; un cambio pedido no se incorporó todavía. |
| Bueno | 2.3 | Presentación con lenguaje técnico que la organización no siguió; aprobación sin minuta. |
| Suficiente | 2.1 | Se envió el documento sin presentarlo ni escuchar a la organización. |
| Insuficiente | 0 | No se presentó a la organización. |

### 10. Entrega, revisión cruzada y trabajo en equipo

3 puntos · Indicador B, F

| Nivel | Puntos | Descripción |
|---|:---:|---|
| Excelente | 3.0 | Todos los diagramas en el mismo proyecto .qea. Cada cambio entró por pull request revisado por otro integrante. Otro equipo revisó con la lista de consistencia y cada observación se respondió en el pull request o en el documento. |
| Notable | 2.6 | Entrega completa por pull request; la revisión cruzada se atendió en parte. |
| Bueno | 2.3 | Pull requests aprobados sin comentarios; sin revisión cruzada. |
| Suficiente | 2.1 | Un solo pull request al final hecho por una persona, o diagramas en archivos separados. |
| Insuficiente | 0 | Entrega fuera del repositorio (correo, adjunto en un issue) o cambios directos a main. |

## Dónde buscar la evidencia

| Criterio | Dónde se revisa |
|---|---|
| 1. Conceptos del dominio | Modelo de dominio, BPMN mejorado y glosario |
| 2. Atributos y asociaciones del dominio | Diagrama del modelo de dominio |
| 3. Escenarios tomados de los casos de uso | Diagramas de secuencia y especificaciones de casos de uso |
| 4. Estructura de la secuencia | Diagramas de secuencia |
| 5. Fragmentos combinados | Diagramas de secuencia |
| 6. Consistencia con el diagrama de clases | Secuencias y diagrama de clases actualizado en el .qea |
| 7. Integración de negocio y requisitos | Documento integrador |
| 8. Modelo de arquitectura en UML | Diagrama de paquetes |
| 9. Presentación y validación con la organización | Minuta y constancia de aprobación (documento o `docs/`) |
| 10. Entrega, revisión cruzada y trabajo en equipo | Pull requests (el robot lista autores y revisores), comentarios de revisión y lista de consistencia |

### Lista de consistencia para la revisión cruzada

El equipo revisor la copia en un comentario del pull request del otro equipo y marca cada regla.

- [ ] Cada línea de vida de entidad es una clase del dominio o del diagrama de clases.
- [ ] Cada mensaje que recibe un objeto existe como operación en su clase.
- [ ] Cada diagrama de secuencia sigue la especificación de un caso de uso.
- [ ] El orden de los mensajes coincide con el BPMN mejorado de la Unidad 2.
- [ ] Los nombres del dominio son los del glosario de la organización.
- [ ] Cada elemento conserva su requisito de origen (RF, RNF o RD).

## Conversión al nivel de desempeño

| Puntos de la rúbrica | Nivel de desempeño | Escala de la instrumentación |
|:---:|:---:|:---:|
| 28.5 – 30.0 | Excelente | 95 – 100 |
| 25.5 – 28.4 | Notable | 85 – 94 |
| 22.5 – 25.4 | Bueno | 75 – 84 |
| 21.0 – 22.4 | Suficiente | 70 – 74 |
| Menos de 21.0 | Insuficiente | NA · competencia no alcanzada |

En Classroom 50, si la tarea está sobre 100, se captura con **Override score** el total × 10 ÷ 3 (por ejemplo, 27 puntos = 90).

## Hoja de calificación

El docente copia esta tabla en un comentario del pull request del equipo (o en el *Feedback pull request* de Classroom 50).

```markdown
| Criterio | Nivel | Puntos | Observación |
|---|---|---:|---|
| 1. Conceptos del dominio |  | / 3 |  |
| 2. Atributos y asociaciones del dominio |  | / 3 |  |
| 3. Escenarios tomados de los casos de uso |  | / 3 |  |
| 4. Estructura de la secuencia |  | / 3 |  |
| 5. Fragmentos combinados |  | / 3 |  |
| 6. Consistencia con el diagrama de clases |  | / 3 |  |
| 7. Integración de negocio y requisitos |  | / 3 |  |
| 8. Modelo de arquitectura en UML |  | / 3 |  |
| 9. Presentación y validación con la organización |  | / 3 |  |
| 10. Entrega, revisión cruzada y trabajo en equipo |  | / 3 |  |
| **Total** |  | **/ 30** |  |

**Lo mejor del trabajo:** 
**Lo primero que deben mejorar:** 
```
