"""Correct the historical packet's field binding and prepare the source cold-boot runner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_name_source_tools_v7041b')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/review_lil_B222_names_v7041.py','scripts/review_lil_B222_names_v7041b.py',{"['Japanese']":"['source_Japanese']"}),
        ('scripts/run_lil_B221_source_v6979.py','scripts/run_lil_B222_source_v7043.py',{
            'B221':'B222','source_fixture_v6978':'source_fixture_v7042','source_run_v6979':'source_run_v7043','source_v6979':'source_v7043',
            "selected['source_block']==221":"selected['source_block']==222",
            'source_event221_not_naturally_selected':'source_event222_not_naturally_selected',
            "'displayed_original_source_block':221":"'displayed_original_source_block':222",'all21_source_commands_retained':'all18_source_commands_retained'})]
    for source,target,changes in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf8'),changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_tools.json',dict(tools=[derive(*j) for j in jobs],
        failed_name_producer_preserved=True,historical_Stockholm_packet_source_Japanese_key_corrected=True,
        no_name_wording_native_address_or_guard_change=True,source_event222_prerequisite89_not_forced=True,new_review_credit=0,full_goal_complete=False))
