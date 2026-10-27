import streamlit as st
import yt_dlp
import os
import shutil
from pathlib import Path

st.set_page_config(page_title="VidDrop", page_icon="⬇️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f; color: #e8e4dc; font-family: 'Syne', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #1a0a2e 0%, #0a0a0f 50%),
                radial-gradient(ellipse at 80% 90%, #0d1a0a 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.block-container { max-width: 720px !important; padding: 3rem 2rem 4rem !important; }
.hero { text-align: center; padding: 2.5rem 0 2rem; }
.hero-badge {
    display: inline-block; font-family: 'Space Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.3em; text-transform: uppercase;
    color: #7aff6e; background: rgba(122,255,110,0.08);
    border: 1px solid rgba(122,255,110,0.25); padding: 0.3rem 1rem;
    border-radius: 2px; margin-bottom: 1.2rem;
}
.hero-title {
    font-size: clamp(3rem, 8vw, 5rem); font-weight: 800; line-height: 0.9;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e8e4dc 0%, #7aff6e 50%, #e8e4dc 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.6rem;
}
.hero-sub { font-family: 'Space Mono', monospace; font-size: 0.78rem; color: #666; }
.card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px; padding: 1.8rem; margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Space Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.25em; text-transform: uppercase;
    color: #7aff6e; margin-bottom: 1rem;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 2px !important; color: #e8e4dc !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(122,255,110,0.4) !important;
    box-shadow: 0 0 0 3px rgba(122,255,110,0.06) !important;
}
[data-testid="stTextInput"] label, [data-testid="stSelectbox"] label,
[data-testid="stRadio"] label {
    color: #888 !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e8e4dc !important;
}
[data-testid="stButton"] button {
    width: 100%; background: #7aff6e !important; color: #0a0a0f !important;
    border: none !important; border-radius: 2px !important;
    font-family: 'Space Mono', monospace !important; font-weight: 700 !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
}
[data-testid="stButton"] button:hover {
    background: #a0ffaa !important;
    box-shadow: 0 8px 24px rgba(122,255,110,0.25) !important;
}
div[data-testid="column"]:last-child [data-testid="stButton"] button {
    background: transparent !important; color: #e8e4dc !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
.status-box {
    background: rgba(122,255,110,0.05); border: 1px solid rgba(122,255,110,0.2);
    border-left: 3px solid #7aff6e; border-radius: 2px; padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #7aff6e;
    margin-top: 1rem; white-space: pre-wrap; word-break: break-all;
}
.error-box {
    background: rgba(255,80,80,0.05); border: 1px solid rgba(255,80,80,0.2);
    border-left: 3px solid #ff5050; border-radius: 2px; padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #ff7070;
    margin-top: 1rem; word-break: break-all;
}
.info-box {
    white-space: pre-wrap;
    background: rgba(100,160,255,0.05); border: 1px solid rgba(100,160,255,0.2);
    border-left: 3px solid #64a0ff; border-radius: 2px; padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #90b8ff;
    margin-top: 1rem;
}
.warn-box {
    background: rgba(255,180,50,0.05); border: 1px solid rgba(255,180,50,0.2);
    border-left: 3px solid #ffb432; border-radius: 2px; padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace; font-size: 0.75rem; color: #ffd080;
    margin-top: 1rem;
}
hr { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.5rem 0; }
.footer { text-align: center; font-family: 'Space Mono', monospace;
    font-size: 0.62rem; color: #333; letter-spacing: 0.1em; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Video Downloader</div>
    <div class="hero-title">VidDrop</div>
    <div class="hero-sub">YouTube · TikTok · Instagram · Twitter · + 1000 sites</div>
</div>
""", unsafe_allow_html=True)

# ── URL ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">↓ Source</div>', unsafe_allow_html=True)
url = st.text_input("URL", placeholder="https://youtu.be/...", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ── Destination ───────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">◎ Destination</div>', unsafe_allow_html=True)
dest_mode = st.radio("Destination", [
    "📥  Dossier Téléchargements (défaut)",
    "📁  Choisir un emplacement personnalisé"
], label_visibility="collapsed")

default_dl = str(Path.home() / "Downloads")
if dest_mode.startswith("📥"):
    save_dir = default_dl
    st.markdown(f'<div class="info-box">→ {save_dir}</div>', unsafe_allow_html=True)
else:
    save_dir = st.text_input("Chemin", value=default_dl, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ── Qualité ───────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">⚙ Qualité & Format</div>', unsafe_allow_html=True)

HAS_FFMPEG = shutil.which("ffmpeg") is not None
if not HAS_FFMPEG:
    st.markdown('<div class="warn-box">ℹ ffmpeg non détecté — seuls les formats pré-fusionnés (sans réencodage) sont disponibles. Installe ffmpeg pour débloquer 1080p+ et le MP3.</div>', unsafe_allow_html=True)

# ── Format map — tous sans fusion ─────────────────────────────────────────────
FORMAT_MAP = {
    "Meilleure qualité (sans ffmpeg)": "best",          # fichier unique déjà fusionné
    "720p (sans ffmpeg)":              "best[height<=720]",
    "480p":                            "best[height<=480]",
    "360p":                            "best[height<=360]",
    "Audio seulement (MP3)":           "bestaudio/best",
}

FORMAT_MAP_FFMPEG = {
    "Meilleure qualité":     "bestvideo+bestaudio/best",
    "1080p":                 "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720p":                  "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480p":                  "bestvideo[height<=480]+bestaudio/best[height<=480]",
    "Audio seulement (MP3)": "bestaudio/best",
}

# YouTube exige un runtime JavaScript (deno ou node) pour extraire les formats
JS_RUNTIMES = {rt: {} for rt in ("deno", "node") if shutil.which(rt)}
BASE_OPTS = {"js_runtimes": JS_RUNTIMES} if JS_RUNTIMES else {}

FORMATS = FORMAT_MAP_FFMPEG if HAS_FFMPEG else FORMAT_MAP

col1, col2 = st.columns(2)
with col1:
    quality = st.selectbox("Qualité", list(FORMATS))
with col2:
    subtitle = st.selectbox("Sous-titres", ["Non", "Oui (auto)"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Progress hook ─────────────────────────────────────────────────────────────
class ProgressLogger:
    def __init__(self, ph):
        self.ph = ph
        self.lines = []

    def hook(self, d):
        if d["status"] == "downloading":
            pct   = d.get("_percent_str", "?").strip()
            speed = d.get("_speed_str",   "?").strip()
            eta   = d.get("_eta_str",     "?").strip()
            self.lines = self.lines[-6:] + [f"⬇ {pct}  —  {speed}  —  ETA {eta}"]
        elif d["status"] == "finished":
            self.lines.append("✔ Fichier reçu, finalisation...")
        self.ph.markdown(
            '<div class="status-box">' + "\n".join(self.lines) + "</div>",
            unsafe_allow_html=True,
        )

# ── Download ──────────────────────────────────────────────────────────────────
def do_download(url, save_dir, fmt, subs, status_ph, done_ph):
    os.makedirs(save_dir, exist_ok=True)
    logger = ProgressLogger(status_ph)

    ydl_opts = {
        **BASE_OPTS,
        "format": fmt,
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [logger.hook],
        "quiet": True,
        "no_warnings": True,
    }

    if fmt == "bestaudio/best":
        if HAS_FFMPEG:
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192",
            }]
        else:
            # Sans ffmpeg : on garde le format audio natif (webm/m4a)
            ydl_opts["format"] = "bestaudio"
    elif HAS_FFMPEG:
        ydl_opts["merge_output_format"] = "mp4"

    if subs == "Oui (auto)":
        ydl_opts.update({"writeautomaticsub": True, "subtitleslangs": ["fr", "en"]})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info  = ydl.extract_info(url, download=True)
            title = info.get("title", "vidéo")
        done_ph.markdown(
            f'<div class="status-box">✦ Terminé !\n→ "{title}"\n→ Sauvegardé dans : {save_dir}</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        done_ph.markdown(
            f'<div class="error-box">✘ Erreur : {e}</div>',
            unsafe_allow_html=True,
        )

# ── Boutons ───────────────────────────────────────────────────────────────────
col_dl, col_info = st.columns([3, 1])
with col_dl:
    go = st.button("⬇  Télécharger")
with col_info:
    info_btn = st.button("ℹ  Infos")

status_ph = st.empty()
done_ph   = st.empty()

if info_btn:
    if not url.strip():
        status_ph.markdown('<div class="error-box">✘ Colle d\'abord une URL.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("Récupération..."):
            try:
                with yt_dlp.YoutubeDL({**BASE_OPTS, "quiet": True}) as ydl:
                    meta = ydl.extract_info(url, download=False)
                m, s = divmod(int(meta.get("duration") or 0), 60)
                status_ph.markdown(
                    f'<div class="info-box"><b>{meta.get("title","N/A")}</b>\n\n'
                    f'🕒 {m}m {s}s\n📺 {meta.get("uploader","?")}\n'
                    f'👁 {meta.get("view_count") or 0:,} vues\n'
                    f'🌐 {meta.get("extractor_key","?")}</div>',
                    unsafe_allow_html=True,
                )
            except Exception as e:
                status_ph.markdown(f'<div class="error-box">✘ {e}</div>', unsafe_allow_html=True)

if go:
    if not url.strip():
        status_ph.markdown('<div class="error-box">✘ Colle d\'abord une URL.</div>', unsafe_allow_html=True)
    elif not save_dir.strip():
        status_ph.markdown('<div class="error-box">✘ Indique un dossier de destination.</div>', unsafe_allow_html=True)
    else:
        status_ph.markdown('<div class="status-box">⟳ Connexion...</div>', unsafe_allow_html=True)
        do_download(url, save_dir.strip(), FORMATS[quality], subtitle, status_ph, done_ph)

st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('<div class="footer">VIDDROP · propulsé par yt-dlp · usage personnel uniquement</div>', unsafe_allow_html=True)