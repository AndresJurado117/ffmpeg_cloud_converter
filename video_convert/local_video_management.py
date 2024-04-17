import os

def local_video_save(filename: str, content) -> None:
    if isinstance(filename, str) == True:
        with open(f"uploaded_videos/{filename}", "wb") as file:
            for chunk in content.chunks():
                file.write(chunk)


def local_video_delete(filename: str) -> None:
    if isinstance(filename, str) == True:
        if os.path.exists(filename):
            os.remove(filename)
        else:
            raise FileNotFoundError
        
def local_video_url(filename: str) -> None:
    if isinstance(filename, str) == True:
        if os.path.exists(filename):
            file_path = f"converted_videos/{filename}"
        else:
            raise FileNotFoundError