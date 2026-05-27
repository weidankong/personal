import os
import asyncio

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from appworld import AppWorld
import world as _world_mod

from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.tool import Toolkit
from agentscope.message import Msg
from codeact_env import CodeActEnv
from instructions import CODEACT_SYSTEM_PROMPT

# Import all AppWorld tools
from api_docs_show_app_descriptions import show_app_descriptions, AppDescriptionsOutput
from api_docs_show_api_descriptions import show_api_descriptions, ApiDescriptionsOutput
from api_docs_show_api_doc import show_api_doc, ApiDocOutput
from show_account_passwords import show_account_passwords, AccountPasswordsOutput
from spotify_login import spotify_login, SpotifyLoginOutput
from spotify_show_playlist_library import show_playlist_library, PlaylistLibraryOutput
from spotify_show_song import show_song, SongOutput
from spotify_show_liked_songs import show_liked_songs, LikedSongsOutput
from spotify_search_songs import search_songs, SearchSongsOutput
from spotify_search_artists import search_artists, SearchArtistsOutput
from spotify_follow_artist import follow_artist, FollowArtistOutput
from spotify_show_playlist import show_playlist, PlaylistOutput
from spotify_add_song_to_playlist import add_song_to_playlist, MessageOutput as AddSongOutput
from spotify_remove_song_from_playlist import remove_song_from_playlist, MessageOutput as RemoveSongOutput
from spotify_review_song import review_song, ReviewSongOutput
from spotify_update_song_review import update_song_review, UpdateSongReviewOutput
from spotify_show_song_review import show_song_review, SongReviewOutput
from spotify_show_song_reviews import show_song_reviews, SongReviewsOutput
from spotify_delete_song_review import delete_song_review, DeleteSongReviewOutput
from phone_login import phone_login, PhoneLoginOutput
from phone_search_text_messages import search_text_messages, TextMessagesOutput
from phone_get_current_date_and_time import get_current_date_and_time, DateTimeOutput
from spotify_show_song_library import show_song_library, SongLibraryOutput
from spotify_show_album_library import show_album_library, AlbumLibraryOutput
from spotify_show_recommendations import show_recommendations, RecommendationsOutput
from spotify_signup import signup, SignupOutput
from spotify_logout import logout, LogoutOutput
from spotify_show_profile import show_profile as spotify_show_profile, SpotifyProfileOutput
from spotify_show_account import show_account, SpotifyAccountOutput
from spotify_update_account_name import update_account_name, UpdateAccountNameOutput
from spotify_search_users import search_users, SearchUsersOutput
from spotify_show_genres import show_genres, GenresOutput
from spotify_show_song_privates import show_song_privates, SongPrivatesOutput
from spotify_like_song import like_song, LikeSongOutput
from spotify_unlike_song import unlike_song, UnlikeSongOutput
from spotify_search_albums import search_albums, SearchAlbumsOutput
from spotify_show_album import show_album, AlbumOutput
from spotify_show_album_privates import show_album_privates, AlbumPrivatesOutput
from spotify_like_album import like_album, LikeAlbumOutput
from spotify_unlike_album import unlike_album, UnlikeAlbumOutput
from spotify_show_liked_albums import show_liked_albums, LikedAlbumsOutput
from spotify_search_playlists import search_playlists, SearchPlaylistsOutput
from spotify_show_playlist_privates import show_playlist_privates, PlaylistPrivatesOutput
from spotify_create_playlist import create_playlist, CreatePlaylistOutput
from spotify_update_playlist import update_playlist, UpdatePlaylistOutput
from spotify_delete_playlist import delete_playlist, DeletePlaylistOutput
from spotify_like_playlist import like_playlist, LikePlaylistOutput
from spotify_unlike_playlist import unlike_playlist, UnlikePlaylistOutput
from spotify_show_liked_playlists import show_liked_playlists, LikedPlaylistsOutput
from spotify_show_artist import show_artist, ArtistOutput
from spotify_show_artist_following import show_artist_following, ArtistFollowingOutput
from spotify_add_song_to_library import add_song_to_library, AddSongToLibraryOutput
from spotify_remove_song_from_library import remove_song_from_library, RemoveSongFromLibraryOutput
from spotify_add_album_to_library import add_album_to_library, AddAlbumToLibraryOutput
from spotify_remove_album_from_library import remove_album_from_library, RemoveAlbumFromLibraryOutput
from spotify_show_downloaded_songs import show_downloaded_songs, DownloadedSongsOutput
from spotify_download_song import download_song, DownloadSongOutput
from spotify_remove_downloaded_song import remove_downloaded_song, RemoveDownloadedSongOutput
from spotify_show_following_artists import show_following_artists, FollowingArtistsOutput
from spotify_unfollow_artist import unfollow_artist, UnfollowArtistOutput
from spotify_show_album_reviews import show_album_reviews, AlbumReviewsOutput
from spotify_review_album import review_album, ReviewAlbumOutput
from spotify_update_album_review import update_album_review, UpdateAlbumReviewOutput
from spotify_delete_album_review import delete_album_review, DeleteAlbumReviewOutput
from spotify_show_album_review import show_album_review, AlbumReviewOutput
from spotify_show_playlist_reviews import show_playlist_reviews, PlaylistReviewsOutput
from spotify_review_playlist import review_playlist, ReviewPlaylistOutput
from spotify_update_playlist_review import update_playlist_review, UpdatePlaylistReviewOutput
from spotify_delete_playlist_review import delete_playlist_review, DeletePlaylistReviewOutput
from spotify_show_playlist_review import show_playlist_review, PlaylistReviewOutput
from spotify_show_payment_cards import show_payment_cards, PaymentCardsOutput
from spotify_show_payment_card import show_payment_card, PaymentCardOutput
from spotify_add_payment_card import add_payment_card, AddPaymentCardOutput
from spotify_update_payment_card import update_payment_card, UpdatePaymentCardOutput
from spotify_delete_payment_card import delete_payment_card, DeletePaymentCardOutput
from spotify_show_current_song import show_current_song, CurrentSongOutput
from spotify_play_music import play_music, PlayMusicOutput
from spotify_pause_music import pause_music, PauseMusicOutput
from spotify_previous_song import previous_song, PreviousSongOutput
from spotify_next_song import next_song, NextSongOutput
from spotify_move_song_in_queue import move_song_in_queue, MoveSongInQueueOutput
from spotify_seek_song import seek_song, SeekSongOutput
from spotify_loop_song import loop_song, LoopSongOutput
from spotify_shuffle_song_queue import shuffle_song_queue, ShuffleSongQueueOutput
from spotify_show_song_queue import show_song_queue, SongQueueOutput
from spotify_add_to_queue import add_to_queue, AddToQueueOutput
from spotify_remove_song_from_queue import remove_song_from_queue, RemoveSongFromQueueOutput
from spotify_clear_song_queue import clear_song_queue, ClearSongQueueOutput
from spotify_show_volume import show_volume, VolumeOutput
from spotify_set_volume import set_volume, SetVolumeOutput
from spotify_show_premium_plans import show_premium_plans
from spotify_subscribe_premium import subscribe_premium, SubscribePremiumOutput
from spotify_show_premium_subscriptions import show_premium_subscriptions, PremiumSubscriptionsOutput
from spotify_download_premium_subscription_receipt import download_premium_subscription_receipt, DownloadReceiptOutput
from supervisor_complete_task import complete_task, CompleteTaskOutput
from supervisor_show_profile import show_profile, SupervisorProfileOutput

