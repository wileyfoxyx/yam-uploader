from __future__ import annotations
from typing import List, Tuple
from yandex_music import Client
import urllib.parse
import os
import socket


class YandexApi:
    def __init__(self, token: str) -> None:
        self.client = Client(token).init()

    def get_playlists(self) -> List[Tuple[str, str]]:
        """
        Returns list of (title, kind) for user's playlists.
        """
        playlists: List[Tuple[str, str]] = []
        # Fetch user playlists via client.users_playlists_list()
        try:
            user_playlists = self.client.users_playlists_list()
        except Exception:
            user_playlists = []
        for p in user_playlists:
            title = getattr(p, "title", None) or f"Playlist {getattr(p, 'kind', '')}"
            kind = str(getattr(p, "kind", ""))
            if kind:
                playlists.append((title, kind))
        # Ensure 'Мне нравится' (Liked) with kind '3' is present at the top
        has_likes = any(k == "3" for _, k in playlists)
        likes_entry = ("Мне нравится", "3")
        if has_likes:
            # Move it to the top
            playlists = [e for e in playlists if e[1] != "3"]
            playlists.insert(0, likes_entry)
        else:
            playlists.insert(0, likes_entry)
        return playlists

    def upload_track(self, file_path: str, playlist_kind: str) -> bool:
        # Reuse the logic from user's snippet, adjusted for windows paths
        file_basename = os.path.basename(file_path)
        file_name = urllib.parse.quote(file_path, safe='_!() ')
        file_name = file_name.replace(" ", "+")

        params = {
            "filename": file_name,
            "kind": playlist_kind,
            "visibility": "private",
            "lang": "ru",
            "external-domain": "music.yandex.ru",
            "overembed": "false",
        }

        try:
            upload_data = self.client.request.get(
                url="https://music.yandex.ru/handlers/ugc-upload.jsx",
                params=params,
                timeout=60,
            )
        except Exception as e:
            raise RuntimeError("Failed to get upload URL") from e
        # upload_data is expected to be a dict with 'post_target'
        if isinstance(upload_data, dict):
            post_target = upload_data.get("post_target", "")
        else:
            post_target = ""
        upload_url = str(post_target).replace(":443", "", 1)
        if not upload_url:
            raise RuntimeError("Upload URL is empty")

        # Stream file; retry once on timeout
        last_err: Exception | None = None
        for attempt in range(2):
            try:
                with open(file_path, mode="rb") as f:
                    files = {"file": (file_basename, f, "application/octet-stream")}
                    upload = self.client.request.post(
                        url=upload_url,
                        files=files,
                        timeout=300,
                    )
                if upload == "CREATED":
                    return True
                raise RuntimeError(f"Unexpected response: {upload}")
            except (TimeoutError, socket.timeout) as e:
                last_err = e
                if attempt == 0:
                    continue
                raise
            except Exception as e:
                # Non-timeout error; don't retry
                raise

        # Should not reach here
        if last_err is not None:
            raise last_err
        return False
