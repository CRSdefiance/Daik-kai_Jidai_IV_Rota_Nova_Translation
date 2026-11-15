"""Sparse two-block research reconstruction with complete original/current inverses.

No ROM is written. Only reviewed speech bodies, the logical-size header and
the four mapped native relative operands may differ in these research blocks.
"""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B54_B60_relocation_v8809')
CURRENT=Path('work/analysis/Hodram_B54_B60_current_v8799/current_effective.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
VIEW=Path('work/analysis/Hodram_B54_B60_compiled_v8808/compiled_body_bindings.json')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();packet,doc,view,control,inp=map(read,[CURRENT,DOC,VIEW,CONTROL,INPUT])
    assert view['manuscript_sha256']==sha(DOC.read_bytes()) and view['compiled_bytes_and82_preambles_bound_to_viewed85_pages']
    assert len(doc['records'])==82 and not doc['typed_choice_records'] and all(not r['review']['formatting'] for r in doc['records'])
    assert inp['current_ROM_sha256']==doc['current_ROM_sha256']==packet['current_ROM_sha256']==control['candidate_sha256']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=image.read_file('/data/SC1.DK4');arm=image.read_file('/__arm9__.bin');assert sha(archive)==packet['current_archive_sha256']==doc['current_archive_sha256']
    container=IlnkContainer.parse(archive);assert len(container.blocks)==325
    inventory,walker,fn=scoped_inventory();ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');groups=[];blocks=list(container.blocks)
    for g in packet['groups']:
        number=g['block'];source_control=next(r for r in control['groups'] if r['block']==number)
        old=container.blocks[number];clean=bytes.fromhex(g['clean_block_hex']);oldend=g['current_logical_end'];cleanend=8+struct.unpack_from('<H',clean,4)[0]
        assert old==bytes.fromhex(g['current_block_hex']) and sha(old)==g['current_block_sha256'] and sha(clean)==g['clean_block_sha256']
        assert oldend==cleanend and len(old)==len(clean) and old[:8]==clean[:8] and old[oldend:]==clean[cleanend:] and not any(old[oldend:])
        before,speeches=inventory(arm,old);assert before==g['all_current_commands'] and len(before)==len(g['all_current_commands']) and len(speeches)==len(g['records'])
        assert inventory(arm,clean)[0]==g['all_source_commands']==source_control['all_original_source_commands']
        patches=[];texts=[]
        for row in [r for r in doc['records'] if r['block']==number]:
            at,ja=row['current_reference']['offset'],row['source_reference']['offset'];previous,source=bytes.fromhex(row['current_hex']),bytes.fromhex(row['source_hex']);value=bytes.fromhex(row['compiled_hex'])
            assert old[at:at+len(previous)+1]==previous+b'\0' and clean[ja:ja+len(source)+1]==source+b'\0'
            assert old[at-5:at+1].hex()==clean[ja-5:ja+1].hex()==row['source_complete_preamble_hex']
            assert at==ja and len(previous)==len(source) and value[0]==previous[0]==source[0]==row['source_selector'] in [1,20,23,24,36,84,113,114,119,141,254]
            assert value[1:] and b'\0' not in value[1:] and old[:at].count(b'\0')==row['current_record_index'] and clean[:ja].count(b'\0')==row['source_record_index']
            assert all(source[1:].count(m)==value[1:].count(m) for m in [b'FI',b'FA',b'FO'])
            pad=len(value)%2!=len(previous)%2;stored=value+(b' ' if pad else b'');assert len(stored)%2==len(previous)%2
            patches.append(dict(id=row['id'],start=at,end=at+len(previous),old=previous,source=source,value=stored))
            texts.append(dict(id=row['id'],file_path=row['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'],old_offset=at,old_length=len(previous),old_hex=previous.hex(),compiled_hex=value.hex(),new_length=len(stored),target_hex=stored.hex(),parity_space_added=pad))
        patches.sort(key=lambda p:p['start']);assert len(patches)==len(speeches) and all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
        def mapped(at):
            delta=0
            for patch in patches:
                if at<patch['start']:break
                assert not patch['start']<at<patch['end'],'Interior reference in replaced speech'
                if at==patch['start']:return at+delta
                delta+=len(patch['value'])-len(patch['old'])
            return at+delta
        chunks=[];last=0
        for patch in patches:chunks.extend([old[last:patch['start']],patch['value']]);last=patch['end']
        chunks.append(old[last:oldend]);logical=bytearray(b''.join(chunks));assert len(logical)==mapped(oldend)<0x2400
        fixups=[];boundaries={c['offset'] for c in before}|{oldend}
        for edge in source_control['operands_requiring_adjustment_when_resizing']:
            assert edge['block']==number and edge['offset'] in boundaries and edge['matched_skip_target'] in boundaries
            assert old[edge['offset']:edge['offset']+4].hex()==edge['source_operand_hex'] and old[edge['offset']:edge['offset']+4]==clean[edge['offset']:edge['offset']+4]
            start,finish=mapped(edge['offset']),mapped(edge['matched_skip_target']);span=finish-start-4
            assert 0<=span<=0xffff and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word']
            struct.pack_into('<H',logical,start+2,span);fixups.append(dict(**edge,new_offset=start,new_unmatched_next=start+4,new_matched_skip_target=finish,target_span=span))
        assert len(fixups)==len(source_control['operands_requiring_adjustment_when_resizing'])
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
        after,finalspeeches=inventory(arm,target);assert len(after)==len(before) and len(finalspeeches)==len(speeches)
        maps=[]
        for previous,new in zip(before,after,strict=True):
            a,z=previous['offset'],new['offset'];word=previous['word'];assert z==mapped(a) and new['word']==word
            assert new['native_extent']==mapped(a+previous['native_extent'])-z and new['ancestor_0100_offsets']==[mapped(x) for x in previous['ancestor_0100_offsets']]
            br,nr=bytes.fromhex(previous['whole_command_hex']),bytes.fromhex(new['whole_command_hex'])
            if word==0x4000:assert br[:6]==nr[:6]
            elif word in [0x100,0x200,0x300,0x400]:assert br[:2]==nr[:2]
            else:assert br==nr
            maps.append(dict(word=word,old_offset=a,new_offset=z,old_extent=previous['native_extent'],new_extent=new['native_extent'],source_0100_ancestors=previous['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
        assert after[-1]['word']==0 and after[-1]['native_extent']==4 and after[-1]['offset']+4==len(logical)
        for row in texts:
            at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
            assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        for source_version,original in [(False,old),(True,clean)]:
            inverse=bytearray(target[:len(logical)]);inverse[:8]=original[:8]
            for fix in fixups:struct.pack_into('<H',inverse,fix['new_offset']+2,fix['source_span'])
            for patch in reversed(patches):
                at=mapped(patch['start']);inverse[at:at+len(patch['value'])]=patch['source'] if source_version else patch['old']
            assert bytes(inverse)+original[oldend:]==original,'Complete clean/current block inverse including separate source tail'
        byoffset={c['offset']:c for c in after};finalboundaries=set(byoffset)|{len(logical)};skipcases=[]
        for fix in fixups:
            result=ctx.execute(native_skip,target,byoffset[fix['new_offset']]);ctx.machines.pop()
            assert all(c['next_offset'] in finalboundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases']);skipcases.append(result)
        bp=ROOT/f'SC1_B{number}_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks[number]=target
        groups.append(dict(block=number,file_path='/data/SC1.DK4',source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(bp),target_block_sha256=sha(target),source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=oldend,source_tail_bytes=len(old)-oldend,target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),text_records=texts,choice_commands=[],relative_fixups=fixups,relocated_skip_cases=skipcases,command_map=maps,all_current_commands=before,all_target_commands=after,source_current_andclean_block_inverse_exact=True))
    assert not ctx.machines
    newarchive=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(newarchive);assert len(parsed.blocks)==325
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[g['block'] for g in packet['groups']]
    inverse=list(parsed.blocks)
    for i in [g['block'] for g in packet['groups']]:inverse[i]=container.blocks[i]
    assert IlnkContainer(inverse).to_bytes()==archive
    planned=deepcopy(image);planned.replace_file('/data/SC1.DK4',newarchive)
    assert [p for _,p,data in image.iter_files() if planned.read_file(p)!=data]==['/data/SC1.DK4'] and all(planned.read_file(p)==data for p,data in image.iter_components())
    restored=deepcopy(planned);restored.replace_file('/data/SC1.DK4',archive);assert bytes(restored.rom.save())==bytes(image.rom.save())
    ap=ROOT/'SC1_B54_B60_RESEARCH_ONLY.DK4';ap.write_bytes(newarchive)
    save(ROOT/'reconstruction.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_packet=str(CURRENT),source_packet_sha256=sha(CURRENT.read_bytes()),file_path='/data/SC1.DK4',source_archive_sha256=sha(archive),target_archive=str(ap),target_archive_sha256=sha(newarchive),groups=groups,
        other318_blocks_byte_exact=True,complete_predecessor_archive_inverse_exact=True,complete_clean_source_block_inverses_exact=True,whole_inmemory_NDS_inverse_andall_other_files_components_exact=True,
        source_relative_sites=24,relocated_native_skip_cases=sum(len(r['cases']) for g in groups for r in g['relocated_skip_cases']),
        complete152commands82sixbytepreambles24relatives6queries33nonprose_controls7normalends_preserved=True,
        parity_space_records=[r['id'] for g in groups for r in g['text_records'] if r['parity_space_added']],
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        research_archives_only_no_ROM_registration_orcredit=True,stored_fonts_queries_ends_actual_names_policy_atomic_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,DOC,VIEW,CONTROL,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Seven research blocks reconstructed:',[(g['block'],g['source_bytes'],g['target_bytes']) for g in groups],flush=True)
    print('152commands/82preambles/24relatives120cases/6queries/33nonprosecontrols/7fullends preserved;318otherblocks/currentarchive/cleanblocks/wholeNDS inverses pass. No ROM orcredit.',flush=True)
