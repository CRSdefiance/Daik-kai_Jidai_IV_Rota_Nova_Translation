"""Complete19 current native progressive planes and152 original alignment cases."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_B202_profile import profile_for
from dk4tool.dialogue.lil_B202_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.lil_current_font_oracles_v5918 import expected_pixels
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B202_fonts_v5976')
DOC=Path('translations/lil_B202_editorial_manuscript_v2.json')
PROFILE=Path('dk4tool/dialogue/lil_B202_profile.py')
FORMATTER=Path('dk4tool/dialogue/lil_B202_layout_v1.py')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);source=read(doc['source_context']);im=NdsImage.open(doc['current_ROM']);arm,common=im.read_file('/__arm9__.bin'),im.read_file('/COMMON/MESFILE.DK4');blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True);inp=Path('work/analysis/lil_B202_voices_v5960/current_native_input.json');ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context')
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds';return ctx.rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    cases=[];reports=[];pictures=[];macro_calls=0
    for row in doc['records']:
        assert row['kind']=='progressive';profile=profile_for(arm,blocks[202]);raw=bytes.fromhex(row['source_hex']);qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))];assert not issues,(row['id'],issues)
        encoded=encode_relocatable_dialogue(raw,row['english'],profile);assert encoded.encoded.hex()==row['compiled_hex'] and encoded.encoded[0]==row['source_selector'];logical=row['english'].split('}',1)[1].encode('ascii');body=encoded.encoded[1:]
        assert all(raw[1:].count(m)==body.count(m)==0 for m in [b'FI',b'FA',b'FO']);pipelines=[]
        for kind,text in [('logical',logical),('compiled-protected',body)]:
            pipelines.append(dict(kind=kind,**ctx.execute(expand,text,row['source_selector'])));macro_calls+=4;ctx.machines.pop()
        assert all(c['output_hex']==body.hex() for c in pipelines[1]['cases'])
        pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events);visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[v for v in body if v not in [32,10]] and len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible);origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert origins and all(x==0 for x in origins.values())
        picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[p] for p in pixels]);preview=ROOT/(row['id']+'_complete_native.png');picture.save(preview);pictures.append((row['id'],row['speaker'],picture))
        cases.append(dict(id=row['id'],kind='progressive',encoded_hex=encoded.encoded.hex(),formatted_markup=encoded.formatted_markup,expanded_hex=body.hex(),current_native_macro_pipelines=pipelines,complete_glyph_events=events,complete_native_independent216x64_plane_equal=True,whole_native_plane_sha256=sha(pixels),all_first_final_internal_glyphs_in_order_and_unique_cells=True,all_visible_origins_zero_and_within_four_rows=True,visible_origins_by_row=origins,one_native_page_consumes_complete_target=True,original_progressive54020_consumer_preserved=True,preview=str(preview),preview_sha256=sha(preview.read_bytes())))
        reports.append(dict(id=row['id'],qa=qa,encoded_hex=encoded.encoded.hex(),unwaived_issues=issues,documented_waivers=row.get('qa_waivers',[])));print(row['id']+' complete progressive',flush=True)
    assert len(cases)==len(reports)==19 and macro_calls==152 and not ctx.machines
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as error:negatives.append(dict(case=label,error=str(error),rejected=True))
        else:raise AssertionError(label)
    reject('mutated-runtime',lambda:profile_for(bytes([arm[0]^1])+arm[1:],blocks[202]))
    reject('unrelated-source-block',lambda:profile_for(arm,blocks[201]))
    reject('mutated-source-block',lambda:profile_for(arm,blocks[202][:-1]+bytes([blocks[202][-1]^1])))
    for consumer in ['typed-choice','FE-paper']:reject('unsupported-'+consumer,lambda c=consumer:profile_for(arm,blocks[202],c))
    for selector in [2,18,147,157]:
        row=next(r for r in doc['records'] if r['source_selector']==selector);profile=profile_for(arm,blocks[202]);tag='{SPEAKER:'+format(selector,'02X')+'}';other='{SPEAKER:'+format(18 if selector==2 else 2,'02X')+'}'
        reject('missing-selector-'+str(selector),lambda r=row,p=profile,t=tag:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,''),p))
        reject('changed-selector-'+str(selector),lambda r=row,p=profile,t=tag,o=other:encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'].replace(t,o),p))
    plain=next(r for r in doc['records'] if r['source_selector']==18);prog=profile_for(arm,blocks[202])
    for macro in ['FI','FA','FO']:reject('invented-macro-'+macro,lambda m=macro:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+' {MACRO:'+m+'}',prog))
    for label,suffix in [('manual-layout','{LB}'),('embedded-NUL','{HEX:00}')]:reject(label,lambda s=suffix:encode_relocatable_dialogue(bytes.fromhex(plain['source_hex']),plain['english']+s,prog))
    reject('source00-outside-scope',lambda:encode_relocatable_dialogue(b'\0Japanese','{SPEAKER:00}Hello.',prog))
    reject('FE-through-progressive',lambda:encode_relocatable_dialogue(b'\xfeJapanese','{SPEAKER:FE}Hello.',prog))
    reject('unbound-actor-prefix',lambda:encode_relocatable_dialogue(b'\x75Japanese','{SPEAKER:75}Hello.',prog));assert len(negatives)==21
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,pic) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white');sheet.paste(pic.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        p=ROOT/f'current_native_sheet{start//8+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all19_progressive_native_planes_and152_alignment_cases.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,full_QA_reports=reports,current_original_macro_alignment_calls=152,progressive_alignment_calls=152,FE_null_actor_alignment_calls=0,complete_progressive_planes=19,complete_FE_logical_and_physical_planes=0,native_source_FI0_FA0_FO0_and_all_four_selectors_preserved=True,all_actor_models_and_current4MiB_context_preserved_without_overlay=True,no_whole_initialized_RAM_overlay=True,scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),negative_controls=negatives,review_sheets=sheets,visual_review_pending=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B202_IDs=[],new_emulator_runs=0,completion_credit_added=0,not_registered_relocation_or_release_approval=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All19 current-font progressive planes,152 alignments and21 source-consumer negatives pass;three sheets await visual review.',flush=True)
