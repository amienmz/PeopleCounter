__author__ = 'orion'
import requests
class PostData(object):
    def __init__(self, url ):
        self.url = url
    def post(self, id, isCome ,  month, date , count=1):
        payload = {'id': id, 'name': isCome, 'count': count , 'month': month, 'date': date }
        r = requests.post(self.url, data=payload)
        return r

payload = {'id': 'xx', 'name': 'aa', 'in_out': 'out' , 'status': 'connect' }
print 'y'
requests.post('http://10.20.13.180:3000/test', data=payload)
print 'x'