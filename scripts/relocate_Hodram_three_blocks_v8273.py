"""Research archive reconstruction for all28 speeches/60commands/eight relative sites; no ROM or credit."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_target_route_context_v8270 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_three_block_relocation_v8273')
CURRENT=Path('work/analysis/Hodram_current_review_binding_v8272/28_exact_current_refs_registered_name_dependency_andnative_reuse.json')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v3.json')
PLAN=Path('work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json')
VIEW=Path('work/analysis/Hodram_B137_B45_B46_native_review_v8247/28_native_pages_directly_viewed_two_exact_boundary_reviews.json')
CONTROL=Path('work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json')
INPUT=Path('work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();current,doc,plan,view,control,inp=map(read,[CURRENT,DOC,PLAN,VIEW,CONTROL,INPUT])
    assert len(doc['records'])==28 and doc['current_ROM_sha256']==inp['current_ROM_sha256']==current['current_ROM_sha256']
    assert view['all28_complete_bodies_visually_read'] and len(view['original_warnings'])==2 and len(view['original_infos'])==5
    assert control['source_relative_sites']==8 and control['source_raw_predicate_query_count']==2
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file(doc['file_path']);container=IlnkContainer.parse(archive)
    assert len(container.blocks)==325 and sha(archive)==doc['current_archive_sha256']==current['current_archive_sha256']
    inventory,walker,inventory_source=scoped_inventory();ROOT.mkdir(parents=True)
    ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    env=dict(end_case.__globals__);exec(compile(control['source_owned_seeded_end_adapter'],__file__+'::original-seeded-value-carry','exec'),env)
    blocks=list(container.blocks);groups=[];relativecases=0;endcases=0
    for spec in current['groups']:
        number=spec['block'];old=container.blocks[number];clean=bytes.fromhex(spec['clean_block_hex']);oldend=spec['current_logical_end']
        assert number in [137,45,46] and old==bytes.fromhex(spec['current_block_hex']) and old[oldend:]==bytes(len(old)-oldend)
        commands,speeches=inventory(arm,old);assert commands==spec['all_current_commands'] and len(speeches)==len(spec['records'])
        patches=[];texts=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['offset'];raw=bytes.fromhex(row['current_hex']);compiled=bytes.fromhex(row['compiled_hex'])
            p=next(r for r in plan['records'] if r['id']==row['id']);assert p['encoded_hex']==row['compiled_hex'] and ' '.join(p['lines'])==row['english']
            assert old[at:at+len(raw)+1]==raw+b'\0' and old[at-5:at+1].hex()==row['source_complete_preamble_hex']
            assert compiled[0]==raw[0]==row['source_selector'] and compiled[0] in [1,2,9,16,18,113] and b'\0' not in compiled[1:]
            pad=len(compiled)%2!=len(raw)%2;stored=compiled+(b' ' if pad else b'')
            assert len(stored)%2==len(raw)%2 and not any(t in stored[1:] for t in [b'FI',b'FA',b'FO',b'%'])
            patches.append(dict(start=at,end=at+len(raw),old=raw,source=bytes.fromhex(row['source_hex']),value=stored,id=row['id']))
            texts.append(dict(id=row['id'],file_path=doc['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],
                source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'],old_offset=at,old_length=len(raw),old_hex=raw.hex(),
                compiled_hex=compiled.hex(),target_hex=stored.hex(),new_length=len(stored),parity_space_added=pad))
        assert len(texts)==len(speeches)
        patches.sort(key=lambda p:p['start']);assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
        def mapped(at):
            delta=0
            for patch in patches:
                if at<patch['start']:break
                assert not patch['start']<at<patch['end'],'Interior reference in a replaced speech'
                if at==patch['start']:return at+delta
                delta+=len(patch['value'])-len(patch['old'])
            return at+delta
        chunks=[];cursor=0
        for patch in patches:chunks.extend([old[cursor:patch['start']],patch['value']]);cursor=patch['end']
        chunks.append(old[cursor:oldend]);logical=bytearray(b''.join(chunks));assert len(logical)==mapped(oldend)<0x2400
        sourcecommands=spec['all_source_commands'];oldboundaries={c['offset'] for c in commands}|{oldend};fixups=[]
        for source,command in zip(sourcecommands,commands,strict=True):
            assert source['word']==command['word']
            if command['word'] not in [0x100,0x200,0x300,0x400]:continue
            at=command['offset'];span=int.from_bytes(old[at+2:at+4],'little');destination=at+4+span
            assert at+4 in oldboundaries and destination in oldboundaries
            newat,newend=mapped(at),mapped(destination);newspan=newend-newat-4;assert 0<=newspan<=0xFFFF and newspan%2==0
            struct.pack_into('<H',logical,newat+2,newspan)
            fixups.append(dict(word=command['word'],offset=at,source_span=span,unmatched_next=at+4,matched_skip_target=destination,
                new_offset=newat,new_unmatched_next=newat+4,new_matched_skip_target=newend,target_span=newspan,
                clean_offset=source['offset'],clean_span=int.from_bytes(clean[source['offset']+2:source['offset']+4],'little')))
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
        final,finalspeeches=inventory(arm,target);assert len(final)==len(commands) and len(finalspeeches)==len(texts)
        bynew={c['offset']:c for c in final};boundaries=set(bynew)|{len(logical)};maps=[]
        for source,before in zip(sourcecommands,commands,strict=True):
            after=bynew[mapped(before['offset'])];word=before['word'];assert after['word']==word
            assert after['native_extent']==mapped(before['offset']+before['native_extent'])-after['offset']
            assert after['ancestor_0100_offsets']==[mapped(a) for a in before['ancestor_0100_offsets']]
            if word==0x4000:assert bytes.fromhex(before['whole_command_hex'])[:6]==bytes.fromhex(after['whole_command_hex'])[:6]
            elif word not in [0x100,0x200,0x300,0x400]:assert before['whole_command_hex']==after['whole_command_hex']==source['whole_command_hex']
            maps.append(dict(word=word,clean_offset=source['offset'],old_offset=before['offset'],new_offset=after['offset'],clean_extent=source['native_extent'],old_extent=before['native_extent'],new_extent=after['native_extent'],
                clean_0100_ancestors=source['ancestor_0100_offsets'],source_0100_ancestors=before['ancestor_0100_offsets'],target_0100_ancestors=after['ancestor_0100_offsets']))
        skips=[]
        for fix in fixups:
            probe=ctx.execute(native_skip,target,bynew[fix['new_offset']]);ctx.machines.pop()
            assert len(probe['cases'])==5 and all(c['next_offset'] in boundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in probe['cases'])
            skips.append(probe);relativecases+=len(probe['cases'])
        for row in texts:
            at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
            assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        def inverse(clean_version):
            restored=bytearray(target[:len(logical)]);restored[:8]=(clean if clean_version else old)[:8]
            for fix in fixups:struct.pack_into('<H',restored,fix['new_offset']+2,fix['clean_span'] if clean_version else fix['source_span'])
            for patch in reversed(patches):
                start=mapped(patch['start']);restored[start:start+len(patch['value'])]=patch['source'] if clean_version else patch['old']
            original=clean if clean_version else old;end=8+int.from_bytes(original[4:6],'little')
            return bytes(restored)+original[end:]
        assert inverse(False)==old and inverse(True)==clean
        terminal=final[-1];assert terminal['word']==0 and terminal['native_extent']==4 and terminal['offset']+4==len(logical)
        ends=[env['end_case'](arm,target,terminal['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
        assert len(ends)==25 and all(e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] and e['native_extent']==4 for e in ends);endcases+=len(ends)
        path=ROOT/f'SC1_block{number}_RESEARCH_ONLY.bin';path.write_bytes(target);blocks[number]=target
        groups.append(dict(block=number,file_path=doc['file_path'],source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(path),target_block_sha256=sha(target),
            source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=oldend,source_tail_bytes=len(old)-oldend,
            target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),text_records=texts,relative_fixups=fixups,relocated_skip_cases=skips,
            command_map=maps,all_source_commands=sourcecommands,all_current_commands=commands,all_target_commands=final,target_seeded_normal_ends=ends,
            source_current_andclean_block_inverse_exact=True,all_source_control_bytes_andsix_byte_preambles_preserved=True,external_references_complete=False))
        print('RELOCATION',number,len(old),'->',len(target),'logical',len(logical),'tail',len(target)-len(logical),'relative',len(fixups),'parity',sum(r['parity_space_added'] for r in texts),flush=True)
    assert not ctx.machines and relativecases==40 and endcases==75 and sum(len(g['text_records']) for g in groups)==28 and sum(len(g['all_target_commands']) for g in groups)==60
    targetarchive=IlnkContainer(blocks).to_bytes();parsed=IlnkContainer.parse(targetarchive)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[45,46,137]
    restored=list(parsed.blocks)
    for g in groups:restored[g['block']]=container.blocks[g['block']]
    assert IlnkContainer(restored).to_bytes()==archive
    output=ROOT/'SC1_B137_B45_B46_RESEARCH_ONLY.DK4';output.write_bytes(targetarchive)
    save(ROOT/'three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],file_path=doc['file_path'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_archive_sha256=sha(archive),target_archive=str(output),target_archive_sha256=sha(targetarchive),groups=groups,
        only_blocks45_46_137_changed_all322_others_exact=True,all_full_predecessor_archive_andthree_clean_source_blocks_reconstructed_exactly=True,
        source_relative_sites=8,fresh_relocated_native_skip_cases=40,fresh_target_seeded_normal_end_cases=75,
        all60_commands28_complete_preambles_two_raw8000_operands_zero_FE_FI_FA_FO_full_terminals_tails_preserved=True,
        structural_previous_results_not_forced_gameplay_states_orall_attainable_paths=True,research_archive_only_no_ROM_orregistered_credit=True,external_references_complete=False,
        stored_body_fonts_actual4800_layout0_hide4700_nameheaders_controls_loader_census_policy_atomic_registered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,DOC,PLAN,VIEW,CONTROL,INPUT,Path(__file__)]}))
    print('Hodram28 research archive:60commands/eightrelative sites40fresh cases/75fresh ends;threeclean andfullparentarchive inverses pass;noROM orcredit.')
