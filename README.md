# VidDrop

Interface web locale (Streamlit) pour télécharger des vidéos et de l'audio avec [yt-dlp](https://github.com/yt-dlp/yt-dlp) : YouTube, TikTok, Instagram, Twitter et plus de 1000 sites.

## Prérequis

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (optionnel) : débloque le 1080p+ et la conversion MP3
- [Node.js](https://nodejs.org/) ou [Deno](https://deno.com/) : nécessaire pour YouTube

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

Les fichiers sont enregistrés sur la machine qui exécute l'app (par défaut dans `~/Downloads`).

> Si YouTube renvoie des erreurs 403 ou « format not available », mets yt-dlp à jour : `pip install -U "yt-dlp[default]"`

## Avertissement

Usage personnel uniquement. Respecte les conditions d'utilisation des sites et les droits d'auteur.

## Installateur Windows

Lance `build.bat` : il génère `build\installer\VidDrop-Setup-1.0.0.exe`. Il faut le `.venv` et [Inno Setup 6](https://jrsoftware.org/isinfo.php) (`winget install JRSoftware.InnoSetup`).

L'installateur ne demande pas de droits administrateur. Il installe l'app dans `%LOCALAPPDATA%\Programs\VidDrop`, crée les raccourcis et peut installer ffmpeg et Node.js via winget s'ils manquent.
