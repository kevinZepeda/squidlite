import sys
import logging
from datetime import datetime
from rules import is_blocked

logging.basicConfig(filename='squid-redirect.log',level=logging.DEBUG)

def main():

    request  = sys.stdin.readline()
    while request:
        [ch_id,url,ipaddr,method,user]=request.split()
        logging.debug(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + request +'\n')
        response  = ch_id + ' OK'
        if is_blocked(url, ipaddr):
            response +=  ' rewrite-url=http://www.myattmx.com/api/blocked?JNI_URL=' + str(url) + '&JNI_SRCIP=' + str(ipaddr)
            logging.debug(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + url + 'Redirected' +'\n')
        logging.debug(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' ' IP: '+ ipaddr + url + 'Redirected' +'\n')
        response += '\n'
        sys.stdout.write(response)
        sys.stdout.flush()
        request = sys.stdin.readline()

if __name__ == '__main__':
    main()