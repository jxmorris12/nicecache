import nicecache
import os
import shutil
import time

def test_times():
    tmp_cache_dir = f'~/.nicecache/test_{time.time()}'
    os.makedirs(tmp_cache_dir)
    @nicecache.nicecache(tmp_cache_dir)
    def slowtimes(a, b):
        time.sleep(5)
        return a * b
    
    ERR = 0.5 # Error in seconds for function timing
    t1 = time.time()
    assert slowtimes(5, 3) == 15
    t2 = time.time()
    assert abs((t2-t1) - 5) < ERR # Assert this took around 5 seconds
    assert slowtimes(5, 3) == 15
    t3 = time.time()
    assert abs(t3-t2) < ERR # Assert this took around 0 seconds
    assert slowtimes(4, 2) == 8
    t4 = time.time()
    assert abs((t4-t3)-5) < ERR # Assert this took around 5 seconds
    assert slowtimes(4, 2) == 8
    t5 = time.time()
    assert abs(t5-t4) < ERR # Assert this took around 0 seconds
    
    # Clean up and delete temporary cache
    shutil.rmtree(tmp_cache_dir)

def test_cache_dict():
    cache = nicecache.NiceCache('jack_tmp_cache_vals')
    cache['hello'] = 'hi'
    
def test_cache_dict2():
    cache = nicecache.NiceCache('jack_tmp_cache_vals')
    assert cache['hello'] == 'hi'

if __name__ == '__main__':
    test_times()