import math
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r"C:\tmp\video_deps")

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


W, H = 1080, 1920
FPS = 18
OUT_DIR = Path(r"C:\Users\chapu\Desktop\codex prueba\video-campus26")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MP4 = OUT_DIR / "campus-verano-2026-reel.mp4"
OUT_POSTER = OUT_DIR / "campus-verano-2026-poster.jpg"

FONT_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\ariali.ttf"
FONT_BOLD_ITALIC = r"C:\Windows\Fonts\arialbi.ttf"

PHOTO_DIR = Path(
    r"C:\Users\chapu\Desktop\alejandrolavid\COLONIAL\COLONIALES\2 CAMPUS\57 a 68 campus verano 2026\fotos para semanas"
)

WEEKS = [
    {
        "n": "01",
        "title": "VACÍO",
        "date": "22 - 26 junio",
        "hook": "Todo revuelto",
        "cells": ("Todo revuelto", "Toma la Calle"),
        "phrase": "El aburrimiento es el primer material.",
        "concept": "El lienzo en blanco, el silencio, el espacio disponible.",
        "color": "#6b9db8",
        "photo": "1 vacio.jpg",
        "symbol": "void",
    },
    {
        "n": "02",
        "title": "PARTÍCULA",
        "date": "29 junio - 3 julio",
        "hook": "Movimiento Browniano",
        "cells": ("Enlaces Covalentes", "Haz que Suene"),
        "phrase": "De lo mínimo emergen sistemas complejos.",
        "concept": "El punto, el origen, el grano de arena.",
        "color": "#c8973a",
        "photo": "2 particulas.jpg",
        "symbol": "particle",
    },
    {
        "n": "03",
        "title": "FILAMENTO",
        "date": "6 - 10 julio",
        "hook": "Vaya telar",
        "cells": ("Vaya Telar", "Moda Tinker"),
        "phrase": "Una línea puede construir un espacio entero.",
        "concept": "La línea, el hilo que busca a otro hilo.",
        "color": "#3aaba0",
        "photo": "3 filamentos.jpg",
        "symbol": "filament",
    },
    {
        "n": "04",
        "title": "NODO",
        "date": "13 - 17 julio",
        "hook": "Lógica recíproca",
        "cells": ("Lógica Recíproca", "Más Madera"),
        "phrase": "El punto de unión es donde nace la fuerza.",
        "concept": "El encuentro, el nudo, el cruce donde nace la fuerza.",
        "color": "#d4663a",
        "photo": "4 nodo.jpg",
        "symbol": "node",
    },
    {
        "n": "05",
        "title": "MEMBRANA",
        "date": "20 - 24 julio",
        "hook": "Tercera piel",
        "cells": ("Modos de Habitar", "Cartón Cartón Cartón"),
        "phrase": "La piel separa sin cerrar: es un filtro, no un muro.",
        "concept": "El plano, la superficie, la piel que envuelve el vacío.",
        "color": "#8b5fc8",
        "photo": "5 membranas.jpg",
        "symbol": "membrane",
    },
    {
        "n": "06",
        "title": "PORO",
        "date": "27 - 31 julio",
        "hook": "Filtra · regula · conecta",
        "cells": ("Enlaces Covalentes", "Toma la Calle"),
        "phrase": "Observar el flujo y transformar el paso de la materia.",
        "concept": "El intercambio, el agujero que permite respirar y filtrar.",
        "color": "#4aaa5e",
        "photo": "6 Poro.jpg",
        "symbol": "pore",
    },
    {
        "n": "07",
        "title": "MATRIZ",
        "date": "3 - 7 agosto",
        "hook": "Estructura hexagonal",
        "cells": ("Estampados", "Todo en Regla"),
        "phrase": "El orden aparece a partir de reglas sencillas.",
        "concept": "El orden, el sistema, la geometría que organiza el caos.",
        "color": "#a8bc2a",
        "photo": "7 matriz.jpg",
        "symbol": "matrix",
    },
    {
        "n": "08",
        "title": "CAMPO",
        "date": "10 - 14 agosto",
        "hook": "Sonido · Imanes",
        "cells": ("Experimentos Electromagnéticos", "Somos Luz"),
        "phrase": "Lo que no se ve también construye.",
        "concept": "La atmósfera, la vibración, lo invisible que irradia.",
        "color": "#4a78c8",
        "photo": "8 campo.jpg",
        "symbol": "field",
    },
    {
        "n": "09",
        "title": "PRANA",
        "date": "17 - 21 agosto",
        "hook": "Haz que suene",
        "cells": ("Haz que Suene", "Canica Dinámica"),
        "phrase": "Todo lo aprendido respira.",
        "concept": "La vida, el aliento, el movimiento que activa todo lo anterior.",
        "color": "#d81b60",
        "photo": "9 prana2.jpg",
        "symbol": "prana",
    },
    {
        "n": "10",
        "title": "SIMBIOSIS",
        "date": "24 - 28 agosto",
        "hook": "Unión · Interdependencia",
        "cells": ("Autonomía", "Modos de Habitar"),
        "phrase": "El todo es mayor que la suma de las partes.",
        "concept": "La convivencia y el apoyo mutuo de sistemas diferentes.",
        "color": "#1aaa90",
        "photo": "10 simbiosis.jpg",
        "symbol": "symbiosis",
    },
    {
        "n": "11",
        "title": "HUELLA",
        "date": "31 agosto - 4 septiembre",
        "hook": "Lo que queda",
        "cells": ("Estampados", "Patrimonio de Cantabria"),
        "phrase": "La huella es el último material del verano.",
        "concept": "El registro, la memoria, lo que queda después del juego.",
        "color": "#b07848",
        "photo": "11 huella.jpg",
        "symbol": "trace",
    },
]

