"""Preserve76 exact-byte font cases and re-execute two for the one changed automatic wrap."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.mood_comments_layout_v980 import layout,compiled
from scripts.prepare_mood_comments_prose_v978 import ROM,MANUSCRIPT,IDS
from scripts.prepare_work_comments_v842 import snapshot
from scripts.probe_work_fonts_v843 import prepare_model,execute
from scripts.probe_mood_comments_fonts_v979 import prepare_mood
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v980')


def main():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'native_font_proof.json').exists()
    prior_path=Path('work/analysis/mood_comments_v979/native_font_proof.json');prior=read(prior_path);doc=read(MANUSCRIPT)
    assert prior['candidate_sha256']==sha(ROM.read_bytes())==doc['current_ROM_sha256'] and prior['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert prior['producer_sha256']==sha(Path('scripts/probe_mood_comments_fonts_v979.py').read_bytes())
    assert prior['layout_producer_sha256']==sha(Path('scripts/mood_comments_layout_v979.py').read_bytes())
    assert tuple(c['message_id'] for c in prior['cases'])==IDS
    assert layout(doc['records'][20]['english'])==['"Mutter, mutter..."','Oh, I was just talking to myself...'] and doc['records'][20]['message_id']==1853
    changed=[r['message_id'] for r,c in zip(doc['records'],prior['cases'],strict=True) if compiled(r).hex()!=c['ordinary_and_battle_font_controls'][0]['text_hex']]
    assert changed==[1853]
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');cases=[];new_cases=0
    for row,original in zip(doc['records'],prior['cases'],strict=True):
        case=deepcopy(original);number=row['message_id'];lines=layout(row['english']);path=ROOT/f'ID{number}_complete_native_ink.png'
        if number not in changed:
            assert case['generated_native_lines']==lines and all(v['text_hex']==compiled(row).hex() for v in case['ordinary_and_battle_font_controls'])
            source=Path(case['preview']);assert sha(source.read_bytes())==case['preview_sha256'];copy2(source,path)
            case['case_origin']={'preserved_original_numeric_font_cases':True,'prior_proof':str(prior_path),'prior_proof_sha256':sha(prior_path.read_bytes()),
                'same_ROM_and_manuscript_and_complete_compiled_bytes':True,'source_preview':str(source)}
        else:
            source,receipt=snapshot('battle_personal_v897_893_Julio',14700);ui,ui_receipt=snapshot('personal_cabin_v840_838_Charles_after',4600)
            prepared,fixture=prepare_model(arm,source,19,2,ui);variants=[];planes=[]
            for name,mode in (('ordinary',(0,0)),('battle',(0,1))):
                raw,mood=prepare_mood(arm,prepared,19,mode,row['mood_ID'])
                variant,plane=execute(rom,raw,19,2,number,compiled(row),lines)
                assert variant['complete_native_copy_macro_draw_and_ABI'] and variant['full252x96_native_and_independent_canvas_equal']
                assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
                variant.update(mode=name,mood_fixture=mood,original_mood_selector_selected_expected_message=True);variants.append(variant);planes.append(plane);new_cases+=1
            assert planes[0]==planes[1]
            Image.frombytes('L',(252,96),bytes(0 if v else 255 for v in planes[0])).save(path)
            case.update(source_snapshot=receipt,isolated_CPU_role_and_widget_fixture=fixture,generated_native_lines=lines,ordinary_and_battle_font_controls=variants,
                case_origin={'reexecuted_for_changed_automatic_wrap':True,'producer_sha256':sha(Path(__file__).read_bytes())})
        assert path.read_bytes() and all(v['generated_native_lines']==lines for v in case['ordinary_and_battle_font_controls'])
        case.update(preview=str(path),preview_sha256=sha(path.read_bytes()));cases.append(case)
    assert new_cases==2 and len(cases)==39
    sheet=Image.new('RGB',(3*442,13*104),'#263238');draw=ImageDraw.Draw(sheet)
    for i,case in enumerate(cases):
        x,y=i%3*442,i//3*104;draw.text((x+5,y+5),f"ID{case['message_id']} complete native body;actual pending",fill='white')
        with Image.open(case['preview']) as im:sheet.paste(im.crop((0,60,216,96)).resize((432,72),Image.Resampling.NEAREST),(x+5,y+25))
    path=ROOT/'all39_native_body_ink_masks_2x.png';sheet.save(path)
    proof={**deepcopy(prior),'cases':cases,'review_sheet':str(path),'review_sheet_sha256':sha(path.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'layout_producer_sha256':sha(Path('scripts/mood_comments_layout_v980.py').read_bytes()),
        'prior_native_font_proof':str(prior_path),'prior_native_font_proof_sha256':sha(prior_path.read_bytes()),'preserved_byte_identical_native_font_cases':76,'new_native_font_cases':2,
        'only_changed_compiled_IDs':[1853],'all78_source_native_font_cases_accounted_for_not_claimed_all_fresh':True,'visual_review_pending':True}
    save(ROOT/'native_font_proof.json',proof)
    print('39 complete native previews:76 original cases remain exact;two1853 cases re-executed for the improved wrap. Actual scenes remain.',flush=True)


if __name__=='__main__':main()
