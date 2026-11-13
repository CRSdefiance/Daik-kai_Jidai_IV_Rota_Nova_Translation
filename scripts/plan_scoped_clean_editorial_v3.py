"""Retain one exact complete phrasal-verb sentence without relaxing display guards."""
import inspect
import linecache
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts import plan_scoped_clean_editorial_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(inspect.getsource(planner.main), {
        "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'}":
            "assert row['id'] in {'DK4_MES_B142_R0159','DK4_MES_B201_R0074'} or (row['id']=='DK4_MES_B197_R0017' and row['english']==\"No... I just felt as though your eyes were drawing me in. Is that what being turned to stone feels like?\" and retention.get('line_index')==1 and retention['exact_line']==\"your eyes were drawing me in.\")",
    })
    filename = __file__ + '::same-planner-one-exact-source-bound-phrasal-verb-retention'
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
    env = {**planner.main.__globals__, '__file__': __file__}
    exec(compile(source, filename, 'exec'), env)
    planner.main = env['main']
    previous.main()


if __name__ == '__main__':
    main()
