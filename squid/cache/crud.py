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

def create_app(name):
    db.execute('''INSERT INTO apps ("name") VALUES ("%s");''' % name)
    conn.commit()
    return db.execute('''SELECT * FROM apps WHERE name = "%s";''' % name)
    
def get_app(id=None, name=None):
    if id != None:
        return db.execute('''SELECT * FROM apps WHERE id = "%s";''' % id)
    elif name != None:
        return db.execute('''SELECT * FROM apps WHERE name = "%s";''' % name)

def create_app_url(app_id, domain):
    db.execute('''INSERT INTO apps_urls ("app_id", "domain") VALUES (?, ?);''', (app_id, domain))
    conn.commit()
    return db.execute('''SELECT * FROM apps_urls WHERE app_id = "%s";''' % app_id)
    
def get_app_url(id=None, app_id=None):
    if id != None:
        return db.execute('''SELECT * FROM apps_urls WHERE id = "%s";''' % id)
    elif app_id != None:
        return db.execute('''SELECT * FROM apps_urls WHERE app_id = "%s";''' % app_id)

def delete_app_url(app_id, domain):
    db.execute('''DELETE FROM apps_urls WHERE app_id = :id and domain = :url''', {"id":app_id, "url":domain})
    conn.commit()
    return db

def create_block(user_id, domain=None, app_id=None):
    if domain != None:
        db.execute('''INSERT INTO block ("user_id", "domain") VALUES (?, ?)''', (user_id, domain))
        conn.commit()
        return db.execute('''SELECT * FROM block WHERE user_id = :user and domain = :url''', {"user":user_id, "url":domain})
    elif app_id != None:
        db.execute('''INSERT INTO block ("user_id", "app_id") VALUES (?, ?)''', (user_id, app_id))
        conn.commit()
        return db.execute('''SELECT * FROM block WHERE user_id = :user and app_id = :id''', {"user":user_id, "id":app_id})

def delete_block(user_id, domain=None, app_id=None):
    if domain != None:
        db.execute('''DELETE FROM block WHERE user_id = :user and domain = :url''', {"user":user_id, "url":domain})
        conn.commit()
        return db
    elif app_id != None:
        db.execute('''DELETE FROM block WHERE user_id = :user and app_id = :id''', {"user":user_id, "id":app_id})
        conn.commit()
        return db

def blocked_sites(user_ip):
    try:
        user = get_user(ip=user_ip).fetchone()
        return db.execute(''' SELECT * FROM block WHERE user_id = "%s" and domain IS NOT NULL;''' % user[0]).fetchall()
    except:
        return []

def blocked_apps(user_ip, names=False):
    try:
        user = get_user(ip=user_ip).fetchone()
        blocked = db.execute(''' SELECT * FROM block WHERE user_id = "%s" and app_id IS NOT NULL;''' % user[0]).fetchall()
        app_urls = [get_app_url(app_id = app[3]).fetchall() for app in blocked]
        if names:
            return [get_app(id=app[3]).fetchone() for app in blocked]
        return [domain for site in app_urls for domain in site]
    except:
        return []

def blocked_urls(user_ip):
    try:
        return blocked_sites(user_ip) + blocked_apps(user_ip)
    except:
        return []
