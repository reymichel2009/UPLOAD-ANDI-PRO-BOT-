import os
import ProxyCloud

BOT_TOKEN =  os.environ.get('bot_token','5626538071:AAFGwvwPpVC-0RiKX3fRRqaQnhcRFEN3zyc')
API_ID =  os.environ.get('api_id','18641760')
API_HASH = os.environ.get('api_hash','b7b026ce9d1d36400c02dc21d8df53a3')
SPLIT_FILE = 1024 * 1024 * int(os.environ.get('split_file','99'))
ROOT_PATH = 'root/'
ACCES_USERS = os.environ.get('tl_admin_user','user12').split(';')
PROXY = ProxyCloud.parse(os.environ.get('proxy_enc','http://KFDDKDYEJIJFGFYDJEGKGJYEIJIIRDGELGGJKG'))

if PROXY:
  print(f'Proxy {PROXY.as_dict_proxy()}')
