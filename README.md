# Yandex Music Uploader GUI

A simple Tkinter-based GUI to upload a local audio file to one of your Yandex Music playlists.

Features:

- Asks for access token on first run and stores it securely in your OS keyring.
- Fetches and lists your playlists for easy selection.
- Pick a local audio file and upload it to the selected playlist.

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

## Notes

- The app uses only official endpoints exposed via the `yandex-music` library to read playlists; the file upload uses the handler shown in your snippet.
- Token is stored in system keyring under service `yandex-music` and username `access-token`.
