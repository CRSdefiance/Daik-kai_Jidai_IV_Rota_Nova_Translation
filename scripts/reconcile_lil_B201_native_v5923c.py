"""Bind final phrase planning to byte-identical existing native planes;no repeated CPU runs."""
from copy import deepcopy
from pathlib import Path
from textwrap import dedent
from PIL import Image,ImageDraw
from dk4tool.dialogue import lil_B201_layout_v4 as codec
from dk4tool.dialogue.lil_B201_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_fonts_v5923c')
DOC=Path('translations/lil_B201_editorial_manuscript_v4.json')
PROOFS=[Path('work/analysis/lil_B201_fonts_v5923b/all24_progressive_FE_native_planes_and192_alignment_cases.json'),
    Path('work/analysis/lil_B201_fonts_v5920/all24_progressive_FE_native_planes_and192_alignment_cases.json')]

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;previous=[read(p) for p in PROOFS]
    for proof in previous:
        assert proof['ARM9_sha256']==sha(arm) and proof['candidate_sha256']==doc['current_ROM_sha256']
        assert proof['current_original_macro_alignment_calls']==192 and len(proof['cases'])==24
    cases=[];reports=[];origins=[];pictures=[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[201],'FE-paper' if row['kind']=='system-FE' else 'progressive')
        enc=codec.encode_relocatable_dialogue(raw,row['english'],profile);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        assert enc.encoded.hex()==row['compiled_hex']
        assert not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and i['code']!='line-break-count']
        match=None
        for path,proof in zip(PROOFS,previous,strict=True):
            before=read(proof['manuscript']);old=next(r for r in before['records'] if r['id']==row['id'])
            candidate=next(r for r in proof['cases'] if r['id']==row['id'])
            if old['source_hex']==row['source_hex'] and old['english']==row['english'] and candidate['encoded_hex']==enc.encoded.hex():
                match=(path,proof,candidate);break
        assert match,row['id'];path,proof,candidate=match
        assert candidate['all_first_final_internal_glyphs_in_order_and_unique_cells'] and candidate['one_native_page_consumes_complete_target']
        assert sum(len(r['cases']) for r in candidate['current_native_macro_pipelines'])==8
        p=Path(candidate['preview']);assert sha(p.read_bytes())==candidate['preview_sha256']
        cases.append(deepcopy(candidate));reports.append(dict(id=row['id'],qa=qa,encoded_hex=enc.encoded.hex(),unwaived_issues=[]))
        origins.append(dict(id=row['id'],proof=str(path),proof_sha256=sha(path.read_bytes()),native_input_source_selector_logical_words_compiled_bytes_ARM9_and_snapshot_context_exact=True,
            reused_native_alignment_cases=8,source_preview=str(p),source_preview_sha256=sha(p.read_bytes())))
        pictures.append((row['id'],row['speaker'],Image.open(p).convert('RGB')))
    # Re-exercise the final formatter's complete source/selector/macro negatives.
    producer=Path('scripts/verify_lil_B201_fonts_v5923b.py');text=producer.read_text(encoding='utf-8')
    start=text.index('    negatives=[]');end=text.index('    sheets=[]',start);scoped=dedent(text[start:end])
    ns=dict(globals(),arm=arm,doc=doc,blocks=blocks,encode_relocatable_dialogue=codec.encode_relocatable_dialogue)
    exec(compile(scoped,__file__+'::unchanged-source-consumer-negatives','exec'),ns);negatives=ns['negatives'];assert len(negatives)==24
    assert len(cases)==24 and sum(r['kind']=='system-FE' for r in cases)==3
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x+5,y+24))
        p=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all24_progressive_FE_native_planes_and192_alignment_cases.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,full_QA_reports=reports,current_original_macro_alignment_calls=192,
        new_native_alignment_calls=0,exact_input_byte_identical_reused_native_alignment_cases=192,individual_native_case_origins=origins,
        progressive_alignment_calls=168,FE_null_actor_alignment_calls=24,complete_progressive_planes=21,complete_FE_logical_and_physical_planes=3,
        native_source_FI2_FA0_FO0_and_all_four_selectors_preserved=True,
        all_actor_models_and_current4MiB_context_preserved_without_overlay=True,no_whole_initialized_RAM_overlay=True,
        FE_historical_calibration=previous[0]['FE_historical_calibration'],
        scoped_profile='dk4tool/dialogue/lil_B201_profile.py',scoped_profile_sha256=sha(Path('dk4tool/dialogue/lil_B201_profile.py').read_bytes()),
        native_formatter_module='dk4tool/dialogue/lil_B201_layout_v4.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_B201_layout_v4.py').read_bytes()),
        negative_controls=negatives,final_source_consumer_negatives_freshly_reexecuted=24,source_owned_negative_adapter=scoped,
        review_sheets=sheets,visual_review_pending=True,
        current_context_plan=previous[0]['current_context_plan'],current_context_plan_sha256=previous[0]['current_context_plan_sha256'],
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,*PROOFS,producer,Path(__file__)]},
        actual_selected_B201_IDs=[],new_emulator_runs=0,completion_credit_added=0,not_registered_relocation_or_release_approval=True,full_goal_complete=False))
    print('Final24 native planes/192 alignment cases bound to exact prior inputs;zero needless native reruns.24 source-consumer negatives rerun;three final sheets await review.')