_TASK_PROMPT = """
USER:
I am your supervisor and you are a super intelligent AI Assistant whose job is to achieve my day-to-day tasks completely autonomously.

To do this, you will need to interact with app/s (e.g., spotify, venmo, etc) using their associated APIs on my behalf. For this you will undertake a *multi-step conversation* using a python REPL environment. That is, you will write the python code and the environment will execute it and show you the result, based on which, you will write python code for the next step and so on, until you've achieved the goal. This environment will let you interact with app/s using their associated APIs on my behalf.

Here are three key APIs that you need to know to get more information

# To get a list of apps that are available to you.
print(show_app_descriptions())

# To get the list of apis under any app listed above, e.g. supervisor
print(show_api_descriptions(app_name='supervisor'))

# To get the specification of a particular api, e.g. supervisor app's show_account_passwords
print(show_api_doc(app_name='supervisor', api_name='show_account_passwords'))

Each code execution will produce an output that you can use in subsequent calls. Using these APIs, you can now generate code, that the environment will execute, to solve the task.

For example, consider the task:

My name is: Jane Doe. My personal email is jane@example.com and phone number is 555-1234.

Task:

What is the password for my Spotify account?

ASSISTANT:
{
    "type": "tool_use",
    "id": "call_07fb51ebe2934bd2933791",
    "name": "run_python_code",
    "input": {
        "code": "# Obtain the supervisor's Spotify account details\npasswords = call_tool('show_account_passwords')\n# So the Spotify password is the entry with account_name=\"spotify\".\n
        spotify_password = [p for p in passwords if p[\"account_name\"] == \"spotify\"][0][\"password\"]"\nprint(spotify_password)\n"
    }
}

USER:
Marked the active task complete.

----------------------------------------------

USER:
**Key instructions and disclaimers**:

1. The email addresses, access tokens and variables in the example above were only for demonstration. Obtain the correct information by calling relevant APIs yourself.
2. Only generate valid code blocks, i.e., do not put them in ```...``` or add any extra formatting. Any thoughts should be put as code comments.
3. You can use the variables from the previous code blocks in the subsequent code blocks.
4. Write small chunks of code and only one chunk of code in every step. Make sure everything is working correctly before making any irreversible change.
5. The provided Python environment has access to its standard library. But modules and functions that have a risk of affecting the underlying OS, file system or process are disabled.
6. Any reference to a file system in the task instructions means the file system *app*, operable via given APIs, and not the actual file system the code is running on.
7. To interact with apps, only use the provided APIs, and not the corresponding Python packages. E.g., do NOT use `spotipy` for Spotify.
8. The provided API documentation has both the input arguments and the output JSON schemas. All calls to APIs and parsing its outputs must be as per this documentation.
9. For APIs that return results in "pages", make sure to consider all pages.
10. To obtain current date or time, use Python functions like `datetime.now()` or obtain it from the phone app. Do not rely on your existing knowledge of what the current date or time is.
11. For all temporal requests, use proper time boundaries, e.g., if I ask for something that happened yesterday, make sure to consider the time between 00:00:00 and 23:59:59.
12. Any reference to friends, family or any other person or relation refers to the people in the phone's contacts list.
13. All personal information, and information about app account credentials, physical addresses and owned payment cards are stored in the "supervisor" app. Access them via the APIs provided by the supervisor app.
14. Once you have completed the task, call `complete_task()`. If the task asks for some information, return it as the answer argument, i.e. call `complete_task(answer=<answer>)`. For tasks that do not require an answer, just skip the answer argument or pass it as None.
15. The answers, when given, should be just entity or number, not full sentences, e.g., `answer=10` for "How many songs are in the Spotify queue?". When an answer is a number, it should be in numbers, not in words, e.g., "10" and not "ten".
16. You can also pass `status="fail"` in the complete_task API if you are sure you cannot solve it and want to exit.
17. You must make all decisions completely autonomously and not ask for any clarifications or confirmations.

for Spotify use lower case spotify
Now, call `run_python_code` tool with your code to solve the actual task:

__INSTRUCTION__

In case of tool_call_error, read the failed API's schema AGAIN.
"""

