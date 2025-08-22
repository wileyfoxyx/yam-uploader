# Yandex Music Uploader GUI

A simple Tkinter-based GUI to upload a local audio file to one of your Yandex Music playlists.

Features:

- Asks for access token on first run and stores it securely in your OS keyring.
- Fetches and lists your playlists for easy selection.
- Pick a local audio file and upload it to the selected playlist.

## Downloads (prebuilt)

Prebuilt binaries are available via GitHub Actions artifacts:

- Windows: YandexMusicUploader.exe
- macOS: YandexMusicUploader.app (zipped)
- Linux: YandexMusicUploader (ELF binary)

Open the Actions tab, select the latest "build" workflow run, and download the artifacts for your OS.

## Requirements

- Python 3.9+
- Windows, macOS, or Linux

## Setup

1. Create & activate a virtual environment (recommended).
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python -m app
```

On first run you'll be prompted to enter your Yandex Music access token. You can obtain an OAuth token as documented by the `yandex-music` library or via Yandex.

## Build from source

The app is pure Python; you can run it with `python -m app` as above, or package distributables with PyInstaller.

### Windows (.exe)

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
python -m PyInstaller --name YandexMusicUploader --windowed --onefile app\__main__.py
```

The executable will appear in `dist/YandexMusicUploader.exe`.

### macOS (.app bundle)

```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt pyinstaller
python3 -m PyInstaller --name YandexMusicUploader --windowed --onefile --osx-bundle-identifier io.github.yandexmusic.uploader app/__main__.py
```

The bundle will appear in `dist/YandexMusicUploader.app`. If Gatekeeper blocks it:

```bash
xattr -dr com.apple.quarantine dist/YandexMusicUploader.app
open dist/YandexMusicUploader.app
```

### Linux (onefile)

```bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt pyinstaller
python3 -m PyInstaller --name YandexMusicUploader --onefile app/__main__.py
```

The binary will appear in `dist/YandexMusicUploader`. Make it executable: `chmod +x dist/YandexMusicUploader`.

## Notes

- The app uses only official endpoints exposed via the `yandex-music` library to read playlists; the file upload uses the handler shown in your snippet.
- For packaged builds, token is stored in system keyring under service `yandex-music-release-1` (to avoid reusing dev tokens). You can override with env var `YM_KEYRING_SERVICE`.
