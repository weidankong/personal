# API / Tool Reference

All tools and APIs used by the AppWorld agent, including function signatures, descriptions, and JSON schemas.

---

## 1. apis.api_docs.show_api_descriptions

**App:** `api_docs`
**Description:** List all available API endpoints under a specific app.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "app_name": { "type": "string", "description": "Name of the app, e.g. 'spotify', 'supervisor', 'venmo'" },
    "access_token": { "type": "string", "description": "Access token (required for some apps)" }
  },
  "required": ["app_name"]
}
```

### Output Schema

**Success** — array of objects:

```json
[
  { "name": "show_account", "description": "Show your account information..." },
  { "name": "login",        "description": "Login to your account." },
  ...
]
```

**Failure** — single object:

```json
{ "message": "string" }
```

---

## 2. apis.api_docs.show_app_descriptions

**App:** `api_docs`
**Description:** Show descriptions of all available apps.

### Input Schema

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

### Output Schema

**Success** — array of objects:

```json
[
  { "name": "api_docs",  "description": "An app to search and explore API documentation." },
  { "name": "supervisor", "description": "An app to access supervisor's personal information..." },
  { "name": "spotify",   "description": "A music streaming app to stream songs..." },
  ...
]
```

---

## 3. apis.api_docs.show_api_doc

**App:** `api_docs`
**Description:** Get the full specification (parameters, response schema, HTTP method) of a single API.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "app_name": { "type": "string", "description": "Name of the app" },
    "api_name": { "type": "string", "description": "Name of the API" },
    "access_token": { "type": "string", "description": "Access token (required for some apps)" }
  },
  "required": ["app_name", "api_name"]
}
```

### Output Schema

**Success** — single object with full API spec:

```json
{
  "app_name": "spotify",
  "api_name": "show_playlist_library",
  "path": "/spotify/library/playlists",
  "method": "GET",
  "description": "Search or show a list of playlists in your playlist library.",
  "parameters": [
    { "name": "access_token", "type": "string", "required": true, "description": "...", "default": null, "constraints": [] },
    { "name": "query",        "type": "string", "required": false, "description": "...", "default": null, "constraints": [] }
  ],
  "response_schemas": {
    "success": { ... },
    "failure": { "message": "string" }
  }
}
```

---

## 4. apis.supervisor.show_account_passwords

**App:** `supervisor`
**Description:** Show all app account passwords stored in the supervisor app.

### Input Schema

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

### Output Schema

**Success** — array of credential objects:

```json
[
  { "account_name": "amazon",      "password": "FJRd9=B" },
  { "account_name": "spotify",     "password": "qge1k1L" },
  { "account_name": "file_system", "password": "DqE8={8" },
  ...
]
```

**Failure** — single object:

```json
{ "message": "string" }
```

---

## 5. apis.spotify.login

**App:** `spotify`
**Description:** Login to a Spotify account and obtain an access token.

### HTTP Details

- **Path:** `/spotify/auth/token`
- **Method:** `POST`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "username": { "type": "string", "description": "Your account email" },
    "password": { "type": "string", "description": "Your account password" }
  },
  "required": ["username", "password"]
}
```

### Output Schema

**Success** — token object:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

**Failure** — error message (HTTP 401):

```json
{ "message": "Invalid credentials" }
```

---

## 6. apis.spotify.show_playlist_library

**App:** `spotify`
**Description:** Search or show a list of playlists in the user's playlist library.

### HTTP Details

- **Path:** `/spotify/library/playlists`
- **Method:** `GET`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "access_token": {
      "type": "string",
      "required": true,
      "description": "Access token obtained from spotify app login"
    },
    "query": {
      "type": "string",
      "required": false,
      "description": "The search query to filter playlists by title, artist, etc.",
      "default": null,
      "constraints": []
    }
  },
  "required": ["access_token"]
}
```

### Output Schema

**Success** — array of playlist objects:

```json
[
  {
    "playlist_id": 344,
    "title": "Intergalactic Anthems: Sci-Fi Songs",
    "is_public": false,
    "rating": 0.0,
    "like_count": 1,
    "review_count": 0,
    "owner": {
      "name": "Joyce Weaver",
      "email": "joyce-weav@gmail.com"
    },
    "created_at": "2023-04-02T07:48:26",
    "song_ids": [70, 78, 124, 188, 229, 231, 308, 314]
  }
]
```

