
import random
import os
import time
import requests
import mechanicalsoup

class Transaction(object):
    def __init__(self):
        self.custom_timers={}
        self.api_url="http://127.0.0.1:8080/hello/kemuyuan"
        self.br=mechanicalsoup.Browser()

    def run(self):
        # r = random.uniform(1, 2)
        # time.sleep(r)
        # self.custom_timers['Example_Timer'] = r
        # self.br.set_handle_robots(False)
        start_time=time.time()
        resp=self.br.get(self.api_url)
        code=resp.status_code
        assert (code==200),'Bad Response:HTTP %s'% code
        self.custom_timers['GET']=time.time()-start_time


# if __name__ == '__main__':
#     trans = Transaction()
#     trans.run()
#     print (trans.custom_timers)
