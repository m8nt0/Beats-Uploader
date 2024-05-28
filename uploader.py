import os
import time
import ffmpeg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def create_video(audio_path, image_path, output_path):
    input_audio = ffmpeg.input(audio_path)
    input_image = ffmpeg.input(image_path)
    (
        ffmpeg
        .output(input_audio, input_image, output_path, vcodec='libx264', acodec='aac', strict='experimental', shortest=None)
        .run()
    )

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_console()
    return build('youtube', 'v3', credentials=credentials)

def upload_to_youtube(video_path, title, description, tags):
    youtube = authenticate_youtube()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path)
    )
    response = request.execute()
    print(f'YouTube Video uploaded: {response}')

def upload_to_instagram(username, password, video_path, title, description, tags):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)

    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

    driver.get('https://www.instagram.com/create/style/')
    time.sleep(3)

    driver.find_element(By.XPATH, '//input[@accept="video/*"]').send_keys(video_path)
    time.sleep(3)

    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    time.sleep(2)
    
    driver.find_element(By.XPATH, '//textarea').send_keys(f'{title}\n{description}\n{" ".join(tags)}')
    time.sleep(1)
    
    driver.find_element(By.XPATH, '//button[text()="Share"]').click()
    time.sleep(5)

    driver.quit()
    print(f'Instagram Video uploaded: {video_path}')

def upload_to_tiktok(username, password, video_path, title, description, tags):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.tiktok.com/login')
    time.sleep(3)

    driver.find_element(By.XPATH, '//input[@name="username"]').send_keys(username)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

    driver.get('https://www.tiktok.com/upload')
    time.sleep(3)

    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(video_path)
    time.sleep(3)

    driver.find_element(By.XPATH, '//textarea').send_keys(f'{title}\n{description}\n{" ".join(tags)}')
    time.sleep(1)
    
    driver.find_element(By.XPATH, '//button[text()="Post"]').click()
    time.sleep(5)

    driver.quit()
    print(f'TikTok Video uploaded: {video_path}')

def process_folder(folder_path, instagram_credentials, tiktok_credentials):
    audio_path = os.path.join(folder_path, 'beat.mp3')
    image_path = os.path.join(folder_path, 'image.jpg')
    video_path = os.path.join(folder_path, 'video.mp4')

    create_video(audio_path, image_path, video_path)
    title = os.path.basename(folder_path)
    description = f'{title} - produced by Beatmaker'
    tags = ['beat', 'music', 'hiphop']  # Customize this as needed

    upload_to_youtube(video_path, title, description, tags)
    upload_to_instagram(instagram_credentials['username'], instagram_credentials['password'], video_path, title, description, tags)
    upload_to_tiktok(tiktok_credentials['username'], tiktok_credentials['password'], video_path, title, description, tags)

def main():
    root_dir = 'path/to/your/beats'
    instagram_credentials = {
        'username': 'your_instagram_username',
        'password': 'your_instagram_password'
    }
    tiktok_credentials = {
        'username': 'your_tiktok_username',
        'password': 'your_tiktok_password'
    }

    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            process_folder(folder_path, instagram_credentials, tiktok_credentials)

if __name__ == '__main__':
    main()
