from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import FileResponse

from ..database import snap as snap_database
from ..dependencies import get_current_user, check_user_is_friend
from ..models import UserInDB, Snap

api = APIRouter(prefix="/api/snap")


@api.post("/", status_code=201)
def send_snap(
    to_user_id: str,
    snap_file: UploadFile,
    current_user: UserInDB = Depends(get_current_user),
):
    # 401 if the recipient is not the user's friend
    if not check_user_is_friend(current_user.id, to_user_id, True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Adds entry to database and returns the snap's id
    snap_id = snap_database.send(current_user.id, to_user_id)
    # Write snap image to file
    file_output = open("snaps/" + snap_id + ".png", "w+b")
    file_output.write(snap_file.file.read())
    file_output.close()


@api.get("/")
def load_snaps(current_user: UserInDB = Depends(get_current_user)):
    return {
        "sent": snap_database.load_sent(current_user.id),
        "received": snap_database.load_received(current_user.id),
    }


@api.delete("/")
def delete_snap(snap_id: str, current_user: UserInDB = Depends(get_current_user)):
    snap_database.delete(snap_id)


@api.get("/download")
def download_snap(snap_id: str, current_user: UserInDB = Depends(get_current_user)):
    snap_data = snap_database.load(snap_id)
    if snap_data.seen:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Snap has been downloaded already")
    if not snap_data.to_user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    snap_database.mark_read(snap_id)
    return FileResponse("snaps/" + snap_id + ".png", media_type="image/png")
