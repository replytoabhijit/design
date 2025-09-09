import time
import uuid
import redis

class DistributedLock:
    def __init__(self, redis_client, lock_key, lock_timeout=10):
        self.redis_client = redis_client
        self.lock_key = lock_key
        self.lock_timeout = lock_timeout
        self.lock_value = str(uuid.uuid4())

    def acquire(self):
        while True:
            if self.redis_client.set(self.lock_key, self.lock_value, nx=True, ex=self.lock_timeout):
                return True
            time.sleep(0.1)

    def release(self):
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        self.redis_client.eval(script, 1, self.lock_key, self.lock_value)

if __name__ == "__main__":
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    lock = DistributedLock(redis_client, "my_distributed_lock")

    print("Acquiring lock...")
    lock.acquire()
    print("Lock acquired!")

    # Critical section
    time.sleep(5)

    print("Releasing lock...")
    lock.release()
    print("Lock released!")