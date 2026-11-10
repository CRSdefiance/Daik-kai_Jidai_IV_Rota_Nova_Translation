"""Run complete static/staged nameplate scenes using the original ordinary A schedule."""
import argparse
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['static_parent','static_target','staged_parent','staged_target'],required=True);case=ap.parse_args().case
    fp=Path('work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json')
    selected=next(f for f in read(fp)['fixtures'] if f['case']==case);number=selected['source_block'];count=selected['original_source_command_count']
    source=Path('scripts/run_lil_B221_English_v7002.py')
    changes={
        'work/analysis/lil_B221_English_fixture_v7001/complete_B221_English_B22_fixture.json':str(fp).replace('\\','/'),
        "fixture['fixtures'][0]":f"next(r for r in fixture['fixtures'] if r['case']=='{case}')",
        "selected['case']=='reviewed_English' and selected['source_block']==221":f"selected['case']=='{case}' and selected['source_block']=={number}",
        'lil_B221_English_run_v7002':f'square_shopkeeper_scene_{case}_v7023','lil_B221_English_v7002':f'square_shopkeeper_{case}_v7023',
        "'source_event221_not_naturally_selected':True":f"'source_event{number}_not_naturally_selected':True",
        "'displayed_original_source_block':221":f"'displayed_original_source_block':{number}",
        "'all21_source_commands_retained':True":f"'all{count}_source_commands_retained':True",
        'B221 reviewed English content':'existing English Shopkeeper nameplate scenes'}
    text=checked_text(source.read_text('utf8'),changes)
    exec(compile(text,str(source)+'::owned-nameplate-comparison','exec'),dict(__name__='__main__',__file__=__file__))
