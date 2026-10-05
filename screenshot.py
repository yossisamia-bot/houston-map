r"""Clean client-ready screenshot of the Houston communities map.

Usage:
    python screenshot.py                 -> screenshots\houston-communities-<date>.png
    python screenshot.py --out X.png     -> custom output path
    python screenshot.py --size 1600x1000

Hides search bar, control buttons, hint, zoom and resources button; renders
index.html headless in Chrome (1600x1000 default) with network tiles.
Nothing is changed in index.html - a temporary copy with extra CSS is used.
"""
import argparse, datetime, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
HIDE = ("<style>.map-controls,.search-container,#searchResults,#welcomeHint,"
        "#svBtn,#resources-btn,.leaflet-control-zoom{display:none!important}</style>")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--size", default="1600x1000")
    a = ap.parse_args()
    out = a.out or os.path.join(HERE, "screenshots",
          f"houston-communities-{datetime.date.today():%Y-%m-%d}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    exe = next((c for c in CHROME if os.path.exists(c)), None)
    if not exe:
        sys.exit("Chrome/Edge not found")
    src = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "clean.html")
    open(page, "w", encoding="utf-8").write(src.replace("</head>", HIDE + "</head>", 1))
    subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={a.size.replace('x', ',')}",
                    "--virtual-time-budget=20000", f"--screenshot={out}",
                    "file:///" + page.replace("\\", "/")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    shutil.rmtree(tmp, ignore_errors=True)
    if not os.path.exists(out) or os.path.getsize(out) < 100_000:
        sys.exit("screenshot failed (tiles not loaded?) - rerun")
    print(out)

if __name__ == "__main__":
    main()
