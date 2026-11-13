"""Compare original name/field/role consumers using each ROM's own cold-boot RAM."""
import contextlib,inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext as ParentContext
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext as TargetContext
from scripts.square_shopkeeper_name_style_v7020 import native_name_raster,style_source_proof
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_shrines_voices_v3167 import names as catalogue_names,dynamic
from scripts.seal_generic_speaker_labels_v5887 import fields
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/square_shopkeeper_names_v7021')
RECEIPT=Path('work/analysis/square_shopkeeper_data_v7018/research_image_receipt.json')
RUN=Path('work/analysis/square_shopkeeper_run_v7019')
BASELINE=Path('work/analysis/square_shopkeeper_baseline_v6973/all414_current_getters207_voices_and_all36_owner_pointer_values.json')

if __name__=='__main__':
    assert not ROOT.exists();r=read(RECEIPT);term=read(RUN/'terminal.json');assert term['terminal']
    newrp=Path(term['report']);newreport=read(newrp)
    oldterm=read('work/analysis/lil_B221_runs_v7014/newgame_terminal.json');oldrp=Path(oldterm['report']);oldreport=read(oldrp)
    assert sha(newrp.read_bytes())==term['report_sha256'] and sha(oldrp.read_bytes())==oldterm['report_sha256']
    assert newreport['ROM_sha256']==r['research_ROM_sha256']==sha(Path(r['research_ROM']).read_bytes())
    assert oldreport['ROM_sha256']==r['parent_sha256']==sha(Path(r['parent']).read_bytes())
    assert newreport['frames']==oldreport['frames']==4001 and newreport['scripted_input_schedule']==oldreport['scripted_input_schedule']
    assert newreport['core_DLL_sha256']==oldreport['core_DLL_sha256'] and newreport['core_options']==oldreport['core_options']
    a,b=[{c['frame']:c for c in report['frames_captured']} for report in [oldreport,newreport]];assert a.keys()==b.keys()
    pairs=[]
    for frame in a:
        x,y=[Image.open(c['path']).convert('RGB') for c in [a[frame],b[frame]]]
        assert all(sha(Path(c['path']).read_bytes())==c['PNG_sha256'] for c in [a[frame],b[frame]])
        assert x.size==y.size==(256,384) and x.tobytes()==y.tobytes()
        pairs.append(dict(frame=frame,capture=b[frame]['path'],sha256=b[frame]['PNG_sha256'],whole_RGB_equal_current_V7011=True))
    assert len(pairs)==9;ROOT.mkdir(parents=True)
    name_adapter=read(BASELINE)['source_owned_getter_adapter'];env=dict(names.__globals__)
    exec(compile(name_adapter,__file__+'::all207-original-name-consumers','exec'),env)
    field_adapter=checked_text(inspect.getsource(fields),{'pointer=get(getter,root+4+ident*32)':'actor=root+0x19E4 if ident==2 else root+4+ident*32\n            pointer=get(getter,actor)'})
    field_env=dict(fields.__globals__);exec(compile(field_adapter,__file__+'::actual-captain-field-consumers','exec'),field_env)
    directory=read(read('work/analysis/current_V6956_native_v6966/current_native_input.json')['native_context_proof'])['directory_sha256']
    versions=[];contexts={}
    for label,Ctx,report,rp,rom,digest,armhash in [
        ('parent',ParentContext,oldreport,oldrp,r['parent'],r['parent_sha256'],r['source_ARM9_sha256']),
        ('target',TargetContext,newreport,newrp,r['research_ROM'],r['research_ROM_sha256'],r['target_ARM9_sha256'])]:
        snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
        assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
        cp=ROOT/(label+'_capture_context.json');save(cp,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=directory))
        inp=ROOT/(label+'_native_input.json');save(inp,dict(current_ROM=rom,current_ROM_sha256=digest,current_ARM9_sha256=armhash,current_COMMON_sha256=r['COMMON_sha256'],native_context_proof=str(cp)))
        ctx=Ctx(inp,'unused-no-historical-ROM',ROOT/(label+'_context'));values={}
        with (ROOT/(label+'_native_log.txt')).open('w',encoding='utf8') as log,contextlib.redirect_stdout(log):
            for key,fn in [('name_getters',env['names']),('catalogue_voices',catalogue_names),('field_getters',field_env['fields']),('dynamic_roles',dynamic)]:
                values[key]=ctx.execute(fn);ctx.machines.pop()
        assert not ctx.machines;contexts[label]=ctx
        versions.append(dict(case=label,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),**values))
    before,after=versions;changes={}
    for key,textkey,count in [('name_getters','text',414),('catalogue_voices','current_catalog_name',207),('field_getters','text_hex',621)]:
        aa,bb=before[key]['rows'],after[key]['rows'];assert len(aa)==len(bb)==count;changed=[]
        for x,y in zip(aa,bb,strict=True):
            assert x.keys()==y.keys()
            difference={k for k in x if x[k]!=y[k]}
            if difference:
                assert difference=={textkey} or key=='name_getters' and difference=={'text','text_hex'}
                assert 82<=x['actor_ID']<=91
                if key=='field_getters':assert x['column']==0 and x[textkey]==b'Square Shopkeeper'.hex() and y[textkey]==b'Shopkeeper'.hex()
                else:assert x[textkey]=='Square Shopkeeper' and y[textkey]=='Shopkeeper'
                changed.append(dict(actor_ID=x['actor_ID'],consumer=x.get('consumer'),column=x.get('column'),before=x[textkey],after=y[textkey],pointer=y['pointer']))
        assert len(changed)==(20 if key=='name_getters' else 10);changes[key]=changed
    assert before['dynamic_roles']['rows']==after['dynamic_roles']['rows']
    assert {x['original_voice_class'] for x in after['catalogue_voices']['rows']}==set(range(8))
    macro_versions=[]
    for label in ['parent','target']:
        ctx=contexts[label];cases=[]
        for ident in [2,*range(82,92)]:
            for body in [b'FI FA FO FU',b'Shopkeeper']:
                value=ctx.execute(expand,body,ident);ctx.machines.pop();cases.append(dict(actor_ID=ident,input_hex=body.hex(),native=value))
        assert not ctx.machines;macro_versions.append(dict(case=label,cases=cases))
    for x,y in zip(macro_versions[0]['cases'],macro_versions[1]['cases'],strict=True):
        assert x['actor_ID']==y['actor_ID'] and x['input_hex']==y['input_hex']
        xx,yy=[[bytes.fromhex(c['output_hex']) for c in z['native']['cases']] for z in [x,y]]
        expected=b'Lil Argot Argot Co. Lil Argot' if bytes.fromhex(x['input_hex'])==b'FI FA FO FU' else b'Shopkeeper'
        assert xx==yy==[expected]*4
    target=contexts['target'];raw=b'Shopkeeper';pixels,events,font=native_name_raster(target.arm,raw)
    assert pixels==expected_pixels(target.arm,font,events);visible,flushes=original_name_events(events,raw)
    assert visible==codes(raw) and not flushes and all(e['kind']=='ascii' and e['y']==0 and 0<=e['x'] and e['x']+6<=216 for e in events)
    im=Image.new('RGB',(216,64));im.putdata([(65,53,42) if p else (250,245,223) for p in pixels]);plane=ROOT/'target_Shopkeeper_native_plane.png';im.save(plane)
    sheet=Image.new('RGB',(864,180),'#263238');draw=ImageDraw.Draw(sheet);draw.text((4,4),'Shopkeeper: exact target style11;ten complete ASCII glyphs /60px',fill='white')
    sheet.paste(im.crop((0,0,216,16)).resize((864,64),Image.Resampling.NEAREST),(0,28));sp=ROOT/'target_Shopkeeper_name_review.png';sheet.save(sp)
    proof=dict(parent=r['parent'],parent_sha256=r['parent_sha256'],research_ROM=r['research_ROM'],research_ROM_sha256=r['research_ROM_sha256'],
        source_ARM9_sha256=r['source_ARM9_sha256'],target_ARM9_sha256=r['target_ARM9_sha256'],versions=versions,changed_consumers=changes,
        source_owned_name_adapter=name_adapter,source_owned_actual_captain_field_adapter=field_adapter,actual_target_opening_pairs=pairs,
        all9_whole_RGB_frames_equal_current_V7011=True,all414_parent_and414_target_getters_pass=True,all621_parent_and621_target_field_consumers_pass=True,
        only_twenty_name_getters_ten_catalogue_names_ten_primary_fields_change=True,all_other197_actors_all207_voices_and_dynamic_CF_D0_assignments_preserved=True,
        original_actual_captain2_uses_special_object=True,all_original_scratch_or_readonly_paths_restore_all4MiB=True,
        macro_versions=macro_versions,macro_alignment_cases=176,original_name_macro_UI_boundary_unexecuted=True,
        native_name_plane=dict(text='Shopkeeper',events=events,zero_ink_flushes=flushes,plane_sha256=sha(pixels),preview=str(plane),preview_sha256=sha(plane.read_bytes()),
            all_leading_internal_final_glyphs_complete_in_one_original_style11_row=True,native_width=60),original_style11_caller=style_source_proof(target.arm),
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        full_catalogue_UI_and_all_conditional_shared_nameplate_visits_not_claimed=True,target_representative_static_and_staged_nameplates_and_registered_release_pending=True,
        own_target_payload_and_each_executed_instruction_exact_no_RAM_overlay_or_forced_roles=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False)
    proof['evidence']={str(p):sha(p.read_bytes()) for p in [RECEIPT,BASELINE,RUN/'terminal.json',newrp,oldrp,Path(__file__),
        Path('scripts/square_shopkeeper_exact_native_context_v7020.py'),Path('scripts/square_shopkeeper_name_style_v7020.py'),Path('scripts/square_shopkeeper_font_oracles_v7020.py')]}
    save(ROOT/'all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json',proof)
    print('Shopkeeper target:414 getters/621 fields/207 voices per version;only20/10/10 approved outputs change.176 macro alignments and complete60px name plane pass. Representative nameplate captures/release remain pending.',flush=True)
