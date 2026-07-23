"""
Chat Storage

Responsible for:
1. Creating chats
2. Saving chats
3. Loading chats
4. Listing chats
5. Deleting chats
"""

import json
import uuid

from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# Storage Location
# --------------------------------------------------

CHAT_DIR = Path("data/chats")
CHAT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _chat_path(chat_id: str):
    return CHAT_DIR / f"{chat_id}.json"


# --------------------------------------------------
# Create Chat
# --------------------------------------------------

def create_chat(title="New Chat"):

    now = datetime.now().isoformat()

    chat = {
        "id": str(uuid.uuid4()),
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": []
    }

    save_chat(chat)

    return chat


# --------------------------------------------------
# Save Chat
# --------------------------------------------------

def save_chat(chat):

    chat["updated_at"] = datetime.now().isoformat()

    with open(
        _chat_path(chat["id"]),
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chat,
            f,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Load Chat
# --------------------------------------------------

def load_chat(chat_id):

    path = _chat_path(chat_id)

    if not path.exists():
        return None

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# --------------------------------------------------
# Delete Chat
# --------------------------------------------------

def delete_chat(chat_id):

    path = _chat_path(chat_id)

    if path.exists():
        path.unlink()


# --------------------------------------------------
# List Chats
# --------------------------------------------------

def list_chats():

    chats = []

    for file in CHAT_DIR.glob("*.json"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            chat = json.load(f)

            # backward compatibility
            if "updated_at" not in chat:
                chat["updated_at"] = chat.get(
                    "created_at",
                    datetime.now().isoformat()
                )

            chats.append(chat)

    chats.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return chats