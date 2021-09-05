import os

from PIL import Image
from PIL.ExifTags import TAGS
import PIL.ExifTags as ExifTags

def main(file):
    im = Image.open(os.path.join('imgs', file))

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