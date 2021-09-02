import os
from PIL import Image
from PIL.ExifTags import TAGS
import PIL.ExifTags as ExifTags

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import detect

def get_exif_of_image(file):
    im = Image.open(file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in im._getexif().items()
            if k in ExifTags.TAGS
        }
    except AttributeError:
        return None
    # タグIDそのままでは人が読めないのでデコードして
    # テーブルに格納する
    exif_table = {}
    try:
        gps_tags = exif["GPSInfo"]
        gps = {
            ExifTags.GPSTAGS.get(t, t): gps_tags[t]
            for t in gps_tags
        }
        # 緯度経度情報を得る --- (*3)
        def conv_deg(v):
            # 分数を度に変換
            d = float(v[0])
            m = float(v[1])
            s = float(v[2])
            return d + (m / 60.0) + (s / 3600.0)
        lat = conv_deg(gps["GPSLatitude"])
        lat_ref = gps["GPSLatitudeRef"]
        if lat_ref != "N": lat = 0 - lat
        lon = conv_deg(gps["GPSLongitude"])
        lon_ref = gps["GPSLongitudeRef"]
        if lon_ref != "E": lon = 0 - lon
        # print(lat, lon)
        # print(exif["DateTime"])
    except KeyError:
        return None
    dict = {"filepath":file,"class":'',"gps":[lat,lon],"datetime":exif["DateTime"]}
    # print (list[0])
    return dict

#auth認証
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file_list = drive.ListFile().GetList()

print(type(file_list))

print(len(file_list))

print(type(file_list[0]))

list = []
filepath_list = []


for f in file_list:
    if f['title'].endswith('.jpg',) or f['title'].endswith('.png',) or f['title'].endswith('.jpeg',) or f['title'].endswith('.JPG',):
        print(f['title'], '   \t', f['id'])

        #画像ダウンロード
        f = drive.CreateFile({'id': f['id']})
        f.GetContentFile(os.path.join('imgs', f['title'])) 
        
        #exif取得してリスト化
        dict = get_exif_of_image(os.path.join('imgs', f['title']))
        if (dict != None):
            list.append(dict)
            filepath_list.append(dict['filepath'])
        print(list)

#(list[0,1,2,3,4....]['filepath'])をAI検出


print(filepath_list)
    

test_list = detect.main(filepath_list)
print(test_list)
for i in range(len(test_list)):
    for dict_i in test_list[i]:
        for j in range(len(filepath_list)):
            for dict_j in filepath_list[j]:
                if dict_i['filepath'] == dict_j['filepath']:
                    dict_i['gps'] = dict_j['gps']
                    dict_i['datetime'] = dict_j['datetime']
print(test_list)
    