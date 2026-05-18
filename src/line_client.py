import requests

from .config import ENV

LINE_PUSH_API_URL = "https://api.line.me/v2/bot/message/push"


def push_text_message(message_text: str) -> None:
    payload = {
        "to": ENV.line_group_id,
        "messages": [{"type": "text", "text": message_text}],
    }
    headers = {
        "Authorization": f"Bearer {ENV.line_access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        LINE_PUSH_API_URL,
        json=payload,
        headers=headers,
        timeout=ENV.request_timeout_sec,
    )
    response.raise_for_status()
