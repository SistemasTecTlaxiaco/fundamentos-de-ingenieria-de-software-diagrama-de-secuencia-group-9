# Práctica 10 · Modelo de dominio y diagramas de secuencia

Fundamentos de Ingeniería de Software (SCC-1007) · Unidad 4 · Sprint 4 · Open Hub Tec

Integren el negocio (Unidad 2) y los requisitos (Unidad 3) en una sola representación técnica: modelo de dominio, diagramas de secuencia y modelo de arquitectura, validados con la organización.

📋 **La rúbrica completa está en [RUBRICA.md](RUBRICA.md).**

## Qué entregan

| Qué | Dónde | Formato |
|---|---|---|
| Documento integrador | `entrega/` | PDF, Word (.docx) o Markdown, **con el nombre que quieran** |
| Imágenes (dominio, 2 secuencias, arquitectura) | Dentro del documento **o** en `docs/analisis/` | PNG o JPG, al menos 4 |
| Proyecto de Architect | `modelo/` | El mismo `.qea` de la Práctica 9, con los diagramas nuevos |
| Minuta y aprobación de la organización | Dentro del documento **o** en `docs/` | Con cargos, sin datos personales |

## Formato libre

- Pueden usar la portada del TecNM, el orden que quieran y sus propios títulos.
- Para empezar rápido tienen dos plantillas en `entrega/`: **`practica-10.md`** (Markdown) y **`plantilla-practica-10.docx`** (Word). Son una guía, no una obligación.
- Lo importante es que el documento tenga evidencia de los **10 criterios** de la rúbrica. Si usan títulos parecidos a los de la rúbrica, el robot los encuentra más fácil; si no, igual busca la evidencia en todo el documento.

## Cómo se trabaja

1. `git pull` y creen una rama: `git switch -c practica-10-secuencia`
2. Hagan sus cambios, `git add .`, `git commit -m "..."`, `git push -u origin practica-10-secuencia`.
   También pueden subir archivos desde la página: **Add file › Upload files** y elijan **Create a new branch**.
3. Abran un **pull request** hacia `main` y llenen la autoevaluación.
4. El robot deja un comentario con lo que encontró:
   - ✅ encontrado · ⚠️ hay evidencia, el docente la confirma · ❌ no encontrado (no bloquea, pero baja el nivel en la rúbrica)
   - ⛔ **bloquea la fusión**: falta el documento o los diagramas, o hay datos personales.
   - ⏳ **al final**: el criterio 9 (presentación y validación con la organización) se califica después de presentar.
5. Corrijan en la misma rama; la revisión se repite sola con cada cambio.
6. Otro integrante revisa con un comentario concreto, aprueba y fusiona.

> ⚠️ **Un PDF adjunto en un issue no es una entrega.** Tiene que estar en el repositorio y entrar por pull request.

La calificación la pone el Product Owner con la rúbrica de 30 puntos.

## El repositorio es público

La minuta va con el **cargo** de cada persona, no con su nombre completo ni datos de contacto. No suban firmas escaneadas: el original firmado se entrega al docente. El robot bloquea la fusión si encuentra teléfonos, correos o CURP.
