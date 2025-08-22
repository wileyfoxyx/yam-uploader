from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from typing import Optional

from app.token_store import get_token, set_token
from app.yandex_api import YandexApi

APP_TITLE = "Yandex Music Uploader"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("480x220")
        self.resizable(False, False)

        self.token: Optional[str] = None
        self.api: Optional[YandexApi] = None

        # UI elements
        self.token_label_var = tk.StringVar()
        self.playlist_var = tk.StringVar()
        self.file_path_var = tk.StringVar()

        self._build_ui()
        self._ensure_token()
        self._load_playlists()

    def _build_ui(self) -> None:
        padx = 8
        pady = 6

        # Token row
        frm_token = ttk.Frame(self)
        frm_token.pack(fill="x", padx=padx, pady=pady)
        ttk.Label(frm_token, text="Access token:").pack(side="left")
        ttk.Label(frm_token, textvariable=self.token_label_var, width=28).pack(side="left", padx=6)
        ttk.Button(frm_token, text="Change", command=self._change_token).pack(side="right")

        # Playlist row
        frm_pl = ttk.Frame(self)
        frm_pl.pack(fill="x", padx=padx, pady=pady)
        ttk.Label(frm_pl, text="Playlist:").pack(side="left")
        self.playlist_combo = ttk.Combobox(frm_pl, textvariable=self.playlist_var, state="readonly", width=34)
        self.playlist_combo.pack(side="left", padx=6, fill="x", expand=True)
        ttk.Button(frm_pl, text="Refresh", command=self._load_playlists).pack(side="right")

        # File row
        frm_file = ttk.Frame(self)
        frm_file.pack(fill="x", padx=padx, pady=pady)
        ttk.Label(frm_file, text="File:").pack(side="left")
        ttk.Entry(frm_file, textvariable=self.file_path_var, width=34).pack(side="left", padx=6, fill="x", expand=True)
        ttk.Button(frm_file, text="Browse", command=self._browse_file).pack(side="right")

        # Upload row
        frm_actions = ttk.Frame(self)
        frm_actions.pack(fill="x", padx=padx, pady=pady)
        self.upload_btn = ttk.Button(frm_actions, text="Upload", command=self._upload)
        self.upload_btn.pack(side="right")

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var).pack(anchor="w", padx=10, pady=(6, 10))

    def _ensure_token(self) -> None:
        token = get_token()
        if not token:
            token = simpledialog.askstring(APP_TITLE, "Enter Yandex Music access token:", show='*')
            if not token:
                messagebox.showerror(APP_TITLE, "Access token is required to continue.")
                self.destroy()
                return
            set_token(token)
        self.token = token
        self.token_label_var.set("••••••••" if token else "—")
        self.api = YandexApi(token)

    def _change_token(self) -> None:
        token = simpledialog.askstring(APP_TITLE, "Enter new access token:", show='*')
        if token:
            set_token(token)
            self.token = token
            self.token_label_var.set("••••••••")
            self.api = YandexApi(token)
            self._load_playlists()

    def _load_playlists(self) -> None:
        if not self.api:
            return
        try:
            self.status_var.set("Loading playlists…")
            self.update_idletasks()
            playlists = self.api.get_playlists()
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Failed to load playlists:\n{e}")
            self.status_var.set("Failed to load playlists")
            return
        titles = [title for title, _ in playlists]
        self.playlist_combo["values"] = titles
        if titles:
            self.playlist_combo.current(0)
        self._playlists_cache = playlists
        self.status_var.set("Playlists loaded")

    def _browse_file(self) -> None:
        filetypes = [
            ("Audio files", ".mp3 .flac .wav .ogg .m4a .aac"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(title="Select audio file", filetypes=filetypes)
        if path:
            self.file_path_var.set(path)

    def _upload(self) -> None:
        if not self.api:
            messagebox.showerror(APP_TITLE, "No API client.")
            return
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning(APP_TITLE, "Please choose an existing file.")
            return
        if not getattr(self, "_playlists_cache", None):
            messagebox.showwarning(APP_TITLE, "Please load playlists first.")
            return
        sel = self.playlist_combo.current()
        if sel < 0:
            messagebox.showwarning(APP_TITLE, "Please select a playlist.")
            return
        title, kind = self._playlists_cache[sel]

        self.upload_btn.config(state="disabled")
        self.status_var.set(f"Uploading to '{title}'…")
        self.update_idletasks()
        error_detail = None
        try:
            ok = self.api.upload_track(file_path, kind)
        except Exception as e:
            ok = False
            error_detail = str(e)
        finally:
            self.upload_btn.config(state="normal")
        if ok:
            messagebox.showinfo(APP_TITLE, "Upload succeeded!")
            self.status_var.set("Done")
        else:
            self.status_var.set("Failed")
            if error_detail:
                messagebox.showerror(APP_TITLE, f"Upload failed:\n{error_detail}")
            else:
                messagebox.showerror(APP_TITLE, "Upload failed.")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
