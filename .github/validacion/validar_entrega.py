#!/usr/bin/env python3
"""Revisión de completitud de una entrega (versión 2, flexible).

No califica. Busca en la entrega del equipo la evidencia que pide cada criterio
de la rúbrica y deja un reporte para el pull request.

Qué cambió respecto a la versión 1:
- Acepta cualquier PDF, Word (.docx) o Markdown, con el nombre que sea.
- Reconoce varios títulos por criterio (los de la plantilla, los de la rúbrica
  y variantes comunes). Si no encuentra el título, busca la evidencia en todo
  el documento y marca ⚠️ en lugar de ❌.
- No cuenta logos ni encabezados repetidos como diagramas.
- Reúne de GitHub la evidencia de pull requests y revisiones.
- Solo bloquea la fusión si no hay entrega, si no hay diagrama o si aparecen
  datos personales. Lo demás es orientación para el equipo y para el docente.

Las reglas viven en reglas.json, junto a este archivo.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
import zipfile
from collections import Counter
from xml.etree import ElementTree as ET

MARCA = "<!-- validar-entrega -->"
OK, REV, FALTA, ALTO, FINAL = "✅ Encontrado", "⚠️ Revisar", "❌ No encontrado", "⛔ Corregir", "⏳ Al final"


# ----------------------------------------------------------------------------
# Texto
# ----------------------------------------------------------------------------
def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower()


def palabras(texto):
    limpio = re.sub(r"[|#*_>`\-]+", " ", texto)
    return len(re.findall(r"\w{2,}", limpio))


def contar(patron, texto):
    return len(re.findall(patron, normalizar(texto), flags=re.M))


# ----------------------------------------------------------------------------
# Lectores. Cada uno devuelve (texto, imagenes, avisos).
# En el texto, los títulos reconocibles empiezan con «# ».
# ----------------------------------------------------------------------------
def leer_md(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as f:
        texto = f.read()
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)  # instrucciones de la plantilla
    lineas = texto.splitlines()
    sep = re.compile(r"^\s*\|?\s*:?-{3,}")
    lineas = [l for i, l in enumerate(lineas)
              if not sep.match(l) and not (i + 1 < len(lineas) and sep.match(lineas[i + 1]))]
    texto = "\n".join(lineas)
    base = os.path.dirname(ruta)
    imagenes, avisos = 0, []
    refs = re.findall(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)", texto) + re.findall(r"<img[^>]+src=[\"']([^\"']+)", texto)
    for ref in refs:
        if ref.startswith(("http://", "https://")):
            avisos.append(f"Imagen con enlace externo: `{ref}`. Súbanla al repositorio para que no se pierda.")
        elif os.path.isfile(os.path.normpath(os.path.join(base, ref))) or os.path.isfile(ref.lstrip("/")):
            imagenes += 1
        else:
            avisos.append(f"Imagen que no se encuentra en el repositorio: `{ref}`.")
    return texto, imagenes, avisos


def leer_pdf(ruta):
    try:
        texto = subprocess.run(["pdftotext", "-enc", "UTF-8", ruta, "-"],
                               capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        return "", 0, [f"No pude leer el PDF `{ruta}` ({e}). ¿Está protegido o dañado?"]
    # Renglones que parecen títulos numerados («7. Trazabilidad…») se marcan como títulos.
    lineas = []
    for l in texto.splitlines():
        s = l.strip()
        if re.match(r"^\d{1,2}(\.\d{1,2})*\.?\s+\S", s) and len(s) <= 90 and not s.endswith((".", ",", ";")):
            lineas.append("# " + s)
        else:
            lineas.append(l)
    return "\n".join(lineas), contar_imagenes_pdf(ruta), []


def contar_imagenes_pdf(ruta):
    """Cuenta imágenes de contenido: sin máscaras, sin miniaturas y sin las que se
    repiten en muchas páginas (logos de encabezado o pie)."""
    try:
        lista = subprocess.run(["pdfimages", "-list", ruta], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return 0
    filas = []
    for linea in lista.splitlines()[2:]:
        c = linea.split()
        if len(c) < 12 or c[2] != "image":
            continue
        try:
            filas.append({"pag": int(c[0]), "w": int(c[3]), "h": int(c[4]), "obj": c[10]})
        except ValueError:
            continue
    if not filas:
        return 0
    paginas = max(f["pag"] for f in filas)
    por_firma = Counter()
    for f in {(f["pag"], f["obj"], f["w"], f["h"]) for f in filas}:
        por_firma[(f[2], f[3])] += 1
    unicas = set()
    for f in filas:
        if f["w"] * f["h"] < 250 * 250:            # iconos, sellos, logos chicos
            continue
        if paginas >= 3 and por_firma[(f["w"], f["h"])] >= max(3, paginas // 2):
            continue                                # se repite en muchas hojas: encabezado
        unicas.add((f["obj"], f["w"], f["h"]))
    return len(unicas)


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def leer_docx(ruta):
    try:
        z = zipfile.ZipFile(ruta)
        raiz = ET.fromstring(z.read("word/document.xml"))
    except Exception as e:  # archivo dañado o no es Word
        return "", 0, [f"No pude leer el Word `{ruta}` ({e}). Expórtenlo como PDF."]
    lineas = []
    for par in raiz.iter(W + "p"):
        txt = "".join(t.text or "" for t in par.iter(W + "t")).strip()
        if not txt:
            continue
        estilo = par.find(f"{W}pPr/{W}pStyle")
        nombre = normalizar(estilo.get(W + "val", "")) if estilo is not None else ""
        es_titulo = any(k in nombre for k in ("heading", "titulo", "title", "ttulo"))
        if not es_titulo and re.match(r"^\d{1,2}(\.\d{1,2})*\.?\s+\S", txt) and len(txt) <= 90 and not txt.endswith("."):
            es_titulo = True
        lineas.append(("# " if es_titulo else "") + txt)
    # Imágenes del cuerpo (las del encabezado viven en otros archivos y no cuentan).
    # Se cuentan por su tamaño en la hoja: un diagrama mide al menos 2" × 1.5";
    # los logos de portada son más chicos o muy bajos.
    WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    vistas = set()
    for dib in raiz.iter(W + "drawing"):
        ext = dib.find(f".//{WP}extent")
        blip = dib.find(f".//{A}blip")
        if ext is None or blip is None:
            continue
        cx, cy = int(ext.get("cx", 0)), int(ext.get("cy", 0))
        if cx >= 1828800 and cy >= 1371600:
            vistas.add(blip.get(R + "embed"))
    imagenes = len(vistas)
    return "\n".join(lineas), imagenes, []


def leer(ruta):
    ext = ruta.lower().rsplit(".", 1)[-1]
    return {"pdf": leer_pdf, "docx": leer_docx}.get(ext, leer_md)(ruta)


# ----------------------------------------------------------------------------
# Localizar la entrega
# ----------------------------------------------------------------------------
def candidatos(regla):
    vistos, salida = set(), []
    for patron in regla["buscar"]:
        for ruta in sorted(glob.glob(patron, recursive=True)):
            base = os.path.basename(ruta).lower()
            if ruta in vistos or base in regla.get("ignorar", []) or ruta.startswith(".github"):
                continue
            vistos.add(ruta)
            salida.append(ruta)
    return salida


def elegir_entrega(regla):
    """Lee todos los documentos posibles y se queda con el más completo."""
    leidos = []
    for ruta in candidatos(regla):
        texto, imgs, avisos = leer(ruta)
        leidos.append((palabras(texto), ruta, texto, imgs, avisos))
    if not leidos:
        return None, [], []
    leidos.sort(key=lambda x: (-x[0], x[1]))
    otros = [l[1] for l in leidos[1:] if l[0] >= regla.get("palabras_minimas_entrega", 150)]
    # PDF o Word con contenido pero sin texto que se pueda leer (exportado como imagen,
    # escaneado o con letras convertidas en trazos, como algunos de Canva).
    sin_texto = [l[1] for l in leidos if l[0] < 20 and l[1].lower().endswith((".pdf", ".docx"))
                 and os.path.getsize(l[1]) > 50_000]
    return leidos[0], otros, sin_texto


# ----------------------------------------------------------------------------
# Secciones
# ----------------------------------------------------------------------------
NUM = re.compile(r"^[\s#*_>|]*(?:(?:\d{1,2}(?:\.\d{1,2})*|[ivx]{1,4})[.)\-–]?\s+)?")


def limpiar_titulo(linea):
    l = normalizar(linea).strip()
    l = NUM.sub("", l)
    return l.strip(" #*_:.\t|")


def localizar_secciones(texto, secciones):
    """Devuelve {criterio: (indice_de_inicio, titulo_hallado)}.
    Primero busca entre títulos; luego entre renglones cortos."""
    lineas = texto.splitlines()
    limpios = [limpiar_titulo(l) for l in lineas]
    es_titulo = [l.lstrip().startswith("#") for l in lineas]
    hallado = {}
    for s in secciones:
        alias = [normalizar(a) for a in s["titulos"]]
        for solo_titulos in (True, False):
            for a in alias:                      # el primer título de la lista tiene prioridad
                for i, l in enumerate(limpios):
                    if not l or (solo_titulos and not es_titulo[i]):
                        continue
                    if not solo_titulos and (lineas[i].lstrip().startswith("|") or len(l) > 70):
                        continue
                    if l.startswith(a) and len(l) <= len(a) + 45:
                        hallado[s["criterio"]] = (i, lineas[i].strip(" #"))
                        break
                if s["criterio"] in hallado:
                    break
            if s["criterio"] in hallado:
                break
    return hallado, lineas


def cuerpos(hallado, lineas, todos_los_titulos):
    """El cuerpo de una sección llega hasta el siguiente título del mismo nivel o superior
    que también sea una sección, o hasta el siguiente título numerado de primer nivel."""
    inicios = sorted({i for i, _ in hallado.values()})

    def es_limite(l):
        m = re.match(r"^(#{1,6})\s*(.*)$", l.strip())
        if not m or len(m.group(1)) > 2:
            return False
        return not re.match(r"^\d{1,2}\.\d", m.group(2))  # 5.1, 5.2… son subsecciones

    primer_nivel = [i for i, l in enumerate(lineas) if es_limite(l)]
    limites = sorted(set(inicios) | set(primer_nivel))
    salida = {}
    for crit, (i, _) in hallado.items():
        fin = next((j for j in limites if j > i), len(lineas))
        salida[crit] = "\n".join(lineas[i + 1:fin])
    return salida


def evaluar(s, cuerpo, texto_completo):
    """Devuelve (estado, mensaje)."""
    def faltantes(t, con_palabras=True):
        f = []
        if con_palabras and palabras(t) < s.get("min_palabras", 0):
            f.append(f"Está muy breve ({palabras(t)} palabras; se esperan al menos {s['min_palabras']}).")
        for c in s.get("comprobaciones", []):
            if contar(c["patron"], t) < c.get("min", 1) and not c.get("aviso"):
                f.append(c["mensaje"])
        return f

    def avisos(t):
        a = [c["mensaje"] for c in s.get("comprobaciones", []) if c.get("aviso")
             and contar(c["patron"], t) < c.get("min", 1) and contar(c["patron"], texto_completo) < c.get("min", 1)]
        a += [c["mensaje"] for c in s.get("prohibido", []) if contar(c["patron"], t)]
        return a

    sugerencia = " o ".join(f"«{t}»" for t in s["titulos"][:2])
    global_ok = s.get("buscar_en_todo", True) and not faltantes(texto_completo, con_palabras=False)

    if cuerpo is not None:
        f = faltantes(cuerpo)
        if not f:
            a = avisos(cuerpo)
            return (REV, " ".join(a)) if a else (OK, "")
        if global_ok:
            return REV, "La sección existe, pero parte de lo que pide está en otra parte del documento: " + " ".join(f) + " El docente lo confirma."
        return FALTA, " ".join(f)

    if global_ok:
        return REV, (f"No encontré un título para este criterio, pero el documento sí trae evidencia. "
                     f"Para que se encuentre fácil, pueden titularlo {sugerencia}.")
    return FALTA, (f"No encontré este criterio en el documento. Agreguen una sección (por ejemplo {sugerencia}). "
                   + " ".join(faltantes(texto_completo, con_palabras=False)))


# ----------------------------------------------------------------------------
# Evidencia de GitHub (pull requests y revisiones)
# ----------------------------------------------------------------------------
def api(ruta):
    token, repo = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        return None
    cab = {"Accept": "application/vnd.github+json"}
    if token:
        cab["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/{ruta}", headers=cab)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception:
        return None


def evidencia_github():
    prs = api("pulls?state=all&per_page=50")
    if prs is None:
        return None
    bot = lambda u: (u or {}).get("type") == "Bot" or (u or {}).get("login", "").endswith("[bot]")
    autores, revisores, comentarios_rev, lineas = set(), set(), 0, []
    for pr in prs[:30]:
        if pr["head"]["ref"].startswith("robot-v2"):
            continue  # actualización del robot hecha por el docente, no es trabajo del equipo
        autor = pr["user"]["login"]
        autores.add(autor)
        quienes = set()
        for rv in api(f"pulls/{pr['number']}/reviews") or []:
            if not bot(rv.get("user")) and rv["user"]["login"] != autor:
                quienes.add(rv["user"]["login"])
                if (rv.get("body") or "").strip():
                    comentarios_rev += 1
        for c in api(f"issues/{pr['number']}/comments") or []:
            if not bot(c.get("user")) and c["user"]["login"] != autor and MARCA not in (c.get("body") or ""):
                quienes.add(c["user"]["login"])
                comentarios_rev += 1
        comentarios_rev += sum(1 for c in api(f"pulls/{pr['number']}/comments") or []
                               if not bot(c.get("user")) and c["user"]["login"] != autor)
        revisores |= quienes
        estado = "fusionado" if pr.get("merged_at") else pr["state"].replace("open", "abierto").replace("closed", "cerrado")
        lineas.append(f"#{pr['number']} de @{autor} ({estado})" + (f", revisado por {', '.join('@' + q for q in sorted(quienes))}" if quienes else ", sin revisión de otra persona"))
    return {"autores": autores, "revisores": revisores, "comentarios": comentarios_rev, "lineas": lineas}


def evaluar_github(tipo, gh, estado_doc, msg_doc):
    """Combina lo que dice el documento con lo que se ve en GitHub."""
    if gh is None:
        return estado_doc, msg_doc
    if tipo == "pull_requests":
        resumen = "En GitHub: " + "; ".join(gh["lineas"][:6]) + "."
        if gh["revisores"]:
            return OK, resumen
        return REV, resumen + " Falta que otro integrante revise y apruebe con un comentario."
    if tipo == "revision":
        if gh["comentarios"] and estado_doc != OK:
            return REV, f"Hay {gh['comentarios']} comentario(s) de revisión en GitHub. " + (msg_doc or "") + " Anoten en el documento qué hicieron con cada observación."
        return estado_doc, msg_doc
    return estado_doc, msg_doc


# ----------------------------------------------------------------------------
# Datos personales
# ----------------------------------------------------------------------------
def datos_personales(texto):
    reglas = [
        (r"\b[a-z]{4}\d{6}[hm][a-z]{5}[a-z0-9]\d\b", "una CURP"),
        (r"(?<![\d.,$])(?:\+?52[\s-]?)?\(?\d{2,3}\)?[\s-]?\d{3,4}[\s-]?\d{4}(?![\d.,])", "un número de teléfono"),
        (r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}[\w.]*\b", "un correo electrónico"),
    ]
    t = normalizar(texto)
    hallados = []
    for p, m in reglas:
        x = re.search(p, t)
        if x:
            hallados.append(f"Parece haber {m} («{x.group(0).strip()}»).")
    return hallados


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reglas", default=os.path.join(os.path.dirname(__file__), "reglas.json"))
    ap.add_argument("--salida", default="reporte.md")
    ap.add_argument("--sin-github", action="store_true")
    args = ap.parse_args()
    with open(args.reglas, encoding="utf-8") as f:
        regla = json.load(f)

    out = [MARCA, f"## Revisión de la entrega · {regla['practica']}", "",
           "> Esta revisión **no califica**. Busca en su entrega la evidencia de cada criterio de la rúbrica, "
           "sin importar el nombre del archivo ni los títulos que usen. La calificación la pone el docente con la rúbrica.", ""]

    elegido, otros, sin_texto = elegir_entrega(regla)
    minimo = regla.get("palabras_minimas_entrega", 150)
    if (not elegido or elegido[0] < minimo) and sin_texto:
        out.append(f"⚠️ **Revisión manual:** encontré {', '.join('`' + x + '`' for x in sin_texto)}, pero no tiene texto que se pueda leer "
                   "(se exportó como imagen, está escaneado o las letras quedaron como dibujos, como pasa con algunos diseños de Canva).")
        out.append("")
        out.append("La entrega **sí cuenta** y no se bloquea: el docente la revisa a mano con la rúbrica. "
                   "Si pueden, vuelvan a exportarla desde Word o Google Docs con **Guardar como PDF** para que el robot también la lea.")
        escribir(args.salida, out)
        return 0
    if not elegido or elegido[0] < minimo:
        donde = f"`{elegido[1]}` está vacío o casi vacío ({elegido[0]} palabras)" if elegido else "no encontré ningún PDF, Word o Markdown"
        out.append(f"⛔ **No encontré la entrega:** {donde}.")
        out.append("")
        out.append("Suban su documento (PDF, Word o Markdown, con el nombre que quieran) a la carpeta `entrega/` "
                   "**en una rama y por pull request**. Un archivo adjunto en un issue no cuenta como entrega.")
        escribir(args.salida, out)
        return 1

    n_pal, ruta, texto, imgs, avisos_lectura = elegido
    pngs = {p for patron in regla.get("imagenes_en", []) for p in glob.glob(patron, recursive=True)
            if not p.startswith(".github")}
    total_imgs = max(imgs, len(pngs))

    hallado, lineas = localizar_secciones(texto, regla["secciones"])
    cuerpo = cuerpos(hallado, lineas, regla["secciones"])
    gh = None if args.sin_github else evidencia_github()

    filas, bloqueos, faltan, revisar, al_final = [], [], 0, 0, []
    for s in regla["secciones"]:
        if s.get("al_final"):
            # Se califica al cerrar la práctica, con el historial completo de pull requests.
            resumen = "; ".join(gh["lineas"][:6]) if gh else ""
            if s.get("al_final_msg"):
                al_final.append((s["criterio"], FINAL, s["al_final_msg"]))
            else:
                al_final.append((s["criterio"], FINAL, "Se califica al final, cuando el pull request ya esté revisado por otro integrante y fusionado."
                                 + (f" Hasta ahora en GitHub: {resumen}." if resumen else "")))
            continue
        estado, msg = evaluar(s, cuerpo.get(s["criterio"]), texto)
        if s.get("github"):
            estado, msg = evaluar_github(s["github"], gh, estado, msg)
        if estado == FALTA:
            faltan += 1
        elif estado == REV:
            revisar += 1
        donde = f" _(en «{hallado[s['criterio']][1][:60]}»)_" if s["criterio"] in hallado and estado != FALTA else ""
        filas.append((s["criterio"] + donde, estado, msg))

    req = regla.get("imagenes_minimas", 1)
    if total_imgs == 0:
        bloqueos.append(("Diagramas", ALTO, "No encontré ninguna imagen de diagrama. Insértenla en el documento o súbanla como PNG a `docs/analisis/`."))
    elif total_imgs < req:
        filas.append(("Diagramas", REV, f"Encontré {total_imgs} imagen(es) de diagramas; la práctica pide al menos {req}."))
        revisar += 1

    personales = datos_personales(texto)
    if personales:
        bloqueos.append(("Datos personales", ALTO, " ".join(personales) + " El repositorio es público: quítenlo y usen el cargo o rol."))

    out.append(f"**Documento revisado:** `{ruta}` ({n_pal} palabras) · **Imágenes de diagramas:** {total_imgs}")
    if otros:
        out.append(f"También encontré: {', '.join('`' + o + '`' for o in otros)}. Revisé el más completo.")
    out.append("")
    out.append("| Criterio de la rúbrica | Estado | Qué falta o qué revisar |")
    out.append("|---|---|---|")
    for c, e, m in bloqueos + filas + al_final:
        out.append(f"| {c} | {e} | {m.replace('|', '/')} |")
    out.append("")

    sugerencias = list(avisos_lectura)
    for rec in regla.get("archivos_recomendados", []):
        patrones = rec["patrones"] if isinstance(rec, dict) else [rec]
        if not any(glob.glob(p, recursive=True) for p in patrones):
            nombre = rec.get("nombre") if isinstance(rec, dict) else f"`{rec}`"
            sugerencias.append(f"Se recomienda subir {nombre}.")
    sugerencias.append("Personas de la organización: por su cargo, rol o apodo, no por su nombre completo.")
    out.append("**Para revisar:**")
    out += [f"- {a}" for a in sugerencias]
    out.append("")
    out.append("<sub>✅ encontrado · ⚠️ hay evidencia, el docente la confirma · ❌ no se encontró (no bloquea, pero cuenta en la rúbrica) · "
               "⛔ bloquea la fusión hasta corregirlo · ⏳ se califica al final</sub>")
    out.append("")
    if bloqueos:
        out.append(f"**Resultado:** hay {len(bloqueos)} punto(s) que bloquean la fusión (⛔). Corríjanlos y suban los cambios a esta misma rama; la revisión se repite sola.")
        codigo = 1
    elif faltan:
        out.append(f"**Resultado:** la entrega se puede revisar. No encontré evidencia de {faltan} criterio(s) (❌); si los completan antes de la fecha, suben de nivel en la rúbrica.")
        codigo = 0
    else:
        out.append("**Resultado:** encontré evidencia de todos los criterios. Ya puede pasar a la revisión de un compañero y del docente.")
        codigo = 0
    escribir(args.salida, out)
    return codigo


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
