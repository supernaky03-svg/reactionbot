from fastapi import FastAPI
app = FastAPI(title="Thinking Auto Reaction Health")
@app.get("/health")
async def health():
    return {"status":"ok"}
