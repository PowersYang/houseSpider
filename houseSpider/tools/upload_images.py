# -*- coding: utf-8 -*-
"""
    图片上传脚本
"""
import hashlib
import json
import os
import datetime
import time

import requests
import schedule as schedule



token = None

file_system_appKey = '011aa03506134a87bd6d4991bc5e0645'

file_upload_url = 'http://hup.demo.ejie365.cn/file/syncUploadFile'

get_token_url = 'http://ssonew.demo.ejie365.cn/userLogin'

insert_data_url = 'http://housedata.ejie.cn/insertAttachmentInfo'


def get_public_token():
    """
    获取token
    :return: token
    """

    params = {
        "account": "NO00003573",
        "pwd": "1234567890",
        "isPhone": "N",
        "appKey": "1d1271546889469f93c313efc74e5bd1"
    }

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json'
    }

    res = requests.post(get_token_url, json=params, headers=headers)
    res = json.loads(res.text)
    if str(res.get('code')) == '0':
        return str(res.get('token'))
    else:
        return None


def read_iamges():
    """
    读取图片
    :return:
    """

    for dirpath, dirnames, filenames in os.walk("D:\houseImages"):
        if filenames is None:
            yield None
        for filename in filenames:
            fromType = dirpath.split("\\")[-2]
            extId = dirpath.split("\\")[-1]
            yield {
                'filename': dirpath + '/' + filename,
                'extId': extId,
                'fromType': fromType
            }


def upload_images(filename, token, extId, fromType, remarks):
    """
    上传图片
    :param fielname: 图片名
    :param token: toekn
    :param remarks: 备注
    :return:
    """
    print(u"上传开始...")
    params = {
        'appKey': file_system_appKey,
        'file': (filename, open(filename, mode='rb'), 'text/plain'),
        'remarks': remarks
    }

    headers = {
        'Accept': 'application/json;charset=UTF-8',
        'Authorization': token,
    }

    files = {'file': open(filename, 'rb')}  # 文件
    res = requests.post(file_upload_url, data=params, files=files, headers=headers)
    res = json.loads(res.text)
    if str(res.get('status')) == '1':
        print(u"上传成功...")
        md1 = hashlib.md5()
        md1.update(filename.encode('utf-8'))
        attachment_id = md1.hexdigest()
        classify_id = 0
        if "community" in fromType:
            classify_id = 1
        hup_id = res.get('data').get('attachId')
        thumb_url = res.get('data').get('thumbUrl')
        attachment_type = res.get('data').get('fileType')
        attachment_name = res.get('data').get('fileName')
        extId = extId
        remarks = remarks
        tag = res.get('data').get('tag')

        return {'attachmentId': attachment_id, 'classifyId': classify_id, 'hupId': hup_id,
                'thumbUrl': thumb_url, 'attachmentType': attachment_type, 'attachmentName': attachment_name,
                'extid': extId, 'remark': remarks, 'tag': tag}

    else:
        print(res.get('data').get('msg'))
        return None


def isExistByMD5Value():
    """
    验证文件是否存在
    :return:
    """
    headers = {
        'Accept': 'application/json;charset=UTF-8',
        'Authorization': token
    }

    params = {
        'appKey': file_system_appKey,

        'md5Value': 'E40742D1FBE502E5861994719777074B'
    }

    res = requests.post('http://hup.demo.ejie365.cn/file/isExistByMD5Value', data=params, headers=headers)
    print(res.text)


def insert_data(data, token):
    headers = {
        'Content-Type': 'application/json',
        'token': token
    }

    params = [data]

    res = requests.post(insert_data_url, json=params, headers=headers)
    js = json.loads(res.text)
    if str(js.get('status')) == '1' and str(js.get('message')) == u"添加成功":
        print(u"上传记录已保存...")
        return True
    else:
        print(u"上传记录保存失败...")
        print(u"失败信息: " + str(data))
        return False


def task():
    token = get_public_token()
    file_list = read_iamges()
    for item in file_list:
        print('---------------------------')
        filename = item['filename']
        ext_id = item['extId']
        from_type = item['fromType']

        upload_res = upload_images(filename, token, ext_id, from_type, '')
        if upload_res is not None:

            if insert_data(upload_res, token):
                os.remove(filename)  # 上传成功之后删除本地文件


if __name__ == '__main__':
    # 任务开始时间
    start_time = "00:10"

    # 执行周期
    schedule.every().day.at(start_time).do(task)
    while True:
        schedule.run_pending()
        time.sleep(10)

    # task()


