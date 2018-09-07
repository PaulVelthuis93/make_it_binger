import redis
import time
import traceback


def RedisCheck():
    try:
        # redis.default.svc.cluster.local
        # servicename.namespace.svc.cluster.local
        r = redis.StrictRedis(host='localhost', port=6379)                          # Connect to local Redis instance



        print("Permission to start...")
        while True:
            message = r.lpop('q')                                               # Checks for message
            if message:
                print(message.decode("utf-8"))

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print("python")
print(traceback.format_exc())
print("python")



if __name__=="__main__":
    RedisCheck()
