"""Keep individually reviewed semantic phrases intact in generated layout only."""
import inspect
import linecache
from scripts import replan_hodram_B171_B190_visual as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "        'or pair in PAIRS));': 'or pair in PAIRS or pair in COHERENT.get(row[\\'id\\'],set())));',":
    """        'or pair in PAIRS));': 'or pair in PAIRS or pair in COHERENT.get(row[\\'id\\'],set())));',
        "            if not final and words[stop-1].endswith(('I','F')):continue":
            "            if not final and words[stop-1].endswith(('I','F')):continue\\n            if not final and (norm(words[stop-1]),norm(words[stop])) in COHERENT.get(row['id'],set()):continue", """,
})
filename = __file__ + '::source-bound-semantic-phrase-continuity'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
env = {**previous.main.__globals__, '__file__': __file__}
exec(compile(source, filename, 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
