#!/usr/bin/env python3
from pathlib import Path
from threading import Event
import os
import time

from vlc import MediaList, MediaListPlayer, EventType

MEDIA_SUFFIXES = {".mp4", ".avi", ".mkv", ".mov", ".png", ".jpg"}



def get_arbitrary_mount_path(media_path):
    try:
        return next(path for path in media_path.iterdir() if path.is_mount())
    except StopIteration:
        raise FileNotFoundError("no mount path found") from None


def check_device_mount():
    return bool(os.listdir('/media/spinoza'))



def main():
    media_path = Path("/media/spinoza")
    while True:
        if check_device_mount():
            try:
                mount_path = get_arbitrary_mount_path(media_path)
                mount_path = Path("/media/spinoza", mount_path)
            except FileNotFoundError:
                print(f"No mount path found under {media_path}")
            else:
                print("Video directory:", mount_path)

                playing_stopped = Event()
                media_files = sorted(
                    [
                        str(path)
                        for path in mount_path.iterdir()
                        if path.is_file() and path.suffix.lower() in MEDIA_SUFFIXES
                    ]
                )
                media_list = MediaList(media_files)
                media_list_player = MediaListPlayer()
                media_list_player.set_media_list(media_list)
                media_list_player.set_playback_mode(1)  # loop mode

                player = media_list_player.get_media_player()
                player.set_fullscreen(True)
                media_list_player.event_manager().event_attach(
                    EventType.MediaListPlayerStopped,
                    lambda _event: playing_stopped.set(),
                )
                media_list_player.play()

                playing_stopped.wait()
        else:
            print("No USB device connected.")
            time.sleep(1)  # Wait for USB device to be connected



if __name__ == "__main__":
    main()
