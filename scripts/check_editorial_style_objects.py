"""Compile source-owned 4100 objects and check all eight target slot pointers."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles,unpack
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime import RegisteredRuntime

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ['manuscript','plan','current-objects','release','startup','out']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    doc,plan,current=map(load,[args.manuscript,args.plan,args.current_objects]);assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes())
    ctx=RegisteredRuntime(args.release,args.startup);assert current['runtime']==ctx.receipt() and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    clean=NdsImage.open('work/clean.nds');clean_blocks=IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks
    current_blocks=IlnkContainer.parse(ctx.image.read_file('/data/SC1.DK4')).blocks
    plans={r['id']:r for r in plan['records']};objects=[];cases=0;negatives=[]
    args.out.mkdir(parents=True)
    for item in current['style_objects']:
        block=item['block'];offset=item['source_command_offset'];source=bytes.fromhex(item['source_object_hex']);prior=bytes.fromhex(item['current_object_hex'])
        assert clean_blocks[block][offset:offset+len(source)]==source
        at=item['current_command_offset'];assert current_blocks[block][at:at+len(prior)]==prior
        rows=[r for r in doc['records'] if r.get('native_object_kind')=='4100-style-alternative' and r['block']==block and r['source_command_offset']==offset]
        rows.sort(key=lambda r:r['source_reference']['offset'])
        target=compile_styles(source,prior,rows,plans,require_formatting=False)
        old_offsets,old_texts=unpack(source);new_offsets,new_texts=unpack(target)
        cpu,get,provider=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
        stream,owner=0x02660000,0x02662000
        cpu.mem_write(stream-16,b'\xa5'*(len(target)+32));cpu.mem_write(stream,target)
        cpu.mem_write(owner-16,b'\xa5'*64);cpu.mem_write(owner,b'\0'*4+stream.to_bytes(4,'little')+b'\0'*8)
        owner_before=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(0x02000000,0x400000));slots=[]
        for index in range(8):
            pointer=get(0x2A154,owner,index);relative=20+new_offsets[index];expected=new_texts[new_offsets[index]]
            assert pointer==stream+relative and bytes(cpu.mem_read(pointer,len(expected)+1))==expected+b'\0'
            assert bytes(cpu.mem_read(0x02000000,0x400000))==before and bytes(cpu.mem_read(owner-16,64))==owner_before
            assert bytes(cpu.mem_read(stream,len(target)))==target
            assert bytes(cpu.mem_read(stream-16,16))==bytes(cpu.mem_read(stream+len(target),16))==b'\xa5'*16
            row=next(r for r in rows if index in r['source_style_indices']);assert expected==bytes.fromhex(plans[row['id']]['encoded_hex'])[1:]
            slots.append(dict(style=index,record_id=row['id'],target_body_offset=relative,target_hex=expected.hex(),
                complete_original_getter_pointer_body_terminator_stream_owner_andall_unowned4MiB_exact=True));cases+=1
        assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes;ctx.calls.clear()
        failed=[]
        for kind in ['reordered','omitted-body','changed-source','changed-current','changed-header','changed-alias','unreviewed','changed-plan','formatting-pending']:
            sample=deepcopy(rows);mapped=deepcopy(plans);full=False
            if kind=='reordered':sample.reverse()
            elif kind=='omitted-body':sample.pop()
            elif kind=='changed-source':sample[0]['source_hex']='00'
            elif kind=='changed-current':sample[0]['current_hex']='00'
            elif kind=='changed-header':sample[0]['source_header_hex']='00'
            elif kind=='changed-alias':sample[0]['source_style_indices']=[]
            elif kind=='unreviewed':sample[0]['review']['naturalness']=False
            elif kind=='changed-plan':mapped[sample[0]['id']]['logical_English']='Not the reviewed prose.'
            else:full=True
            try:compile_styles(source,prior,sample,mapped,require_formatting=full)
            except ValueError:failed.append(kind)
            else:raise AssertionError(kind)
        negatives.append(dict(block=block,command_offset=offset,rejected=failed))
        path=args.out/f'B{block}_C{offset}_compiled_style_object.bin';path.write_bytes(target)
        objects.append(dict(block=block,source_command_offset=offset,current_command_offset=at,source_object_hex=source.hex(),current_object_hex=prior.hex(),
            target_object_hex=target.hex(),target_path=str(path),target_sha256=sha(target),physical_record_IDs=[r['id'] for r in rows],
            source_alias_offsets=old_offsets,target_alias_offsets=new_offsets,header_flag_selector_exact=True,virtual_prefix_not_stored=True,native_slots=slots,
            current_executed_instruction_addresses=len(provider.executed_current)))
    assert len(objects)==8 and cases==64 and sum(len(o['physical_record_IDs']) for o in objects)==48
    save(args.out/'compiled_style_objects.json',dict(manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),
        runtime=ctx.receipt(),objects=objects,native_target_slot_cases=cases,physical_alternatives=48,source_alias_equivalence_exact=True,
        compiler_negatives=negatives,source_current_getter_cases_reused=str(args.current_objects),
        new_font_page_ornew_actual_personality_assignment_claim=False,stored_relocation_actual_scene_andregistered_release_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.manuscript,args.plan,args.current_objects,Path(__file__),Path('dk4tool/dialogue/reviewed_actor_style_object_v1.py')]}))
    print('PASS8 compiled4100 objects/48 physical alternatives/64 original target slot cases/72 semantic rejection checks; virtual prefixes not stored.')

if __name__=='__main__':main()
