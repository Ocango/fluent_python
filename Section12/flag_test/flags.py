import os
import time
import sys

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR'
).split()
BASE_URL = 'http://flupy.org/data/flags'

DEST_URL = 'downloads/'


def save_flags(img,filename):
    path = os.path.join(DEST_URL,filename)
    with open(path,'wb') as fp:
        fp.write(img)

def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL,cc=cc.lower())
    resp = requests.get(url)
    return resp.content

def show(text):
    print(text,end=' ')
    sys.stdout.flush()#刷新缓存区，就是立即显示

def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flags(image,cc.lower() + '.gif')
    
    return len(cc_list)

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloading in {:.2f}s'
    print(msg.format(count,elapsed))

if __name__ == '__main__':
    main(download_many)