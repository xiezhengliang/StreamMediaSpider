# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymysql
import configparser
from os import path
import urllib
import json
import uuid

config = configparser.ConfigParser()
# 获取当前目录
d = path.dirname(__file__)
config.read(d + "/config/config.ini")
# 初始化数据库连接
db_host = config.get("db", "host")
db_port = config.get("db", "port")
db_user = config.get("db", "user")
db_password = config.get("db", "password")
db_name = config.get("db", "dbname")


class SinaAppPipeline(object):

    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8", use_unicode=True)
        title = str(item['title'])
        sel_sql = "SELECT * FROM sina_app WHERE MATCH(title) AGAINST('" + title + "')"
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        cursor.close()
        # 判断数据库中是否已经存在相同广告id的数据
        if not cam_row:
            curTime = datetime.datetime.now()
            curTime.strftime('%Y-%m-%d %H:%M:%S')
            cursor = db.cursor()
            # 保存图片
            # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
            img = item['pic']
            filename = ""
            if img is not None:
                try:
                    image_path = "D:/sina_image/"
                    if ".png" in img:
                        filename = str(uuid.uuid1()) + ".png"
                    if ".gif" in img:
                        filename = str(uuid.uuid1()) + ".gif"
                    else:
                        filename = str(uuid.uuid1()) + ".jpg"
                    urllib.request.urlretrieve(img, image_path + '%s' % filename)
                except Exception as E:
                    pass
            cursor.execute("""INSERT INTO sina_app 
              (pos, newsId, title,link, pic,showTag,articlePreload,commentStatus,adid,dislikeTags,create_time,local_img)  
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)""",
                           (
                               item['pos'].encode('utf-8'),
                               item['newsId'].encode('utf-8'),
                               item['title'].encode('utf-8'),
                               item['link'].encode('utf-8'),
                               item['pic'].encode('utf-8'),
                               item['showTag'].encode('utf-8'),
                               item['articlePreload'].encode('utf-8'),
                               item['commentStatus'].encode('utf-8'),
                               item['adid'].encode('utf-8'),
                               item['dislikeTags'].encode('utf-8'),
                               curTime, filename,))
            sina_ad_id = str(cursor.lastrowid)
            cursor.execute(
                """INSERT INTO sina_ad_to_parameter (sina_ad_id, sina_para_id,time) VALUES(%s,%s,%s)""",
                (sina_ad_id, str(item['parameter_id']), curTime))
            db.commit()
            cursor.close()
        else:
            updateTime = datetime.datetime.now()
            updateTime.strftime('%Y-%m-%d %H:%M:%S')
            id = cam_row[0]
            amount = cam_row[13] + 1
            # 保存图片
            # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
            img = item['pic']
            filename = ""
            if img is not None:
                try:
                    image_path = "D:/sina_image/"
                    if ".png" in img:
                        filename = str(uuid.uuid1()) + ".png"
                    if ".gif" in img:
                        filename = str(uuid.uuid1()) + ".gif"
                    else:
                        filename = str(uuid.uuid1()) + ".jpg"
                    urllib.request.urlretrieve(img, image_path + '%s' % filename)
                except Exception as E:
                    pass
            sql = 'update sina_app set pos =' + '"' + str(item['pos']) + '"' + ',newsId=' + '"' + str(
                item['newsId']) + '"' + ',title=' + '"' + str(item['title']) + '"' + ',link=' + '"' + str(
                item['link']) + '"' + ',pic=' + '"' + str(item['pic']) + '"' + ',showTag=' + '"' + str(
                item['showTag']) + '"' + ',articlePreload=' + '"' + str(
                item['articlePreload']) + '"' + ',commentStatus=' + '"' + str(
                item['commentStatus']) + '"' + ',dislikeTags=' + '"' + str(
                item['dislikeTags']) + '"' + ',update_time=' + '"' + str(updateTime) + '"' + ',amount=' + '"' + str(
                amount) + '"' + ' where id=' + '"' + str(id) + '"'
            try:
                # 执行SQL语句
                cursor = db.cursor()
                cursor.execute(sql)
                cursor.execute(
                    """INSERT INTO sina_ad_to_parameter (sina_ad_id, sina_para_id,time) VALUES(%s,%s,%s)""",
                    (str(id), str(item['parameter_id']), datetime.datetime.now()))
                # 提交到数据库执行
                db.commit()
                cursor.close()
            except:
                # 发生错误时回滚
                db.rollback()
                cursor.close()

        return item


