# YouTube Playlist Fetcher

## Overview
This script retrieves all playlists of a YouTube channel using its handle and formats the output in different styles (Markdown, MediaWiki, PukiWiki). It uses the YouTube Data API v3.

## Installation
1. Install required dependencies:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip3 install -r requirements.txt
   ```
2. Set up your Goole Cloud API key as an environment variable:
   ```sh
   export YOUTUBE_API_KEY="your_api_key_here"
   ```

## Usage
Run the script with the following command:
```sh
python3 main.py <style> <handle>
```

### Arguments
- `<style>`: The output format. Supported values(case-sensitive):
  - `Markdown` ...  Markdown style: `[Name_of_a_playlist](URL)`
  - `MediaWiki` ... MediaWiki or Scrapbox style: `[Name_of_a_playlist URL]`
  - `PukiWiki` ... Pukiwiki or WIKIWIKI style: `[Name_of_a_playlist>URL]`
- `<handle>`: The YouTube channel handle (e.g., `@channelname`)

### Example
```sh
python3 main.py Markdown @examplechannel
```

Use the shell's redirections(`> file_name`) to save the results in a file as needed.
