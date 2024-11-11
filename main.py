import os
import re
import socket
import random
import datetime
import logging
import json
from typing import Optional

from dotenv import load_dotenv  # Add this import

import praw
from praw.models import Submission

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.color import Color

import winsound

# Load environment variables from .env file
load_dotenv()  # Add this line


# Load configuration from config.json
def load_config(config_path: str = "config.json") -> dict:
    """Loads configuration from a JSON file."""
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing the configuration file: {e}")
        raise


# Load configuration
config = load_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.get("logging_level", "INFO").upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

console = Console()


def main():
    """Main entry point of the application."""
    try:
        reddit = get_initial_token()
        subreddit = reddit.subreddit(config["subreddit"])
        logging.info(f"Started streaming submissions from r/{config['subreddit']}.")

        for submission in subreddit.stream.submissions(
            skip_existing=config["skip_existing"]
        ):
            title_filter = config["title_filter"].lower()
            if not title_filter or (
                title_filter and title_filter in submission.title.lower()
            ):
                timestamp = datetime.datetime.fromtimestamp(
                    submission.created_utc
                ).strftime("%I:%M %p")
                console.print(f"[bold green]{timestamp}[/bold green]")
                display_submission(submission)
    except Exception as e:
        logging.error(f"An error occurred in main: {e}", exc_info=True)


def display_submission(submission: Submission):
    """
    Highlight keywords in the title or body of the submission.
    Displays the title in bold and the body with highlighted keywords.
    """
    try:
        title = Text(submission.title.lower(), style="bold")
        body_content = (
            f"User: {submission.author} [{submission.author_flair_text}]\n"
            f"{submission.url}\n\n{submission.selftext.lower()}"
        )
        body = Text(body_content)

        keywords = config.get("keywords", [])

        # Highlight URLs in the body
        url_pattern = re.compile(r"(https?://[^\s)]+)", re.IGNORECASE)
        body.highlight_regex(
            re_highlight=url_pattern, style=Style(color="blue", bold=True)
        )

        should_beep = config.get("beep_all_posts", False)
        highlight_style = Style(color="red", bold=True, italic=True)

        for keyword in keywords:
            keyword_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            if keyword_pattern.search(submission.title):
                should_beep = True
                title.highlight_regex(
                    re_highlight=keyword_pattern, style=highlight_style
                )
            if keyword_pattern.search(submission.selftext):
                should_beep = True
                body.highlight_regex(
                    re_highlight=keyword_pattern, style=highlight_style
                )

        if should_beep and config.get("beep", {}).get("enabled", False):
            play_beep(
                frequency=config["beep"].get("frequency", 1440),
                duration=config["beep"].get("duration", 100),
            )

        if config.get("color_flairs", True):
            flair_color_style = determine_flair_color(submission.author_flair_text)
            if flair_color_style:
                flair_text = f"[{submission.author_flair_text.lower()}]"
                body.highlight_words([flair_text], style=flair_color_style)

        panel = Panel(
            body,
            title=title,
            expand=False,
            border_style="bold",
            padding=(1, 1),
        )

        console.print(panel)
    except Exception as e:
        logging.error(
            f"Error displaying submission {submission.id}: {e}", exc_info=True
        )


def play_beep(frequency: int = 1440, duration: int = 100):
    """Plays a beep sound. Adjusts frequency and duration as needed."""
    try:
        winsound.Beep(frequency, duration)
    except RuntimeError as e:
        logging.warning(f"Beep failed: {e}")


def determine_flair_color(flair_text: Optional[str]) -> Optional[Style]:
    """
    Determines the color style based on the flair score.
    Returns a Style object or None.
    """
    if not flair_text:
        return Style(color="white")

    try:
        flair_score_part = flair_text.split("(")[0].strip()
        flair_score = flair_score_part.split("+")[1]
        int_flair_score = min(int(flair_score), 100)
        flair_color_idx = int_flair_score // 20

        flair_color_scale = {
            0: Style(color=Color.from_rgb(255, 255, 255)),
            1: Style(color=Color.from_rgb(0, 255, 0)),
            2: Style(color=Color.from_rgb(0, 0, 255)),
            3: Style(color=Color.from_rgb(128, 0, 128)),
            4: Style(color=Color.from_rgb(255, 165, 0)),
            5: Style(color=Color.from_rgb(255, 0, 0)),
        }

        return flair_color_scale.get(flair_color_idx, Style(color="white"))
    except (IndexError, ValueError) as e:
        logging.warning(f"Failed to parse flair score '{flair_text}': {e}")
        return Style(color="white")


def get_initial_token() -> praw.Reddit:
    """
    Initializes Reddit instance and obtains the access token.
    Returns a praw.Reddit instance.
    """
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            password=os.getenv("PASSWORD"),
            user_agent=os.getenv("USER_AGENT"),
            username=os.getenv("USERNAME"),
            redirect_uri=os.getenv("REDIRECT_URI"),
        )
        state = str(random.randint(0, 65000))
        url = reddit.auth.url(duration="permanent", scopes=["read"], state=state)
        logging.info(f"Authorize the app by ctrl+clicking this link: {url}")

        client = receive_connection()
        data = client.recv(1024).decode("utf-8")
        logging.debug(f"Received data: {data}")

        param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        params = {token.split("=")[0]: token.split("=")[1] for token in param_tokens}

        if state != params.get("state"):
            send_message(
                client,
                f"State mismatch. Expected: {state} Received: {params.get('state')}",
            )
            raise ValueError("State mismatch in OAuth flow.")
        elif "error" in params:
            send_message(client, params["error"])
            raise ValueError(f"Error in OAuth flow: {params['error']}")

        refresh_token = reddit.auth.authorize(params["code"])
        send_message(client, "Authorization successful. You can close this window.")
        logging.info("Reddit authorization successful.")
        return reddit
    except Exception as e:
        logging.error(f"Failed to get initial token: {e}", exc_info=True)
        raise


def receive_connection() -> socket.socket:
    """
    Waits for and returns a connected socket.
    Opens a TCP connection on port 8080 and waits for a single client.
    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        logging.info("Waiting for OAuth callback connection on port 8080...")
        client, addr = server.accept()
        logging.info(f"Connected by {addr}")
        server.close()
        return client
    except Exception as e:
        logging.error(f"Failed to receive connection: {e}", exc_info=True)
        raise


def send_message(client: socket.socket, message: str):
    """Sends an HTTP response message to the client and closes the connection."""
    try:
        http_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{message}"
        client.sendall(http_response.encode())
        logging.debug(f"Sent message to client: {message}")
    except Exception as e:
        logging.error(f"Failed to send message to client: {e}", exc_info=True)
    finally:
        client.close()


if __name__ == "__main__":
    main()
