"""Native constructor width, result forwarding and full caption planes; actual backing still pending."""
import inspect,struct
from types import SimpleNamespace
from pathlib import Path
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_menu_backing_surface_v4080 as backing
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_choice_planes_v7934')
DOC=Path('translations/rafael_B46_editorial_manuscript_v1.json')
MENU=Path('work/analysis/Rafael_B46_current_menu_v7929/two_current_choices_native_getters_geometry_exact_control_inverse_Hayreddin_component.json')
FLOW=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,menu,flow=map(read,[DOC,MENU,FLOW])
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(arm)==doc['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    chunks=[];offsets=[];cursor=0
    for row in doc['typed_choice_records']:
        label=row['english'].encode('ascii')
        assert label and label.strip()==label and not any(v in label for v in [b'\n',b'\r',b'\0',b'%'])
        offsets.append(cursor);chunk=label+b'\0';chunk+=b'\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    target=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks);assert len(target)==30
    venv=dict(original.__dict__);exec(compile(flow['source_owned_VM_adapter'],__file__+'::target-native-choice-provider','exec'),venv)
    target_vm=venv['choice_vm'](arm,target)
    assert target_vm['labels']==[r['english'] for r in doc['typed_choice_records']]
    assert target_vm['minimum_width_units']==11 and target_vm['native_width_units']==[10,11]
    previous=next(r for r in menu['native_menu_versions'] if r['version']=='current-English')
    assert previous['native_VM']['labels']==['Please do.  ','No, thanks.   '] and previous['native_VM']['minimum_width_units']==14
    assert [(r['modal_selection'],r['VM_state'],r['VM_selection_word']) for r in target_vm['VM_cases']]==[(r['modal_selection'],r['VM_state'],r['VM_selection_word']) for r in previous['native_VM']['VM_cases']]
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    owned=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];executed=set()
    def machine(current_arm):
        assert current_arm==arm;cpu=original.machine(current_arm)
        def exact(u,pc,size,unused):
            owners=[s for s in owned if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            section=owners[0];at=pc-section.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(section.data[at:at+size]),hex(pc)
            executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    proxy=SimpleNamespace(**(dict(original.__dict__)|{'machine':machine}))
    adapter=checked_text(inspect.getsource(backing.paint),{
        "'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
        '    assert 0<width<=228':"    assert sha(arm)==CURRENT_ARM9\n    assert 0<width<=228",
    })
    env={**backing.__dict__,'original':proxy,'CURRENT_ARM9':sha(arm)}
    exec(compile(adapter,__file__+'::current-full-independent-menu-glyphs','exec'),env)
    ROOT.mkdir(parents=True);cases=[];pictures=[]
    for version,labels,width in [('current-padded',previous['native_VM']['labels'],84),('reviewed-trimmed',target_vm['labels'],66)]:
        planes=[]
        for index,label in enumerate(labels):
            for style in [1,15]:
                pixels,proof=env['paint'](arm,label.encode('ascii'),style,width,(0,index*12))
                assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                if version=='reviewed-trimmed':assert proof['visible_cell_center_twice']==width
                path=ROOT/f'{version}_O{index}_style{style}.bin';path.write_bytes(pixels)
                planes.append(dict(index=index,native_plane=str(path),native_plane_sha256=sha(pixels),**proof))
                if style==1:
                    im=Image.new('RGB',(width,12));im.putdata([(8,8,8) if p else (239,232,201) for p in pixels])
                    ip=path.with_suffix('.png');im.save(ip);pictures.append((f'{version} option{index}: {label!r}',im))
        cases.append(dict(version=version,caption_width_px=width,caption_height_px=12,
            historical_owned_backing_model=[256,36],actual_B46_backing_not_yet_observed=True,planes=planes))
    assert sum(len(c['planes']) for c in cases)==8 and len(pictures)==4
    sheet=Image.new('RGB',(1000,160),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(title,im) in enumerate(pictures):
        x,y=i//2*500,i%2*80;draw.text((x+5,y+5),title,fill='white')
        sheet.paste(im.resize((im.width*3,36),Image.Resampling.NEAREST),(x+5,y+25))
    sp=ROOT/'two_current_and_reviewed_native_choices.png';sheet.save(sp)
    save(ROOT/'two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json',dict(
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),current_menu=str(MENU),current_menu_sha256=sha(MENU.read_bytes()),
        target_menu_object_hex=target.hex(),target_menu_bytes=30,previous_menu_bytes=36,
        native_target_VM=target_vm,previous_native_VM=previous['native_VM'],records=cases,
        complete_current_andreviewed_label_style_planes=8,reviewed_labels_centered_complete_first_internal_final_glyphs_bounds_canaries=True,
        only_storage_spaces_removed_no_choice_wording_ororder_change=True,original_constructor_controls_geometry_not_authored_padding=True,
        target_caption_width66_previous84_from_native_providers=True,
        source_owned_painter_adapter=adapter,all_executed_instructions_exact_current_sections_and123264_staged_payload=True,
        native_painter_executed_instruction_addresses=len(executed),current_font_one_pixel_descent_independently_matched=True,
        historical_backing_model_reference='work/analysis/lil_B166_menu_owner_trace_v4086/actual_caption_context_view_and_backing.json',
        actual_B46_backing_view_highlights_original_input_selection_andbranch_return_pending=True,
        offline_full_surface_checks_not_actual_B46_capture=True,
        review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,
        no_ROM_registry_ledger_font_runtime_orcompletion_change=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MENU,FLOW,Path(backing.__file__),Path(original.__file__),Path(__file__)]},full_goal_complete=False))
    print('Two labels/eight full native style planes pass; width84 padded→66 trimmed computed by native constructor. Three bridged result cases unchanged; actual backing/highlights pending.')
