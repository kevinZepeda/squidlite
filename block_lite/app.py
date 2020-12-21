import sys
import logging
import logging.handlers
from datetime import datetime
from rules import is_blocked

logging.basicConfig(
        # filename='squid-redirect.log',
        level=logging.DEBUG,
        handlers=[
            logging.handlers.SysLogHandler(address=('172.31.21.190', 5000))
        ]
    )

def main():
    request  = sys.stdin.readline()
    while request:
        [ch_id,url,ipaddr,method,user]=request.split()
        logging.debug(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': request ' + request +'\n')
        response  = ch_id + ' OK'
        if is_blocked(url, ipaddr):
            response +=  ' rewrite-url=http://www.myattmx.com/api/blocked?JNI_URL=' + str(url) + '&JNI_SRCIP=' + str(ipaddr)
            logging.error(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + 'squidlite  src_ip=' + str(ipaddr)+' url=' + str(url) + ' action=REDIRECT' +'\n')
        else:
            logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + 'squidlite  src_ip=' + str(ipaddr)+' url=' + str(url) + ' action=CONNECT' +'\n')
        response += '\n'
        sys.stdout.write(response)
        sys.stdout.flush()
        request = sys.stdin.readline()

if __name__ == '__main__':
    main()