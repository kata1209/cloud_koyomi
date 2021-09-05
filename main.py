import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import detect
import get_exif_of_image
import edit_db

#auth認証
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

gdrive_file_list = drive.ListFile().GetList()

print(type(gdrive_file_list))
print(len(gdrive_file_list))
print(type(gdrive_file_list[0]))

exif_list = []
filepath_list = []

for f in gdrive_file_list:
    if f['title'].endswith('.jpg',) or f['title'].endswith('.png',) or f['title'].endswith('.jpeg',) or f['title'].endswith('.JPG',):
        print(f['title'], '   \t', f['id'])

        #画像ダウンロード
        f = drive.CreateFile({'id': f['id']})
        f.GetContentFile(os.path.join('imgs', f['title'])) 
        
        #exif取得してリスト化
        dict = get_exif_of_image.main(f['title'])
        if (dict != None):
            exif_list.append(dict)
            filepath_list.append(dict['filepath'])

#検出結果をデータベースにup
detected_list = detect.main(filepath_list)
edit_db.main(detected_list,exif_list)