import re
import sys
from crud import get_user, get_url, delete_block, blocked_sites

def unblock(user_ip, domain):
    user = get_user(ip=user_ip).fetchone()
    url = get_url(domain=domain).fetchone()
    if user and url:
        return delete_block(user_id=user[0],url_id=url[0])
    elif user and not url:
        print("No existe la url")
    else:
        return f"User {user_ip} has no locks."


if __name__ == '__main__':
    help_message = """
Unblock User BY [user_ip]

        usage: [user_ip] [domain] | [--get] [user_ip]

        <user_ip>:  IPV4 Network user

        <domaini>:  Word included in the domain to block

         --get:     Option to get blocked sites by user

        ie: unblock.py 172.17.0.2 .google.com 
    """
    IPV4_PATTERN = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    if '--get' in sys.argv[1]:
        print(blocked_sites(sys.argv[2], all=False))
    elif re.match(IPV4_PATTERN, sys.argv[1]):
        try:
            unblock(sys.argv[1],sys.argv[2])
            print(blocked_sites(sys.argv[1], all=False))
        except:
            print(f"It is not possible to unblock {sys.argv[2]}")
    else:
        print(help_message)