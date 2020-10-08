# nicecache

A cache that persists data between runs. Trust me, you need this.

![nicecache on pypi](https://badge.fury.io/py/nicecache.svg)

`@functools.cache` is nice, but there's a slight problem -- each program starts
its own cache fresh. In comes `@nicecache.nicecache`. Use it just like you'd
use `@functools.cache`, but rest assured that you really only have to compute
this *once* and they'll persist across runs (by saving to disk!).

<hr>

Uses [diskcache](http://www.grantjenks.com/docs/diskcache/index.html) to
manage things behind the scenes.

## `@nicecache` decorator

Got some slow data-loading or preprocessing that you'd rather just compute once?
Frustrated that `functools.cache` spawns a new cache each time you re-run
your program? You're in the right place.


Here's a really simple example:
```python
from time import time
from nicecache import nicecache
@nicecache(tmp_cache_dir)
def slowtimes(a, b):
    print('saving to cache:', (a, b))
    time.sleep(5)
    return a * b

def test():
    t1 = time()
    print(slowtimes(5, 3))
    t2 = time()
    print(f'Func 1 time: {t2-t1}s')
    print(slowtimes(5, 3))
    t3 = time()
    print(f'Func 2 time: {t3-t2}s')
    print(slowtimes(4, 2))
    t4 = time()
    print(f'Func 3 time: {t4-t3}s')
    print(slowtimes(4, 2))
    t5 = time()
    print(f'Func 4 time: {t5-t4}s')
saving to cache: (5, 3)
15
Func 1 time: 5.0264012813568115
15
Func 2 time: 0.0017404556274414062
saving to cache: (4, 2)
8
Func 3 time: 5.011389970779419
8
Func 4 time: 0.0015897750854492188
```

### Specifying a cache path

By default values are cached to `~/.nicecache`. Specify a different folder path
by passing an argument to the decorator. For example, 
`@nicecache('/tmp/cache/path')`.

## `NiceCache` object

You can also initialize a `NiceCache` object and use it like a dictionary. It 
functions like a normal dictionary, but values persist between runs.

In one of a program:
```
import nicecache
cache = nicecache.NiceCache('jack_tmp_cache_vals')
cache['hello'] = 'hi'
```

And in another run of the program:
```
>> import nicecache
>> cache = nicecache.NiceCache('jack_tmp_cache_vals')
>> print(cache['hello'])
'hi'
```