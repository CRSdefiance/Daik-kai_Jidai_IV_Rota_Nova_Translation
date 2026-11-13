"""Bind B205's observed return,without inheriting B204 timing."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_source_return_tools_v6183')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/review_lil_B204_source_return_v6076.py','scripts/review_lil_B205_source_return_v6183.py',{
        'B204':'B205','source_return_v6076':'source_return_v6183','source_run_v6071':'source_run_v6181','source_paths_v6072':'source_paths_v6182',
        '1308':'616','7894':'7175','9101':'8382','2234':'2312','[7870,7930,8350,9070,9190,13001]':'[7150,7210,7630,8350,8470,13001]',
        'complete20_objects35_commands_observed':'complete17_objects34_commands_observed',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_return_derivation.json',dict(tool=tool,source_end=616,end_frame=7175,first_later_B120_frame=8382,final_B120_offset=2312,new_review_credit=0))
