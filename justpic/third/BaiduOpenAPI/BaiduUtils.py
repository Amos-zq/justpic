#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'guan hua (guanhua2011@gmail.com)'

'''
http object class
'''

import json
import urllib
import urllib2
import time
import OpenApiError
from md5 import md5

class HttpObject():  
    __HTTP_GET = 1
    __HTTP_POST = 2
    __HTTP_UPLOAD = 3
    
    def params_encode(self,  **args):
        '''
        Encode params
        '''
        params = []
        for key,  value in args.iteritems():
            v = value.encode('utf-8') if isinstance(value,  unicode) else str(value)
            params.append('%s=%s' % (key,  urllib.quote(v)))
        return '&'.join(params)
        
    def __get_file_type(self,  ext):
        '''
        Get file type
        '''
        file_types = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg'}
        return file_types.get(ext,  'application/octet-stream')
    
    def __multipart_encode(self,  **args):
        '''
        Build a multipart/form-data body with generated random boundary.
        '''
        boundary = '---------%s' % hex(int(time.time() * 1000))
        data = []
        for key,  value in args.iteritems():
            data.append('--%s' % boundary)
            if hasattr(value,  'read'):
                ext = ''
                filename = getattr(value,  'name',  '')
                n = filename.rfind('.')
                if -1 != n:
                    ext = filename[n:].lower()
                content = value.read()
                data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % key)
                data.append('Content-Length: %d' % len(content))
                data.append('Content-Type: %s\r\n' % self.__get_file_type(ext))
                data.append(content)
            else:
                data.append('Content-Disposition: form-data; name="%s"\r\n' % key)
                data.append(value.encode('utf-8') if isinstance(value, unicode) else value)
        data.append('--%s--\r\n' % boundary)
        return '\r\n'.join(data), boundary
        
    def get(self,  url = None,  **args):
        return self.__call(url,  self.__HTTP_GET,  **args);
         
    def post(self,  url = None,  **args):
        return self.__call(url,  self.__HTTP_POST,  **args)
        
    def upload(self,  url = None,  **args):
        return self.__call(url,  self.__HTTP_UPLOAD,  **args)
    
    def __call(self,  url,  http_type,  **args):
        params = None
        boundary = None
        if http_type == self.__HTTP_UPLOAD:
            params, boundary = self.__multipart_encode(**args)
        else:
            params = self.params_encode(**args)
        http_url = '%s?%s' % (url, params) if http_type == self.__HTTP_GET else url
        http_body = None if http_type == self.__HTTP_GET else params
        req = urllib2.Request(http_url, data=http_body)
        if boundary:
            req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        try:
            res = urllib2.urlopen(req)
            body = res.read()
            ret = json.loads(body)
            return ret
        except urllib2.HTTPError,  e:
            raise OpenApiError('10001',  'HTTP Error! URL: %s' % http_url)
        except urllib2.URLError,  e:
            raise OpenApiError('10002',  'URL error: %s' % http_url)
        except ValueError,  e:
            raise OpenApiError('10003',  'Format is not json')
                
                
class BaiduUtils():
    def generate_sign(self,  params,  secret_key,  namespace = 'sign'):
        '''
        Generate the signature for passed parameters.
        '''
        keys = params.keys() 
        keys.sort()
        str = ''
        for key in keys:
            if key != namespace:
                str += key + '=' + params[key]
        str += secret_key
        m = md5()  
        m.update(str)  
        return m.hexdigest() 
    
