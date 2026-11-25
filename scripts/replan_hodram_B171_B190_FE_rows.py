"""Use proven guarded row budgeting for the four observed FE row failures only."""
import inspect
import linecache
from pathlib import Path
from scripts import plan_hodram_B171_B190 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

DIAGNOSTIC = Path('work/analysis/Hodram_B171_B190_FE_diagnostic_20261104/row_diagnostic.json')
observed = load(DIAGNOSTIC)
failed = ('DK4_MES_B172_R0333', 'DK4_MES_B172_R0336', 'DK4_MES_B179_R0072', 'DK4_MES_B190_R0063')
assert tuple(observed['failed_IDs']) == failed
source = checked_text(inspect.getsource(previous.main), {
    "cells=(36 if row['id'] in ('DK4_MES_B118_R0022','DK4_MES_B127_R0053') else 38) if row['kind']=='system-FE' else 36;limit=4;":
    "cells=(36 if row['id'] in " + repr(failed) + " else 38) if row['kind']=='system-FE' else 36;limit=4;",
})
filename = __file__ + '::four-observed-FE-guarded-row-findings'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
env = {**previous.main.__globals__, '__file__': __file__}
exec(compile(source, filename, 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
