"""Derive corrected review from exact current12-byte ownership,retaining the original guard failure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_review_tools_v8202b')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/review_Gerhard_surname_v8202.py','scripts/review_Gerhard_surname_v8202b.py',{
        'Gerhard_surname_review_v8202':'Gerhard_surname_review_v8202b',
        "OUT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')":"OUT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')\nOWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')",
        'current,effective,names,oldnames=map(read,[CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES])':'current,effective,names,oldnames=map(read,[CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES]);ownership=read(OWNERSHIP);assert ownership[\'ARM9_sha256\']==current[\'current_ARM9_sha256\']',
        'slot=1435252;size=20':'slot=1435252;size=12',
        'all14_existing_Adernkatz_occurrences_protected=True,all6_inconsistent_consumers_explicitly_planned=True,':'all14_existing_Adernkatz_occurrences_protected=True,all6_inconsistent_consumers_explicitly_planned=True,\n        current_name_ownership=str(OWNERSHIP),current_name_ownership_sha256=sha(OWNERSHIP.read_bytes()),protected_Blades_neighbor_must_remain_byte_exact=True,',
        '[CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES,HODRAM_NAMES,Path(__file__)]':'[CURRENT,EFFECTIVE,NAMES,OLD_HODRAM_NAMES,HODRAM_NAMES,OWNERSHIP,Path(__file__)]',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared corrected12-byte surname review withowned-span/Blades proof;original20-byte assumption failure preserved.')
