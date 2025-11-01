from fastapi import FastAPI, File, UploadFile
from faster_whisper import WhisperModel

app = FastAPI()

# faster-whisperモデルのロード
model = WhisperModel("small")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
  # ファイルを一時保存
  file_location = f"temp_{file.filename}"
  with open(file_location, "wb") as f:
      f.write(await file.read())
  
  # 音声認識
  segments, info = model.transcribe(file_location)
  
  # 結果を文字列にまとめる
  text = " ".join([segment.text for segment in segments])
  return {"text": text}
