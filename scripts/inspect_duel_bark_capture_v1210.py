"""Read-only scan of original duel bitmap matches and actual visible reaction glyphs."""
import argparse
from pathlib import Path
import struct
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_duel_actual_holds_v1171 import actual_widget
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_actual_v1210')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_bark_v1207_1206')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--through',type=int,required=True);args=parser.parse_args()
    target=ROOT/f'scan_through{args.through}.json';assert not target.exists()
    rom=NdsImage.open('out/all_routes_combined_v1206_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    native=read('work/analysis/duel_bark_native_v1202/native_font_scope_verification.json')
    assert native['ARM9_sha256']==sha(arm)
    by_sha={c['source_208x36_4bit_SHA256']:c for c in native['cases'] if 1957<=c['message_ID']<=1972}
    candidates=[];holds=[];scanned=[]
    for path in sorted(CAP.glob('frame_*_arm9_ram.bin')):
        frame=int(path.name.split('_')[1])
        if frame<5782 or frame>args.through:continue
        image_path=CAP/f'frame_{frame:06d}_navigation.png'
        if not image_path.exists():continue
        raw=path.read_bytes()
        if len(raw)!=0x400000:continue
        scanned.append({'frame':frame,'RAM_sha256':sha(raw)})
        try:widget,controller,header,h=actual_widget(raw)
        except AssertionError:continue
        assert h[:3]==(4,52,36) and h[4]==40
        at=header-0x02000000+40;packed=raw[at:at+3744]
        pixels=bytes((v>>shift)&15 for v in packed for shift in (0,4))
        case=by_sha.get(sha(pixels))
        if not case:continue
        n=case['message_ID'];image=Image.open(image_path).convert('RGB')
        cpu,get=get_machine(arm,raw);actors=list(struct.unpack('<2I',cpu.mem_read(controller+0x34,8)))
        actor_ids=[get(0x7EE08,a) for a in actors]
        assert actor_ids==[1,32]
        table=0x02117560 if n<1965 else 0x021175C0
        assert get(0x53F4C,actors[0],table)==n
        bad=[]
        for row in range(3):
            for y in range(12):
                for x in range(144):
                    expected=(0,8,0) if pixels[(row*12+y)*208+x] else (255,255,255)
                    actual=image.getpixel((56+x,212+row*20+y))
                    if actual!=expected:bad.append((x,y,row))
        record={'message_ID':n,'frame':frame,'source_actor_IDs':actor_ids,'speaker_source_side':0,'original_table':table,
            'whole208x36_native_font_plane_sha256':sha(pixels),'lines':case['lines'],'source_widget':widget,
            'source_controller':controller,'RAM':str(path),'RAM_sha256':sha(raw),
            'capture':str(image_path),'capture_sha256':sha(image_path.read_bytes()),
            'actual_visible_three144x12_crops_exact':not bad,'RGB_mismatch_pixels':len(bad)}
        candidates.append(record)
        if not bad:holds.append(record)
    ROOT.mkdir(parents=True,exist_ok=True)
    save(target,{'candidate':'out/all_routes_combined_v1206_candidate.nds',
        'candidate_sha256':sha(Path('out/all_routes_combined_v1206_candidate.nds').read_bytes()),
        'through':args.through,'scanned_RAM_frames':scanned,'native_bitmap_match_candidates':candidates,'complete_visible_holds':holds,
        'visible_message_IDs':sorted({r['message_ID'] for r in holds}),
        'persisting_bitmap_without_matching_RGB_is_not_an_actual_visible_activation_claim':True,
        'source_geometry_and_full_native_ink_blank_masks_used_not_fitted_to_letters':True,
        'read_only_no_emulator_input_or_state_changes':True,'no_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Scanned',len(scanned),'frames;visible IDs',sorted({r['message_ID'] for r in holds}),
        'visible holds',len(holds),'bitmap-only candidates',len(candidates)-len(holds),flush=True)


if __name__=='__main__':main()
