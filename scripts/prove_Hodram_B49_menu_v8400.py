"""Original B49 menu getters, sizing, bridged results and complete English caption planes."""
import inspect
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts import native_menu_backing_surface_v4080 as backing
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_menu_v8400')
DOC=Path('translations/hodram_B49_editorial_manuscript_v2.json')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')
RELOCATION=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,packet,relocation=map(read,[DOC,CURRENT,RELOCATION])
    assert relocation['manuscript_sha256']==sha(DOC.read_bytes())
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==doc['current_ARM9_sha256']=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
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
    vm_adapter=checked_text(inspect.getsource(original.choice_vm),{
        'def choice_vm(arm, object_bytes):':'def choice_vm(arm, object_bytes, alignment):',
        "    cpu.mem_write(text - 16, b'\\xA5' * 96)":"    assert alignment in [0,2];text+=alignment\n    cpu.mem_write(text - 16, b'\\xA5' * 96)",
        'p.decode() for p in labels':"p.decode('cp932') for p in labels",
        "'VM_state': state,":"'VM_state': state, 'VM_selection_word': selection,",
    })
    env={**original.__dict__,'machine':machine};exec(compile(vm_adapter,__file__+'::exact-provider-even-alignments','exec'),env)
    m=relocation['groups'][0]['choice_commands'][0];block=Path(relocation['groups'][0]['target_block']).read_bytes()
    assert sha(block)==relocation['groups'][0]['target_block_sha256']
    at=m['new_offset'];target=block[at:at+m['new_length']];assert target.hex()==m['target_hex'] and len(target)==22
    menu=packet['typed_choices'][0];versions=[]
    for version,raw,expected in [
        ('clean-Japanese',bytes.fromhex(menu['source_command']['whole_command_hex']),[r['source_Japanese'] for r in doc['typed_choice_records']]),
        ('current-padded-English',bytes.fromhex(menu['current_command']['whole_command_hex']),['All right.','No.   ']),
        ('reviewed-stored-English',target,[r['english'] for r in doc['typed_choice_records']]),
    ]:
        cases=[]
        for alignment in [0,2]:
            result=env['choice_vm'](arm,raw,alignment)
            assert result['labels']==expected
            assert [(c['modal_selection'],c['VM_state']) for c in result['VM_cases']]==[(0,2),(1,2),(-1,0)]
            assert [c['VM_selection_word'] for c in result['VM_cases'][:2]]==[0,1]
            assert all(c['next_command_delta']==len(raw) and c['original_dispatch_ABI_and_guards_pass'] for c in result['VM_cases'])
            cases.append(dict(alignment=alignment,actual_stored_alignment=version=='reviewed-stored-English' and alignment==at%4,native_VM=result))
        assert cases[0]['native_VM']==cases[1]['native_VM']
        versions.append(dict(version=version,object_hex=raw.hex(),object_bytes=len(raw),cases=cases))
    current=versions[1]['cases'][0]['native_VM'];reviewed=versions[2]['cases'][0]['native_VM']
    assert current['minimum_width_units']==reviewed['minimum_width_units']==10
    assert current['native_width_units']==[10,6] and reviewed['native_width_units']==[10,3]
    assert current['native_menu_rectangle']==reviewed['native_menu_rectangle']
    proxy=SimpleNamespace(**({**original.__dict__,'machine':machine}))
    paint_adapter=checked_text(inspect.getsource(backing.paint),{
        "'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
        '    assert 0<width<=228':"    assert sha(arm)==CURRENT_ARM9\n    assert 0<width<=228",
    })
    penv={**backing.__dict__,'original':proxy,'CURRENT_ARM9':sha(arm)}
    exec(compile(paint_adapter,__file__+'::complete-current-font-menu-planes','exec'),penv)
    ROOT.mkdir(parents=True);planes=[];pictures=[]
    for version,vm in [('current-padded-English',current),('reviewed-stored-English',reviewed)]:
        width=vm['minimum_width_units']*6;assert width==60
        for i,label in enumerate(vm['labels']):
            for style in [1,15]:
                pixels,proof=penv['paint'](arm,label.encode('ascii'),style,width,(0,i*12))
                assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                if version=='reviewed-stored-English':assert proof['visible_cell_center_twice']==width
                path=ROOT/f'{version}_O{i}_S{style}.bin';path.write_bytes(pixels)
                planes.append(dict(version=version,option_index=i,native_plane=str(path),native_plane_sha256=sha(pixels),**proof))
                if style==1:
                    picture=Image.new('RGB',(width,12));picture.putdata([(0,8,0) if v else (239,232,201) for v in pixels])
                    pictures.append((version+' '+repr(label),picture))
    assert len(planes)==8 and len(pictures)==4
    sheet=Image.new('RGB',(920,160),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,picture) in enumerate(pictures):
        x,y=i//2*460,i%2*80;draw.text((x+5,y+5),label,fill='white');sheet.paste(picture.resize((picture.width*3,36),Image.Resampling.NEAREST),(x+5,y+25))
    sp=ROOT/'menu_caption_comparison.png';sheet.save(sp)
    save(ROOT/'menu_provider_and_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),versions=versions,even_alignment_provider_cases=6,bridged_modal_return_cases=18,native_current_andreviewed_rectangle_exact=True,current_andreviewed_caption_width_px=60,only_three_No_storage_spaces_removed_no_words_ororder_changed=True,records=planes,complete_native_caption_style_planes=8,reviewed_complete_first_internal_final_glyphs_centering_bounds_andcanaries_pass=True,source_owned_VM_adapter=vm_adapter,source_owned_painter_adapter=paint_adapter,all_executed_instructions_exact_current_sections_and123264_payload=True,executed_instruction_addresses=len(executed),historical_backing_model=[256,36],actual_B49_backing_view_highlight_controller_selection_andnormal_dismissal_pending=True,modal_loop_bridged_not_actual_controller_input=True,offline_native_calls_not_actual_whole_B49_activation=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,CURRENT,RELOCATION,Path(original.__file__),Path(backing.__file__),Path(__file__)]}))
    print('B49 menu:6 native even-alignment providers/18 bridged returns;8 complete English style planes. Width60 andrectangle unchanged;No. centered afterstorage-onlytrim.Actual backing/controller tests pending.')
