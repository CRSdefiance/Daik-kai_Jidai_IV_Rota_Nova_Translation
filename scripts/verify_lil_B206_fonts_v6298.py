"""24 complete current-native progressive planes and192 original alignment calls;four menus separate."""
from pathlib import Path
from types import FunctionType
from dataclasses import replace
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B206_profile_v1 import profile_for
from dk4tool.dialogue.lil_B206_layout_v3 import encode_relocatable_dialogue,audit_relocatable_dialogue_record,ORDINARY_WRAP_REVIEWS
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_fonts_v6298');DOC=Path('translations/lil_B206_editorial_manuscript_v5.json');PROFILE=Path('dk4tool/dialogue/lil_B206_profile_v1.py');FORMATTER=Path('dk4tool/dialogue/lil_B206_layout_v3.py')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;ROOT.mkdir(parents=True)
    ctx=CurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    cases=[];reports=[];pictures=[];calls=0;reused_calls=0
    from copy import deepcopy
    priorpath=Path('work/analysis/lil_B206_fonts_v6295/all24_progressive_complete_native_planes192_alignment_cases.json');previous=read(priorpath);old_doc=read(previous['manuscript']);old_rows={r['id']:r for r in old_doc['records']};old_cases={r['id']:r for r in previous['cases']}
    assert previous['ARM9_sha256']==sha(arm) and previous['COMMON_sha256']==sha(ctx.common) and previous['candidate_sha256']==doc['current_ROM_sha256'] and previous['scoped_profile_sha256']==sha(PROFILE.read_bytes())
    assert read(previous['current_context_plan'])['actual_snapshot']['sha256']==sha(ctx.raw)
    for path,digest in previous['evidence'].items():assert sha(Path(path).read_bytes())==digest
    fresh_indices=[];reused_indices=[]
    for row in doc['records']:
        if row['kind']=='typed-choice-label':assert row['review']['formatting'];continue
        assert row['kind']=='progressive';raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[206]);qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))];assert not issues,(row['id'],issues)
        encoded=encode_relocatable_dialogue(raw,row['english'],profile);assert encoded.encoded.hex()==row['compiled_hex'] and encoded.encoded[0]==row['source_selector'];logical=row['english'].split('}',1)[1].encode('ascii');body=encoded.encoded[1:]
        assert all(raw[1:].count(m)==logical.count(m)==body.count(m)==0 for m in [b'FI',b'FA',b'FO'])
        old_row=old_rows[row['id']];old_case=old_cases[row['id']]
        assert all(old_row[k]==row[k] for k in ['source_hex','current_hex','source_reference','current_reference','english','source_selector'])
        if old_row['compiled_hex']==row['compiled_hex']:
            assert old_case['encoded_hex']==encoded.encoded.hex() and old_case['expanded_hex']==body.hex() and old_case['complete_native_independent216x64_plane_equal'] and old_case['one_native_page_consumes_complete_target']
            assert sha(Path(old_case['preview']).read_bytes())==old_case['preview_sha256'] and sum(len(v['cases']) for v in old_case['current_native_macro_pipelines'])==8
            assert all(c['output_hex']==body.hex() for p in old_case['current_native_macro_pipelines'] if p['kind']=='compiled-protected' for c in p['cases'])
            case=deepcopy(old_case);case['reviewed_ordinary_boundaries']=qa.get('reviewed_ordinary_boundaries',[]);case['native_evidence_reused_from']=str(priorpath);case['native_evidence_reused_from_sha256']=sha(priorpath.read_bytes());cases.append(case)
            reports.append(dict(id=row['id'],qa=qa,unwaived_issues=issues,documented_rowcount_waivers=row.get('qa_waivers',[])));pictures.append((row['id'],row['speaker'],Image.open(case['preview']).convert('RGB')));reused_calls+=8;reused_indices.append(row['source_record_index']);print(row['id']+' exact native input/plane reuse',flush=True);continue
        fresh_indices.append(row['source_record_index']);pipelines=[]
        for kind,value in [('logical',logical),('compiled-protected',body)]:
            pipelines.append(dict(kind=kind,**ctx.execute(expand,value,row['source_selector'])));ctx.machines.pop();calls+=4
        assert all(bytes.fromhex(c['output_hex'])==body for c in pipelines[1]['cases'])
        pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events)
        visible=[e for e in events if e['code']!=32];assert [e['code'] for e in visible]==[b for b in body if b not in [10,32]] and len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible);origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        path=ROOT/(row['id']+'_complete_native.png');photo=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};photo.putdata([colors[p] for p in pixels]);photo.save(path);pictures.append((row['id'],row['speaker'],photo))
        cases.append(dict(id=row['id'],source_selector=row['source_selector'],encoded_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,expanded_hex=body.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,whole_native_plane_sha256=sha(pixels),complete_native_independent216x64_plane_equal=True,one_native_page_consumes_complete_target=True,all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and_within_four_rows=True,visible_origins_by_row=origins,preview=str(path),preview_sha256=sha(path.read_bytes()),reviewed_ordinary_boundaries=qa.get('reviewed_ordinary_boundaries',[])))
        reports.append(dict(id=row['id'],qa=qa,unwaived_issues=issues,documented_rowcount_waivers=row.get('qa_waivers',[])));print(row['id']+' complete progressive',flush=True)
    assert len(cases)==24 and calls==24 and reused_calls==168 and fresh_indices==[24,53,90] and not ctx.machines and sum(bool(r['reviewed_ordinary_boundaries']) for r in cases)==5
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,error=str(e),rejected=True))
        else:raise AssertionError('Invalid accepted:'+label)
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[206]));reject('unrelated-source-block',lambda:profile_for(arm,blocks[205]));reject('mutated-source-block',lambda:profile_for(arm,blocks[206][:-1]+bytes([blocks[206][-1]^1])));reject('FE-consumer',lambda:profile_for(arm,blocks[206],'FE-paper'));reject('typed-menu-through-speech-profile',lambda:profile_for(arm,blocks[206],'typed-choice'))
    p=profile_for(arm,blocks[206]);rows=[r for r in doc['records'] if r['kind']=='progressive']
    for selector in [2,7,173]:
        row=next(r for r in rows if r['source_selector']==selector);tag='{SPEAKER:'+format(selector,'02X')+'}';other='{SPEAKER:'+format(7 if selector==2 else 2,'02X')+'}'
        reject('missing-selector-'+str(selector),lambda r=row,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),p));reject('changed-selector-'+str(selector),lambda r=row,t=tag,o=other:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,o),p))
    plain=rows[0];raw=bytes.fromhex(plain['source_hex'])
    for macro in ['FI','FA','FO']:reject('invented-macro-'+macro,lambda m=macro:encode_relocatable_dialogue(raw,plain['english']+' {MACRO:'+m+'}',p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{HEX:00}']:reject('unsafe-'+tag,lambda t=tag:encode_relocatable_dialogue(raw,plain['english']+t,p))
    for selector in [0,15,254]:reject('unowned-selector-'+str(selector),lambda s=selector:encode_relocatable_dialogue(bytes([s])+b'Japanese','{SPEAKER:'+format(s,'02X')+'}Hello.',p))
    for label,bad in [('width',replace(p,window_width_px=228)),('rows',replace(p,max_lines=5)),('glyph-width',replace(p,default_ascii_width=5)),('row-spacing',replace(p,line_height_px=12)),('guard',replace(p,guard_linebreaks=False)),('pair-phase',replace(p,pair_phase_safe_breaks=False)),('balancing',replace(p,balanced_wrapping=False)),('macro-length',replace(p,macro_ascii_lengths={**p.macro_ascii_lengths,'FI':4})),('widened-selector-set',replace(p,leading_speaker_bytes=p.leading_speaker_bytes|{254})),('unscoped-base',get_dialogue_profile('lil-opening-editorial-native-v1'))]:reject('formatter-'+label,lambda bad=bad:encode_relocatable_dialogue(raw,plain['english'],bad))
    for rule in ORDINARY_WRAP_REVIEWS:
        original=bytes.fromhex(rule['source_hex']);bad=original[:1]+bytes([original[1]^1])+original[2:];reject('ordinary-boundary-wrong-source-'+rule['id'],lambda bad=bad,r=rule:encode_relocatable_dialogue(bad,r['target'],p))
        altered=audit_relocatable_dialogue_record(original,rule['target']+' Huh?',p);assert not altered.get('reviewed_ordinary_boundaries');negatives.append(dict(case='ordinary-boundary-no-blanket-English-exemption-'+rule['id'],rejected=True,error='Changed prose receives no source-specific boundary approval'))
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,photo) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white');sheet.paste(photo.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'all24_final_progressive_planes24_fresh168_exact_reused_alignment_cases.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(ctx.common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,full_QA_reports=reports,current_original_macro_alignment_calls=24,covered_native_alignment_cases=192,exact_input_byte_identical_reused_native_alignment_cases=168,fresh_plane_indices=fresh_indices,reused_plane_indices=reused_indices,complete_progressive_planes=24,source_FE_planes=0,source_three_static_actors_zero_macros_and_separate_four_approved_menu_labels=True,all_actor_models_and_current4MiB_context_preserved_without_overlay=True,no_whole_initialized_RAM_overlay=True,scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B206_IDs=[],new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,PROFILE,FORMATTER,Path(__file__),Path('scripts/shady_man_font_oracles_v6263.py'),Path('scripts/current_build_native_context_v6261b.py'),Path('scripts/verify_lil_B174_fonts_v4470.py')]}));print(dict(complete_progressive_planes=24,new_original_alignment_calls=24,exact_reused_alignment_cases=168,source_and_formatter_negatives=len(negatives),viewed_sheets_pending=len(sheets),actual_English_scene_and_release_pending=True))
