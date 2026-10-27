"""Point d'entrée de VidDrop.exe : démarre le serveur Streamlit et ouvre le navigateur."""
import os
import socket
import sys
import webbrowser

PORT = 8765
URL = f"http://localhost:{PORT}"


def base_dir():
    # PyInstaller extrait les données dans sys._MEIPASS
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def extend_path():
    # ffmpeg / node installés par winget ne sont pas toujours dans le PATH hérité
    local = os.environ.get("LOCALAPPDATA", "")
    extra = [
        os.path.join(local, "Microsoft", "WinGet", "Links"),
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "nodejs"),
    ]
    winget_pkgs = os.path.join(local, "Microsoft", "WinGet", "Packages")
    if os.path.isdir(winget_pkgs):
        for pkg in os.listdir(winget_pkgs):
            if pkg.startswith("Gyan.FFmpeg"):
                for root, dirs, files in os.walk(os.path.join(winget_pkgs, pkg)):
                    if "ffmpeg.exe" in files:
                        extra.append(root)
                        break
    os.environ["PATH"] = os.pathsep.join([os.environ.get("PATH", "")] + [p for p in extra if os.path.isdir(p)])


def main():
    if port_in_use(PORT):
        # Déjà lancé : on rouvre simplement l'onglet
        webbrowser.open(URL)
        return

    extend_path()
    print("VidDrop est lancé sur", URL)
    print("Ferme cette fenêtre pour quitter VidDrop.\n")

    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit", "run", os.path.join(base_dir(), "app.py"),
        "--global.developmentMode=false",
        "--server.port", str(PORT),
        "--server.address", "localhost",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
