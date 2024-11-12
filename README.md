# Subreddit Monitor

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/chanzer0/subreddit-monitor-template)
![GitHub Forks](https://img.shields.io/github/forks/chanzer0/subreddit-monitor-template)
![GitHub Stars](https://img.shields.io/github/stars/chanzer0/subreddit-monitor-template)

A terminal-based Python script that allows you to monitor one or multiple subreddits for new posts containing specific keywords. It leverages your own Reddit account and a Reddit-hosted developer application to provide real-time notifications directly in your terminal.

![Example Usage](example_usage.png)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1. Create a Reddit Authorized Application](#1-create-a-reddit-authorized-application)
  - [2. Configure the `.env` File](#2-configure-the-env-file)
  - [3. Set Up the `config.json` File](#3-set-up-the-configjson-file)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Real-time Monitoring:** Continuously checks for new posts in specified subreddits.
- **Keyword Filtering:** Alerts you when post titles or bodies contain your specified keywords.
- **Custom Notifications:** Optional beep sounds to notify you of new relevant posts.
- **Flexible Configuration:** Easily customize subreddits, keywords, and notification settings.
- **Logging:** Detailed logs with adjustable logging levels for easier debugging and monitoring.
- **Flair Highlighting:** Option to color flair text for better visibility in trading subreddits.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a [Reddit](https://www.reddit.com/) account.
- You have installed [Python](https://www.python.org/) (version 3.10 or higher).
- You have access to a terminal or command prompt.
- Basic understanding of using command-line interfaces.

## Setup

### 1. Create a Reddit Authorized Application

To interact with Reddit's API, you need to create an authorized application.

1. **Navigate to Reddit App Preferences:**
   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps/).

2. **Create a New Application:**
   - Click on the **"are you a developer? create an app..."** button.

3. **Fill in the Application Details:**
   - **Name:** Choose a descriptive name for your application.
   - **App Type:** Select **"script"** since this is a personal use script.
   - **Description:** (Optional) Provide a brief description of your application.
   - **Redirect URI:** Use `http://localhost:8080` (ensure the port number matches the one in your `.env` file and is not used by other applications).

4. **Save the Application:**
   - Click **"Create app"** to save your application.

5. **Retrieve Credentials:**
   - After creation, note down your **Client ID** (displayed under the app name) and **Client Secret** (located next to "secret"). These will be used in your `.env` file.

### 2. Configure the `.env` File

The `.env` file securely stores your environment variables.

1. **Create a `.env` File:**
   - In the root directory of your project, create a file named `.env`.

2. **Add the Following Variables:**

   ```env:path/to/.env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=your_user_agent
   ```

   - **REDDIT_CLIENT_ID:** Your Reddit application's Client ID.
   - **REDDIT_CLIENT_SECRET:** Your Reddit application's Client Secret.
   - **REDDIT_USERNAME:** Your Reddit username.
   - **REDDIT_PASSWORD:** Your Reddit password.
   - **REDDIT_USER_AGENT:** A unique identifier for your application (e.g., `SubredditMonitor/1.0 by /u/YourUsername`).

   > **⚠️ Security Notice:** Ensure that your `.env` file is **never** committed to version control systems like GitHub. Add `.env` to your `.gitignore` file to prevent accidental exposure of your credentials.

### 3. Set Up the `config.json` File

The `config.json` file contains configuration settings for the application.

1. **Create a `config.json` File:**
   - In the root directory of this repository, copy the contents of the `sample_config.json` file into a new file named `config.json`. Remove any `//` comments as JSON does not support them.

2. **Add Configuration Settings:**

   ```json:path/to/config.json
   {
     "subreddits": ["YourTargetSubreddit1", "YourTargetSubreddit2"],
     "keywords": ["keyword1", "keyword2"],
     "beep_all_posts": true,
     "beep": {
       "enabled": true,
       "frequency": 1440,
       "duration": 100
     },
     "color_flairs": true,
     "logging_level": "INFO",
     "skip_existing": false,
     "title_filter": "[Selling]"
   }
   ```

   - **subreddits:** List of subreddits to monitor (without the `r/` prefix).
   - **keywords:** List of keywords to filter content in post titles or bodies.
   - **beep_all_posts:** `true` or `false` to enable/disable beep notifications for all new posts.
   - **beep:** Configuration for beep notifications:
     - **enabled:** `true` or `false` to enable/disable beeps.
     - **frequency:** Frequency of the beep in Hz.
     - **duration:** Duration of the beep in milliseconds.
   - **color_flairs:** `true` or `false` to enable/disable colored flair text.
   - **logging_level:** Logging verbosity (`INFO`, `DEBUG`, `ERROR`, etc.).
   - **skip_existing:** `true` or `false` to skip already existing submissions on startup.
   - **title_filter:** String to filter the title of submissions (useful for specific post types like `[Selling]`).

   > **Tip:** Customize these settings based on your monitoring needs to optimize performance and relevance.

## Installation

Follow these steps to get the project up and running on your local machine.

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/chanzer0/subreddit-monitor-template.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd subreddit-monitor-template
   ```

3. **Create a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** If your project uses additional package managers or has specific installation steps, adjust accordingly.

## Usage

Once installation and configuration are complete, you can start the application.

1. **Start the Application:**

   ```bash
   python main.py
   ```

2. **Authorize the Application:**
   
   - Upon starting, the application will provide a URL in the console.
   - Navigate to this URL in your browser to authorize the application.
   - After authorization, you can close the browser window, and the application will continue running in the terminal.

3. **Monitor Subreddit Posts:**

   - The application will display new submissions that match your keywords and filters in real-time.
   - If beep notifications are enabled, you'll hear a sound for each new relevant post.

## Configuration Options

Detailed descriptions of configuration settings to help you fine-tune the application's behavior.

- **subreddits:**  
  List the subreddits you want to monitor. Example:
  
  ```json
  "subreddits": ["python", "learnprogramming"]
  ```

- **keywords:**  
  Specify keywords to filter posts. The application will notify you if any of these appear in the title or body.

  ```json
  "keywords": ["help", "tutorial", "release"]
  ```

- **beep_all_posts:**  
  Toggle beep notifications for all new posts regardless of keyword matching.

  ```json
  "beep_all_posts": true
  ```

- **beep:**  
  Customize beep notifications.

  ```json
  "beep": {
    "enabled": true,
    "frequency": 1440,
    "duration": 100
  }
  ```

- **color_flairs:**  
  Enable colored flair text for better visibility.

  ```json
  "color_flairs": true
  ```

- **logging_level:**  
  Set the verbosity of logs. Suitable options include `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

  ```json
  "logging_level": "INFO"
  ```

- **skip_existing:**  
  Choose whether to ignore existing posts when the application starts.

  ```json
  "skip_existing": false
  ```

- **title_filter:**  
  Filter posts based on specific title patterns.

  ```json
  "title_filter": "[Selling]"
  ```

## Troubleshooting

Common issues and their solutions to help you get the application running smoothly.

- **Authentication Errors:**
  - **Solution:** Double-check your `.env` file for correct `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, and `REDDIT_PASSWORD`. Ensure there are no extra spaces or hidden characters.

- **Port Conflicts:**
  - **Solution:** If you encounter issues related to the redirect URI port, ensure that the port specified in your `.env` file is not being used by another application.

- **Missing Dependencies:**
  - **Solution:** Ensure all dependencies are installed correctly by running `pip install -r requirements.txt`.

- **Beep Not Functioning:**
  - **Solution:** Verify that your system supports audio playback and that the beep settings in `config.json` are correctly configured.

- **No Posts Being Detected:**
  - **Solution:** Ensure that the subreddits and keywords specified in `config.json` are correct and that there are new posts matching your criteria.

- **Logging Issues:**
  - **Solution:** Adjust the `logging_level` in `config.json` to `DEBUG` for more detailed logs, which can help identify issues.

## Contributing

Contributions are welcome! Whether it's reporting bugs, suggesting features, or improving documentation, your input is valuable.

### Steps to Contribute:

1. **Fork the Repository.**
2. **Create a New Branch:**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes:**

   ```bash
   git commit -m "Add feature: YourFeatureDescription"
   ```

4. **Push to the Branch:**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request:**
   - Navigate to your forked repository on GitHub.
   - Click on "Compare & pull request".
   - Provide a clear description of your changes and submit the pull request.

> **Guidelines:**
> - Ensure your code adheres to the project's coding standards.
> - Include appropriate tests for new features or bug fixes.
> - Update documentation as necessary.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).

---

*Feel free to reach out or open an issue if you encounter any problems or have suggestions for improvements. Happy monitoring!*