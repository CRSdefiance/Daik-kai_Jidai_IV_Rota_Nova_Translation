"""Derive bounded no-relative single-block reconstruction;preserve all source/preamble/parity/inverse guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_rebuild_tools_v8494')
if __name__=='__main__':
    assert not ROOT.exists();result=derive('dk4tool/patch/hodram_outcome_rebuild_v1.py','dk4tool/patch/hodram_B50_rebuild_v1.py',{
        'all6 Hodram outcome speeches':'all3 Hodram B50 speeches','len(rows)!=6':'len(rows)!=3','[47,48]':'[50]',
        'Exact6 SC1 B47/B48 records and325 blocks required':'Exact3 SC1 B50 records and325 blocks required',
        'len(selected)!={47:3,48:3}[number]':'len(selected)!=3',
        'Exactly two reviewed blocks may change':'Exactly one reviewed B50 block may change',
        "sum(len(g['all_target_commands']) for g in groups)!=15":"sum(len(g['all_target_commands']) for g in groups)!=12",
        'Complete15commands/zerorelative sites/all6speech bodies required':'Complete12commands/zerorelative sites/all3speech bodies required','unchanged_archive_blocks=323':'unchanged_archive_blocks=324',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_source_current_preamble_native_extent_parity_relative_cache_andinverse_guards_preserved=True,all_native_numeric_constants_andmultiplicity_preserved=True,only_three_sourcequalified_B50_records_owned=True,no_ROM_archive_write_orcredit_by_preparer=True,new_credit=0,full_goal_complete=False))