class ToutiaoAppPipeline(object):
    # def __init__(self):
    # self.db = pymysql.connect(user=dbuser, passwd=dbpass, db=dbname, host=dbhost, port=dbport,charset="utf8", use_unicode=True)
    # 使用 cursor() 方法创建一个游标对象 cursor
    # self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8", use_unicode=True)
        title = str(item['title'])
        sel_sql = "SELECT * FROM toutiao_app WHERE MATCH(title) AGAINST('" + title + "')"
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        cursor.close()
        # 用source和title来判断数据是否已经存在
        if not cam_row:
            curTime = datetime.datetime.now()
            curTime.strftime('%Y-%m-%d %H:%M:%S')
            cursor1 = db.cursor()
            try:
                cursor1.execute("""INSERT INTO toutiao_app 
                      (abstract, action_list, aggr_type,allow_download, article_sub_type,article_tpye,
                      article_url,ban_comment,behot_time,bury_count,cell_flag,cell_layout_style,cell_type,comment_count,
                      content_decoration,digg_count,display_url,filter_words,group_flags,group_id,has_video,hot,
                      ignore_web_transform,is_subject,item_id,item_version,label,label_style,large_image_list,
                      level,log_pb,natant_level,preload_web,publish_time,raw_ad_data,read_count,repin_count,
                      rid,share_count,share_info,share_url,show_dislike,show_portrait,show_portrait_article,
                      source,source_avatar,tag,tag_id,title,url,user_repin,user_verified,video_detail_info,
                      video_duration,video_id,video_play_info,video_proportion_article,video_style,create_time,parameter_id)  
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
                    str(item['abstract']).encode('utf-8'),
                    item['action_list'].encode('utf-8'),
                    item['aggr_type'].encode('utf-8'),
                    item['allow_download'].encode('utf-8'),
                    item['article_sub_type'].encode('utf-8'),
                    item['article_tpye'].encode('utf-8'),
                    item['article_url'].encode('utf-8'),
                    item['ban_comment'].encode('utf-8'),
                    item['behot_time'].encode('utf-8'),
                    item['bury_count'].encode('utf-8'),
                    item['cell_flag'].encode('utf-8'),
                    item['cell_layout_style'].encode('utf-8'),
                    item['cell_type'].encode('utf-8'),
                    item['comment_count'].encode('utf-8'),
                    item['content_decoration'].encode('utf-8'),
                    item['digg_count'].encode('utf-8'),
                    item['display_url'].encode('utf-8'),
                    item['filter_words'].encode('utf-8'),
                    item['group_flags'].encode('utf-8'),
                    item['group_id'].encode('utf-8'),
                    item['has_video'].encode('utf-8'),
                    item['hot'].encode('utf-8'),
                    item['ignore_web_transform'].encode('utf-8'),
                    item['is_subject'].encode('utf-8'),
                    item['item_id'].encode('utf-8'),
                    item['item_version'].encode('utf-8'),
                    item['label'].encode('utf-8'),
                    item['label_style'].encode('utf-8'),
                    item['large_image_list'].encode('utf-8'),
                    item['level'].encode('utf-8'),
                    item['log_pb'].encode('utf-8'),
                    item['natant_level'].encode('utf-8'),
                    item['preload_web'].encode('utf-8'),
                    item['publish_time'].encode('utf-8'),
                    item['raw_ad_data'].encode('utf-8'),
                    item['read_count'].encode('utf-8'),
                    item['repin_count'].encode('utf-8'),
                    item['rid'].encode('utf-8'),
                    item['share_count'].encode('utf-8'),
                    item['share_info'].encode('utf-8'),
                    item['share_url'].encode('utf-8'),
                    item['show_dislike'].encode('utf-8'),
                    item['show_portrait'].encode('utf-8'),
                    item['show_portrait_article'].encode('utf-8'),
                    item['source'].encode('utf-8'),
                    item['source_avatar'].encode('utf-8'),
                    item['tag'].encode('utf-8'),
                    item['tag_id'].encode('utf-8'),
                    item['title'].encode('utf-8'),
                    item['url'].encode('utf-8'),
                    item['user_repin'].encode('utf-8'),
                    item['user_verified'].encode('utf-8'),
                    item['video_detail_info'].encode('utf-8'),
                    item['video_duration'].encode('utf-8'),
                    item['video_id'].encode('utf-8'),
                    item['video_play_info'].encode('utf-8'),
                    item['video_proportion_article'].encode('utf-8'),
                    item['video_style'].encode('utf-8'),
                    curTime,
                    str(item['parameter_id']),))
                toutiao_ad_id = str(cursor1.lastrowid)
                cursor1.execute(
                    """INSERT INTO toutiao_ad_to_parameter (toutiao_ad_id, toutiao_para_id,time) VALUES(%s,%s,%s)""",
                    (toutiao_ad_id, str(item['parameter_id']), curTime))
                large_image_list = item['large_image_list'].encode('utf-8')
                img = large_image_list[1:len(large_image_list) - 1].replace('\'', '"')
                img = json.loads(img).get('url')
                if (img == '' or img == ' '):
                    img = json.loads(large_image_list[1:len(large_image_list) - 1].replace('\'', '"')).get('uri')
                # 保存图片
                # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
                image_path = "D:/touttiao_image/"
                filename = img
                urllib.request.urlretrieve(img, image_path + '%s' % filename)
                db.commit()
                cursor1.close()
            except:
                pass
        else:
            updateTime = datetime.datetime.now()
            updateTime.strftime('%Y-%m-%d %H:%M:%S')
            toutiao_cursor = db.cursor()
            id = cam_row[0]
            amount = cam_row[61] + 1
            sql = 'update toutiao_app set abstract =' + '"' + str(item['abstract'].replace("\"", "'")) + '"' \
                  + ',action_list=' + '"' + str(item['action_list'].replace("\"", "'")) + '"' \
                  + ',aggr_type=' + '"' + str(item['aggr_type'].replace("\"", "'")) + '"' \
                  + ',allow_download=' + '"' + str(item['allow_download'].replace("\"", "'")) + '"' \
                  + ',article_sub_type=' + '"' + str(item['article_sub_type'].replace("\"", "'")) + '"' \
                  + ',article_tpye=' + '"' + str(item['article_tpye'].replace("\"", "'")) + '"' \
                  + ',article_url=' + '"' + str(item['article_url'].replace("\"", "'")) + '"' \
                  + ',ban_comment=' + '"' + str(item['ban_comment'].replace("\"", "'")) + '"' \
                  + ',behot_time=' + '"' + str(item['behot_time'].replace("\"", "'")) + '"' \
                  + ',bury_count=' + '"' + str(item['bury_count'].replace("\"", "'")) + '"' \
                  + ',cell_flag=' + '"' + str(item['cell_flag'].replace("\"", "'")) + '"' \
                  + ',cell_layout_style=' + '"' + str(item['cell_layout_style'].replace("\"", "'")) + '"' \
                  + ',cell_type=' + '"' + str(item['cell_type'].replace("\"", "'")) + '"' \
                  + ',comment_count=' + '"' + str(item['comment_count'].replace("\"", "'")) + '"' \
                  + ',content_decoration=' + '"' + str(item['content_decoration'].replace("\"", "'")) + '"' \
                  + ',digg_count=' + '"' + str(item['digg_count'].replace("\"", "'")) + '"' \
                  + ',display_url=' + '"' + str(item['display_url'].replace("\"", "'")) + '"' \
                  + ',filter_words=' + '"' + str(item['filter_words'].replace("\"", "'")) + '"' \
                  + ',group_flags=' + '"' + str(item['group_flags'].replace("\"", "'")) + '"' \
                  + ',group_id=' + '"' + str(item['group_id'].replace("\"", "'")) + '"' \
                  + ',has_video=' + '"' + str(item['has_video'].replace("\"", "'")) + '"' \
                  + ',hot=' + '"' + str(item['hot'].replace("\"", "'")) + '"' \
                  + ',ignore_web_transform=' + '"' + str(item['ignore_web_transform'].replace("\"", "'")) + '"' \
                  + ',is_subject=' + '"' + str(item['is_subject'].replace("\"", "'")) + '"' \
                  + ',item_id=' + '"' + str(item['item_id'].replace("\"", "'")) + '"' \
                  + ',item_version=' + '"' + str(item['item_version'].replace("\"", "'")) + '"' \
                  + ',label=' + '"' + str(item['label'].replace("\"", "'")) + '"' \
                  + ',label_style=' + '"' + str(item['label_style'].replace("\"", "'")) + '"' \
                  + ',large_image_list=' + '"' + str(item['large_image_list'].replace("\"", "'")) + '"' \
                  + ',level=' + '"' + str(item['level'].replace("\"", "'")) + '"' \
                  + ',log_pb=' + '"' + str(item['log_pb'].replace("\"", "'")) + '"' \
                  + ',log_pb=' + '"' + str(item['log_pb'].replace("\"", "'")) + '"' \
                  + ',preload_web=' + '"' + str(item['preload_web'].replace("\"", "'")) + '"' \
                  + ',publish_time=' + '"' + str(item['publish_time'].replace("\"", "'")) + '"' \
                  + ',raw_ad_data=' + '"' + str(item['raw_ad_data'].replace("\"", "'")) + '"' \
                  + ',read_count=' + '"' + str(item['read_count'].replace("\"", "'")) + '"' \
                  + ',repin_count=' + '"' + str(item['repin_count'].replace("\"", "'")) + '"' \
                  + ',rid=' + '"' + str(item['rid'].replace("\"", "'")) + '"' \
                  + ',share_count=' + '"' + str(item['share_count'].replace("\"", "'")) + '"' \
                  + ',share_info=' + '"' + str(item['share_info'].replace("\"", "'")) + '"' \
                  + ',share_url=' + '"' + str(item['share_url'].replace("\"", "'")) + '"' \
                  + ',show_dislike=' + '"' + str(item['show_dislike'].replace("\"", "'")) + '"' \
                  + ',show_portrait=' + '"' + str(item['show_portrait'].replace("\"", "'")) + '"' \
                  + ',show_portrait_article=' + '"' + str(item['show_portrait_article'].replace("\"", "'")) + '"' \
                  + ',source=' + '"' + str(item['source'].replace("\"", "'")) + '"' \
                  + ',source_avatar=' + '"' + str(item['source_avatar'].replace("\"", "'")) + '"' \
                  + ',tag=' + '"' + str(item['tag'].replace("\"", "'")) + '"' \
                  + ',tag_id=' + '"' + str(item['tag_id'].replace("\"", "'")) + '"' \
                  + ',title=' + '"' + str(item['title'].replace("\"", "'")) + '"' \
                  + ',url=' + '"' + str(item['url'].replace("\"", "'")) + '"' \
                  + ',user_repin=' + '"' + str(item['user_repin'].replace("\"", "'")) + '"' \
                  + ',user_verified=' + '"' + str(item['user_verified'].replace("\"", "'")) + '"' \
                  + ',video_detail_info=' + '"' + str(item['video_detail_info'].replace("\"", "'")) + '"' \
                  + ',video_duration=' + '"' + str(item['video_duration'].replace("\"", "'")) + '"' \
                  + ',video_id=' + '"' + str(item['video_id'].replace("\"", "'")) + '"' \
                  + ',video_play_info=' + '"' + str(item['video_play_info'].replace("\"", "'")) + '"' \
                  + ',video_proportion_article=' + '"' + str(item['video_proportion_article'].replace("\"", "'")) + '"' \
                  + ',video_style=' + '"' + str(item['video_style'].replace("\"", "'")) + '"' \
                  + ',update_time=' + '"' + str(updateTime) + '"' \
                  + ',amount=' + '"' + str(amount) + '"' \
                  + ' where id=' + '"' + str(id) + '"'
            try:
                # 执行SQL语句
                toutiao_cursor.execute(sql)
                toutiao_cursor.execute(
                    """INSERT INTO toutiao_ad_to_parameter (toutiao_ad_id, toutiao_para_id,time) VALUES(%s,%s,%s)""",
                    (str(id), str(item['parameter_id']), datetime.datetime.now()))
                large_image_list = item['large_image_list'].encode('utf-8')
                img = large_image_list[1:len(large_image_list) - 1].replace('\'', '"')
                img = json.loads(img).get('url')
                if img is None:
                    img = json.loads(large_image_list[1:len(large_image_list) - 1].replace('\'', '"')).get('uri')
                # 保存图片
                # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
                image_path = "D:/touttiao_image/"
                filename = img
                urllib.request.urlretrieve(img, image_path + '%s' % filename)
                # 提交到数据库执行
                db.commit()
                toutiao_cursor.close()
                # cursor2.close()
            except:
                # 发生错误时回滚
                db.rollback()
                toutiao_cursor.close()
        return item


class SouhuAppPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8", use_unicode=True)
        resource_text = str(eval(item['resource'])['text'])
        adid = str(item['adid'])
        sel_sql = "SELECT * FROM souhu_app WHERE MATCH(resource_text) AGAINST('" + resource_text + "')" + " OR MATCH(adid) AGAINST('" + adid + "')"
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        # 用source和title来判断数据是否已经存在
        if not cam_row:
            curTime = datetime.datetime.now()
            curTime.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""INSERT INTO souhu_app 
                  (monitorkey, resource,resource_text, resource2,weight, itemspaceid,resource1,
                  impressionid,special,offline,adid,viewmonitor,size,online,position,
                  tag,editNews,statsType,isPreload,newsType,gbcode,commentNum,isHasSponsorships,
                  recomTime,newsId,iconNight,isWeather,isRecom,iconText,link,
                  iconDay,abposition,adType,playTime,adp_type,isFlash,isHasTv,newschn,create_time)  
                                VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,
                                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                   %s, %s, %s, %s, %s, %s, %s, %s)""", (
                item['monitorkey'].encode('utf-8'),
                item['resource'].encode('utf-8'),
                resource_text,
                item['resource2'].encode('utf-8'),
                item['weight'].encode('utf-8'),
                item['itemspaceid'].encode('utf-8'),
                item['resource1'].encode('utf-8'),
                item['impressionid'].encode('utf-8'),
                item['special'].encode('utf-8'),
                item['offline'].encode('utf-8'),
                item['adid'].encode('utf-8'),
                item['viewmonitor'].encode('utf-8'),
                item['size'].encode('utf-8'),
                item['online'].encode('utf-8'),
                item['position'].encode('utf-8'),
                item['tag'].encode('utf-8'),
                item['editNews'].encode('utf-8'),
                item['statsType'].encode('utf-8'),
                item['isPreload'].encode('utf-8'),
                item['newsType'].encode('utf-8'),
                item['gbcode'].encode('utf-8'),
                item['commentNum'].encode('utf-8'),
                item['isHasSponsorships'].encode('utf-8'),
                item['recomTime'].encode('utf-8'),
                item['newsId'].encode('utf-8'),
                item['iconNight'].encode('utf-8'),
                item['isWeather'].encode('utf-8'),
                item['isRecom'].encode('utf-8'),
                item['iconText'].encode('utf-8'),
                item['link'].encode('utf-8'),
                item['iconDay'].encode('utf-8'),
                item['abposition'].encode('utf-8'),
                item['adType'].encode('utf-8'),
                item['playTime'].encode('utf-8'),
                item['adp_type'].encode('utf-8'),
                item['isFlash'].encode('utf-8'),
                item['isHasTv'].encode('utf-8'),
                item['newschn'].encode('utf-8'),
                curTime))
            souhu_ad_id = str(cursor.lastrowid)
            cursor.execute(
                """INSERT INTO souhu_ad_to_parameter (souhu_ad_id, souhu_para_id,time) VALUES(%s,%s,%s)""",
                (souhu_ad_id, str(item['parameter_id']), curTime))
            # 保存图片
            # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
            resource = item['resource1'].replace('\'', '"')
            j = json.loads(resource)
            img = j.get('file')
            image_path = "D:/souhu_image/"
            filename = img
            urllib.request.urlretrieve(img, image_path + '%s' % filename)
            db.commit()
        else:
            updateTime = datetime.datetime.now()
            updateTime.strftime('%Y-%m-%d %H:%M:%S')
            id = cam_row[0]
            cursor1 = db.cursor()
            amount = cam_row[41] + 1
            sql = 'update souhu_app set monitorkey =' + '"' + str(item['monitorkey']) + '"' \
                  + ',resource=' + '"' + str(item['resource']) + '"' \
                  + ',resource2=' + '"' + str(item['resource2']) + '"' \
                  + ',weight=' + '"' + str(item['weight']) + '"' \
                  + ',itemspaceid=' + '"' + str(item['itemspaceid']) + '"' \
                  + ',resource1=' + '"' + str(item['resource1']) + '"' \
                  + ',impressionid=' + '"' + str(item['impressionid']) + '"' \
                  + ',special=' + '"' + str(item['special']) + '"' \
                  + ',offline=' + '"' + str(item['offline']) + '"' \
                  + ',adid=' + '"' + str(item['adid']) + '"' \
                  + ',viewmonitor=' + '"' + str(item['viewmonitor']) + '"' \
                  + ',size=' + '"' + str(item['size']) + '"' \
                  + ',online=' + '"' + str(item['online']) + '"' \
                  + ',position=' + '"' + str(item['position']) + '"' \
                  + ',tag=' + '"' + str(item['tag']) + '"' \
                  + ',editNews=' + '"' + str(item['editNews']) + '"' \
                  + ',statsType=' + '"' + str(item['statsType']) + '"' \
                  + ',isPreload=' + '"' + str(item['isPreload']) + '"' \
                  + ',newsType=' + '"' + str(item['newsType']) + '"' \
                  + ',gbcode=' + '"' + str(item['gbcode']) + '"' \
                  + ',commentNum=' + '"' + str(item['commentNum']) + '"' \
                  + ',isHasSponsorships=' + '"' + str(item['isHasSponsorships']) + '"' \
                  + ',recomTime=' + '"' + str(item['recomTime']) + '"' \
                  + ',newsId=' + '"' + str(item['newsId']) + '"' \
                  + ',iconNight=' + '"' + str(item['iconNight']) + '"' \
                  + ',isWeather=' + '"' + str(item['isWeather']) + '"' \
                  + ',isRecom=' + '"' + str(item['isRecom']) + '"' \
                  + ',iconText=' + '"' + str(item['iconText']) + '"' \
                  + ',link=' + '"' + str(item['link']) + '"' \
                  + ',iconDay=' + '"' + str(item['iconDay']) + '"' \
                  + ',abposition=' + '"' + str(item['abposition']) + '"' \
                  + ',adType=' + '"' + str(item['adType']) + '"' \
                  + ',playTime=' + '"' + str(item['playTime']) + '"' \
                  + ',adp_type=' + '"' + str(item['adp_type']) + '"' \
                  + ',isFlash=' + '"' + str(item['isFlash']) + '"' \
                  + ',newschn=' + '"' + str(item['newschn']) + '"' \
                  + ',isHasTv=' + '"' + str(item['isHasTv']) + '"' \
                  + ',update_time=' + '"' + str(updateTime) + '"' \
                  + ',amount=' + '"' + str(amount) + '"' \
                  + ' where id=' + '"' + str(id) + '"'
            try:
                # 执行SQL语句
                cursor1.execute(sql)
                cursor1.execute(
                    """INSERT INTO souhu_ad_to_parameter (souhu_ad_id, souhu_para_id,time) VALUES(%s,%s,%s)""",
                    (str(id), str(item['parameter_id']), datetime.datetime.now()))
                # 保存图片
                # image_path ="/usr/local/Sina/ImageFile" #linux保存地址
                resource = item['resource1'].replace('\'', '"')
                j = json.loads(resource)
                img = j.get('file')
                image_path = "D:/souhu_image/"
                filename = img
                urllib.request.urlretrieve(img, image_path + '%s' % filename)
                # 提交到数据库执行
                db.commit()
                cursor1.close()
            except:
                # 发生错误时回滚
                db.rollback()
                cursor1.close()
        return item


class FenghuangAppPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8", use_unicode=True)
        adId = str(item['adId'])
        title = item['title']
        sel_sql = "SELECT * FROM fenghuang_app WHERE MATCH(adId) AGAINST('" + adId + "')" + " OR MATCH(title) AGAINST('" + title + "')"
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        curTime = datetime.datetime.now()
        curTime.strftime('%Y-%m-%d %H:%M:%S')
        # 用source和title来判断数据是否已经存在
        if not cam_row:
            cursor.execute("""INSERT INTO fenghuang_app 
                  (thumbnail, title,appSource, intro,adId, adPositionId,type,
                  source,weburl,view,images,create_time)  
                                VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)""", (
                item['thumbnail'],
                item['title'],
                item['appSource'],
                item['intro'],
                item['adId'],
                item['adPositionId'],
                item['type'],
                item['source'],
                item['weburl'],
                item['view'],
                item['images'],
                curTime))
            fenghuang_ad_id = str(cursor.lastrowid)
            cursor.execute(
                """INSERT INTO fenghuang_ad_to_parameter (fenghuang_ad_id, fenghuang_para_id,time) VALUES(%s,%s,%s)""",
                (fenghuang_ad_id, str(item['parameter_id']), curTime))
            db.commit()
        else:
            updateTime = datetime.datetime.now()
            updateTime.strftime('%Y-%m-%d %H:%M:%S')
            id = cam_row[0]
            cursor1 = db.cursor()
            amount = cam_row[14] + 1
            sql = """update fenghuang_app set thumbnail = %s ,title = %s ,appSource = %s ,intro = %s ,
                    adPositionId = %s ,type = %s ,source = %s ,weburl = %s ,view = %s ,images = %s, 
                    update_time = %s, amount =%s where adId = %s"""
            try:
                # 执行SQL语句
                cursor1.execute(sql, (item['thumbnail'], item['title'], item['appSource'], item['intro'],
                                      item['adPositionId'], item['type'], item['source'], item['weburl'],
                                      item['view'], item['images'], curTime,amount, item['adId'],))
                cursor1.execute(
                    """INSERT INTO fenghuang_ad_to_parameter (fenghuang_ad_id, fenghuang_para_id,time) VALUES(%s,%s,%s)""",
                    (str(id), str(item['parameter_id']), datetime.datetime.now()))
                # 提交到数据库执行
                db.commit()
                cursor1.close()
            except:
                # 发生错误时回滚
                db.rollback()
                cursor1.close()
        return item