_TASK_PROMPT = """
USER:
I am your supervisor and you are a super intelligent AI Assistant whose job is to achieve my day-to-day tasks completely autonomously.

To do this, you will need to interact with app/s (e.g., spotify, venmo, etc) using their associated APIs on my behalf. For this you will undertake a *multi-step conversation* using a python REPL environment. That is, you will write the python code and the environment will execute it and show you the result, based on which, you will write python code for the next step and so on, until you've achieved the goal. This environment will let you interact with app/s using their associated APIs on my behalf.

Here are three key APIs that you need to know to get more information

# To get a list of apps that are available to you.
print(show_app_descriptions())

# To get the list of apis under any app listed above, e.g. supervisor
print(show_api_descriptions(app_name='supervisor'))

# To get the specification of a particular api, e.g. supervisor app's show_account_passwords
print(show_api_doc(app_name='supervisor', api_name='show_account_passwords'))

Each code execution will produce an output that you can use in subsequent calls. Using these APIs, you can now generate code, that the environment will execute, to solve the task.

For example, consider the task:

My name is: Jane Doe. My personal email is jane@example.com and phone number is 555-1234.

Task:

What is the password for my Spotify account?

ASSISTANT:
{
    "type": "tool_use",
    "id": "call_07fb51ebe2934bd2933791",
    "name": "run_python_code",
    "input": {
        "code": "# Obtain the supervisor's Spotify account details\npasswords = call_tool('show_account_passwords')\n# So the Spotify password is the entry with account_name=\"spotify\".\n
        spotify_password = [p for p in passwords if p[\"account_name\"] == \"spotify\"][0][\"password\"]"\nprint(spotify_password)\n"
    }
}

USER:
Marked the active task complete.

----------------------------------------------

USER:
**Key instructions and disclaimers**:

1. The email addresses, access tokens and variables in the example above were only for demonstration. Obtain the correct information by calling relevant APIs yourself.
2. Only generate valid code blocks, i.e., do not put them in ```...``` or add any extra formatting. Any thoughts should be put as code comments.
3. You can use the variables from the previous code blocks in the subsequent code blocks.
4. Write small chunks of code and only one chunk of code in every step. Make sure everything is working correctly before making any irreversible change.
5. The provided Python environment has access to its standard library. But modules and functions that have a risk of affecting the underlying OS, file system or process are disabled.
6. Any reference to a file system in the task instructions means the file system *app*, operable via given APIs, and not the actual file system the code is running on.
7. To interact with apps, only use the provided APIs, and not the corresponding Python packages. E.g., do NOT use `spotipy` for Spotify.
8. The provided API documentation has both the input arguments and the output JSON schemas. All calls to APIs and parsing its outputs must be as per this documentation.
9. For APIs that return results in "pages", make sure to consider all pages.
10. To obtain current date or time, use Python functions like `datetime.now()` or obtain it from the phone app. Do not rely on your existing knowledge of what the current date or time is.
11. For all temporal requests, use proper time boundaries, e.g., if I ask for something that happened yesterday, make sure to consider the time between 00:00:00 and 23:59:59.
12. Any reference to friends, family or any other person or relation refers to the people in the phone's contacts list.
13. All personal information, and information about app account credentials, physical addresses and owned payment cards are stored in the "supervisor" app. Access them via the APIs provided by the supervisor app.
14. Once you have completed the task, call `complete_task()`. If the task asks for some information, return it as the answer argument, i.e. call `complete_task(answer=<answer>)`. For tasks that do not require an answer, just skip the answer argument or pass it as None.
15. The answers, when given, should be just entity or number, not full sentences, e.g., `answer=10` for "How many songs are in the Spotify queue?". When an answer is a number, it should be in numbers, not in words, e.g., "10" and not "ten".
16. You can also pass `status="fail"` in the complete_task API if you are sure you cannot solve it and want to exit.
17. You must make all decisions completely autonomously and not ask for any clarifications or confirmations.

for Spotify use lower case spotify
Now, call `run_python_code` tool with your code to solve the actual task:

__INSTRUCTION__

In case of tool_call_error, read the failed API's schema AGAIN.
"""

