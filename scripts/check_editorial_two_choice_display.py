"""Source/current/reviewed native two-choice providers and complete English caption planes."""
import argparse
import inspect
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from PIL import Image,ImageDraw
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices,labels
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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('manuscript','release','startup','out'):parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc=load(args.manuscript);rows=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(rows)==doc['typed_choice_objects']==2
    source,current=bytes.fromhex(rows[0]['source_choice_object_hex']),bytes.fromhex(rows[0]['current_choice_object_hex'])
    clean=NdsImage.open('work/clean.nds');ctx=RegisteredRuntime(args.release,args.startup);arm=ctx.arm
    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    for image,raw,key in [(clean,source,'source_reference'),(ctx.image,current,'current_reference')]:
        ref=rows[0][key];block=IlnkContainer.parse(image.read_file(ref['file_path'])).blocks[ref['block']]
        assert block[ref['command_offset']:ref['command_offset']+len(raw)]==raw
    target=compile_choices(source,current,rows,require_formatting=False)
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
    adapter=load(PRECEDENT)['source_owned_VM_adapter']
    env={**original.__dict__,'machine':machine};exec(compile(adapter,__file__+'::original-provider','exec'),env)
    versions=[]
    for name,raw in [('clean-Japanese',source),('current-padded-English',current),('reviewed-English',target)]:
        expected=[v.decode('cp932') for v in labels(raw)];cases=[]
        for alignment in [0,2]:
            result=env['choice_vm'](arm,raw,alignment)
            assert result['labels']==expected
            assert [(c['modal_selection'],c['VM_state']) for c in result['VM_cases']]==[(0,2),(1,2),(-1,0)]
            assert [c['VM_selection_word'] for c in result['VM_cases'][:2]]==[0,1]
            assert all(c['next_command_delta']==len(raw) and c['original_dispatch_ABI_and_guards_pass'] for c in result['VM_cases'])
            cases.append(dict(alignment=alignment,native_VM=result))
        assert cases[0]['native_VM']==cases[1]['native_VM']
        versions.append(dict(version=name,object_hex=raw.hex(),bytes=len(raw),cases=cases))
    paint_adapter=checked_text(inspect.getsource(backing.paint),{
        "'expected[(y+yy)*backing_width+x+index*6+xx]'":"'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
        '    assert 0<width<=228':"    assert sha(arm)==CURRENT_ARM9\n    assert 0<width<=228",
    })
    proxy=SimpleNamespace(**{**original.__dict__,'machine':machine})
    env={**backing.__dict__,'original':proxy,'CURRENT_ARM9':sha(arm)}
    exec(compile(paint_adapter,__file__+'::unchanged-native-caption-backing','exec'),env)
    args.out.mkdir(parents=True);planes=[];pictures=[]
    for version in versions[1:]:
        vm=version['cases'][0]['native_VM'];width=vm['minimum_width_units']*6
        for index,label in enumerate(vm['labels']):
            for style in [1,15]:
                pixels,proof=env['paint'](arm,label.encode('ascii'),style,width,(0,index*12))
                assert proof['independent_complete_native_pixels_match'] and proof['storage_padding_all_blank'] and proof['extra_flush_stays_within_physical_backing']
                if version['version']=='reviewed-English':assert proof['visible_cell_center_twice']==width
                path=args.out/f"{version['version']}_O{index}_S{style}.bin";path.write_bytes(pixels)
                planes.append(dict(version=version['version'],option=index,path=str(path),sha256=sha(pixels),**proof))
                if style==1:
                    pic=Image.new('RGB',(width,12));pic.putdata([(0,8,0) if v else (239,232,201) for v in pixels])
                    pictures.append((version['version']+' '+repr(label),pic))
    sheet=Image.new('RGB',(900,240),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,pic) in enumerate(pictures):
        y=i*60;draw.text((4,y+2),label,fill='white');sheet.paste(pic.resize((pic.width*3,36),Image.Resampling.NEAREST),(4,y+19))
    sheetpath=args.out/'native_caption_review.png';sheet.save(sheetpath)
    negatives=[]
    for kind in ['reordered','changed-source','changed-current','unreviewed','padded-prose','speech-control','formatting-pending']:
        case=deepcopy(rows);full=False
        if kind=='reordered':case.reverse()
        elif kind=='changed-source':case[0]['source_hex']='00'
        elif kind=='changed-current':case[1]['current_hex']='00'
        elif kind=='unreviewed':case[1]['review']['naturalness']=False
        elif kind=='padded-prose':case[0]['english']+=' '
        elif kind=='speech-control':case[1]['english']='{SPEAKER:01}No.'
        else:full=True
        try:compile_choices(source,current,case,require_formatting=full)
        except ValueError:negatives.append(kind)
        else:raise AssertionError(kind)
    save(args.out/'menu_provider_and_planes.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        runtime=ctx.receipt(),versions=versions,records=planes,native_provider_alignments=6,bridged_modal_returns=18,
        complete_English_caption_style_planes=len(planes),compiler_negatives_rejected=negatives,
        native_choice_object_hex=target.hex(),source_owned_VM_adapter=adapter,source_owned_painter_adapter=paint_adapter,
        exact_instruction_addresses=len(executed),complete_caption_glyphs_centering_bounds_guards_andconsumption_pass=True,
        compiler_owned_zero_alignment_only_no_speech_encoder=True,source_index_andcount_preserved=True,
        direct_view_pending=True,review_sheet=dict(path=str(sheetpath),sha256=sha(sheetpath.read_bytes())),
        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,
        actual_menu_highlight_controller_response_paths_andstored_integration_pending=True,
        new_ROM=False,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRECEDENT,args.manuscript,Path(backing.__file__),Path(original.__file__),Path('dk4tool/dialogue/reviewed_two_choice_object_v1.py'),Path(__file__)]}))
    (args.out/'compiled_choice_object.bin').write_bytes(target)
    print(dict(provider_alignments=6,bridged_returns=18,complete_planes=len(planes),compiled_bytes=len(target),
        reviewed_rectangle=versions[-1]['cases'][0]['native_VM']['native_menu_rectangle'],negatives=len(negatives),actual_pending=True))

if __name__=='__main__':main()
