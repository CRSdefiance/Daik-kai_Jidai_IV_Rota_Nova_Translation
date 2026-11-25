"""Complete B178 progressive/FE native planes and104 original alignment cases."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B178_profile import profile_for
from dk4tool.dialogue.lil_B178_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_fonts_v4677')
DOC=Path('translations/lil_B178_editorial_manuscript_v2.json')
PROFILE=Path('dk4tool/dialogue/lil_B178_profile.py')
FORMATTER=Path('dk4tool/dialogue/lil_B178_layout_v1.py')

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(DOC);source=read(doc['source_context']);im=NdsImage.open(doc['current_ROM'])
    arm,common=im.read_file('/__arm9__.bin'),im.read_file('/COMMON/MESFILE.DK4')
    blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True)
    contextpath=ROOT/'historical_source_context.json'
    save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json'
    save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__)
    raster.__kwdefaults__=original_raster.__kwdefaults__
    paint,calibration=make_painter(im)
    cases=[];qa_reports=[];pictures=[];macro_calls=0
    for row in doc['records']:
        isFE=row['kind']=='system-FE'
        profile=profile_for(arm,blocks[row['block']],'FE-paper' if isFE else 'progressive')
        raw=bytes.fromhex(row['source_hex'])
        qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not
                (i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))]
        assert not issues,(row['id'],issues)
        encoded=encode_relocatable_dialogue(raw,row['english'],profile)
        assert encoded.encoded.hex()==row['compiled_hex'] and encoded.encoded[0]==row['source_selector']
        qa_reports.append(dict(id=row['id'],qa=qa,encoded_hex=encoded.encoded.hex(),unwaived_issues=issues,
            documented_waivers=row.get('qa_waivers',[])))
        logical=row['english'].split('}',1)[1]
        for m in ['FI','FA','FO']:logical=logical.replace('{MACRO:'+m+'}',m)
        logical=logical.encode('ascii');body=encoded.encoded[1:]
        assert all(raw.count(m)==body.count(m) for m in [b'FI',b'FA',b'FO'])
        expected=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        pipelines=[]
        for kind,text in [('logical',logical),('compiled-protected',body)]:
            args=() if isFE else (row['source_selector'],)
            pipelines.append(dict(kind=kind,**ctx.execute(FE_expand if isFE else progressive_expand,text,*args)))
            macro_calls+=4;ctx.machines.pop()
        assert all(c['output_hex']==expected.hex() for c in pipelines[1]['cases'])
        if isFE:
            assert all(c['null_source_actor'] for p in pipelines for c in p['cases'])
            target=paint(expected);events=target['events']
            assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
            picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if p else (239,232,201) for p in target['physical']])
            plane=ROOT/(row['id']+'_complete_logical_228x48.bin');plane.write_bytes(target['logical'])
            details=dict(complete_native_independent228x48_plane_equal=True,whole_native_plane_sha256=sha(target['logical']),
                native_plane=str(plane),whole_physical228x64_plane_sha256=sha(target['physical']),
                one_native_page_consumes_complete_target=True,original_null_actor_consumer_preserved=True,
                input_objects_canaries_and_all_glyphs_complete=True,object_rebindings=target['object_rebindings'])
            pitch=12;maxx=222;maxy=36
        else:
            pixels,events,font=raster(arm,expected)
            assert pixels==expected_pixels(arm,font,events)
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
            picture.putdata([colors[p] for p in pixels])
            details=dict(complete_native_independent216x64_plane_equal=True,whole_native_plane_sha256=sha(pixels),
                one_native_page_consumes_complete_target=True,original_progressive54020_consumer_preserved=True)
            pitch=16;maxx=210;maxy=48
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[v for v in expected if v not in [32,10]]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=maxx and 0<=e['y']<=maxy and e['y']%pitch==0 for e in visible)
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})}
        assert origins and all(x==0 for x in origins.values())
        preview=ROOT/(row['id']+'_complete_native.png');picture.save(preview)
        pictures.append((row['id'],row['speaker'],picture))
        cases.append(dict(id=row['id'],kind=row['kind'],encoded_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,
            expanded_hex=expected.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,
            all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and_within_four_rows=True,
            visible_origins_by_row=origins,preview=str(preview),preview_sha256=sha(preview.read_bytes()),**details))
        print(row['id']+' complete '+('FE' if isFE else 'progressive'),flush=True)
    assert len(cases)==len(qa_reports)==13 and macro_calls==104 and not ctx.machines
    assert sum(c['kind']=='system-FE' for c in cases)==1
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,error=str(error),rejected=True))
        else:raise AssertionError(label)
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[178]))
    reject('unrelated-source-block',lambda:profile_for(arm,blocks[177]))
    reject('mutated-source-block',lambda:profile_for(arm,blocks[178][:-1]+bytes([blocks[178][-1]^1])))
    reject('invented-consumer',lambda:profile_for(arm,blocks[178],'typed-choice'))
    for selector in [166,167,168,254]:
        row=next(r for r in doc['records'] if r['source_selector']==selector)
        profile=profile_for(arm,blocks[178],'FE-paper' if selector==254 else 'progressive')
        tag='{SPEAKER:'+format(selector,'02X')+'}';other='{SPEAKER:'+format(167 if selector==166 else 166,'02X')+'}'
        reject('missing-selector-'+str(selector),lambda r=row,p=profile,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),p))
        reject('changed-selector-'+str(selector),lambda r=row,p=profile,t=tag,o=other:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,o),p))
    plain=next(r for r in doc['records'] if r['source_selector']==166 and '{MACRO:' not in r['english'])
    prog=profile_for(arm,blocks[178]);fe=profile_for(arm,blocks[178],'FE-paper')
    for macro in ['FI','FA','FO']:
        reject('invented-macro-'+macro,lambda m=macro:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:'+m+'}',prog))
    for label,suffix in [('manual-layout','{LB}'),('embedded-NUL','{HEX:00}')]:
        reject(label,lambda s=suffix:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+s,prog))
    reject('source00-outside-scope',lambda:encode_relocatable_dialogue(b'\0Japanese','{SPEAKER:00}Hello.',prog))
    reject('FE-through-progressive-profile',lambda:encode_relocatable_dialogue(b'\xfeJapanese','{SPEAKER:FE}Hello.',prog))
    reject('progressive-through-FE-profile',lambda:encode_relocatable_dialogue(b'\x02Japanese','{SPEAKER:02}Hello.',fe))
    assert len(negatives)==20
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160
            draw.text((x+5,y+3),ident+' / '+speaker,fill='white')
            sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'all13_progressive_FE_native_planes_and104_alignment_cases.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,full_QA_reports=qa_reports,
        current_original_macro_alignment_calls=104,progressive_alignment_calls=96,FE_null_actor_alignment_calls=8,
        complete_progressive_planes=12,complete_FE_logical_and_physical_planes=1,
        native_source_FI0_FA0_FO0_and_all_four_selectors_preserved=True,
        all_actor_models_and_original4MiB_context_preserved_under_bounded_overlays=True,no_whole_initialized_RAM_overlay=True,
        FE_historical_calibration=calibration,scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),
        native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),
        negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,
        current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_selected_B178_IDs=[],new_emulator_runs=0,completion_credit_added=0,
        not_registered_relocation_or_release_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All13 complete native planes,104 alignment cases and20 source-consumer negatives pass;two sheets need visual review.',flush=True)
