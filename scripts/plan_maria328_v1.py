"""Reuse the full-width planner withall328 mixed source/current references and27 FE panels."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'), {
    'work/Maria_B0_B32_clean_20261109':'work/Maria_B73_B95_clean_20261109',
    "doc['physical_speech_objects']==299":"doc['physical_speech_objects']==313",
    "doc['blocks']==list(range(15))+list(range(16,33))":"doc['blocks']==[73,74,75,76,77,78,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95]",
    "len(bound)==len(original)==len(doc['records'])==301":"len(bound)==len(original)==len(doc['records'])==328",
    "assert before[:2]==now[:2]==b'\\0!'":"assert before[:2]==now[:2]==int(row['source_word']).to_bytes(2,'little') and row['source_word']==0x2200",
    "        bindings.append(dict(id=row['id']":"        if raw[0]==254:assert row['kind']=='system-FE' and row['FE_is_not_an_ordinary_actor_nameplate']\n        bindings.append(dict(id=row['id']",
    'assert len(bindings)==299':'assert len(bindings)==313',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-complete-source-controls-parity-andpagination-contract328','exec'),globals())
