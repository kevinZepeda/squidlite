import sys
import re
import logging
import logging.handlers
from datetime import datetime
from rules import connected

logging.basicConfig(
        # filename='squid-redirect.log',
        level=logging.DEBUG,
        handlers=[
            logging.handlers.SysLogHandler(address=('172.31.21.190', 5100))
        ]
    )

def main():
    request  = sys.stdin.readline()
    while request:
        [ch_id,url,ipaddr,method,user]=request.split()
        response  = ch_id + ' OK'
        user = connected(url, ipaddr)
        if user[0]:
            response +=  ' rewrite-url=http://www.myattmx.com/api/blocked?JNI_URL=' + str(url) + '&JNI_SRCIP=' + str(ipaddr)
            logging.error(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '|squidlite|src_ip=' + str(ipaddr)+'|domain=' + user[1] + '|app=' + user[2] + '|action=REDIRECT' +'\n')
        else:
            logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '|' + 'squidlite|src_ip=' + str(ipaddr)+'|domain=' + str(re.findall(r':\/\/(.[^/]+)', url)[0] if 'http' in url else url)  + '|app=_|action=CONNECT' +'\n')
        response += '\n'
        sys.stdout.write(response)
        sys.stdout.flush()
        request = sys.stdin.readline()

if __name__ == '__main__':
    main()