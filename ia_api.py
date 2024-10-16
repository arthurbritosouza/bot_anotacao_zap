import os
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from notion_api import create_block
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def analisar_video(msg):
    try:
        if "youtube.com" in msg:
            video_id = msg.split("v=")[1]  
            transcripts = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
            subtitle_text = " ".join([entry["text"] for entry in transcripts])
            yt = YouTube(msg)
            title = yt.title
            response = model.generate_content(f'faça um resumo detalhado dessa descricao de video e deixe esse texto de uma forma mais bonito: {subtitle_text}')
            body = response.text
            create_block(title,body)    
            return response.text
        else:
            return "não é um link do youtube"
    
    except Exception as e:
        print(f"Um erro no ia_api: {e}")
        return "Não foi possível processar sua solicitação."
    

if __name__ == '__main__':

    msg = "https://www.youtube.com/watch?v=ol_S9G0nCNE"
    response = analisar_video(msg)
    print(response)