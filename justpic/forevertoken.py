#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from baidupcs.tools import get_new_access_token
# refresh_token='22.e2af831a914d80d3fe47cbfb7d11b22a.315360000.1714727227.3875775130-1056026'
# access_token='21.7db53becd91fe93afad905c4f91ab4ca.2592000.1401958847.3875775130-1056026'
# client_id='oA8jMPTjA8yrtaGsc2i5HHdx'
# client_secret='kas6A0XFr7uArRnXL4Da0GCvyxRqRiWw'
# scope='netdisk'
# response=get_new_access_token(refresh_token,client_id,client_secret,scope)
# print response.json()
# access_token=response.json()['access_token']
# refresh_token=response.json()['refresh_token']
# print access_token
# print refresh_token
# access_token='21.ac128af3d73bf4ba98c496534f5a8dc6.2592000.1401959227.3875775130-1056026'

import os
import time

from utils import content_md5, content_crc32, slice_md5
from vendor.baidupcs import PCS, InvalidToken

access_token = '21.9403b998cd9b271fa44a54199aad2949.2592000.1401980588.3875775130-1056026'
pcs = PCS(access_token)


verify = True
# verify = False  # 因为在我电脑上会出现 SSLError 所以禁用 https 证书验证


def _file(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    f = open(filepath, 'rb')  # rb 模式
    return f


def test_invalidtoken():
    try:
        PCS('abc').info()
    except InvalidToken:
        assert True
    else:
        assert False


def test_upload():
    """上传"""
    response = pcs.upload('/apps/justpic/test.txt', _file('test1'),
                          ondup='overwrite', verify=verify)
    assert response.ok and response.json()

    response = pcs.upload('/apps/justpic/test.txt', _file('test1'),
                          ondup='overwrite', verify=verify,
                          headers={'Accept': '*/*'})
    assert response.ok and response.json()


def test_upload_tmpfile():
    """分片上传 - 上传临时文件"""
    response = pcs.upload_tmpfile(_file('test1'), verify=verify)
    assert response.ok and response.json()


def test_upload_superfile():
    f1_md5 = pcs.upload_tmpfile(_file('test1'), verify=verify).json()['md5']
    f2_md5 = pcs.upload_tmpfile(_file('test2'), verify=verify).json()['md5']
    time.sleep(1)
    response = pcs.upload_superfile('/apps/test_sdk/super2.txt',
                                    [f1_md5, f2_md5], ondup='overwrite')
    assert response.ok and response.json()


def test_download():
    response = pcs.download('/apps/test_sdk/super2.txt', verify=verify)
    assert response.ok and 'abc'.encode() in response.content


def test_download_range():
    test_upload_superfile()
    headers = {'Range': 'bytes=0-2'}
    response1 = pcs.download('/apps/test_sdk/super2.txt', headers=headers,
                             verify=verify)
    assert response1.content == 'abc'.encode()
    headers = {'Range': 'bytes=3-5'}
    response2 = pcs.download('/apps/test_sdk/super2.txt', headers=headers,
                             verify=verify)
    assert response2.content == 'def'.encode()


def test_mkdir():
    response = pcs.mkdir('/apps/test_sdk/testmkdir')
    assert response.json()
    if not response.ok:
        assert response.json()['error_code'] == 31061


def test_meta():
    response = pcs.meta('/apps/test_sdk/super2.txt')
    assert response.ok and response.json()


def test_multi_meta():
    response = pcs.multi_meta(['/apps/test_sdk/super2.txt',
                              '/apps/test_sdk/testmkdir'])
    assert response.ok and response.json()


def test_list_files():
    response = pcs.list_files('/apps/test_sdk/testmkdir')
    assert response.ok and response.json()


def test_move():
    response = pcs.move('/apps/test_sdk/test.txt',
                        '/apps/test_sdk/testmkdir/a.txt')
    assert response.json()
    if not response.ok:
        assert response.json()['error_code'] == 31061


def test_multi_move():
    pcs.upload('/apps/test_sdk/test.txt', _file('test1'), verify=verify)
    pcs.upload('/apps/test_sdk/b.txt', _file('test1'), verify=verify)
    path_list = [
        ('/apps/test_sdk/test.txt', '/apps/test_sdk/testmkdir/b.txt'),
        ('/apps/test_sdk/b.txt', '/apps/test_sdk/testmkdir/a.txt'),
    ]
    time.sleep(1)
    response = pcs.multi_move(path_list)
    if not response.ok:
        assert response.json()['error_code'] == 31061


def test_copy():
    pcs.upload('/apps/test_sdk/test.txt', _file('test1'), verify=verify)
    response = pcs.copy('/apps/test_sdk/test.txt',
                        '/apps/test_sdk/testmkdir/c.txt')
    if not response.ok:
        assert response.json()['error_code'] == 31061


def test_multi_copy():
    pcs.upload('/apps/test_sdk/test.txt', _file('test1'), verify=verify)
    pcs.upload('/apps/test_sdk/b.txt', _file('test2'), verify=verify)
    path_list = [
        ('/apps/test_sdk/test.txt', '/apps/test_sdk/testmkdir/b.txt'),
        ('/apps/test_sdk/b.txt', '/apps/test_sdk/testmkdir/a.txt'),
    ]
    time.sleep(1)
    response = pcs.multi_copy(path_list)
    if not response.ok:
        assert response.json()['error_code'] == 31061


def test_delete():
    pcs.upload('/apps/test_sdk/testmkdir/e.txt', _file('test3'), verify=verify)
    time.sleep(1)
    response = pcs.delete('/apps/test_sdk/testmkdir/e.txt')
    assert response.ok


def test_multi_delete():
    pcs.upload('/apps/test_sdk/testmkdir/e.txt', _file('test1'), verify=verify)
    pcs.upload('/apps/test_sdk/testmkdir/d.txt', _file('test2'), verify=verify)
    time.sleep(1)
    response = pcs.multi_delete(['/apps/test_sdk/testmkdir/e.txt',
                                '/apps/test_sdk/testmkdir/d.txt'])
    assert response.ok


def test_search():
    response = pcs.upload('/apps/test_sdk/test.txt', _file('test1'),
                          ondup='overwrite', verify=verify)
    response = pcs.search('/apps/test_sdk/', 'test')
    assert response.ok


def test_thumbnail():
    response = pcs.thumbnail('/apps/justpic/5K/118000/118097.jpeg', 512, 512)
    print response.url
    # im = Image.open(StringIO(response.content))
    # im.show()
    assert response.ok


def test_diff():
    pcs.upload('/apps/test_sdk/testmkdir/h.txt', _file('test2'),
               ondup='overwrite', verify=verify)
    response0 = pcs.diff()
    new_cursor = response0.json()['cursor']

    time.sleep(1)
    pcs.upload('/apps/test_sdk/testmkdir/h.txt', str(time.time()),
               ondup='overwrite', verify=verify)
    response1 = pcs.diff(cursor=new_cursor)
    new_cursor = response1.json()['cursor']

    time.sleep(1)
    pcs.upload('/apps/test_sdk/testmkdir/h.txt', str(time.time()),
               ondup='overwrite', verify=verify)
    response2 = pcs.diff(cursor=new_cursor)
    assert response2.ok and response2.json()


def test_video_convert():
    response = pcs.video_convert('/apps/test_sdk/testmkdir/test.mp4',
                                 'M3U8_320_240')
    assert response.ok


def test_list_streams():
    response1 = pcs.list_streams('image')
    response2 = pcs.list_streams('doc', filter_path='/apps/test_sdk/test')
    assert response2.ok


def test_download_stream():
    response = pcs.download_stream('/apps/test_sdk/testmkdir/404.png',
                                   verify=verify)
    assert response.ok


def test_rapid_upload():
    content = ('a' * 1024 * 1024).encode('utf8')
    pcs.upload('/apps/test_sdk/testmkdir/upload.txt', content,
               ondup='overwrite', verify=verify)
    time.sleep(1)
    response = pcs.rapid_upload('/apps/test_sdk/testmkdir/rapid.txt',
                                len(content), content_md5(content),
                                content_crc32(content),
                                slice_md5(content[:1024 * 256]),
                                ondup='overwrite')
    assert response.ok


def test_add_download_task():
    url = 'http://img3.douban.com/pics/nav/logo_db.png'
    remote_path = '/apps/test_sdk/testmkdir/bdlogo.gif'
    response = pcs.add_download_task(url, remote_path)
    assert response.ok


def test_query_download_tasks():
    url1 = 'http://img3.douban.com/pics/nav/lg_main_a11_1.png'
    url2 = 'http://img3.douban.com/pics/nav/logo_db.png'
    remote_path = '/apps/test_sdk/testmkdir/%s'
    task1 = pcs.add_download_task(url1, remote_path % os.path.basename(url1))
    task2 = pcs.add_download_task(url2, remote_path % os.path.basename(url2))

    time.sleep(1)
    task_ids = [task1.json()['task_id'], task2.json()['task_id']]
    response = pcs.query_download_tasks(task_ids)
    assert response.ok


def test_list_download_tasks():
    response = pcs.list_download_tasks()
    assert response.ok


def test_cancel_download_task():
    response = pcs.list_download_tasks()
    task_info = response.json()['task_info']
    if task_info:
        task_id = task_info[0]['task_id']
        response2 = pcs.cancel_download_task(task_id)
        assert response2.ok


def test_list_recycle_bin():
    pcs.upload('/apps/test_sdk/testmkdir/10.txt', _file('test2'),
               ondup='overwrite', verify=verify)
    time.sleep(1)
    pcs.delete('/apps/test_sdk/testmkdir/10.txt')
    time.sleep(1)
    response = pcs.list_recycle_bin()
    assert response.ok


def test_restore_recycle_bin():
    pcs.upload('/apps/test_sdk/testmkdir/10.txt', _file('test1'),
               ondup='overwrite', verify=verify)
    pcs.delete('/apps/test_sdk/testmkdir/10.txt')

    time.sleep(1)
    response1 = pcs.list_recycle_bin()
    fs_id = response1.json()['list'][0]['fs_id']
    response = pcs.restore_recycle_bin(fs_id)
    assert response.ok


def test_multi_restore_recycle_bin():
    pcs.upload('/apps/test_sdk/testmkdir/1.txt', _file('test2'),
               ondup='overwrite', verify=verify)
    time.sleep(1)
    pcs.delete('/apps/test_sdk/testmkdir/1.txt')
    pcs.upload('/apps/test_sdk/testmkdir/2.txt', _file('test1'),
               ondup='overwrite', verify=verify)

    time.sleep(1)
    pcs.delete('/apps/test_sdk/testmkdir/2.txt')
    time.sleep(1)
    response1 = pcs.list_recycle_bin()
    fs_ids = [x['fs_id'] for x in response1.json()['list'][:1]]
    response = pcs.multi_restore_recycle_bin(fs_ids)
    assert response.ok


def test_clean_recycle_bin():
    response = pcs.clean_recycle_bin()
    assert response.ok

if __name__=="__main__":
    # test_invalidtoken()
    # test_upload()
    test_thumbnail()