TRANSITIONS = [
    ("CONDENSACIÓN", "La energía se concentra. Nace la primera unidad."),
    ("ATRACCIÓN", "Las partículas se reconocen y empiezan a formar patrones."),
    ("CONEXIÓN", "El punto busca al punto. Aparece la línea."),
    ("TENSIÓN", "Las líneas se cruzan. La estructura aprende a sostenerse."),
    ("ENVOLTURA", "El nodo se expande y aparece una piel habitable."),
    ("INTERCAMBIO", "La piel respira. Algo pasa, algo queda."),
    ("ORGANIZACIÓN", "Los poros ordenan el flujo. Nace una matriz."),
    ("IRRADIACIÓN", "La matriz vibra. Lo invisible empieza a dirigir."),
    ("ACTIVACIÓN", "El campo se mueve. El sistema cobra vida."),
    ("COOPERACIÓN", "Las partes se apoyan y aparece un organismo común."),
    ("MEMORIA", "Lo vivido deja rastro. El verano se convierte en huella."),
]


def font(size, bold=False, italic=False):
    path = FONT_REG
    if bold and italic:
        path = FONT_BOLD_ITALIC
    elif bold:
        path = FONT_BOLD
    elif italic:
        path = FONT_ITALIC
    return ImageFont.truetype(path, size=size)


