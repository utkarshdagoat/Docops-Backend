from mongoengine import  *
import datetime

class FileDoc(Document):
    created_at = DateTimeField(default=datetime.datetime.now())
    sqlRef = IntField(min_value=1)
    doc = DynamicField()