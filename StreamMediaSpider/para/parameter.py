import configparser
import pymysql
import os
from os import path

config = configparser.ConfigParser()
# 获取当前目录
d = path.dirname(__file__)
# 获取当前目录的父级目录
parent_path = os.path.dirname(d)
# log.msg("路径"+d,log.INFO)
config.read(parent_path + "/config/config.ini")

# 初始化数据库连接
db_host = config.get("db", "host")
db_port = config.get("db", "port")
db_user = config.get("db", "user")
db_password = config.get("db", "password")
db_name = config.get("db", "dbname")
db = pymysql.connect(user=db_user, passwd=db_password, db=db_name, host=db_host, port=int(db_port),
                     charset="utf8", use_unicode=True)


class Parameter():
    def __init__(self):
        pass

    def get_toutiao_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            url_joint = ""
            for dict_key in dict:
                if dict[dict_key] is not None:
                    if dict_key == "_as":  # mysql中as为保留关键字，所以换成了_as，这里进行转换
                        url_joint = url_joint + "&" + "as" + "=" + str(dict[dict_key])
                    else:
                        url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls

    def get_sina_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            url_joint = ""
            # for dict_key in dict:
            if dict['type'] == "ios":
                url_joint = "&resource=" + str(dict['resource']) + "&abt=" + str(dict['abt']) + "&abver=" + str(
                    dict['abver']) + "&accessToken=" + str(
                    dict['accessToken']) + "&chwm=" + str(dict['chwm']) + "&city=" + str(
                    dict['city']) + "&connectionType=" + str(
                    dict['connectionType']) + "&deviceId=" + str(dict['deviceId']) + "&deviceModel=" + str(
                    dict['deviceModel']) + "&from=" + str(dict['from']) + "&idfa=" + str(dict['idfa']) + "&idfv=" + str(
                    dict['idfv']) + "&imei=" + str(dict['imei']) + "&location=" + str(
                    dict['location']) + "&osVersion=" + str(dict['osVersion']) + "&resolution=" + str(
                    dict['resolution']) + "&seId=" + str(dict['seId']) + "&ua=" + str(
                    dict['ua']) + "&unicomFree=" + str(dict['unicomFree']) + "&weiboSuid=" + str(
                    dict['weiboSuid']) + "&weiboUid=" + str(dict['weiboUid']) + "&wm=" + str(
                    dict['wm']) + "&rand=" + str(dict['rand']) + "&urlSign=" + str(
                    dict['urlSign']) + "&behavior=" + str(dict['behavior']) + "&channel=" + str(
                    dict['channel']) + "&downTimes=" + str(dict['downTimes']) + "&downTotalTimes=" + str(
                    dict['downTotalTimes']) + "&lastTimestamp=" + str(dict['lastTimestamp']) + "&listCount=" + str(
                    dict['listCount']) + "&p=" + str(dict['p']) + "&pullDirection=" + str(
                    dict['pullDirection']) + "&pullTimes=" + str(dict['pullTimes']) + "&replacedFlag=" + str(
                    dict['replacedFlag']) + "&s=" + str(dict['s']) + "&upTimes=" + str(
                    dict['upTimes']) + "&upTotalTimes=" + str(dict['upTotalTimes'])
            if dict['type'] == "android":
                url_joint = "&resource=" + str(dict['resource']) + "&mpName=" + str(dict['mpName']) + "&lDid=" + str(
                    dict['lDid']) + "&oldChwm=" + str(dict['oldChwm']) + "&upTimes=" + str(
                    dict['upTimes']) + "&city=" + str(
                    dict['city']) + "&loginType=" + str(dict['loginType']) + "&authToken=" + str(
                    dict['authToken']) + "&channel=" + str(
                    dict['channel']) + "&link=" + str(dict['link']) + "&authGuid=" + str(
                    dict['authGuid']) + "&ua=" + str(
                    dict['ua']) + "&deviceId=" + str(dict['deviceId']) + "&connectionType=" + str(
                    dict['connectionType']) + "&resolution=" + str(dict['resolution']) + "&mac=" + str(
                    dict['mac']) + "&weiboUid=" + str(dict['weiboUid']) + "&replacedFlag=" + str(
                    dict['replacedFlag']) + "&osVersion=" + str(dict['osVersion']) + "&chwm=" + str(
                    dict['chwm']) + "&pullTimes=" + str(dict['pullTimes']) + "&weiboSuid=" + str(
                    dict['weiboSuid']) + "&andId=" + str(dict['andId']) + "&from=" + str(
                    dict['from']) + "&sn=" + str(dict['sn']) + "&behavior=" + str(
                    dict['behavior']) + "&aId=" + str(dict['aId']) + "&localSign=" + str(
                    dict['localSign']) + "&deviceIdV1=" + str(dict['deviceIdV1']) + "&todayReqTime=" + str(
                    dict['todayReqTime']) + "&osSdk=" + str(dict['osSdk']) + "&abver=" + str(
                    dict['abver']) + "&listCount=" + str(dict['listCount']) + "&accessToken=" + str(
                    dict['accessToken']) + "&downTimes=" + str(dict['downTimes']) + "&lastTimestamp=" + str(
                    dict['lastTimestamp']) + "&pullDirection=" + str(dict['pullDirection']) + "&seId=" + str(
                    dict['seId']) + "&imei=" + str(dict['imei']) + "&deviceModel=" + str(
                    dict['deviceModel']) + "&location=" + str(dict['location']) + "&authUid=" + str(
                    dict['authUid']) + "&loadingAdTimestamp=" + str(dict['loadingAdTimestamp']) + "&urlSign=" + str(
                    dict['urlSign']) + "&rand=" + str(dict['rand'])
            start_url = url + url_joint.lstrip("&").replace("is_need", "")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls


    def get_souhu_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            url_joint = ""
            for dict_key in dict:
                if dict[dict_key] is not None:
                    url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls

    def get_fenghuang_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            dict.pop("type")
            url_joint = ""
            para_id = dict.pop("_id")
            dict['id'] = para_id
            for dict_key in dict:
                if dict[dict_key] is not None:
                    url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls

    def get_tengxunxinwen_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            dict.pop("type")
            url_joint = ""
            for dict_key in dict:
                if dict[dict_key] is not None:
                    url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls

    def get_toutiaoxinwen_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            dict.pop("type")
            url_joint = ""
            for dict_key in dict:
                if dict[dict_key] is not None:
                    url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls

    def get_qutoutiao_para(spder_db_name):
        cursor = db.cursor()
        sql = "select * from " + spder_db_name
        cursor.execute(sql)
        desc = cursor.description
        parameter_list = []
        for p in desc:
            parameter_list.append(p[0])
        dict = {}
        all_para_list = cursor.fetchall()  # 所有参数list
        para_len = len(parameter_list)
        scrawl_urls = set()
        for para in all_para_list:
            for n in range(para_len):  # 将参数信息以键值对的方式保存
                dict[parameter_list[n]] = para[n]
            id = dict.pop("id")
            header = dict.pop("header")
            url = dict.pop("url")
            dict.pop("type")
            url_joint = ""
            for dict_key in dict:
                if dict[dict_key] is not None:
                    url_joint = url_joint + "&" + str(dict_key) + "=" + str(dict[dict_key])
            start_url = url + url_joint.lstrip("&")
            par_tup = (id, header, start_url)
            scrawl_urls.add(par_tup)
        return scrawl_urls