F = {
    "tiny": font(27, bold=True),
    "small": font(34, bold=True),
    "body": font(42),
    "body_bold": font(44, bold=True),
    "date": font(52, bold=True),
    "h2": font(75, bold=True),
    "h1": font(104, bold=True),
    "mega": font(178, bold=True),
    "italic": font(43, italic=True),
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def ease(x):
    x = max(0, min(1, x))
    return x * x * (3 - 2 * x)


def clamp(x, a=0, b=1):
    return max(a, min(b, x))


def fit_cover(img, w=W, h=H, zoom=1.0, offset=(0, 0)):
    iw, ih = img.size
    scale = max(w / iw, h / ih) * zoom
    nw, nh = int(iw * scale), int(ih * scale)
    im = img.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (w - nw) // 2 + int(offset[0])
    y = (h - nh) // 2 + int(offset[1])
    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    canvas.paste(im, (x, y))
    return canvas


def load_photo(name):
    img = Image.open(PHOTO_DIR / name).convert("RGB")
    return img


PHOTOS = [load_photo(w["photo"]) for w in WEEKS]


def overlay_color(img, color, alpha=70):
    ov = Image.new("RGBA", img.size, color + (alpha,))
    return Image.alpha_composite(img.convert("RGBA"), ov)


def shadow_text(draw, xy, text, fnt, fill, anchor=None, stroke=0, align="left"):
    x, y = xy
    draw.text((x + 3, y + 5), text, font=fnt, fill=(0, 0, 0, 145), anchor=anchor, align=align, stroke_width=stroke)
    draw.text((x, y), text, font=fnt, fill=fill, anchor=anchor, align=align, stroke_width=stroke)


def wrap_text(text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for word in words:
        cand = (cur + " " + word).strip()
        if probe.textlength(cand, font=fnt) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_symbol(draw, kind, cx, cy, r, color, alpha=210, t=0):
    c = color + (alpha,)
    pale = color + (90,)
    if kind == "void":
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=12)
        draw.ellipse((cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45), outline=pale, width=4)
    elif kind == "particle":
        for i in range(18):
            a = i * math.tau / 18 + t * 0.7
            rr = r * (0.15 + 0.78 * ((i * 37) % 100) / 100)
            x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=c)
    elif kind == "filament":
        for i in range(7):
            y = cy - r + i * r / 3
            pts = []
            for k in range(80):
                x = cx - r + 2 * r * k / 79
                pts.append((x, y + math.sin(k / 7 + i + t) * 22))
            draw.line(pts, fill=c, width=6)
    elif kind == "node":
        pts = [(cx, cy - r), (cx + r * 0.86, cy - r * 0.2), (cx + r * 0.55, cy + r * 0.9), (cx - r * 0.55, cy + r * 0.9), (cx - r * 0.86, cy - r * 0.2)]
        for i, p in enumerate(pts):
            for q in pts[i + 1 :]:
                draw.line((p, q), fill=pale, width=4)
        for p in pts:
            draw.ellipse((p[0] - 20, p[1] - 20, p[0] + 20, p[1] + 20), fill=c)
    elif kind == "membrane":
        for i in range(5):
            box = (cx - r + i * 12, cy - r * 0.65 + i * 18, cx + r - i * 12, cy + r * 0.65 - i * 18)
            draw.arc(box, 190, 350, fill=c if i == 0 else pale, width=8)
    elif kind == "pore":
        for i in range(5):
            for j in range(4):
                x = cx - r * 0.8 + i * r * 0.4
                y = cy - r * 0.55 + j * r * 0.38
                rr = 12 + ((i + j) % 3) * 8
                draw.ellipse((x - rr, y - rr, x + rr, y + rr), outline=c, width=7)
    elif kind == "matrix":
        for i in range(-2, 3):
            for j in range(-2, 3):
                x = cx + i * r * 0.43 + (j % 2) * r * 0.21
                y = cy + j * r * 0.38
                poly = [(x + math.cos(math.tau * k / 6) * 28, y + math.sin(math.tau * k / 6) * 28) for k in range(6)]
                draw.polygon(poly, outline=c)
    elif kind == "field":
        for rr in [r * 0.35, r * 0.55, r * 0.75, r * 0.95]:
            draw.ellipse((cx - rr, cy - rr * 0.55, cx + rr, cy + rr * 0.55), outline=c, width=6)
        draw.line((cx, cy - r, cx, cy + r), fill=pale, width=5)
    elif kind == "prana":
        pts = []
        for k in range(120):
            x = cx - r + 2 * r * k / 119
            y = cy + math.sin(k / 8 + t) * 45
            pts.append((x, y))
        draw.line(pts, fill=c, width=10)
        draw.arc((cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5), 35, 320, fill=pale, width=8)
    elif kind == "symbiosis":
        draw.ellipse((cx - r * 0.85, cy - r * 0.45, cx + r * 0.15, cy + r * 0.55), outline=c, width=10)
        draw.ellipse((cx - r * 0.15, cy - r * 0.55, cx + r * 0.85, cy + r * 0.45), outline=pale, width=10)
    else:
        for i in range(7):
            box = (cx - r + i * 17, cy - r * 0.8 + i * 12, cx + r - i * 17, cy + r * 0.8 - i * 12)
            draw.arc(box, 105, 430, fill=c if i < 3 else pale, width=6)


def prepare_base(idx):
    xoff = math.sin(idx * 1.7) * 30
    yoff = math.cos(idx * 1.3) * 25
    im = fit_cover(PHOTOS[idx], zoom=1.08, offset=(xoff, yoff))
    im = ImageEnhance.Color(im).enhance(0.78)
    im = ImageEnhance.Contrast(im).enhance(0.92)
    color = hex_to_rgb(WEEKS[idx]["color"])
    im = overlay_color(im, color, 46)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade, "RGBA")
    sd.rectangle((0, 0, W, H), fill=(0, 0, 0, 78))
    sd.rectangle((0, int(H * 0.58), W, H), fill=(0, 0, 0, 112))
    return Image.alpha_composite(im, shade)


