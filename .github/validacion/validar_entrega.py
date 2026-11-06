#!/usr/bin/env python3
"""Revisa que la entrega (Markdown o PDF) contenga la información que pide la rúbrica.

No califica. Solo confirma que cada sección existe y trae lo mínimo para poder
evaluarla. Las reglas viven en reglas.json, junto a este archivo.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata

MARCA = "<!-- validar-entrega -->"


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def leer_md(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as f:
        texto = f.read()
    # Las instrucciones de la plantilla van en comentarios HTML y no cuentan.
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    # Los encabezados de las tablas de la plantilla tampoco cuentan.
    lineas = texto.splitlines()
    sep = re.compile(r"^\s*\|?\s*:?-{3,}")
    lineas = [l for i, l in enumerate(lineas)
              if not sep.match(l) and not (i + 1 < len(lineas) and sep.match(lineas[i + 1]))]
    texto = "\n".join(lineas)
    base = os.path.dirname(ruta)
    imagenes = 0
    rotas = []
    for ref in re.findall(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)", texto) + re.findall(r"<img[^>]+src=[\"']([^\"']+)", texto):
        if ref.startswith(("http://", "https://")):
            rotas.append(ref + " (enlace externo: suban la imagen al repositorio)")
        elif os.path.isfile(os.path.normpath(os.path.join(base, ref))):
            imagenes += 1
        else:
            rotas.append(ref)
    return texto, imagenes, rotas


def leer_pdf(ruta):
    try:
        texto = subprocess.run(["pdftotext", "-enc", "UTF-8", ruta, "-"], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise SystemExit(f"No pude leer el PDF {ruta}: {e}")
    imagenes = 0
    try:
        lista = subprocess.run(["pdfimages", "-list", ruta], capture_output=True, text=True, check=True).stdout
        imagenes = sum(1 for linea in lista.splitlines()[2:] if linea.strip() and " smask " not in linea)
    except (OSError, subprocess.CalledProcessError):
        pass
    return texto, imagenes, []


def buscar_entrega(regla):
    carpeta = regla["carpeta"]
    for nombre in regla["nombres"]:
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            return ruta
    return None


def cortar_secciones(texto, secciones):
    """Devuelve {titulo: texto_de_la_seccion}. Un título es un renglón corto que lo contiene."""
    lineas = texto.splitlines()
    norm = [normalizar(l).strip(" #*_:\t") for l in lineas]
    es_titulo = [l.lstrip().startswith("#") for l in lineas]
    inicio = {}
    for s in secciones:
        t = normalizar(s["titulo"])
        # Primero los encabezados de Markdown; si no hay (PDF), cualquier renglón corto.
        for solo_titulos in (True, False):
            for i, l in enumerate(norm):
                if solo_titulos and not es_titulo[i]:
                    continue
                if t in l and len(l) <= len(t) + 25 and i not in inicio.values():
                    inicio[s["titulo"]] = i
                    break
            if s["titulo"] in inicio:
                break
    orden = sorted(inicio.items(), key=lambda kv: kv[1])
    cuerpo = {}
    for k, (titulo, i) in enumerate(orden):
        fin = orden[k + 1][1] if k + 1 < len(orden) else len(lineas)
        cuerpo[titulo] = "\n".join(lineas[i + 1:fin])
    return cuerpo


def contar(patron, texto):
    return len(re.findall(patron, normalizar(texto), flags=re.M))


def palabras(texto):
    limpio = re.sub(r"[|#*_>`\-]+", " ", texto)
    return len(re.findall(r"\w{2,}", limpio))


def revisar_seccion(s, cuerpo):
    faltas, avisos = [], []
    if cuerpo is None:
        return [f"No encontré la sección «{s['titulo']}». Usen el título tal como viene en la plantilla."], []
    n = palabras(cuerpo)
    if n < s.get("min_palabras", 0):
        faltas.append(f"Está muy corta ({n} palabras; se esperan al menos {s['min_palabras']}).")
    for c in s.get("comprobaciones", []):
        hallados = contar(c["patron"], cuerpo)
        cumple = hallados >= c.get("min", 1)
        if not cumple:
            (avisos if c.get("aviso") else faltas).append(c["mensaje"])
    for c in s.get("prohibido", []):
        if contar(c["patron"], cuerpo):
            avisos.append(c["mensaje"])
    return faltas, avisos


def revisar_datos_personales(texto):
    reglas = [
        (r"\b[a-z]{4}\d{6}[hm][a-z]{5}[a-z0-9]\d\b", "Parece haber una CURP."),
        (r"(?<!\d)(?:\+?52[\s-]?)?\d{2,3}[\s-]?\d{3,4}[\s-]?\d{4}(?!\d)", "Parece haber un número de teléfono."),
        (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "Parece haber un correo electrónico."),
    ]
    t = normalizar(texto)
    return [m for p, m in reglas if re.search(p, t)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reglas", default=os.path.join(os.path.dirname(__file__), "reglas.json"))
    ap.add_argument("--salida", default="reporte.md")
    args = ap.parse_args()

    with open(args.reglas, encoding="utf-8") as f:
        regla = json.load(f)

    out = [MARCA, f"## Revisión de la entrega · {regla['practica']}", ""]
    out.append("> Esta revisión **no califica**. Solo confirma que la información que pide la rúbrica está en la entrega. "
               "La calificación la pone el Product Owner con la rúbrica.")
    out.append("")

    ruta = buscar_entrega(regla)
    if not ruta:
        nombres = " o ".join(f"`{regla['carpeta']}/{n}`" for n in regla["nombres"])
        out.append(f"❌ **No encontré la entrega.** Suban {nombres}, partiendo de la plantilla de `{regla['carpeta']}/`.")
        escribir(args.salida, out)
        return 1

    texto, imgs, rotas = leer_pdf(ruta) if ruta.lower().endswith(".pdf") else leer_md(ruta)
    pngs = [p for patron in regla.get("imagenes_en", []) for p in glob.glob(patron)]
    total_imgs = max(imgs, len(pngs))

    filas, avisos_globales, faltan = [], [], 0
    cuerpos = cortar_secciones(texto, regla["secciones"])
    for s in regla["secciones"]:
        f_, a_ = revisar_seccion(s, cuerpos.get(s["titulo"]))
        if f_:
            faltan += 1
            filas.append((s["criterio"], "❌ Falta", " ".join(f_)))
        elif a_:
            filas.append((s["criterio"], "⚠️ Revisar", " ".join(a_)))
        else:
            filas.append((s["criterio"], "✅ Completo", ""))

    req_imgs = regla.get("imagenes_minimas", 0)
    if total_imgs < req_imgs:
        faltan += 1
        filas.append(("Diagramas", "❌ Falta",
                      f"Encontré {total_imgs} imagen(es) de diagramas; se esperan al menos {req_imgs}. "
                      "Inclúyanlas en el documento o como PNG en docs/analisis."))
    for r in rotas:
        avisos_globales.append(f"Imagen que no se encuentra en el repositorio: `{r}`.")

    for patron in regla.get("archivos_requeridos", []):
        if not glob.glob(patron):
            faltan += 1
            filas.append(("Archivos", "❌ Falta", f"No encontré `{patron}`."))
    for patron in regla.get("archivos_recomendados", []):
        if not glob.glob(patron):
            avisos_globales.append(f"Se recomienda subir `{patron}`.")

    datos = revisar_datos_personales(texto)
    if datos:
        faltan += 1
        filas.append(("Datos personales", "❌ Quitar",
                      " ".join(datos) + " El repositorio es público: usen el cargo o rol, no datos de contacto."))

    out.append(f"**Archivo revisado:** `{ruta}` · **Imágenes de diagramas:** {total_imgs}")
    out.append("")
    out.append("| Criterio de la rúbrica | Estado | Qué falta o qué revisar |")
    out.append("|---|---|---|")
    for c, e, m in filas:
        out.append(f"| {c} | {e} | {m.replace('|', '/')} |")
    out.append("")
    if avisos_globales:
        out.append("**Para revisar:**")
        out += [f"- {a}" for a in avisos_globales]
        out.append("")
    if faltan:
        out.append(f"**Resultado:** falta información en {faltan} punto(s). Complétenla y suban los cambios a esta misma rama; la revisión se repite sola.")
    else:
        out.append("**Resultado:** la entrega trae toda la información que pide la rúbrica. Ya puede pasar a revisión de un compañero.")
    escribir(args.salida, out)
    return 1 if faltan else 0


def escribir(ruta, lineas):
    texto = "\n".join(lineas) + "\n"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(texto)
    print(texto)


if __name__ == "__main__":
    sys.exit(main())
