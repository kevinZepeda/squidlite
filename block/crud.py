from session import db
from tables import users, urls, block

def get_user(id = None, ip = None):
    if id != None:
        return db.query(users).filter(users.c.id == id).first()
    elif ip != None:
        return db.query(users).filter(users.c.ip == ip).first()
def get_users():
    return db.query(users).all()

def create_user(ip):
    try:
        db.execute(users.insert().values(ip=ip))
        db.commit()
        return db.query(users).filter(users.c.ip == ip).first()
    except:
        return False

def get_url(id = None, domain = None):
    if id != None:
        return db.query(urls).filter(urls.c.id == id).first()
    elif domain != None:
        return db.query(urls).filter(urls.c.domain == domain).first()

def create_url(domain):
    try:
        db.execute(urls.insert().values(domain=domain))
        db.commit()
        return db.query(urls).filter(urls.c.domain == domain).first()
    except:
        return False

def get_block(id=None, user_id=None, url_id=None):
    if id != None:
        return db.query(block).filter(block.c.id == id).first()
        pass
    elif user_id != None and url_id != None:
        return db.query(block).filter(block.c.user_id == user_id, block.c.url_id == url_id).first()
    elif user_id != None and url_id == None:
        return db.query(block).filter(block.c.user_id == user_id).all()
    elif user_id == None and url_id != None:
        return db.query(block).filter(block.c.url_id == url_id).all()

def create_block(user_id, url_id):
    try:
        db.execute(block.insert().values(user_id=user_id, url_id=url_id))
        db.commit()
        return db.query(block).filter(block.c.url_id == url_id, block.c.user_id == user_id).first()
    except:
        return False

def delete_block(id):
    try:
        db.execute(block.delete().where(block.c.id == id))
        db.commit()
        return id
    except:
        return False

def blocked_sites(user_ip):
    try:
        user = db.query(users).filter(users.c.ip == user_ip).first()
        blocked = db.query(block).filter(block.c.user_id == user.id).all()
        return [db.query(urls).filter(urls.c.id == site.url_id).first() for site in blocked]
    except:
        return []