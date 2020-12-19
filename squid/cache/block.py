import sys
import re
from crud import get_user, get_url, create_block, create_url, create_user, blocked_sites


def block(user_ip, domain):
    user = get_user(ip=user_ip).fetchone()
    url = get_url(domain=domain).fetchone()

    if user and url:
        return create_block(user[0], url[0])
    elif user and not url:
        url = create_url(domain).fetchone()
        return create_block(user[0], url[0])
    elif not user and url:
        user = create_user(user_ip).fetchone()
        return create_block(user[0], url[0])
    else:
        user = create_user(user_ip).fetchone()
        url = create_url(domain).fetchone()
        return create_block(user[0], url[0])

if __name__ == '__main__':
    help_message = """
    Block User BY [user_ip]

        usage:  [user_ip] [domain] | [--get] [user_ip]

        <user_ip>:  IPV4 Network user

        <domaini>:  Word included in the domain to block

         --get:     Option to get blocked sites by user

        ie: block.py 172.17.0.2 .google.com 
    """
    IPV4_PATTERN = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    if len(sys.argv) < 2:
        print(help_message)
    elif '--get' in sys.argv[1]:
        print(blocked_sites(user_ip=sys.argv[2], all=False))
    elif re.match(IPV4_PATTERN, sys.argv[1]):
        try:
            block(sys.argv[1],sys.argv[2])
            print(blocked_sites(user_ip=sys.argv[1], all=False))
        except:
            print(f"It is not possible to block {sys.argv[2]}")
    else:
        print(help_message)