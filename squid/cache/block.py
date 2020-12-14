import sys
import re
from crud import get_user, get_url, create_block, create_url, create_user, blocked_sites


def block(user_ip, domain):
    user = get_user(ip=user_ip)
    url = get_url(domain=domain)
    if hasattr(user, "id") and hasattr(url, "id"):
        return create_block(user.id, url.id)
    elif hasattr(user, "id") and not hasattr(url, "id"):
        url = create_url(domain)
        return create_block(user.id, url.id)
    elif not hasattr(user, "id") and hasattr(url, "id"):
        user = create_user(user_ip)
        return create_block(user.id, url.id)
    else:
        user = create_user(user_ip)
        url = create_url(domain)
        return create_block(user.id, url.id)

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
    if '--get' in sys.argv[1]:
        print([site.domain for site in blocked_sites(sys.argv[2])])
    elif re.match(IPV4_PATTERN, sys.argv[1]):
        try:
            block(sys.argv[1],sys.argv[2])
            print([site.domain for site in blocked_sites(sys.argv[1])])
        except:
            print(f"It is not possible to block {sys.argv[2]}")
    else:
        print(help_message)