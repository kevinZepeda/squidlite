from crud import blocked_sites

def check_urls(url, user_urls):
    if len(user_urls) == 0:
        return False
    elif user_urls[0].domain in url:
        return True
    else:
        return check_urls(url, user_urls[1:]) 

def is_blocked(url, user_ip):
    return check_urls(url, blocked_sites(user_ip))
