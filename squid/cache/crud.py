from session import conn, db

def create_user(ip):
    db.execute('''INSERT INTO users ("IP") VALUES ("%s");''' % ip)
    conn.commit()
    return db.execute('''SELECT * FROM users WHERE ip = "%s";''' % ip)

def get_user(id=None, ip=None):
    if id != None:
        return db.execute('''SELECT * FROM users WHERE id = "%s";''' % id)
    elif ip != None:
        return db.execute('''SELECT * FROM users WHERE ip = "%s";''' % ip)

def create_url(domain):
    db.execute('''INSERT INTO urls ("domain") VALUES ("%s");''' % domain)
    conn.commit()
    return db.execute('''SELECT * FROM urls WHERE domain = "%s";''' % domain)
    
def get_url(id=None, domain=None):
    if id != None:
        return db.execute('''SELECT * FROM urls WHERE id = "%s";''' % id)
    elif domain != None:
        return db.execute('''SELECT * FROM urls WHERE domain = "%s";''' % domain)

def create_child_url(url_id, domain):
    db.execute('''INSERT INTO urls_child ("url_id", "domain") VALUES (?, ?);''', (url_id, domain))
    conn.commit()
    return db.execute('''SELECT * FROM urls_child WHERE url_id = "%s";''' % url_id)
    
def get_child_url(id=None, url_id=None):
    if id != None:
        return db.execute('''SELECT * FROM urls_child WHERE id = "%s";''' % id)
    elif url_id != None:
        return db.execute('''SELECT * FROM urls_child WHERE url_id = "%s";''' % url_id)

def create_block(user_id, url_id):
    db.execute('''INSERT INTO block ("user_id", "url_id") VALUES (?, ?)''', (user_id, url_id))
    conn.commit()
    return db.execute('''SELECT * FROM block WHERE user_id = :user and url_id = :url''', {"user":user_id, "url":url_id})

def delete_block(user_id, url_id):
    db.execute('''DELETE FROM block WHERE user_id = :user and url_id = :url''', {"user":user_id, "url":url_id})
    conn.commit()
    return db

def blocked_sites(user_ip=None, all=True):
    try:
        user = get_user(ip=user_ip).fetchone()
        blocked = db.execute(''' SELECT * FROM block WHERE user_id = "%s";''' % user[0]).fetchall()
        sites = [get_url(site[2]).fetchone()[1] for site in blocked]
        if (all == True):
            sites.extend([ domain for site in list(map(lambda x: list(map(lambda site: site[2], x)), [get_child_url(url_id=site[2]).fetchall() for site in blocked])) for domain in site])
        return sites
    except:
        return []



