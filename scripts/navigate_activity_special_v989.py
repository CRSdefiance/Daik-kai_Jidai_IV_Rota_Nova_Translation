"""Append navigation only after current RAM proves the original combat predicate."""

import argparse,json,struct

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

from dk4tool.rom.nds import NdsImage

from scripts.native_activity_special_room_v988 import CASES

from scripts.verify_personal_gameplay_v841 import get_machine

from scripts.verify_village_wrap_v608 import read,save



ROOT=Path('work/analysis/activity_special_v989')

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')





def main():

    p=argparse.ArgumentParser();p.add_argument('--case',choices=tuple(CASES),required=True);p.add_argument('--phase',choices=('combat','body'),required=True);args=p.parse_args()

    journal=ROOT/f'{args.case}_navigation.jsonl';commands=[json.loads(s) for s in journal.read_text().splitlines()]

    if args.phase=='combat':

        assert commands[-1]['until']==11700

        extra=[{'until':n,'buttons':['A'],'duration':8} for n in range(11900,15301,200)]

    else:

        assert commands[-1]['until']==15300

        folder=CAP/f'activity_special_v989_987_{args.case}';path=folder/'frame_015300_arm9_ram.bin';raw=path.read_bytes()

        rom=NdsImage.open('out/all_routes_combined_v987_candidate.nds');arm=rom.read_file('/__arm9__.bin');cpu,get=get_machine(arm,raw)

        context=get(0x3F0F8);assert list(struct.unpack('<2I',cpu.mem_read(context+8,8)))==[0,1]

        assert get(0x7F244)==1

        save(ROOT/f'{args.case}_observed_original_combat.json',{'frame':15300,'RAM':str(path),'RAM_sha256':sha(raw),'mode_fields8_12':[0,1],

            'native_combat_predicate_observed_before_any_room_or_mood_fixture':True,'actor_ID':CASES[args.case][0]})

        extra=[{'until':15500,'buttons':['A'],'duration':8,'activity_special_fixture':args.case},

            {'until':15700,'buttons':['X'],'duration':8},

            {'until':15900,'touch':[93,101],'duration':8},

            {'until':16100,'buttons':['A'],'duration':8},

            {'until':16300,'touch':[66,110],'duration':8,'activity_special_fixture':{'case':args.case,'late_case_only':True}},

            {'until':16500,'duration':1},

            {'until':16700,'buttons':['B'],'duration':8},

            {'until':16900,'buttons':['B'],'duration':8},{'stop':True}]

    with journal.open('a',encoding='utf-8') as f:

        for command in extra:f.write(json.dumps(command)+'\n')

    print(args.case,args.phase,'appended',len(extra),'commands',flush=True)





if __name__=='__main__':main()

