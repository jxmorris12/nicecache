import diskcache
import functools
import inspect
import logging
import os

logger = logging.getLogger(__name__)

def _hash(s):
    """ Hashes a string to another string. """
    import hashlib
    hash_object = hashlib.md5(s.encode())
    return hash_object.hexdigest()


class NiceCache:
    """ Will create cache in <cache_root>/<name>. 
    
        ``cache_root`` defaults to '~/.nicecache'.
    """
    def __init__(self, name, cache_root='~/.nicecache'):
        self.path = os.path.join(os.path.expanduser(cache_root), name)
        logger.info(f'NiceCache initialized with path {self.path}.')
    
    def __getitem__(self, key): 
        with diskcache.Cache(self.path) as cache:
            value = cache[key]
        return value
    
    def __setitem__(self, key, newvalue): 
        cache = diskcache.Cache(self.path)
        cache[key] = newvalue
        cache.close()
        

def _nicecache(func, cache_root='~/.nicecache'):
    """ A decorator for memoizing function results. Like @functools.cache 
    except it persists between runs.
    """
    # Cache based off file path.
    caller_frame = inspect.stack()[1]
    caller_filename = os.path.abspath(caller_frame.filename)
    cache_path = f'{caller_filename}:{func.__name__}'
    func_hash = _hash(cache_path)
    logger.info(f'@nicecache caching function with key {cache_path} and hash {func_hash}')
    # Create decorator.
    cache_save_path = os.path.join(os.path.expanduser(cache_root), func_hash)
    cache = diskcache.Cache(cache_save_path)
    @functools.wraps(func)
    def wrap(*args):
      if args not in cache:
        cache[args] = func(*args)
      return cache[args]
    cache.close()
    return wrap

def nicecache(arg):
    if callable(arg):
        return _nicecache(arg)
    else:
        def nicecache_factory(func):
            return _nicecache(func, arg)
        return nicecache_factory