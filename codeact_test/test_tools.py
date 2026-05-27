"""Test all tool functions with task_id: 82e2fac_1."""

import sys
import os
import json

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure appworld src is on the path
PROJECT_ROOT = os.path.dirname(TOOL_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

# Ensure codeact_test is on the path so tool imports work
sys.path.insert(0, TOOL_DIR)

from appworld import AppWorld

# Create world instance
_world_instance = AppWorld(task_id="82e2fac_1", experiment_name="tool_test")

# Inject into world module before any tool is imported
import world as _w  # noqa: E402
_w.world = _world_instance

# Import tools (they will see the injected world)
from api_docs_show_app_descriptions import show_app_descriptions
from api_docs_show_api_descriptions import show_api_descriptions
from api_docs_show_api_doc import show_api_doc
from show_account_passwords import show_account_passwords
from spotify_login import login
from spotify_show_playlist_library import show_playlist_library
from spotify_show_song import show_song
from supervisor_complete_task import complete_task


def get_text(r):
    """Extract text string from ToolResponse content."""
    c = r.content[0]
    if isinstance(c, dict):
        return c.get("text", str(c))
    return c.text


def test_all():
    # 1. show_app_descriptions
    print("\n>>> 1. show_app_descriptions()")
    r = show_app_descriptions()
    print(get_text(r)[:500])

    # 2. show_api_descriptions (spotify)
    print("\n>>> 2. show_api_descriptions('spotify')")
    r = show_api_descriptions(app_name="spotify")
    print(get_text(r)[:500])

    # 3. show_api_doc (spotify.login)
    print("\n>>> 3. show_api_doc('spotify', 'login')")
    r = show_api_doc(app_name="spotify", api_name="login")
    print(get_text(r)[:500])

    # 4. show_account_passwords
    print("\n>>> 4. show_account_passwords()")
    r = show_account_passwords()
    print(get_text(r)[:500])

    # Parse passwords for step 5
    passwords = json.loads(get_text(r))
    spotify_pw = [p["password"] for p in passwords if p["account_name"] == "spotify"][0]

    # 5. spotify.login
    sup = _world_instance.task.supervisor
    print(f"\n>>> 5. login(username={sup['email']!r}, password=***)")
    r = login(username=sup["email"], password=spotify_pw)
    print(get_text(r)[:500])

    # Parse access_token for step 6
    token = json.loads(get_text(r))["access_token"]

    # 6. show_playlist_library
    print(f"\n>>> 6. show_playlist_library(access_token={token[:20]}...)")
    r = show_playlist_library(access_token=token)
    print(get_text(r)[:500])

    # Parse first song_id for step 7
    playlists = json.loads(get_text(r))
    song_id = playlists[0]["song_ids"][0]

    # 7. show_song
    print(f"\n>>> 7. show_song(song_id={song_id})")
    r = show_song(song_id=song_id)
    print(get_text(r)[:500])

    # 8. complete_task
    print("\n>>> 8. complete_task()")
    r = complete_task()
    print(get_text(r)[:200])

    print("\n\nAll 8 tools tested successfully!")


if __name__ == "__main__":
    try:
        test_all()
    finally:
        _world_instance.close()
