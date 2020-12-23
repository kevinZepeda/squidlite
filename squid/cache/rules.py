from crud import blocked_urls, get_app

def check_urls(url, user_urls):
    if len(user_urls) == 0:
        return (False,0,0)
    elif user_urls[0][2] in url:
        if len(user_urls[0]) == 3: #its app
            return (True, user_urls[0][2], get_app(id=user_urls[0][1]).fetchone()[1])
        elif len(user_urls[0]) == 4: #its url
            return (True, user_urls[0][2], '_')
    else:
        return check_urls(url, user_urls[1:]) 

def connected(url, user_ip):
    return check_urls(url, blocked_urls(user_ip=user_ip))