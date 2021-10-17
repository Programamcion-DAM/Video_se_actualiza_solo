# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import cv2

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "aqui va la ruta a tu clientFile"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    while True:
      video_id = 'aquí va tu id del video'
      image = cv2.imread('/content/drive/MyDrive/miniaturaIncompleta.jpg')

      request = youtube.videos().list(
          part="snippet,statistics",
          id=video_id
      )
      response = request.execute()

      snippet = response["items"][0]["snippet"]
      statistics  = response["items"][0]["statistics"]

      snippet["title"] = "Si entras en este video serás la visita " + str((statistics["viewCount"]+1))+". Así que bienvenido."
      cv2.putText(image, str((statistics["viewCount"]+1)), (28, 505),
          cv2.FONT_HERSHEY_DUPLEX, 5.5, (45, 45, 255), 18)
    
      cv2.imwrite('miniatura-output.jpg', image)
      youtube.videos().update(part="snippet",body=dict(snippet=snippet, id=video_id)).execute()
      youtube.thumbnails().set(videoId=video_id, media_body='/content/miniatura-output.jpg').execute()

      sleep(300)
    

if __name__ == "__main__":
    main()