class ToutiaoxinwenAppPipeline(object):
    def process_item(self, item, spider):
        db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                             charset="utf8", use_unicode=True)
        title = str(item['title'])
        sel_sql = "SELECT * FROM toutiaoxinwen_app WHERE MATCH(title) AGAINST('" + title + "')"
        cursor = db.cursor()
        cursor.execute(sel_sql)
        cam_row = cursor.fetchone()
        curTime = datetime.datetime.now()
        curTime.strftime('%Y-%m-%d %H:%M:%S')
        # 用source和title来判断数据是否已经存在
        if not cam_row:
            cursor.execute("""INSERT INTO toutiaoxinwen_app 
                  (title, data_description, ad_id, url, publisher,img_url,create_time)  
                                VALUES (%s, %s, %s, %s, %s,%s, %s)""", (
                item['title'],
                item['data_description'],
                item['ad_id'],
                item['url'],
                item['publisher'],
                item['img_url'],
                curTime))
            toutiaoxinwen_ad_id = str(cursor.lastrowid)
            cursor.execute(
                """INSERT INTO toutiaoxinwen_ad_to_parameter (toutiaoxinwen_ad_id, toutiaoxinwen_para_id,time) VALUES(%s,%s,%s)""",
                (toutiaoxinwen_ad_id, str(item['parameter_id']), curTime))
            db.commit()
        else:
            updateTime = datetime.datetime.now()
            updateTime.strftime('%Y-%m-%d %H:%M:%S')
            id = cam_row[0]
            amount = cam_row[9] + 1
            cursor1 = db.cursor()
            sql = """update toutiaoxinwen_app set ad_id = %s ,data_description = %s ,url = %s ,
                    publisher = %s ,img_url = %s ,update_time = %s, amount= %s  where title = %s"""
            try:
                # 执行SQL语句
                cursor1.execute(sql, (item['ad_id'], item['data_description'], item['url'], item['publisher'],
                                      item['img_url'],  curTime, amount, item['title'],))
                cursor1.execute(
                    """INSERT INTO toutiaoxinwen_ad_to_parameter (toutiaoxinwen_ad_id, toutiaoxinwen_para_id,time) VALUES(%s,%s,%s)""",
                    (str(id), str(item['parameter_id']), datetime.datetime.now()))
                # 提交到数据库执行
                db.commit()
                cursor1.close()
            except:
                # 发生错误时回滚
                db.rollback()
                cursor1.close()
        return item

class QutoutiaoAppPipeline(object):
    pass
