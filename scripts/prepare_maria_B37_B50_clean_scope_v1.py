"""Seal286 disjoint clean SC3 objects in14 complete exchanges before current dialogue intake."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria_B0_B32_clean_scope_v1.py').read_text(encoding='utf-8'), {
    'work/Maria_B0_B32_clean_20261109': 'work/Maria_B37_B50_clean_20261109',
    'work/story_source_coverage_20261109_SC3_v1/coverage.json': 'work/story_source_coverage_20261109_SC3_v2/coverage.json',
    "assert digest(ledger)==census['ledger_sha256'] and load(ledger)['records_editorially_completed']==19161":
        """completion=load('work/maria301_release_v1/completion_checkpoint.json')
    assert census['ledger_sha256']==completion['ledger_after_sha256']
    current=load(ledger);assert current['records_editorially_completed']==19462
    credited={(r['file_path'],r['id']) for r in current['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys'] if r['file_path']=='/data/SC3.DK4'}
    matched={(r['file_path'],b['id']) for r in census['records'] for b in r['exact_credited_source_bindings']}
    assert credited==matched and len(credited)==498""",
    'scope=list(range(15))+list(range(16,33))': 'scope=list(range(37,51))',
    '==301 and len(groups)==32': '==286 and len(groups)==14',
    "Counter({'ordinary-speech':292,'physical-style-alternative':7,'typed-menu-caption':2})":
        "Counter({'ordinary-speech':282,'typed-menu-caption':4})",
    'records=301,ordinary_speeches=292,': 'records=286,ordinary_speeches=282,',
    'physical_style_alternatives=7,typed_captions=2,all301_positions_uncredited=True':
        'physical_style_alternatives=0,typed_captions=4,all286_positions_uncredited=True',
    '[(0,11),(11,22),(22,33)]': '[(37,44),(44,51)]',
    'Sealed301 clean-source objects in32 complete exchanges:292 ordinary,7 physical styles,two captions;current English unread,zero credit.':
        'Sealed286 clean-source objects in14 complete exchanges:282 ordinary,four captions;current conversation English unread,zero credit.',
})
exec(compile(source,__file__+'::same-clean-source-binder-disjoint-Maria37-50-andexact-ledger-reconciliation','exec'),globals())
