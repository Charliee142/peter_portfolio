import requests

from django.conf import settings


def verify_turnstile(token):

    response = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": settings.TURNSTILE_SECRET_KEY,
            "response": token,
        },
    )

    result = response.json()

    return result.get("success", False)
