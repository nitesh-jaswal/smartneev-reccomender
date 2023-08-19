import time
import functools

def timeit(fmt_msg: str):

    def decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = func(*args, **kwargs)
            time_taken = round(time.monotonic() - start_time, 2)
            print(fmt_msg.format(time_taken))
            return result

        return wrapper
    
    return decorator