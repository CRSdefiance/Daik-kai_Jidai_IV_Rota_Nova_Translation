"""Allow one byte-bound grammatical line-ending retention that avoids an early opening row."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v18 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "assert row['id']=='DK4_MES_B142_R0159'":
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}",
    "assert result['lines'][3]==retention['exact_line']":
        "assert result['lines'][retention.get('line_index',3)]==retention['exact_line']",
})
env = {**previous.main.__globals__, '__file__': __file__}
filename = __file__ + '::same-planner-two-exact-grammatical-retentions'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
