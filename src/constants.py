from pathlib import Path


BASE_URL = "https://aliexpress.com/"
DOWNLOAD_PATH = Path().home() / "Downloads"
if not DOWNLOAD_PATH.exists():
    DOWNLOAD_PATH = Path().home() / "Documents"
if not DOWNLOAD_PATH.exists():
    DOWNLOAD_PATH = Path(__file__).parent
