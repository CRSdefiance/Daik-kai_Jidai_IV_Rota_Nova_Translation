"""Seven complete ordinary startup/New Game captures versus current verified V928."""



from pathlib import Path



from PIL import Image,ImageDraw



from dk4tool.patch.grand_race_menu_release import sha

from scripts.finish_refit_display_v712 import load

from scripts.verify_village_wrap_v608 import read,save



ROM=Path('out/all_routes_combined_v938_candidate.nds')

ROOT=Path('work/analysis/battle_survey_lookout_v938')

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')





def main():

    digest=sha(ROM.read_bytes())

    current,images,receipt=load(CAP/'battle_survey_lookout_v938_newgame',digest,4000)

    reference_digest=read('work/analysis/battle_bridge_v928/registered_release_verification.json')['candidate_sha256']

    prior,old,reference=load(CAP/'battle_bridge_v928_newgame',reference_digest,4000)

    assert not any(v for k,v in current.items() if k.startswith('synthetic_'))

    assert 'battery_save_preloaded' not in current

    frames=(1,60,180,1600,2000,3200,4000)

    sheet=Image.new('RGB',(7*256,410),'#263238');draw=ImageDraw.Draw(sheet);pairs=[]

    for i,n in enumerate(frames):

        assert images[n].tobytes()==old[n].tobytes()

        pairs.append({'frame':n,'whole256x384_RGB_exact_to_V928':True})

        draw.text((i*256+4,4),str(n),fill='white');sheet.paste(images[n],(i*256,24))

    path=ROOT/'ordinary7_startup_controls.png';sheet.save(path)

    save(ROOT/'ordinary_startup_verification.json',{'candidate':str(ROM),'candidate_sha256':digest,

        'current_receipt':receipt,'reference_receipt':reference,'pairs':pairs,'all7_full_screen_pairs_exact':True,

        'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),'visual_review_pending':True,

        'ordinary_inputs_no_battery_save_savestate_or_fixtures':True,

        'scope':'Seven ordinary cold-boot/New Game character selection,confirmation and opening captures;not a full route or hardware test.',

        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})

    print('Seven whole ordinary startup/New Game frames match V928;visual review pending.',flush=True)





if __name__=='__main__':main()

