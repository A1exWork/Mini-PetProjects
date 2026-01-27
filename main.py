from fastapi import FastAPI
from datetime import datetime
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "qr_generator"}

@app.get("/qr/{text}")
async def generate_qr(text: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = BytesIO()
    img.save(img_bytes, "PNG")
    img_bytes.seek(0)
    return StreamingResponse(img_bytes, media_type="image/png")
