import mongoengine

def connect_to_mongo():
    mongoengine.connect('files')

connect_to_mongo()