BASES = [prepare_base(i) for i in range(len(WEEKS))]


def base_from_week(idx, t, dur):
    return BASES[idx].copy()


def draw_brand(draw, color):
    draw.text((64, 64), "COLONIALES", font=F["tiny"], fill=(255, 255, 255, 210))
    draw.line((64, 105, 257, 105), fill=color + (230,), width=5)
    draw.text((64, 124), "Espacio de aprendizaje, estimulación y juego", font=font(24), fill=(255, 255, 255, 185))


def intro_frame(t, dur):
    idx = min(len(WEEKS) - 1, int(t / dur * len(WEEKS)))
    bg = base_from_week(idx, t, dur)
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 95))
    img = Image.alpha_composite(bg, wash)
    draw = ImageDraw.Draw(img, "RGBA")
    color = hex_to_rgb("#d81b60")
    draw_brand(draw, color)
    p = ease(t / 1.3)
    y = 470 - (1 - p) * 80
    shadow_text(draw, (64, y), "CAMPUS\nVERANO\n2026", F["mega"], (255, 255, 255, int(255 * p)))
    rounded_rect(draw, (64, 1120, 1016, 1368), 30, (255, 255, 255, 235))
    draw.text((104, 1160), "Un mundo por construir", font=F["h2"], fill=(17, 17, 17, 255))
    desc = "Imaginar el mundo desde dentro: tocarlo, construirlo y transformarlo paso a paso."
    draw.text((104, 1258), wrap_text(desc, F["body"], 850), font=F["body"], fill=(70, 70, 70, 255), spacing=10)
    draw.text((64, 1510), "22 junio - 4 septiembre", font=F["date"], fill=(255, 255, 255, 235))
    draw.text((64, 1582), "4 a 15 años · Enclave Pronillo", font=F["body_bold"], fill=color + (255,))
    draw.text((64, 1648), "10 a 14 h / 9 a 15 h extendido", font=F["body"], fill=(255, 255, 255, 220))
    return img.convert("RGB")


def week_frame(idx, t, dur):
    w = WEEKS[idx]
    color = hex_to_rgb(w["color"])
    img = base_from_week(idx, t, dur)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_brand(draw, color)

    p1 = ease((t - 0.15) / 0.8)
    p2 = ease((t - 0.65) / 0.9)
    p3 = ease((t - 1.15) / 0.9)
    p4 = ease((t - 1.65) / 0.9)
    out = 1 - ease((t - (dur - 0.7)) / 0.7)
    alpha = int(255 * out)

    draw_symbol(draw, w["symbol"], 840, 352, 155, color, int(190 * out), t)
    rounded_rect(draw, (64, 318, 218, 472), 12, color + (int(235 * p1 * out),))
    draw.text((141, 394), w["n"], font=F["h2"], fill=(255, 255, 255, int(255 * p1 * out)), anchor="mm")

    shadow_text(draw, (64, 540 - (1 - p1) * 45), w["title"], F["h1"], (255, 255, 255, int(alpha * p1)))
    draw.text((66, 648), w["concept"], font=F["italic"], fill=color + (int(245 * p2 * out),))

    y = 810
    rounded_rect(draw, (64, y, 1016, y + 366), 28, (255, 255, 255, int(236 * p2 * out)))
    draw.text((104, y + 42), w["date"].upper(), font=F["date"], fill=(17, 17, 17, int(255 * p2 * out)))
    draw.text((104, y + 118), w["hook"], font=F["body_bold"], fill=color + (int(255 * p3 * out),))

    c1, c2 = w["cells"]
    draw.text((104, y + 194), "CELDAS", font=F["tiny"], fill=(130, 130, 130, int(255 * p3 * out)))
    cells_text = wrap_text(f"{c1}  +  {c2}", F["body_bold"], 820)
    draw.text((104, y + 236), cells_text, font=F["body_bold"], fill=(28, 28, 28, int(255 * p3 * out)), spacing=6)

    phrase = wrap_text(w["phrase"], F["h2"], 860)
    draw.text((64, 1288 + (1 - p4) * 40), phrase, font=F["h2"], fill=(255, 255, 255, int(245 * p4 * out)), spacing=8)
    draw.line((64, 1512, 1016, 1512), fill=color + (int(230 * p4 * out),), width=8)
    draw.text((64, 1552), "Campus urbano · Santander", font=F["body_bold"], fill=(255, 255, 255, int(225 * p4 * out)))
    return img.convert("RGB")


