from urllib.request import urlopen
import warnings,os,json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'

def load():
    '''
    下载并返回JSON的python原生对象
    '''
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL,JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote,open(JSON,'wb',encoding='utf-8') as local:
            local.write(remote.read())
        
    with open(JSON,encoding='utf-8') as fq:
        return json.load(fq)