**Failure** — error message (HTTP 401/4xx):

```json
{ "message": "You are either not authorized to access this spotify API endpoint or your access token is missing, invalid or expired." }
```

---

## 7. apis.spotify.show_song

**App:** `spotify`
**Description:** Get details of a specific song.

### HTTP Details

- **Path:** `/spotify/songs/{song_id}`
- **Method:** `GET`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "song_id": { "type": "integer", "required": true, "description": "The song id to retrieve" }
  },
  "required": ["song_id"]
}
```

### Output Schema

**Success** — song object:

```json
{
  "song_id": 78,
  "title": "A Love That Never Was",
  "album_id": 17,
  "album_title": "Enchanted Melodies",
  "duration": 237,
  "artists": [
    { "id": 12, "name": "Mia Sullivan", "genre": "classical", "follower_count": 16 },
    { "id": 27, "name": "Carter Knight", "genre": "classical", "follower_count": 19 }
  ],
  "release_date": "2020-10-15T13:57:09",
  "genre": "classical",
  "play_count": 479,
  "rating": 3.0,
  "like_count": 18,
  "review_count": 1,
  "shareable_link": "https://spotify.com/song/78"
}
```

---

## 8. apis.supervisor.complete_task

**App:** `supervisor`
**Description:** Mark the currently active task as complete with the given answer.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "answer": {
      "type": ["string", "number", "null"],
      "required": false,
      "description": "The answer to the task. Should be a single entity or number, not a full sentence."
    },
    "status": {
      "type": "string",
      "required": false,
      "description": "Use 'fail' to explicitly mark the task as unsolvable.",
      "enum": ["fail"]
    }
  },
  "required": []
}
```

### Output Schema

**Success** — confirmation message:

```
"Execution successful."
```

or

```
"Marked the active task complete."
```

---

## 9. apis.spotify.show_liked_songs

**App:** `spotify`
**Description:** Get a list of songs you have liked.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "access_token": { "type": "string", "required": true, "description": "Access token obtained from spotify app login." },
    "page_index": { "type": "integer", "required": false, "default": 0 },
    "page_limit": { "type": "integer", "required": false, "default": 5 },
    "sort_by": { "type": "string", "required": false, "default": "-liked_at" }
  },
  "required": ["access_token"]
}
```

### Output Schema

**Success** — array of song objects:

```json
[
  {
    "song_id": 17,
    "title": "string",
    "album_id": 4,
    "album_title": "string",
    "duration": 238,
    "artists": [{ "id": 36, "name": "string" }],
    "liked_at": "2023-05-18T12:00:00"
  }
]
```

**Failure** — `{ "message": "string" }`

---

## 10. apis.spotify.review_song

**App:** `spotify`
**Description:** Rate or review a song (create new review). Returns 409 if review already exists.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "song_id": { "type": "integer", "required": true, "description": "ID of the song to review." },
    "rating": { "type": "integer", "required": true, "description": "Song rating (1-5)." },
    "access_token": { "type": "string", "required": true, "description": "Access token obtained from spotify app login." },
    "title": { "type": "string", "required": false, "default": "" },
    "text": { "type": "string", "required": false, "default": "" }
  },
  "required": ["song_id", "rating", "access_token"]
}
```

### Output Schema

**Success** — `{ "message": "string", "song_review_id": 1 }`
**Failure** — `{ "message": "string" }`

---

## 11. apis.spotify.update_song_review

**App:** `spotify`
**Description:** Update an existing song review. Requires `review_id` (not `song_id`).

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "review_id": { "type": "integer", "required": true, "description": "ID of the song review." },
    "access_token": { "type": "string", "required": true, "description": "Access token obtained from spotify app login." },
    "rating": { "type": "integer", "required": false, "description": "Song rating (1-5)." },
    "title": { "type": "string", "required": false },
    "text": { "type": "string", "required": false }
  },
  "required": ["review_id", "access_token"]
}
```

### Output Schema

**Success** — `{ "message": "string" }`
**Failure** — `{ "message": "string" }`

---

## 12. apis.spotify.show_song_review

**App:** `spotify`
**Description:** Show a single song review by `review_id`.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "review_id": { "type": "integer", "required": true, "description": "The song review id to retrieve." }
  },
  "required": ["review_id"]
}
```

