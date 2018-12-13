from datetime import datetime,timedelta

class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.proxy = 'http://'+ '%s:%s' % (self.ip, self.port)
        self.expire_time = self.detail_time
        #代理是否已经被拉入黑名单了
        self.blacked = False
    #这个函数用于把str格式的过期时间（expire_time）转化为datetime格式，方便我们来
    #根据过期时间换新的代理
    @property
    def detail_time(self):
        date_str,time_str = self.expire_str.split(" ")
        year,month,day = date_str.split('-')
        hour,minute,second = time_str.split(':')
        expire_time = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
            second=int(second),
        )
        return expire_time
    #比较代理的过期时间和现在的时间
    #如果这个代理的存活时间少于10，那么就要准备更换代理IP了
    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time - now) <timedelta(seconds=10):
            return True
        else:
            return False




