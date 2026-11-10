"""Keep the ancient-times phrase and the bean question's final condition intact."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v11 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "{('let','me'),('me','ask'),('ask','you'),('you','another'),('fills','up'),('turn','them'),('equal','terms'),('stop','them')}":
        "{('ancient','times'),('started','with'),('with','two'),('let','me'),('me','ask'),('ask','you'),('you','another'),('fills','up'),('turn','them'),('equal','terms'),('stop','them')}",
})
env={**previous.main.__globals__,'__file__':__file__}
filename=__file__+'::coherent-ancient-times-and-comparison-clause'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
