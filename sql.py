"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors
import pandas as pd

connection = pymysql.connect(host='localhost',
                             user='',
                             password='',
                             db='database',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# 保存评论
def insert_comments(music_id, music_name, comments):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `comments` (`MUSIC_ID`, `MUSIC_NAME`, `COMMENTS`) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (music_id, music_name, comments))
        except Exception as e:
            print(str(e))
    connection.commit()


# 保存音乐
def insert_music(music_id, music_name, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`, `ARTIST_NAME`) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (music_id, music_name, artist_name))
        except Exception as e:
            print(str(e))
    connection.commit()

#保存每日推荐歌曲
def insert_recommendation_music(music_id, music_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `recommendation` (`MUSIC_ID`, `MUSIC_NAME`) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (music_id, music_name))
        except Exception as e:
            print(str(e))
    connection.commit()

# 保存歌手
def insert_artist(artist_id, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (%s, %s)"
        cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY ARTIST_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()

#获取评论
def get_comments():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `comments`"
        cursor.execute(sql, ())
        return cursor.fetchall()

def get_text():
    sql = "SELECT * FROM `comments`"
    return pd.read_sql(sql, con = connection)

def dis_connect():
    connection.close()
