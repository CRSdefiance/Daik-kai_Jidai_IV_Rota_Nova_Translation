"""Refine one unpublished Inn sentence after actual-font preview review."""

from copy import deepcopy
from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_runtime_v802/layout_v2_delta')
V1=Path('translations/inn_editorial_manuscript_v1.json')
V2=Path('translations/inn_editorial_manuscript_v2.json')


def main():
    assert not V2.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    doc=deepcopy(read(V1));old=deepcopy(doc['records'])
    row=next(r for r in doc['records'] if r['message_id']==1180)
    assert row['english']=="You're staying for %s nights, then?{PAD}"
    row['english']="You're staying %s nights, then?{PAD}"
    row['localization_note']+=' Preview refinement: omit optional for in this natural duration confirmation;all three original choices now remain on a single line. Meaning,argument and tone are unchanged.'
    doc['reviewed_research_manuscript']=str(V1);doc['reviewed_research_manuscript_sha256']=sha(V1.read_bytes())
    assert [r for r in doc['records'] if r['message_id']!=1180]==[r for r in old if r['message_id']!=1180]
    save(V2,doc)
    arm=Path('work/analysis/inn_runtime_v802/ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    source=Path('work/analysis/inn_runtime_v802/layout/effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    kanji=NdsImage.open('out/all_routes_combined_v799_candidate.nds').read_file('/GRP/KANJI.FNT')
    cases=[]
    for nights in (3,10,30):
        value=str(nights).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
        case=env['format_case'](prepared(arm),row,(value,))
        assert not case['findings'] and len(case['lines'])==1
        pixels=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert pixels==independent_font(arm,kanji,case['lines'])
        path=ROOT/f'stay_{nights}_full_font.png'
        Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(path)
        cases.append(dict(**case,nights=nights,path=str(path),sha256=sha(path.read_bytes()),single_line_complete_independent_font_exact=True))
    image=Image.new('RGB',(476,540),'#30343c');draw=ImageDraw.Draw(image)
    for i,c in enumerate(cases):
        draw.text((5,i*180+4),f'ID1180 / {c["nights"]} nights',fill='white')
        image.paste(Image.open(c['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(5,i*180+24))
    path=ROOT/'three_stay_choices_2x.png';image.save(path)
    save(ROOT/'verification.json',dict(research_manuscript=str(V2),manuscript_sha256=sha(V2.read_bytes()),
        previous_full_layout='work/analysis/inn_runtime_v802/layout/verification.json',
        previous_full_layout_sha256=sha(Path('work/analysis/inn_runtime_v802/layout/verification.json').read_bytes()),
        all_other22_records_byte_exact=True,changed_native_cases=cases,
        preview=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,
        production_COMMON_integration_and_actual_revised_playback_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Unpublished Inn1180 refined:3/10/30-night confirmations all fit one line with complete fonts;other22 records unchanged.',flush=True)


if __name__=='__main__':main()
