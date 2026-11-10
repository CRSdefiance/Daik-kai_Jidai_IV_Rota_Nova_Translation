"""Apply 67 source-bound decisions with the established per-record dialogue checks."""
from pathlib import Path
from types import FunctionType

from scripts import write_rafael_B177_B180_contextual_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
    "B177_B180_clean_first_v1/sealed_drafts.json":"B161_B165_clean_first_v1/sealed_drafts_v2.json",
    "Rafael_B177_B180_current1424_20261105":"Rafael_B161_B165_current1607_20261105",
    "CAPTIONS = CURRENT.parent / 'objects/current_objects.json'\n":"",
    "rafael_B177_B180_contextual_decisions_v1.txt":"rafael_B161_B165_contextual_decisions_v1.txt",
    "rafael_B177_B180_contextual_review_v1.json":"rafael_B161_B165_contextual_review_v1.json",
    """    drafts, effective, captions, identity = map(load, [DRAFTS, CURRENT, CAPTIONS, IDENTITY])
    current_rows = [row for group in effective['groups'] for row in group['records']] + captions['choice_records']""":
        """    drafts, effective, identity = map(load, [DRAFTS, CURRENT, IDENTITY])
    current_rows = [row for group in effective['groups'] for row in group['records']]""",
    "== 183":"== 67",
    "{177: 56, 178: 65, 179: 33, 180: 29}":"{161: 19, 162: 5, 163: 14, 164: 21, 165: 8}",
    "assert sum(row['kind'] == 'typed-choice-label' for row in rows) == 8":"assert not any(row['kind'] == 'typed-choice-label' for row in rows)",
    "[DRAFTS, CURRENT, CAPTIONS, IDENTITY, DECISIONS, Path(__file__)]":"[DRAFTS, CURRENT, IDENTITY, DECISIONS, TEMPLATE, Path(__file__)]",
    "CONTEXTS = {":"OLDER_CONTEXTS = {",
    "MACROS = re.compile":"CONTEXTS = load(DRAFTS)['source_contexts']\nCONTEXTS = {int(k):v for k,v in CONTEXTS.items()}\nMACROS = re.compile",
})
TEMPLATE=Path(previous.__file__)
if __name__=='__main__':
    exec(compile(source,__file__+'::same-exact-editorial-decisions-on-five-exchanges','exec'),globals())
