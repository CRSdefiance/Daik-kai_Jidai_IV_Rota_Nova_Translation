"""Fresh native calls for changed bytes;reuse only exact byte-identical reviewed planes."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue import lil_B167_layout_v5 as codec
from dk4tool.dialogue.lil_B167_profile import profile_for
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B167_fonts_v4132d import expand
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B167_fonts_v4134b')
DOC=Path('translations/lil_B167_editorial_manuscript_v7.json')
PRIOR=Path('work/analysis/lil_B167_fonts_v4134/current_macro_QA_and_progressive_font_proof.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,prior=read(DOC),read(PRIOR)
    old={r['id']:r for r in prior['cases']}
    source=read(doc['source_context'])
    im=NdsImage.open(doc['current_ROM'])
    arm=im.read_file('/__arm9__.bin')
    blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    assert sha(arm)==prior['ARM9_sha256'] and doc['current_ROM_sha256']==prior['candidate_sha256']
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B167_voices_v4120/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    cases,qa_reports,pictures,changed=[],[],[],[]
    for row in doc['records']:
        raw=bytes.fromhex(row['source_hex'])
        profile=profile_for(arm,blocks[167])
        result=codec.encode_relocatable_dialogue(raw,row['english'],profile)
        assert result.encoded.hex()==row['compiled_hex']
        qa=codec.audit_relocatable_dialogue_record(raw,row['english'],profile)
        unwaived=[i for i in qa['issues'] if i['severity'] in ['error','warning'] and not(
            i['severity']=='warning' and i['code']=='line-break-count' and row.get('qa_waiver_reason'))]
        assert not unwaived,(row['id'],unwaived)
        qa_reports.append(dict(id=row['id'],qa=qa,unwaived_issues=unwaived,documented_waivers=row.get('qa_waivers',[]),encoded_hex=result.encoded.hex()))
        previous=old[row['id']]
        if result.encoded.hex()==previous['encoded_hex']:
            assert sha(Path(previous['preview']).read_bytes())==previous['preview_sha256']
            case=deepcopy(previous)
            case['native_proof_method']='Exact compiled bytes,logical words,current runtime and source profile reuse all eight original alignment calls and complete native plane.'
        else:
            changed.append(row['id'])
            body=row['english'].split('}',1)[1].encode('ascii')
            wrapped=result.encoded[1:]
            assert all(m not in body for m in [b'FI',b'FA',b'FO'])
            pipelines=[]
            for kind,value in [('logical',body),('compiled-protected',wrapped)]:
                pipelines.append(dict(kind=kind,**ctx.execute(expand,value,raw[0])))
                ctx.machines.pop()
            assert all(c['output_hex']==wrapped.hex() for c in pipelines[1]['cases'])
            pixels,events,font=raster(ctx.arm,wrapped)
            assert pixels==expected_pixels(ctx.arm,font,events)
            visible=[e for e in events if e['code']!=32]
            assert [e['code'] for e in visible]==[ord(c) for c in wrapped.decode('ascii') if c not in ' \n']
            assert all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible)
            assert len(visible)==len({(e['x'],e['y']) for e in visible})
            origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})}
            assert all(x==0 for x in origins.values())
            path=ROOT/(row['id']+'_complete_native.png')
            image=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            image.putdata([colors[p] for p in pixels]);image.save(path)
            case=dict(id=row['id'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,expanded_hex=wrapped.hex(),
                current_native_macro_pipelines=pipelines,complete_glyph_events=events,complete_native_independent216x64_plane_equal=True,
                all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and16px_rows_within4rows=True,
                whole_native_plane_sha256=sha(pixels),visible_origins_by_row=origins,preview=str(path),preview_sha256=sha(path.read_bytes()),
                native_proof_method='Fresh original eight alignment calls and complete independent/native plane for the changed protected wrap.')
        cases.append(case)
        pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(case['preview']).convert('RGB')))
    assert changed==['DK4_MES_B167_R0112'] and len(cases)==27 and not ctx.machines
    baseline=Path('scripts/verify_lil_B167_fonts_v4132d.py')
    code=baseline.read_text(encoding='utf-8')
    negative_adapter=code[code.index('    negatives=[]'):code.index('    sheets=[]')]
    env=dict(arm=arm,blocks=blocks,doc=doc,profile_for=profile_for,encode_relocatable_dialogue=codec.encode_relocatable_dialogue)
    exec(compile('if True:\n'+negative_adapter,__file__+'::fresh-current-consumer-negatives','exec'),env)
    negatives=env['negatives']
    assert len(negatives)==19
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(920,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,image) in enumerate(pictures[start:start+8]):
            x,y=i%2*460,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white')
            sheet.paste(image.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path)
        previous=prior['review_sheets'][start//8]
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),byte_identical_to_viewed_predecessor=sha(path.read_bytes())==previous['sha256']))
    assert [s['byte_identical_to_viewed_predecessor'] for s in sheets]==[True,True,False,True]
    save(ROOT/'current_macro_QA_and_progressive_font_proof.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        ARM9_sha256=sha(arm),COMMON_sha256=sha(im.read_file('/COMMON/MESFILE.DK4')),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        cases=cases,all27_full_QA_reports=qa_reports,current_original_macro_alignment_calls=216,
        new_current_original_macro_alignment_calls=8,reused_original_macro_alignment_calls=208,new_planes=1,exact_reused_planes=26,
        negative_controls=negatives,source_owned_fresh_negative_adapter=negative_adapter,review_sheets=sheets,visual_review_pending=True,
        scoped_profile=doc['scoped_profile_module'],scoped_profile_sha256=doc['scoped_profile_module_sha256'],
        native_formatter_module=doc['native_formatter_module'],native_formatter_module_sha256=doc['native_formatter_module_sha256'],
        prior_native_proof=str(PRIOR),prior_native_proof_sha256=sha(PRIOR.read_bytes()),
        all27_progressive_full_QA_and_complete_native_fonts_pass=True,no_FE_objects_and_typed_choice_requires_separate_consumer_proof=True,
        source_complete_preambles_and_all_five_static_actors_no_macros_preserved=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PRIOR,baseline,Path(__file__)]},
        actual_selected_B167_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_completion_change=True,full_goal_complete=False))
    print(dict(planes=27,alignment_cases=216,fresh_cases=8,exact_reused_cases=208,fresh_planes=1,consumer_negatives=19,
        sheets_1_2_4_hash_match_previously_viewed=True,sheet3_visual_review_pending=True,credit=0))
