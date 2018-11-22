'''
Created on 2018年4月8日

@author: xzl
'''
import json

##用于判断一个字符串是否符合Json格式
def check_json_format(raw_msg):
    if isinstance(raw_msg, str):    # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False

##字典参数拼接后返回url参数
def parameter_back_url_p(parameter):
    back_str =''
    for key in parameter:
        back_str += "&"+ key +"="+str(parameter[key])
    return back_str[1:]