async def run_one_case(task_id):
    # Create and inject the AppWorld instance

    codebox = CodeActEnv()

    # Register tools callable in the codebox
    codebox.register_callable_tool(show_account_passwords, output_model=AccountPasswordsOutput)
    codebox.register_callable_tool(spotify_login, output_model=SpotifyLoginOutput)
    codebox.register_callable_tool(show_playlist_library, output_model=PlaylistLibraryOutput)
    codebox.register_callable_tool(show_song, output_model=SongOutput)
    codebox.register_callable_tool(show_liked_songs, output_model=LikedSongsOutput)
    codebox.register_callable_tool(search_songs, output_model=SearchSongsOutput)
    codebox.register_callable_tool(search_artists, output_model=SearchArtistsOutput)
    codebox.register_callable_tool(follow_artist, output_model=FollowArtistOutput)
    codebox.register_callable_tool(show_playlist, output_model=PlaylistOutput)
    codebox.register_callable_tool(add_song_to_playlist, output_model=AddSongOutput)
    codebox.register_callable_tool(remove_song_from_playlist, output_model=RemoveSongOutput)
    codebox.register_callable_tool(review_song, output_model=ReviewSongOutput)
    codebox.register_callable_tool(update_song_review, output_model=UpdateSongReviewOutput)
    codebox.register_callable_tool(show_song_review, output_model=SongReviewOutput)
    codebox.register_callable_tool(show_song_reviews, output_model=SongReviewsOutput)
    codebox.register_callable_tool(delete_song_review, output_model=DeleteSongReviewOutput)
    codebox.register_callable_tool(phone_login, output_model=PhoneLoginOutput)
    codebox.register_callable_tool(search_text_messages, output_model=TextMessagesOutput)
    codebox.register_callable_tool(get_current_date_and_time, output_model=DateTimeOutput)
    codebox.register_callable_tool(show_song_library, output_model=SongLibraryOutput)
    codebox.register_callable_tool(show_album_library, output_model=AlbumLibraryOutput)
    codebox.register_callable_tool(show_recommendations, output_model=RecommendationsOutput)
    codebox.register_callable_tool(signup, output_model=SignupOutput)
    codebox.register_callable_tool(logout, output_model=LogoutOutput)
    codebox.register_callable_tool(spotify_show_profile, output_model=SpotifyProfileOutput)
    codebox.register_callable_tool(show_account, output_model=SpotifyAccountOutput)
    codebox.register_callable_tool(update_account_name, output_model=UpdateAccountNameOutput)
    codebox.register_callable_tool(search_users, output_model=SearchUsersOutput)
    codebox.register_callable_tool(show_genres, output_model=GenresOutput)
    codebox.register_callable_tool(show_song_privates, output_model=SongPrivatesOutput)
    codebox.register_callable_tool(like_song, output_model=LikeSongOutput)
    codebox.register_callable_tool(unlike_song, output_model=UnlikeSongOutput)
    codebox.register_callable_tool(search_albums, output_model=SearchAlbumsOutput)
    codebox.register_callable_tool(show_album, output_model=AlbumOutput)
    codebox.register_callable_tool(show_album_privates, output_model=AlbumPrivatesOutput)
    codebox.register_callable_tool(like_album, output_model=LikeAlbumOutput)
    codebox.register_callable_tool(unlike_album, output_model=UnlikeAlbumOutput)
    codebox.register_callable_tool(show_liked_albums, output_model=LikedAlbumsOutput)
    codebox.register_callable_tool(search_playlists, output_model=SearchPlaylistsOutput)
    codebox.register_callable_tool(show_playlist_privates, output_model=PlaylistPrivatesOutput)
    codebox.register_callable_tool(create_playlist, output_model=CreatePlaylistOutput)
    codebox.register_callable_tool(update_playlist, output_model=UpdatePlaylistOutput)
    codebox.register_callable_tool(delete_playlist, output_model=DeletePlaylistOutput)
    codebox.register_callable_tool(like_playlist, output_model=LikePlaylistOutput)
    codebox.register_callable_tool(unlike_playlist, output_model=UnlikePlaylistOutput)
    codebox.register_callable_tool(show_liked_playlists, output_model=LikedPlaylistsOutput)
    codebox.register_callable_tool(show_artist, output_model=ArtistOutput)
    codebox.register_callable_tool(show_artist_following, output_model=ArtistFollowingOutput)
    codebox.register_callable_tool(add_song_to_library, output_model=AddSongToLibraryOutput)
    codebox.register_callable_tool(remove_song_from_library, output_model=RemoveSongFromLibraryOutput)
    codebox.register_callable_tool(add_album_to_library, output_model=AddAlbumToLibraryOutput)
    codebox.register_callable_tool(remove_album_from_library, output_model=RemoveAlbumFromLibraryOutput)
    codebox.register_callable_tool(show_downloaded_songs, output_model=DownloadedSongsOutput)
    codebox.register_callable_tool(download_song, output_model=DownloadSongOutput)
    codebox.register_callable_tool(remove_downloaded_song, output_model=RemoveDownloadedSongOutput)
    codebox.register_callable_tool(show_following_artists, output_model=FollowingArtistsOutput)
    codebox.register_callable_tool(unfollow_artist, output_model=UnfollowArtistOutput)
    codebox.register_callable_tool(show_album_reviews, output_model=AlbumReviewsOutput)
    codebox.register_callable_tool(review_album, output_model=ReviewAlbumOutput)
    codebox.register_callable_tool(update_album_review, output_model=UpdateAlbumReviewOutput)
    codebox.register_callable_tool(delete_album_review, output_model=DeleteAlbumReviewOutput)
    codebox.register_callable_tool(show_album_review, output_model=AlbumReviewOutput)
    codebox.register_callable_tool(show_playlist_reviews, output_model=PlaylistReviewsOutput)
    codebox.register_callable_tool(review_playlist, output_model=ReviewPlaylistOutput)
    codebox.register_callable_tool(update_playlist_review, output_model=UpdatePlaylistReviewOutput)
    codebox.register_callable_tool(delete_playlist_review, output_model=DeletePlaylistReviewOutput)
    codebox.register_callable_tool(show_playlist_review, output_model=PlaylistReviewOutput)
    codebox.register_callable_tool(show_payment_cards, output_model=PaymentCardsOutput)
    codebox.register_callable_tool(show_payment_card, output_model=PaymentCardOutput)
    codebox.register_callable_tool(add_payment_card, output_model=AddPaymentCardOutput)
    codebox.register_callable_tool(update_payment_card, output_model=UpdatePaymentCardOutput)
    codebox.register_callable_tool(delete_payment_card, output_model=DeletePaymentCardOutput)
    codebox.register_callable_tool(show_current_song, output_model=CurrentSongOutput)
    codebox.register_callable_tool(play_music, output_model=PlayMusicOutput)
    codebox.register_callable_tool(pause_music, output_model=PauseMusicOutput)
    codebox.register_callable_tool(previous_song, output_model=PreviousSongOutput)
    codebox.register_callable_tool(next_song, output_model=NextSongOutput)
    codebox.register_callable_tool(move_song_in_queue, output_model=MoveSongInQueueOutput)
    codebox.register_callable_tool(seek_song, output_model=SeekSongOutput)
    codebox.register_callable_tool(loop_song, output_model=LoopSongOutput)
    codebox.register_callable_tool(shuffle_song_queue, output_model=ShuffleSongQueueOutput)
    codebox.register_callable_tool(show_song_queue, output_model=SongQueueOutput)
    codebox.register_callable_tool(add_to_queue, output_model=AddToQueueOutput)
    codebox.register_callable_tool(remove_song_from_queue, output_model=RemoveSongFromQueueOutput)
    codebox.register_callable_tool(clear_song_queue, output_model=ClearSongQueueOutput)
    codebox.register_callable_tool(show_volume, output_model=VolumeOutput)
    codebox.register_callable_tool(set_volume, output_model=SetVolumeOutput)
    codebox.register_callable_tool(show_premium_plans)
    codebox.register_callable_tool(subscribe_premium, output_model=SubscribePremiumOutput)
    codebox.register_callable_tool(show_premium_subscriptions, output_model=PremiumSubscriptionsOutput)
    codebox.register_callable_tool(download_premium_subscription_receipt, output_model=DownloadReceiptOutput)
    codebox.register_callable_tool(show_profile, output_model=SupervisorProfileOutput)
    codebox.register_callable_tool(complete_task, output_model=CompleteTaskOutput)

    # Start sandbox + tool server + inject proxies
    await codebox.start()
    _world_mod.world = AppWorld(task_id=task_id, experiment_name="codeact_test")

    try:
        toolkit = Toolkit()

        # Register code execution tools (from sandbox)
        toolkit.register_tool_function(
            codebox.run_python_code,
            func_description=codebox.run_python_code_description,
        )
        print(codebox.run_python_code_description)

        # Register host tools directly (agent can call them without sandbox)
        # toolkit.register_tool_function(show_app_descriptions)
        # toolkit.register_tool_function(show_api_descriptions)
        # toolkit.register_tool_function(show_api_doc)

        agent = ReActAgent(
            name="Friday",
            sys_prompt=CODEACT_SYSTEM_PROMPT,
            model=DashScopeChatModel(
                model_name="qwen-max",
                api_key=os.environ["DASHSCOPE_API_KEY"],
                stream=True,
            ),
            memory=InMemoryMemory(),
            formatter=DashScopeChatFormatter(),
            toolkit=toolkit,
        )

        world = _world_mod.world

        print(f"\n{'='*60}")
        print(f"Task ID: {task_id}")
        sup = world.task.supervisor
        print(f"Supervisor: {sup}")
        print(f"Instruction: {world.task.instruction}")
        print(f"{'='*60}\n")

        msg = Msg(
            name="user",
            content=_TASK_PROMPT.replace("__INSTRUCTION__", world.task.instruction),
            role="user",
        )
        msg.content += f"\nMy name is: {sup['first_name']} {sup['last_name']}. My personal email is {sup['email']} and phone number is {sup['phone_number']}."
        while True:
            msg = await agent(msg)
            if world.task_completed():
                print("\nTask completed!")
                break
            # msg = Msg(name="user", content="continue", role="user")
            break

        report = world.evaluate().report()
        print(f"\n--- Evaluation Report ---")
        print(report)

    finally:
        await codebox.stop()
        _world_mod.world.close()

async def main():
    cases = read_cases()
    await run_one_case(task_id='287e338_2')
    # for case in cases:
    #     await run_one_case(task_id=case)

def read_cases():
    cases_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cases.txt")
    cases = []
    with open(cases_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(line)
    return cases

asyncio.run(main())