### Output Schema

**Success** — `{ "song_review_id": 1, "song_id": 1, "rating": 1.0, "title": "string", "text": "string", "created_at": "...", "user": { "name": "string", "email": "string" } }`
**Failure** — `{ "message": "string" }`

---

## 13. apis.spotify.show_song_reviews

**App:** `spotify`
**Description:** Search or show a list of reviews for a song. Use this to find reviews by `song_id` and get `review_id` for `update_song_review`.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "song_id": { "type": "integer", "required": true, "description": "ID of the song." },
    "query": { "type": "string", "required": false },
    "user_email": { "type": "string", "required": false },
    "min_rating": { "type": "integer", "required": false },
    "max_rating": { "type": "integer", "required": false },
    "page_index": { "type": "integer", "required": false, "default": 0 },
    "page_limit": { "type": "integer", "required": false, "default": 5 },
    "sort_by": { "type": "string", "required": false }
  },
  "required": ["song_id"]
}
```

### Output Schema

**Success** — array of review objects:

```json
[
  {
    "song_review_id": 1,
    "song_id": 1,
    "rating": 1.0,
    "title": "string",
    "text": "string",
    "created_at": "2019-01-01T00:00:00",
    "user": { "name": "string", "email": "string" }
  }
]
```

**Failure** — `{ "message": "string" }`

---

## 14. apis.spotify.delete_song_review

**App:** `spotify`
**Description:** Delete a song review by `review_id`.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "review_id": { "type": "integer", "required": true, "description": "ID of the song review." },
    "access_token": { "type": "string", "required": true, "description": "Access token obtained from spotify app login." }
  },
  "required": ["review_id", "access_token"]
}
```

### Output Schema

**Success** — `{ "message": "string" }`
**Failure** — `{ "message": "string" }`

---

## 15. apis.spotify.search_songs

**App:** `spotify`
**Description:** Search for songs with a query. Does NOT require access_token.

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "query": { "type": "string", "required": false, "default": "", "description": "The search query string." },
    "artist_id": { "type": "integer", "required": false },
    "album_id": { "type": "integer", "required": false },
    "genre": { "type": "string", "required": false },
    "min_release_date": { "type": "string", "required": false, "default": "1500-01-01" },
    "max_release_date": { "type": "string", "required": false, "default": "3000-01-01" },
    "min_duration": { "type": "integer", "required": false, "default": 0 },
    "max_duration": { "type": "integer", "required": false },
    "min_rating": { "type": "number", "required": false, "default": 0.0 },
    "max_rating": { "type": "number", "required": false, "default": 5.0 },
    "min_like_count": { "type": "integer", "required": false, "default": 0 },
    "max_like_count": { "type": "integer", "required": false },
    "min_play_count": { "type": "integer", "required": false, "default": 0 },
    "max_play_count": { "type": "integer", "required": false },
    "page_index": { "type": "integer", "required": false, "default": 0 },
    "page_limit": { "type": "integer", "required": false, "default": 5, "constraints": ["value >= 1, <= 20"] },
    "sort_by": { "type": "string", "required": false, "description": "Valid: rating, like_count, play_count. Prefixed with +/- for ascending/descending." }
  },
  "required": []
}
```

### Output Schema

**Success** — array of song objects:

```json
[
  {
    "song_id": 305,
    "title": "Electric Pulse",
    "album_id": null,
    "album_title": null,
    "duration": 191,
    "artists": [{ "id": 33, "name": "Felix Blackwood" }],
    "release_date": "2021-07-21T10:11:55",
    "genre": "classical",
    "play_count": 233,
    "rating": 4.0,
    "like_count": 6,
    "review_count": 1,
    "shareable_link": "https://spotify.com/songs/305"
  }
]
```

**Failure** — `{ "message": "string" }`

---

## 16. apis.spotify.show_playlist

**App:** `spotify`
**Description:** Get detailed information about a specific playlist. View own or public playlists.

### HTTP Details

- **Path:** `/spotify/playlists/{playlist_id}`
- **Method:** `GET`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "playlist_id": { "type": "integer", "required": true },
    "access_token": { "type": "string", "required": false, "description": "Required for private playlists." }
  },
  "required": ["playlist_id"]
}
```

