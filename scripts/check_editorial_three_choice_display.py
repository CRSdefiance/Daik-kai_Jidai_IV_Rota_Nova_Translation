"""Check source/current/reviewed three-choice providers and every native caption plane."""
import argparse
import inspect
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image,ImageDraw
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices,labels
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts import native_menu_backing_surface_v4080 as backing
from scripts.source_locked_derivation_v5118 import checked_text

PRECEDENT=Path('work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json')
THREE_PRECEDENT=Path('work/analysis/lil_B197_choice_source_v5655/all_three_indices_and_cancel_original_VM_geometry_without_live_input.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('manuscript','release','startup','out'):parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc=load(args.manuscript);rows=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(rows)==doc['typed_choice_objects']==15
    groups={}
    for row in rows:groups.setdefault((row['block'],row['source_command_offset']),[]).append(row)
    assert len(groups)==5
    clean=NdsImage.open('work/clean.nds');ctx=RegisteredRuntime(args.release,args.startup);arm=ctx.arm
    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];executed=set()
    def machine(value):
        assert value==arm;cpu=original.machine(value)
        def exact(u,pc,size,_):
            hit=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(hit)==1,hex(pc)
            owner=hit[0];offset=pc-owner.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(owner.data[offset:offset+size]),hex(pc)
            executed.add(pc)
        cpu.hook_add(UC_HOOK_CODE,exact);return cpu
    adapter=checked_text(load(PRECEDENT)['source_owned_VM_adapter'],{
        'cpu.reg_read(UC_ARM_REG_R0) == 2':'cpu.reg_read(UC_ARM_REG_R0) == 3',
        'for index in (0, 1):':'for index in range(3):',
        '(rect, provider, maximum, 2)':'(rect, provider, maximum, 3)',
        'for selected in (0, 1, -1):':'for selected in (0, 1, 2, -1):',
    })
    # Same three-index consumer contract as the earlier source-qualified Lil proof.
    assert 'for selected in (0, 1, 2, -1):' in load(THREE_PRECEDENT)['source_derived_three_option_VM_adapter']
    env={**original.__dict__,'machine':machine};exec(compile(adapter,__file__+'::three-original-source-indices','exec'),env)
    paint_adapter=checked_text(inspect.getsource(backing.paint),{
        "'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
        '    assert 0<width<=228':'    assert sha(arm)==CURRENT_ARM9\n    assert 0<width<=228',
    })
    proxy=SimpleNamespace(**{**original.__dict__,'machine':machine})
    paint_env={**backing.__dict__,'original':proxy,'CURRENT_ARM9':sha(arm)}
    exec(compile(paint_adapter,__file__+'::unchanged-native-caption-backing','exec'),paint_env)
    args.out.mkdir(parents=True);menus=[];planes=[];pictures=[];negatives=[]
    for (block,offset),items in groups.items():
        assert [r['source_index'] for r in items]==[0,1,2]
        source,current=bytes.fromhex(items[0]['source_choice_object_hex']),bytes.fromhex(items[0]['current_choice_object_hex'])
        for image,raw,key in [(clean,source,'source'),(ctx.image,current,'current')]:
            if key=='source':ref=dict(file_path=items[0]['file_path'],block=block,command_offset=offset)
            else:ref=items[0]['current_reference']
            data=IlnkContainer.parse(image.read_file(ref['file_path'])).blocks[block]
            assert data[ref['command_offset']:ref['command_offset']+len(raw)]==raw
        target=compile_choices(source,current,items,require_formatting=False)
        versions=[]
        for name,raw in [('clean-Japanese',source),('current-padded-English',current),('reviewed-English',target)]:
            assert len(raw)+16<=96 and max(map(len,labels(raw)))<32
            expected=[v.decode('cp932') for v in labels(raw)];cases=[]
            for alignment in [0,2]:
                result=env['choice_vm'](arm,raw,alignment)
                assert result['labels']==expected
                assert [(c['modal_selection'],c['VM_state']) for c in result['VM_cases']]==[(0,2),(1,2),(2,2),(-1,0)]
                assert [c['VM_selection_word'] for c in result['VM_cases'][:3]]==[0,1,2]
                assert all(c['next_command_delta']==len(raw) and c['original_dispatch_ABI_and_guards_pass'] for c in result['VM_cases'])
                cases.append(dict(alignment=alignment,native_VM=result))
            assert cases[0]['native_VM']==cases[1]['native_VM']
            versions.append(dict(version=name,object_hex=raw.hex(),bytes=len(raw),cases=cases))
        stem=f'B{block}_C{offset}';(args.out/(stem+'_compiled_choice_object.bin')).write_bytes(target)
        for version in versions[1:]:
            vm=version['cases'][0]['native_VM'];width=vm['minimum_width_units']*6
            for index,label in enumerate(vm['labels']):
                for style in [1,15]:
                    pixels,proof=paint_env['paint'](arm,label.encode('ascii'),style,width,(0,index*12))
                    assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                    if version['version']=='reviewed-English':assert proof['visible_cell_center_twice']==width
                    path=args.out/(stem+f'_{version["version"]}_O{index}_S{style}.bin');path.write_bytes(pixels)
                    planes.append(dict(block=block,command_offset=offset,version=version['version'],option=index,path=str(path),sha256=sha(pixels),**proof))
                    if style==1:
                        pic=Image.new('RGB',(width,12));pic.putdata([(0,8,0) if v else (239,232,201) for v in pixels])
                        pictures.append((stem+' '+version['version']+' '+repr(label),pic))
        rejected=[]
        for kind in ['reordered','missing-third','changed-source','changed-current','unreviewed','padded-prose','speech-control','formatting-pending']:
            case=deepcopy(items);full=False
            if kind=='reordered':case.reverse()
            elif kind=='missing-third':case.pop()
            elif kind=='changed-source':case[0]['source_hex']='00'
            elif kind=='changed-current':case[1]['current_hex']='00'
            elif kind=='unreviewed':case[2]['review']['naturalness']=False
            elif kind=='padded-prose':case[0]['english']+=' '
            elif kind=='speech-control':case[1]['english']='{SPEAKER:01}No.'
            else:full=True
            try:compile_choices(source,current,case,require_formatting=full)
            except ValueError:rejected.append(kind)
            else:raise AssertionError(kind)
        negatives.append(dict(block=block,source_command_offset=offset,rejected=rejected))
        menus.append(dict(block=block,source_command_offset=offset,record_IDs=[r['id'] for r in items],versions=versions,target_object_hex=target.hex()))
        print(stem,'three indices/cancel and12 complete caption planes pass',flush=True)
    sheets=[]
    for start in range(0,len(pictures),12):
        part=pictures[start:start+12];sheet=Image.new('RGB',(1100,((len(part)+1)//2)*70),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(part):
            x,y=i%2*550,i//2*70;draw.text((x+4,y+2),label,fill='white');sheet.paste(pic.resize((pic.width*3,36),Image.Resampling.NEAREST),(x+4,y+22))
        path=args.out/f'native_caption_review_{start//12+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),captions=len(part)))
    # The generic successor is byte-identical for the already-qualified two-choice case.
    from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices as compile_two
    old=load('translations/hodram_B91_B110_contextual_final_review_v1.json')
    oldrows=[r for r in old['records'] if r['kind']=='typed-choice-label']
    a,b=map(bytes.fromhex,[oldrows[0]['source_choice_object_hex'],oldrows[0]['current_choice_object_hex']])
    assert compile_choices(a,b,oldrows)==compile_two(a,b,oldrows)
    save(args.out/'menu_provider_and_planes.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),runtime=ctx.receipt(),
        menus=menus,records=planes,native_provider_alignments=30,bridged_modal_returns=120,complete_English_caption_style_planes=len(planes),
        compiler_negatives_rejected=negatives,source_owned_VM_adapter=adapter,source_owned_painter_adapter=paint_adapter,review_sheets=sheets,
        exact_instruction_addresses=len(executed),complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        generic_compiler_matches_existing_two_choice_target=True,compiler_owned_zero_alignment_only_no_speech_encoder=True,
        direct_view_pending=True,actual_menu_highlight_controller_response_paths_andstored_integration_pending=True,
        bridged_modal_loop_not_actual_controller=True,new_ROM=False,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRECEDENT,THREE_PRECEDENT,args.manuscript,Path(backing.__file__),Path(original.__file__),Path('dk4tool/dialogue/reviewed_choice_object_v2.py'),Path(__file__)]}))
    print('PASS5 three-choice objects/15 labels/30 provider alignments/120 bridged returns/60 complete planes; direct review and actual English pending.')

if __name__=='__main__':main()
