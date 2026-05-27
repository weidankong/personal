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
