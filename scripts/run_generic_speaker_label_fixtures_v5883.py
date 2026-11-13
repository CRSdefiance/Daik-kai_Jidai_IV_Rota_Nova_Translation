"""Two complete existing scenes; target labels, ordinary input, read-only observation."""
import argparse
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=['tea','recovery'],required=True)
    args=parser.parse_args();case=args.case;block={'tea':184,'recovery':200}[case]
    source=Path('scripts/run_lil_B200_English_fixture_v5860.py')
    changes={
        "work/analysis/lil_B200_English_fixture_v5859/complete_B200_English_B22_fixture.json":"work/analysis/generic_speaker_label_fixtures_v5882/two_complete_existing_exchanges_with_target_name_data.json",
        "fixture=read(fp);selected=fixture['fixtures'][0]":"fixture=read(fp);selected=next(r for r in fixture['fixtures'] if r['case']==CASE)",
        "assert selected['case']=='reviewed_English' and selected['source_block']==200":"assert selected['case']==CASE and selected['source_block']==BLOCK",
        "work/analysis/lil_B200_English_run_v5860_reviewed_English":f'work/analysis/generic_speaker_label_run_v5883_{case}',
        "E:/Rota Nova translations/Generated/work/emulation_v193/lil_B200_English_v5860_reviewed_English":f'E:/Rota Nova translations/Generated/work/emulation_v193/generic_speaker_labels_v5883_{case}',
        'range(2600,12501,240)':'range(2600,7681,240)',
        "'source_event200_not_naturally_selected':True,'displayed_original_source_block':200,'all31_source_commands_retained':True":"'original_event_not_naturally_selected':True,'displayed_original_source_block':SELECTED['source_block'],'all_complete_original_source_commands_retained':True",
        "'--frames','13001'":"'--frames','8001'",
        "'--capture-at',*map(str,range(2350,13001,60))":"'--capture-every','60','--capture-at','4000'",
        '"\'--dump-ram\'"':'"\'--dump-capture-ram\',\'--dump-ram\'"',
        "'--capture-at','4000','6000','--pause-at','6000'":"'--capture-every','999999','--capture-at','4000','6000','--pause-at','6000'",
        "::B200-complete-source-fixture":"::generic-label-complete-scene-fixture",
    }
    text=checked_text(source.read_text(encoding='utf-8'),changes)
    exec(compile(text,str(source)+'::generic-label-wrapper','exec'),dict(
        __name__='__main__',__file__=__file__,CASE=case,BLOCK=block))
