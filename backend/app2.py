import shutil
import os
import traceback
import uuid
import traceback
import aiofiles
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from langgraph.graph import StateGraph
from typing import Dict, Any
from pydantic import BaseModel
from agent import graph, ResPaperExtractState, PPTPresentation, Conversation
"""
FastAPI application for processing PDF files and generating PowerPoint presentations.
This is early stage, so just one endpoint, which sends both ppt and podcast, as I need to make that display in the frontend as a first step. 
Then it will be split into two endpoints, one for ppt and one for podcast, and with db storage to avoid re-executing the graph again for the same file.
    (but, for later, might check that, becuz if user wants to re-create the ppt, maybe with diff temp or something)
"""
app = FastAPI()
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PPTResponse(BaseModel):
    title: str
    authors: list[str]
    institution: str
    slides: list[dict[str, Any]]

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

#from the frontend, get want_ppt along with the file
@app.post("/generate")
async def generate( want_ppt: bool = Form(...), file: UploadFile = File(...)):
    """Endpoint to process a PDF file and generate either a PowerPoint presentation or a podcast.
    Returns the content as a FileResponse if successful, or raises an HTTPException on error.
    """
    print(f"Received file: {file.filename}, want_ppt: {want_ppt} {type(want_ppt)}")
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided in uploaded file.")
    pdf_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        async with aiofiles.open(pdf_path, 'wb') as out_file:
            while chunk := await file.read(1024*1024):  # Read in chunks of 1MB
                await out_file.write(chunk)
        print(f"File saved to {pdf_path}")
        # Initialize state
        state: ResPaperExtractState = ResPaperExtractState(pdf_path=pdf_path, want_ppt=want_ppt)
        
        # Run the graph workflow
        # result: Dict[str, Any] = graph.invoke(state)
        result = dict() # debug
        print("Graph invocation result:", result)
        # if not result:
        #     raise HTTPException(status_code=500, detail="Graph invocation failed or returned no result.")
        
        if want_ppt:
            ppt_object_path: str = result.get("ppt_file_path") # type: ignore
            if not ppt_object_path:
                raise HTTPException(status_code=500, detail="PPT generation failed.")

            return FileResponse(
                path=ppt_object_path,
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename=os.path.basename(ppt_object_path)
            )
        else:
            # podcast_path: str = result.get("podcast_file_path") # type: ignore
            podcast_path = "podcast_1751204720_024152.wav"
            if not podcast_path:
                raise HTTPException(status_code=500, detail="Podcast generation failed.")

            return FileResponse(
                path=podcast_path,
                media_type="audio/wav",
                filename=os.path.basename(podcast_path)
            )

    except Exception as e:
        print("--- ERROR STACK TRACE ---")
        traceback.print_exc() # This prints the traceback to stderr (your console)
        print("-------------------------")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        print(f"Cleaning up temporary files...")
        # if os.path.exists(pdf_path):
        #     os.remove(pdf_path)

# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
