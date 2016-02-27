# coding=utf8
#!/usr/bin/env python

#################################
#
# 有道查词 for Alfred Wordflows
# Authors: Zeek Wang
#
#################################


import urllib2
import json
import sys
import alfred

reload(sys)
sys.setdefaultencoding("utf-8")

base_url = "http://fanyi.youdao.com/openapi.do?keyfrom=YouDaoWorkflow&key=514771982&type=data&doctype=json&version=1.1&only=dict&q=";

def item(title, sub_title, icon="icon.png"):
    return alfred.Item({"arg": title}, title, sub_title, icon);

def query_api(word):
    url = base_url + word;
    result = json.load(urllib2.urlopen(url))
    return result;

def handle_error(query_result, output):
    error_code = query_result["errorCode"];
    status = True;
    if (error_code == 60) or (error_code == 0 and not "basic" in query_result):
        output.append(item("无此单词释义", "", icon="icon.png"));
        status = False;
    elif error_code != 0:
        output.append(item("有道查词错误", "", icon="icon.png"));
        status = False;
    return status;

def output_word_explains(word, query_result, output):
    basic = query_result["basic"];
    explains = basic["explains"];
    title = " ".join(explains);
    sub_title = word;
    if "us-phonetic" in basic:
        sub_title += "  美:[" + basic["us-phonetic"] + "]";
    if "uk-phonetic" in basic:
        sub_title += "  英:[" + basic["uk-phonetic"] + "]";
    output.append(item(title, sub_title));
    for explain in explains:
        output.append(item(explain, word));

def query_word(word):
    output = [];
    result = query_api(word);
    if handle_error(result, output):
        output_word_explains(word, result, output);
    
    xml = alfred.xml(output)
    return xml;

def query_phonetic(word):
    output = [];
    result = query_api(word);
    if handle_error(result, output):
        basic = result["basic"];
        if "us-phonetic" in basic:
            output.append(item(basic["us-phonetic"], word + " 美式音标"));
        if "uk-phonetic" in basic:
            output.append(item(basic["uk-phonetic"], word + " 英式音标"));
        output_word_explains(word, result, output);
    
    xml = alfred.xml(output)
    return xml;    


if __name__ == '__main__':
    query_word("test");