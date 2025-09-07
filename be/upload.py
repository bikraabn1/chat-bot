from fastapi import UploadFile, File, APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_file(files : list[UploadFile] = File(...)):
    filenames = [file.filname for file in files]
    return {"uploaded files" : filenames}