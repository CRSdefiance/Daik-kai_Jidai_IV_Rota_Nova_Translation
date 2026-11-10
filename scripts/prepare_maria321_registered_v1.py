"""Freeze321 complete mixed reviews over the exact720-entry registered parent."""
from scripts.prepare_maria305_registered_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.maria305_release_v2': 'dk4tool.patch.maria321_release_v1',
    'dk4tool/patch/maria305_release_v2.py': 'dk4tool/patch/maria321_release_v1.py',
    'Maria_B176_B195_clean_20261110': 'Maria_B196_B215_clean_20261110',
    'maria_B176_B195': 'maria_B196_B215',
    'translations/maria305_editorial_release_v1.json': 'translations/maria321_editorial_release_v1.json',
    'work/maria390_B152_B175_release_v1/registered_release_verification.json':
        'work/maria305_B176_B195_release_v1/registered_release_verification.json',
    '==(719,114,54)': '==(720,114,55)',
    "OUT=ROOT/'registered_preparation_v2'": "OUT=ROOT/'registered_preparation_v1'",
    'scripts/finalize_maria305_research_v1.py': 'scripts/finalize_maria321_research_v3.py',
    "Path('scripts/finalize_maria321_research_v3.py'),Path(__file__)":
        "Path('scripts/finalize_maria321_research_v3.py'),Path('scripts/finalize_maria321_research_v2.py'),Path('scripts/finalize_maria321_research_v1.py'),Path(__file__)",
    "format='dk4-reviewed-maria305-release-v1',record_count=305,speech_count=294,ordinary_count=272,style_count=22,typed_choice_count=11,menu_count=5":
        "format='dk4-reviewed-maria321-release-v1',record_count=321,speech_count=317,ordinary_count=296,style_count=21,typed_choice_count=4,menu_count=2",
    'scoped_name_count=27,native_pages=302,relative_cases=170,FE_count=16':
        'scoped_name_count=24,native_pages=325,relative_cases=120,FE_count=2',
    'actual_frames=63843': 'actual_frames=73443',
    "len(proof['changed_records'])==305": "len(proof['changed_records'])==321",
    'source_records=305,physical_body_candidates=294,native_pages=302':
        'source_records=321,physical_body_candidates=317,native_pages=325',
    'Qualified305 reviews over719-entry Maria390': 'Qualified321 reviews over720-entry Maria305',
})
exec(compile(source,__file__+'::same-frozen-inputs-pure-complete-transaction-andparent-inverse','exec'),globals())
