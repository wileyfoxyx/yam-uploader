# Yandex Music Uploader

A simple Tkinter-based GUI app to upload a local audio file to one of your Yandex Music playlists. Mostly usable as a workaround for uploading tracks to "My Favorites" playlist (since the ability to do so was removed with Yandex Music's new web UI), but it can upload tracks to any of your playlists.

## Downloads

Prebuilt binaries are available via GitHub Actions artifacts:

- Windows: YandexMusicUploader.exe
- macOS: YandexMusicUploader.app (zipped)
- Linux: YandexMusicUploader (ELF binary)

## Requirements

- Python 3.9+
- Windows, macOS, or Linux

## Setup

1. Create & activate a virtual environment (recommended).
2. Install dependencies. Below is the example for Windows:

```powershell
pip install -r requirements.txt
```

3. Run:

```powershell
python -m app
```

On first run you'll be prompted to enter your Yandex Music access token. You can learn how to obtain it [here](https://yandex-music.readthedocs.io/en/main/token.html).

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

