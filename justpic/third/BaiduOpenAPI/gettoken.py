from BaiduOpenAPI.Baidu import Baidu

client_id='oA8jMPTjA8yrtaGsc2i5HHdx'
client_secret='kas6A0XFr7uArRnXL4Da0GCvyxRqRiWw'
redirect_uri = 'oob'
baidu=Baidu(client_id,client_secret)
auth2_server=baidu.get_baidu_oauth2_server()

authorize_url=auth2_server.get_authorize_url(scope='netdisk')
print authorize_url
#baiduapi_client=baidu.get_baidu_api_client_server()
#code=baiduapi_client.api(authorize_url)
#print code
#token=auth2_server.get_access_token_by_authorization_code(code='483d633f81d4d03eada833d42361104f')
#print token
token=auth2_server.get_access_token_by_refresh_token(refresh_token='d0abe663410bf146740d5147e4099311',scope='')
#token=auth2_server.get_access_token_by_client_credentials(scope='basic netdisk')
print token




