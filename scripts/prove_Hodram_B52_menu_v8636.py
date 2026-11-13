"""Compile retained B52 choice words and measure both native English menu shapes/glyph planes."""
import inspect,struct
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
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_menu_v8636')
DOC=Path('translations/hodram_B52_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Hodram_B52_current_v8631/current_effective.json')
SOURCE=Path('work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')

def compile_object(rows):
    assert len(rows)==2 and [r['option_index'] for r in rows]==[0,1]
    chunks=[];offsets=[];cursor=0
    for row in rows:
        label=row['english'];assert label==label.strip() and label and not any(v in label for v in ['\n','\r','\0','%','{','}'])
        offsets.append(cursor);chunk=label.encode('ascii')+b'\0';chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    return struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)

if __name__=='__main__':
    assert not ROOT.exists();doc,packet,source=map(read,[DOC,CURRENT,SOURCE]);rows=doc['typed_choice_records']
    assert [r['id'] for r in rows]==['DK4_MES_B52_R0011','DK4_MES_B52_R0013'] and all(r['decision']=='retention' and not r['review']['formatting'] for r in rows)
    target=compile_object(rows);assert len(target)==32 and struct.unpack_from('<3H',target)==(0x2100,0,12)
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==source['candidate_sha256'] and sha(arm)==doc['current_ARM9_sha256']==source['ARM9_sha256']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    owned=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];executed=set()
    def machine(current_arm):
        assert current_arm==arm;cpu=original.machine(current_arm)
        def exact(u,pc,size,unused):
            owners=[s for s in owned if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            section=owners[0];at=pc-section.ramAddress;assert bytes(u.mem_read(pc,size))==bytes(section.data[at:at+size]),hex(pc);executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    vm_adapter=source['source_owned_VM_adapter'];env={**original.__dict__,'machine':machine};exec(compile(vm_adapter,__file__+'::exact-original-choice-provider','exec'),env)
    menu=packet['typed_choices'][0];current=bytes.fromhex(menu['current_command']['whole_command_hex'])
    assert len(current)==36 and [r['english'] for r in rows]==[r['current_effective_paragraph'] for r in menu['records']]
    versions=[]
    for version,raw,expected in [('current-padded-English',current,[r['current_English'] for r in menu['records']]),('reviewed-stored-English',target,[r['english'] for r in rows])]:
        cases=[]
        for alignment in [0,2]:
            result=env['choice_vm'](arm,raw,alignment);assert result['labels']==expected
            assert [(c['modal_selection'],c['VM_state']) for c in result['VM_cases']]==[(0,2),(1,2),(-1,0)]
            assert [c['VM_selection_word'] for c in result['VM_cases'][:2]]==[0,1]
            assert all(c['next_command_delta']==len(raw) and c['original_dispatch_ABI_and_guards_pass'] for c in result['VM_cases'])
            getters=choice_getters(arm,dict(offset=68,whole_command_hex=raw.hex(),word=0x2100,native_extent=len(raw)))
            assert len(getters)==2 and all(c['count']==2 and [r['text'] for r in c['labels']]==expected for c in getters)
            cases.append(dict(alignment=alignment,native_VM=result))
        assert cases[0]['native_VM']==cases[1]['native_VM'];versions.append(dict(version=version,object_hex=raw.hex(),object_bytes=len(raw),cases=cases))
    current_VM,target_VM=[v['cases'][0]['native_VM'] for v in versions]
    assert current_VM['native_width_units']==[14,12] and target_VM['native_width_units']==[11,12]
    assert current_VM['minimum_width_units']==14 and target_VM['minimum_width_units']==12
    proxy=SimpleNamespace(**({**original.__dict__,'machine':machine}))
    paint_adapter=checked_text(inspect.getsource(backing.paint),{
        "'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
        '    assert 0<width<=228':"    assert sha(arm)==CURRENT_ARM9\n    assert 0<width<=228",
    })
    penv={**backing.__dict__,'original':proxy,'CURRENT_ARM9':sha(arm)};exec(compile(paint_adapter,__file__+'::complete-native-caption-planes','exec'),penv)
    ROOT.mkdir(parents=True);planes=[];pictures=[]
    (ROOT/'compiled_two_choice_object.bin').write_bytes(target)
    for version,vm in [('current-padded-English',current_VM),('reviewed-stored-English',target_VM)]:
        width=vm['minimum_width_units']*6
        for index,label in enumerate(vm['labels']):
            for style in [1,15]:
                pixels,proof=penv['paint'](arm,label.encode('ascii'),style,width,(0,index*12))
                assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                if version=='reviewed-stored-English':assert proof['visible_cell_center_twice']==width
                path=ROOT/f'{version}_O{index}_S{style}.bin';path.write_bytes(pixels);planes.append(dict(version=version,option_index=index,native_plane=str(path),native_plane_sha256=sha(pixels),**proof))
                if style==1:
                    picture=Image.new('RGB',(width,12));picture.putdata([(0,8,0) if v else (239,232,201) for v in pixels]);pictures.append((version+' '+repr(label),picture))
    assert len(planes)==8 and len(pictures)==4
    sheet=Image.new('RGB',(920,180),'#263238');draw=ImageDraw.Draw(sheet)
    for index,(label,picture) in enumerate(pictures):
        x,y=index//2*460,index%2*90;draw.text((x+5,y+5),label,fill='white');sheet.paste(picture.resize((picture.width*3,36),Image.Resampling.NEAREST),(x+5,y+28))
    path=ROOT/'current_andreviewed_menu_caption_shapes.png';sheet.save(path)
    save(ROOT/'menu_provider_and_planes.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),current=str(CURRENT),current_sha256=sha(CURRENT.read_bytes()),source_VM=str(SOURCE),source_VM_sha256=sha(SOURCE.read_bytes()),versions=versions,compiled_choice_object=str(ROOT/'compiled_two_choice_object.bin'),compiled_choice_object_sha256=sha(target),even_alignment_provider_cases=4,bridged_modal_return_cases=12,source_Japanese_provider_cases_reused_not_replayed=True,current_width_px=84,reviewed_width_px=72,current_rectangle=current_VM['native_menu_rectangle'],reviewed_rectangle=target_VM['native_menu_rectangle'],menu_shape_changes_due_only_to_three_unspoken_storage_spaces_removed=True,all_choice_words_order_original_count_andsource_identity_retained=True,records=planes,complete_native_caption_style_planes=8,reviewed_complete_first_internal_final_glyphs_centering_bounds_andcanaries_pass=True,source_owned_VM_adapter=vm_adapter,source_owned_painter_adapter=paint_adapter,source_owned_choice_compiler=inspect.getsource(compile_object),all_executed_instructions_exact_current_sections_and123264_payload=True,executed_instruction_addresses=len(executed),source_Japanese_caption_glyphs_andactual_source_English_backing_highlight_controller_normal_andflagged_end_transitions_pending=True,modal_loop_bridged_not_actual_controller_input=True,offline_native_calls_not_actual_whole_B52_activation=True,review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),direct_view_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,CURRENT,SOURCE,Path(original.__file__),Path(backing.__file__),Path(__file__)]}))
    print('B52 retained choice words:32-byte typed object,4native providers/12bridgedreturns,8complete styleplanes; width84 to72 after3storage spaces removed. Actual changed-menu geometry/highlight/controller/end transitions remain pending.')
