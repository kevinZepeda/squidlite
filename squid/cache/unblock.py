import re
import sys
from crud import get_user, get_app, delete_block, blocked_sites, blocked_apps

def unblock(user_ip, domain=None, app_name=None):
    if app_name != None:
        user = get_user(ip=user_ip).fetchone()
        app = get_app(name=app_name).fetchone()
        if user and app:
            return delete_block(user_id=user[0],app_id=app[0])
        elif user and not app:
            print("App not exist")
        else:
            return f"User {user_ip} has no locks."
    elif domain != None:
        user = get_user(ip=user_ip).fetchone()
        return delete_block(user_id=user[0], domain=domain)


if __name__ == '__main__':
    help_message = """
Unblock User BY [user_ip]

        usage: [--get | --gat | --app | --url] [user_ip] [domain | app]

        <user_ip>:  IPV4 Network user

        <app>    :  Name of app

        <domaini>:  Word included in the domain to block

         --get:     Option to get blocked sites by user
         --gat:     Option to get blocked apps by user
         --app:     Option to select app to block
         --url:     Option to select url to block

        ie: unblock.py --app 172.17.0.2 facebook
    """
    IPV4_PATTERN = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    if '--get' in sys.argv[1]:
        print([domain[2] for domain in blocked_sites(user_ip=sys.argv[2])])
    elif '--gat' in sys.argv[1]:
        print([app[1] for app in blocked_apps(user_ip=sys.argv[2], names=True)])
    elif '--app' in sys.argv[1] and re.match(IPV4_PATTERN, sys.argv[2]):
        unblock(user_ip=sys.argv[2], app_name=sys.argv[3])
        print([app[2] for app in blocked_apps(user_ip=sys.argv[2], names=True)])
    elif '--url' in sys.argv[1] and re.match(IPV4_PATTERN, sys.argv[2]):
        unblock(user_ip=sys.argv[2], domain=sys.argv[3])
        print([domain[2] for domain in blocked_sites(user_ip=sys.argv[2])])
    else:
        print(help_message)