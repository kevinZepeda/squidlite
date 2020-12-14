import re
import sys
from crud import get_user, get_url, get_block, delete_block, blocked_sites

def maybe_sites(url, sites):
    if len(sites) == 0:
        return ["No site matches."]
    return [site for site in sites if site.domain in url]


def unblock(user_ip, domain):
    user = get_user(ip=user_ip)
    url = get_url(domain=domain)
    if hasattr(user, "id") and hasattr(url, "id"):
        blocking = get_block(user_id=user.id, url_id=url.id)
        return delete_block(blocking.id)
    elif hasattr(user, "id") and not hasattr(url, "id"):
        return f"This domain does not exist, maybe you meant:\n {maybe_sites(domain, blocked_sites(user_ip))}"
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
        print([site.domain for site in blocked_sites(sys.argv[2])])
    elif re.match(IPV4_PATTERN, sys.argv[1]):
        try:
            unblock(sys.argv[1],sys.argv[2])
            print([site.domain for site in blocked_sites(sys.argv[1])])
        except:
            print(f"It is not possible to unblock {sys.argv[2]}")
    else:
        print(help_message)