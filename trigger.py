from tbd.tasks import add, upgrade
from celery.result import AsyncResult
import time

def upgrade_workers(target=None):
    if target is None:
        result = upgrade.s()
        
def get_result():
    result = add.delay(3, 10)
    r_id = result.id
    ar = AsyncResult(r_id)
    # print("get ready: {}".format(ar.ready()))
    # print("get ongoing status : {}".format(ar.status))
    # time.sleep(1)
    # print("get ready: {}".format(ar.ready()))
    # print("get ongoing status : {}".format(ar.status))
    # time.sleep(1)
    # print("get ready: {}".format(ar.ready()))
    # print("get ongoing status : {}".format(ar.status))
    time.sleep(3)
    print("get successful: {}".format(ar.successful()))
    print("get result: {}".format(ar.get()))
        
def query_result():
    result = add.delay(3, 10)
    r_id = result.id
    ar = AsyncResult(r_id)

    while True:
        if ar.ready():
            if ar.successful():
                print("get result: {}".format(result.get()))
            else:
               print("get exception: {}".format(ar.traceback))
            break
        else:
           print("get ongoing status : {}".format(ar.status))
        time.sleep(1)

if __name__ == '__main__':
    query_result()
    # get_result()
    # t1 = time.time()
    # result = upgrade.delay()
    # res = None
    # res2 = None
    # t2 = time.time()
    # print("upgrade {} 2: {} cost {} secs!".format(res, res2, t2-t1))
    # time.sleep(10)