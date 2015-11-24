__author__ = 'orion'
import requests
class PostData(object):
    def __init__(self, url ):
        self.url = url
    def post(self, id, isCome ,  month, date , count=1):
        payload = {'id': id, 'is_come': isCome, 'count': count , 'month': month, 'date': date }
        r = requests.post(self.url, data=payload)
        return r

