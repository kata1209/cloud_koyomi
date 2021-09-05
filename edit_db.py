import sqlite3

def main(detected_list,exif_list):
    dbname = 'cloud_koyomi.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS cloud_koyomi_data')
    cur.execute("""CREATE TABLE cloud_koyomi_data(
        id INTEGER PRIMARY KEY,
        image_name TEXT,
        object_name TEXT,
        longitude_latitude TEXT,
        datetime DATETIME
    )""")

    for dict in detected_list:
        cur.execute("""INSERT INTO cloud_koyomi_data (image_name , object_name) 
        VALUES (?,?)""",(str(dict['filepath']), str(dict['class'])))

    for dict in exif_list:
        cur.execute("""UPDATE cloud_koyomi_data SET longitude_latitude = ?, datetime = ? 
        WHERE image_name = ?""",(str(dict['gps']), str(dict['datetime']),str(dict['filepath'])))

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    for a in cur.execute('SELECT * FROM cloud_koyomi_data'):
        print(a)
    conn.close()