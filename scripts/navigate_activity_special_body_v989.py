"""Inspect each distinct consumer before scheduling its native dismissal."""
import argparse,json,struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_activity_special_fixture_v988 import SPECS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v989')

def main():
    p=argparse.ArgumentParser();p.add_argument('--case',choices=tuple(SPECS),required=True)
    p.add_argument('--phase',choices=('body','dismiss','finish'),required=True);args=p.parse_args()
    journal=ROOT/f'{args.case}_navigation.jsonl';commands=[json.loads(s) for s in journal.read_text().splitlines()]
    folder=Path(read(ROOT/f'{args.case}_run_plan.json')['folder']);modal=SPECS[args.case][2] is None
    if args.phase=='body':
        assert commands[-1]['until']==15300
        path=folder/'frame_015300_arm9_ram.bin';raw=path.read_bytes();arm=NdsImage.open('out/all_routes_combined_v987_candidate.nds').read_file('/__arm9__.bin')
        cpu,get=get_machine(arm,raw);context=get(0x3F0F8)
        assert list(struct.unpack('<2I',cpu.mem_read(context+8,8)))==[0,1] and get(0x7F244)==1
        save(ROOT/f'{args.case}_observed_original_combat.json',{'frame':15300,'RAM':str(path),'RAM_sha256':sha(raw),
            'native_combat_predicate_observed_before_any_personnel_fixture':True,'mode_fields8_12':[0,1]})
        extra=[{'until':15500,'buttons':['A'],'duration':8,'activity_special_fixture':args.case},
            {'until':15700,'buttons':['X'],'duration':8},{'until':15900,'touch':[93,101],'duration':8},
            {'until':16100,'buttons':['A'],'duration':8},
            {'until':16300,'touch':[66,110],'duration':8,'activity_special_fixture':{'case':args.case,'late_case_only':True}},
            {'until':16500,'duration':1}]
    elif args.phase=='dismiss':
        assert commands[-1]['until']==16500 and (folder/'frame_016500_arm9_ram.bin').exists()
        if modal:
            extra=[{'until':16700,'buttons':['A'],'duration':8},{'until':16900,'buttons':['B'],'duration':8},{'until':17100,'duration':1}]
        else:extra=[{'until':16700,'buttons':['B'],'duration':8},{'until':16900,'buttons':['B'],'duration':8},{'stop':True}]
    else:
        assert modal and commands[-1]['until']==17100 and (folder/'frame_017100_arm9_ram.bin').exists()
        extra=[{'stop':True}]
    with journal.open('a',encoding='utf-8') as f:
        for command in extra:f.write(json.dumps(command)+'\n')
    print(args.case,args.phase,'appended',len(extra),'commands')

if __name__=='__main__':main()