### Output Schema

**Success** — playlist object:

```json
{
  "playlist_id": 654,
  "title": "Road Trip with Roommates",
  "is_public": true,
  "rating": 0.0,
  "like_count": 0,
  "review_count": 0,
  "owner": { "name": "Jose Harrison", "email": "joseharr@gmail.com" },
  "created_at": "2023-05-18T12:00:00",
  "shareable_link": "https://spotify.com/playlists/654",
  "songs": [
    { "id": 6, "title": "string", "album_id": 1, "album_title": "string", "duration": 1, "artists": [{ "id": 1, "name": "string" }] }
  ]
}
```

**Failure** — `{ "message": "string" }`

---

## 17. apis.spotify.add_song_to_playlist

**App:** `spotify`
**Description:** Add a song to a playlist.

### HTTP Details

- **Path:** `/spotify/playlists/{playlist_id}/songs/{song_id}`
- **Method:** `POST`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "playlist_id": { "type": "integer", "required": true },
    "song_id": { "type": "integer", "required": true },
    "access_token": { "type": "string", "required": true }
  },
  "required": ["playlist_id", "song_id", "access_token"]
}
```

### Output Schema

**Success** — `{ "message": "Song added to the playlist." }`
**Failure** — `{ "message": "string" }`

---

## 18. apis.spotify.remove_song_from_playlist

**App:** `spotify`
**Description:** Remove a song from a playlist.

### HTTP Details

- **Path:** `/spotify/playlists/{playlist_id}/songs/{song_id}`
- **Method:** `DELETE`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "playlist_id": { "type": "integer", "required": true },
    "song_id": { "type": "integer", "required": true },
    "access_token": { "type": "string", "required": true }
  },
  "required": ["playlist_id", "song_id", "access_token"]
}
```

### Output Schema

**Success** — `{ "message": "Song removed from playlist." }`
**Failure** — `{ "message": "string" }`

---

## 19. apis.phone.login

**App:** `phone`
**Description:** Login to your phone account.

### HTTP Details

- **Path:** `/phone/auth/token`
- **Method:** `POST`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "username": { "type": "string", "required": true, "description": "Your account phone number." },
    "password": { "type": "string", "required": true, "description": "Your account password." }
  },
  "required": ["username", "password"]
}
```

### Output Schema

**Success** — `{ "access_token": "string", "token_type": "Bearer" }`
**Failure** — `{ "message": "string" }`

---

## 20. apis.phone.search_text_messages

**App:** `phone`
**Description:** Show or search your text messages.

### HTTP Details

- **Path:** `/phone/messages/text`
- **Method:** `GET`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "access_token": { "type": "string", "required": true },
    "query": { "type": "string", "required": false, "default": "" },
    "phone_number": { "type": "string", "required": false, "description": "Phone number of the contact." },
    "only_latest_per_contact": { "type": "boolean", "required": false, "default": false },
    "page_index": { "type": "integer", "required": false, "default": 0 },
    "page_limit": { "type": "integer", "required": false, "default": 5, "constraints": ["value >= 1, <= 20"] },
    "sort_by": { "type": "string", "required": false, "description": "Valid: created_at. Defaults to -created_at if no query." }
  },
  "required": ["access_token"]
}
```

### Output Schema

**Success** — array of message objects:

```json
[
  {
    "text_message_id": 16793,
    "sender": { "contact_id": null, "name": "Jose Harrison", "phone_number": "2474975253" },
    "receiver": { "contact_id": 259, "name": "Chris Mccoy", "phone_number": "5584932120" },
    "message": "I am putting together this playlist for our roadtrip...",
    "sent_at": "2023-05-17T19:59:54"
  }
]
```

**Failure** — `{ "message": "string" }`

---

## 21. apis.supervisor.show_profile

**App:** `supervisor`
**Description:** Show your supervisor's profile information.

### Input Schema

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

### Output Schema

**Success** — profile object:

```json
{
  "first_name": "Jose",
  "last_name": "Harrison",
  "email": "joseharr@gmail.com",
  "phone_number": "2474975253",
  "birthday": "1985-12-15",
  "sex": "male"
}
```

**Failure** — `{ "message": "string" }`

---