def transition_frame(idx, t, dur):
    p = ease(t / dur)
    bg = Image.blend(BASES[idx].convert("RGB"), BASES[min(idx + 1, len(WEEKS) - 1)].convert("RGB"), p).convert("RGBA")
    bg = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (0, 0, 0, 150)))
    draw = ImageDraw.Draw(bg, "RGBA")
    color = hex_to_rgb(WEEKS[min(idx + 1, len(WEEKS) - 1)]["color"])
    title, phrase = TRANSITIONS[idx]
    draw.line((64, 480, 1016, 480), fill=color + (230,), width=8)
    shadow_text(draw, (64, 645), title, F["h1"], (255, 255, 255, 255))
    draw.text((64, 770), wrap_text(phrase, F["h2"], 890), font=F["h2"], fill=(255, 255, 255, 238), spacing=10)
    draw.text((64, 1190), f"{WEEKS[idx]['title']}  →  {WEEKS[min(idx + 1, len(WEEKS) - 1)]['title']}", font=F["body_bold"], fill=color + (255,))
    return bg.convert("RGB")


def outro_frame(t, dur):
    bg = base_from_week(10, t, dur)
    bg = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (0, 0, 0, 130)))
    draw = ImageDraw.Draw(bg, "RGBA")
    color = hex_to_rgb("#d81b60")
    draw_brand(draw, color)
    shadow_text(draw, (64, 460), "DEL VACÍO\nAL SISTEMA", F["mega"], (255, 255, 255, 255))
    draw.text((64, 910), wrap_text("Construiremos con partículas, líneas, estructuras, pieles y espacios habitables.", F["h2"], 900), font=F["h2"], fill=(255, 255, 255, 238), spacing=8)
    rounded_rect(draw, (64, 1278, 1016, 1578), 30, (255, 255, 255, 238))
    draw.text((104, 1324), "Campus urbano · 4 a 15 años", font=F["date"], fill=(17, 17, 17, 255))
    draw.text((104, 1400), "22 junio - 4 septiembre · Santander", font=F["body_bold"], fill=color + (255,))
    draw.text((104, 1464), "625 039 565 · tallerescoloniales.com", font=F["body"], fill=(45, 45, 45, 255))
    draw.text((104, 1522), "@tallerescoloniales", font=F["body_bold"], fill=(45, 45, 45, 255))
    return bg.convert("RGB")


def make_timeline():
    items = [("intro", None, 4.2)]
    for i in range(len(WEEKS)):
        items.append(("week", i, 3.35))
        items.append(("transition", i, 1.0))
    items.append(("outro", None, 4.4))
    return items


def render():
    frames_dir = OUT_DIR / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame_*.jpg"):
        old.unlink()
    frame_no = 0
    poster_saved = False
    for kind, idx, dur in make_timeline():
        frames = int(round(dur * FPS))
        for f in range(frames):
            t = f / FPS
            if kind == "intro":
                frame = intro_frame(t, dur)
            elif kind == "week":
                frame = week_frame(idx, t, dur)
            else:
                if idx is None:
                    frame = outro_frame(t, dur)
                else:
                    frame = transition_frame(idx, t, dur)
            if not poster_saved and frame_no > FPS * 7:
                frame.save(OUT_POSTER, quality=92)
                poster_saved = True
            frame.save(frames_dir / f"frame_{frame_no:05d}.jpg", quality=90, optimize=False)
            frame_no += 1
            if frame_no % 120 == 0:
                print(f"rendered {frame_no} frames")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    if OUT_MP4.exists():
        OUT_MP4.unlink()
    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        str(frames_dir / "frame_%05d.jpg"),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "21",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)
    print(f"OK {OUT_MP4}")
    print(f"POSTER {OUT_POSTER}")


if __name__ == "__main__":
    render()
