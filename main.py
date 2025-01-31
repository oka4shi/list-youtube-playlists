import sys
import os

from googleapiclient.discovery import build


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_youtube_client(api_key: str):
    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()

    return build("youtube", "v3", developerKey=api_key)


def get_chennel_id(youtube) -> str:
    request = youtube.channels().list(
        part="id",
        forHandle=handle
    )
    response = request.execute()
    response_items = response.get("items")
    if not (response_items and len(response_items) >= 1):
        return ""

    return response_items[0].get("id")

def get_playlists_of_channel(youtube, channel_id: str):
    if not channel_id:
        return []

    nextPageToken = None

    playlists = []
    
    while True:
        request = youtube.playlists().list(
                part="snippet",
                channelId=channel_id,
                maxResults="50",
                pageToken=nextPageToken
                )
        response = request.execute()

        items = response.get("items")
        if not (items and len(items) > 0):
            continue

        for item in items:
            snippet = item.get("snippet")
            title = snippet.get("title", "") if snippet else ""

            id = item.get("id", "")

            playlists.append({"title": title, "url": f"https://www.youtube.com/playlist?list={id}"})

        print(f"{len(playlists)}/{response.get("pageInfo").get("totalResults")}")

        if response and (not response.get("nextPageToken")):
            break

        nextPageToken = response.get("nextPageToken")

    return reversed(playlists)



def main(api_key: str, handle: str, style: str):
    youtube = get_youtube_client(api_key)
    channel_id = get_chennel_id(youtube)

    if not channel_id:
        return (None, "The channel is not found.")

    playlists = get_playlists_of_channel(youtube, channel_id)
    
    result = []
    for playlist in playlists:
        title = playlist.get("title")
        url = playlist.get("url")

        if style == "Markdown":
            result.append(f"[{title}]({url})")
        elif style == "Scrapbox" or style == "MediaWiki":
            result.append(f"[{title} {url}]")
        elif style == "WIKIWIKI":
            result.append(f"[[{title}>{url}]]")
        else:
            return (None, "Incorrect style")
    return (result, None)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("The number of arguments is incorrect.")

    style = sys.argv[1]
    if not style:
        sys.exit("Please specify the output style.")

    handle = sys.argv[2]
    if not handle:
        sys.exit("Please specify a handle name.")

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Please set YOUTUBE_API_KEY.")

    result, error = main(api_key, handle, style)
    if error is not None:
        sys.exit(error)

    for line in result:
        print(line)
