import sys
from crud import get_app, create_app, create_app_url, get_app_url, delete_app_url


def add_to_app(app_name, app_url):
    app = get_app(name=app_name).fetchone()
    if app: 
        return create_app_url(app_id=app[0], domain=app_url).fetchall()
    else:
        app = create_app(name=app_name).fetchone()
        return create_app_url(app_id=app[0], domain=app_url).fetchall()

def get_to_app(app_name):
    app = get_app(name=app_name).fetchone()
    if app:
        return get_app_url(app_id=app[0]).fetchall()
    else:
        return []

def remove_to_app(app_name, app_url):
    app = get_app(name=app_name).fetchone()
    if app:
        delete_app_url(app_id=app[0], domain=app_url)
        return get_app_url(app_id=app[0]).fetchall()
    else:
        return []

if __name__ == '__main__':
    try:
        if '--get' in sys.argv[1]:
            print([app[2] for app in get_to_app(sys.argv[2])])
        elif '--add' in sys.argv[1]:
            print([app[2] for app in add_to_app(sys.argv[2], sys.argv[3])])
        elif '--del' in sys.argv[1]:
            print([app[2] for app in remove_to_app(sys.argv[2], sys.argv[3])])
    except:
        print("""
URLS FROM APPs
    usage: [[--get] | [--add] | [--del]] [app] [url] 

    <comand>: --get
    Get all urls from app name
    ei: --get tiktok

    <comand>: --add
    Add url for app name
    ei: --add tiktok music.ly

    <comand>: --del
    Delete url from app
    ei: --del tiktok apy.ticktok.me
        """)

