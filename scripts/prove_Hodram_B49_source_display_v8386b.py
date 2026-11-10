"""Source-only six dispatches/24 macro alignments, distinct FE page and Lil name binding."""
import inspect,struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_registered_route_context_v8303 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_source_display_v8386b')
GLOSS=Path('work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json')
INPUT=Path('work/analysis/current_V8300_Hodram_native_v8303/current_native_input.json')
START=Path('work/analysis/Hodram_registered_binding_v8303/own_Hodram_startup_andstrict_captain1_context.json')
VIEW=Path('work/analysis/Hodram_registered_startup_view_v8304/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json')
NAMES=Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
OLD_NAMES=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
DISPATCH=Path('work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json')
STORED=Path('work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json')

if __name__=='__main__':
    assert not ROOT.exists();gloss,inp,start,view,names,oldnames,dispatch,stored=map(read,[GLOSS,INPUT,START,VIEW,NAMES,OLD_NAMES,DISPATCH,STORED])
    assert gloss['all14_clean_utterances_andtwo_choices_glossed_before_current_English'] and gloss['no_current_English_comparison_localized_revision_name_item_approval_orcompletion_credit']
    image=NdsImage.open(inp['current_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT');clean=NdsImage.open('work/clean.nds')
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==start['candidate_sha256']==view['candidate_sha256']
    assert view['viewed'] and view['whole_actors_equal'] and view['reuse_requires_identical_complete_ARM9_COMMON_font_andwhole_actual_actors']
    oldimage=NdsImage.open(names['candidate']);assert all(oldimage.read_file(p)==image.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    assert sha(arm)==names['ARM9_sha256']==stored['ARM9_sha256'] and start['actual_original_captain_ID']==1
    identities=[next(r for r in oldnames['complete_clean_andcurrent_name_fields'] if r['actor_ID']==actor) for actor in [1,2]]
    for identity in identities:
        for version,im in [('clean_fields',clean),('current_fields',image)]:
            code=im.read_file('/__arm9__.bin')
            for f in identity[version]:
                at=f['table_field'];assert code[at:at+4].hex()==f['table_field_hex']
                if f['pointer']:
                    off=f['offset'];raw=bytes.fromhex(f['hex']);assert code[off:off+len(raw)+1]==raw+b'\0'
    assert [f.get('text') for f in identities[1]['clean_fields']]==['リル','アーゴット',None]
    assert [[f.get('text') for f in r['current_fields']] for r in identities]==[['Hodram','Bergstrom','Joakim'],['Lil','Argot',None]]
    getters=[r for r in names['native_twelve_progressive_andfull_getters']['rows'] if r['actor_ID'] in [1,2]]
    assert len(getters)==4 and [[r['text'] for r in getters if r['actor_ID']==actor] for actor in [1,2]]==[['Hodram Bergstrom','Hodram Joakim Bergstrom'],['Lil Argot','Lil Argot']]
    nameplanes=[r for r in names['name_planes'] if r['actor_ID'] in [1,2]];assert len(nameplanes)==2
    for name in nameplanes:assert sha(Path(name['native_plane']).read_bytes())==name['native_plane_sha256']
    progressive=checked_text(inspect.getsource(progressive_expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==1'})
    fe=checked_text(inspect.getsource(FE_expand),{"b'Lil'":"b'Hodram'","b'Argot'":"b'Bergstrom'","b'Argot Co.'":"b'Bergstrom Fleet'"})
    pe=dict(progressive_expand.__globals__);exec(compile(progressive,__file__+'::source-captain1-progressive','exec'),pe)
    fe_env=dict(FE_expand.__globals__);exec(compile(fe,__file__+'::original-null-actor-FE','exec'),fe_env)
    pixels,factory,oracle=bind(image)
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    adapters=dict(dispatch['source_owned_dispatch_adapters'])
    adapters['bind_current_catalog']=checked_text(adapters['bind_current_catalog'],{'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':'12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'})
    for key,text in adapters.items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    exec(compile(dispatch['source_owned_measured_macro_body_adapter'],__file__+'::current-captain1-substitutions','exec'),ns)
    pages_env={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes}
    page_adapter=stored['source_owned_target_page_adapter'];exec(compile(page_adapter,__file__+'::unchanged-target-complete-pages','exec'),pages_env)
    FE,calibration=factory(image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];pictures=[]
    for g in gloss['groups']:
        for row in g['records']:
            raw=bytes.fromhex(row['source_hex']);prefix=raw[0];body=raw[1:];is_FE=prefix==254
            assert prefix in [1,2,254] and body not in ns['CATALOG_LOOKUP']
            result=ctx.execute(ns['dispatch'],prefix,body);ctx.machines.pop()
            assert result['resolved_actor_ID']==(None if is_FE else prefix) and result['source_voice_class']==(None if is_FE else {1:1,2:3}[prefix])
            boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            assert boundary['text_hex']==expected.hex() and result['registered_catalog_match'] is None
            aligned=ctx.execute(fe_env['expand'] if is_FE else pe['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
            assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
            if is_FE:
                assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
                rendered=FE(expected);plane=rendered.pop('physical');logical=rendered.pop('logical');file=ROOT/(row['id']+'_FE_physical.bin');file.write_bytes(plane);logicalfile=file.with_name(row['id']+'_FE_logical.bin');logicalfile.write_bytes(logical)
                rendered.update(native_physical_plane=str(file),native_physical_plane_sha256=sha(plane),native_logical_plane=str(logicalfile),native_logical_plane_sha256=sha(logical),pages=1)
                picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in plane]);pictures.append((row['id']+' original FE',picture))
            else:
                rendered=pages_env['pages'](arm,font,expected)
                for page in rendered['pages']:
                    plane=bytes.fromhex(page.pop('native_plane_hex'));file=ROOT/(row['id']+f'_page{page["page"]}.bin');file.write_bytes(plane);page.update(native_plane=str(file),native_plane_sha256=sha(plane))
                    picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[v] for v in plane]);pictures.append((row['id']+f' original p{page["page"]}',picture))
                assert rendered['complete_consumed_bytes']==len(expected)
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],source_selector=prefix,source_hex=raw.hex(),expanded_source_hex=expected.hex(),original_dispatch=result,original_four_alignments=aligned,complete_native_source_display=rendered))
    assert len(rows)==14 and sum(len(r['original_four_alignments']['cases']) for r in rows)==56 and not ctx.machines
    assert sum(len(r['complete_native_source_display']['pages']) for r in rows if r['source_selector']!=254)==13
    sheet=Image.new('RGB',(912,1120),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,picture) in enumerate(pictures):
        x,y=i%2*456,i//2*160;draw.text((x+3,y+3),label+' offline native',fill='white');sheet.paste(picture.resize((picture.width*2,128),Image.Resampling.NEAREST),(x,y+24))
    sheetfile=ROOT/'fourteen_clean_source_pages.png';sheet.save(sheetfile)
    save(ROOT/'source_display.json',dict(candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),records=rows,
        clean_current_scoped_fields=identities,reused_original_scoped_getters=getters,reused_original_scoped_style11_planes=nameplanes,source_qualified_scoped_name_scope='Approved Hodram andestablished Lil Argot fields/getters/nameplanes reused through exact complete current code/shared/font/actualactors;no new207-name approval orasset.',
        no_FE_actor254_name_orvoice_invented=True,actual_same_captain1_whole_actors_code_COMMON_andfont_bind_prior_getters_andnameplane=True,
        original_FI_default='Hodram',default_FI6_FA9_FO15=names['measured_default_macro_lengths'],source_macro_counts=dict(FI=0,FA=0,FO=0),source_note_count=0,
        FE_original_null_actor_and228x48_288stride_6x12_metrics_16physicalpitch_bound_offline=True,FE_incidental_r1_not_panel_geometry=True,
        FE_factory_calibration=calibration,target_oracle_binding=oracle,registered_catalogue_binding=catalogue,source_owned_dispatch_adapters=adapters,source_owned_macro_body_adapter=dispatch['source_owned_measured_macro_body_adapter'],
        source_owned_progressive_adapter=progressive,source_owned_FE_adapter=fe,source_owned_target_page_adapter=page_adapter,
        review_sheet=dict(path=str(sheetfile),sha256=sha(sheetfile.read_bytes())),direct_view_pending=True,
        current_English_dialogue_bodies_unconsulted=True,current_prose_formatting_actual_source_FE_geometry_palette_andtransition_tests_pending=True,
        offline_native_CPU_tests_not_new_gameplay_orall207_names_custom_player_names_ornatural_event_activation=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,INPUT,START,VIEW,NAMES,OLD_NAMES,DISPATCH,STORED,Path('scripts/Hodram_FE_font_oracles_v8315.py'),Path(__file__)]}))
    print('Source14:14dispatches/56guarded alignments/13progressivepages/1original FEpage/no FI ornote;Hodram andLil scoped identity/getter/nameplane reuse bound.CurrentEnglish unread;source-sheet view andactualFE context pending.')
