"""Reconstruct only five SC2 surname speeches; preserve every other command and body."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_sparse_relocation_v8208')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
MANUSCRIPT=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
PLAN=Path('work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json')
VIEW=Path('work/analysis/Gerhard_native_review_v8207/five_native_pages_directly_viewed_one_info_zero_warnings.json')
INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')

if __name__=='__main__':
    assert not ROOT.exists();current,doc,plan,view=map(read,[CURRENT,MANUSCRIPT,PLAN,VIEW])
    assert plan['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and view['plan_sha256']==sha(PLAN.read_bytes())
    assert view['all_five_complete_bodies_visually_read'] and not plan['failures']
    assert not any(i['severity'] in ['error','warning'] for p in plan['records'] for i in p['base_QA']['issues'])
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=image.read_file(doc['file_path']);assert sha(archive)==current['current_archive_sha256']
    container=IlnkContainer.parse(archive);arm=image.read_file('/__arm9__.bin');inventory,walker,fn=scoped_inventory()
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    blocks=list(container.blocks);groups=[];total_source_cases=total_current_cases=total_target_cases=0
    for spec in current['groups']:
        number=spec['block'];old=container.blocks[number];clean=bytes.fromhex(spec['clean_block_hex'])
        assert old==bytes.fromhex(spec['current_block_hex']) and sha(old)==spec['current_block_sha256']
        oldend=8+struct.unpack_from('<H',old,4)[0];cleanend=8+struct.unpack_from('<H',clean,4)[0]
        assert oldend<=len(old)<oldend+4 and cleanend<=len(clean)<cleanend+4
        patches=[];texts=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['offset'];oldraw=bytes.fromhex(row['current_hex']);p=next(r for r in plan['records'] if r['id']==row['id'])
            assert old[at:at+len(oldraw)+1]==oldraw+b'\0'
            value=bytes.fromhex(p['encoded_hex']);pad=len(value)%2!=len(oldraw)%2
            if pad:value+=b' '
            assert b'\0' not in value and value[0]==oldraw[0]==row['source_selector'] and len(value)%2==len(oldraw)%2
            patches.append(dict(start=at,end=at+len(oldraw),old=oldraw,value=value,id=row['id']))
            texts.append(dict(id=row['id'],file_path=row['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],
                source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
                old_offset=at,old_length=len(oldraw),old_hex=oldraw.hex(),compiled_hex=p['encoded_hex'],new_length=len(value),target_hex=value.hex(),parity_space_added=pad))
        patches.sort(key=lambda p:p['start']);assert len(patches)==(2 if number==27 else 3)
        assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
        def mapped(at):
            delta=0
            for p in patches:
                if at<p['start']:break
                assert not p['start']<at<p['end'],'Interior reference inside replaced speech'
                if at==p['start']:return at+delta
                delta+=len(p['value'])-len(p['old'])
            return at+delta
        chunks=[];last=0
        for p in patches:chunks.extend([old[last:p['start']],p['value']]);last=p['end']
        chunks.append(old[last:oldend]);logical=bytearray(b''.join(chunks))
        assert len(logical)==mapped(oldend)<0x2400
        originals=spec['all_current_commands'];source_commands=spec['all_source_commands']
        assert len(originals)==len(source_commands)
        clean_to_current={a['offset']:b['offset'] for a,b in zip(source_commands,originals,strict=True)};clean_to_current[cleanend]=oldend
        current_boundaries={c['offset'] for c in originals}|{oldend};fixups=[];source_cases=[];current_cases=[]
        for source,command in zip(source_commands,originals,strict=True):
            assert source['word']==command['word']
            assert [clean_to_current[a] for a in source['ancestor_0100_offsets']]==command['ancestor_0100_offsets']
            at,word=command['offset'],command['word']
            if word not in [0x100,0x200,0x300,0x400]:
                if word==0x4000:assert bytes.fromhex(source['whole_command_hex'])[:6]==bytes.fromhex(command['whole_command_hex'])[:6]
                else:assert source['whole_command_hex']==command['whole_command_hex']
                continue
            source_span=struct.unpack_from('<H',clean,source['offset']+2)[0];span=struct.unpack_from('<H',old,at+2)[0]
            finish=at+4+span;assert finish in current_boundaries
            assert clean_to_current[source['offset']+4+source_span]==finish
            start,end=mapped(at),mapped(finish);target_span=end-start-4
            assert 0<=target_span<=0xFFFF and target_span%2==0 and struct.unpack_from('<H',logical,start)[0]==word
            struct.pack_into('<H',logical,start+2,target_span)
            fixups.append(dict(word=word,offset=at,source_span=span,new_offset=start,target_span=target_span,
                unmatched_next=at+4,matched_skip_target=finish,new_unmatched_next=start+4,new_matched_skip_target=end,
                clean_offset=source['offset'],clean_span=source_span))
            for label,block,cmd,out in [('clean',clean,source,source_cases),('current',old,command,current_cases)]:
                value=ctx.execute(native_skip,block,cmd);ctx.machines.pop();out.append(value)
                boundaries=set(clean_to_current) if label=='clean' else current_boundaries
                assert all(r['next_offset'] in boundaries for r in value['cases'])
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
        commands,speeches=inventory(arm,target);assert len(commands)==len(originals)
        assert len(speeches)==sum(c['word']==0x4000 for c in originals)
        byoffset={c['offset']:c for c in commands};boundaries=set(byoffset)|{len(logical)};maps=[];target_cases=[]
        for previous in originals:
            new=byoffset[mapped(previous['offset'])];word=previous['word']
            assert new['word']==word and new['native_extent']==mapped(previous['offset']+previous['native_extent'])-new['offset']
            assert new['ancestor_0100_offsets']==[mapped(a) for a in previous['ancestor_0100_offsets']]
            if word==0x4000:
                before,after=bytes.fromhex(previous['whole_command_hex']),bytes.fromhex(new['whole_command_hex'])
                assert before[:6]==after[:6]
                if not any(previous['offset']==p['start']-5 for p in patches):assert before==after
            elif word in [0x100,0x200,0x300,0x400]:assert previous['whole_command_hex'][:4]==new['whole_command_hex'][:4]
            else:assert previous['whole_command_hex']==new['whole_command_hex']
            maps.append(dict(word=word,old_offset=previous['offset'],new_offset=new['offset'],old_extent=previous['native_extent'],new_extent=new['native_extent'],
                source_0100_ancestors=previous['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
        for fix in fixups:
            result=ctx.execute(native_skip,target,byoffset[fix['new_offset']]);ctx.machines.pop()
            assert all(r['next_offset'] in boundaries for r in result['cases'])
            assert all(r['next_offset']==(fix['new_matched_skip_target'] if r['taken'] else fix['new_unmatched_next']) for r in result['cases'])
            target_cases.append(result)
        for row in texts:
            at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
            assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0'
            assert target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        restored=bytearray(target[:len(logical)]);restored[:8]=old[:8]
        for fix in fixups:struct.pack_into('<H',restored,fix['new_offset']+2,fix['source_span'])
        for patch in reversed(patches):
            at=mapped(patch['start']);restored[at:at+len(patch['value'])]=patch['old']
        assert bytes(restored)+old[oldend:]==old
        terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4 and terminal['offset']+4==len(logical)
        bp=ROOT/f'SC2_block{number}_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks[number]=target
        total_source_cases+=5*len(source_cases);total_current_cases+=5*len(current_cases);total_target_cases+=5*len(target_cases)
        groups.append(dict(block=number,file_path=doc['file_path'],source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(bp),target_block_sha256=sha(target),
            source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=oldend,source_tail_bytes=len(old)-oldend,
            target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),text_records=texts,relative_fixups=fixups,
            clean_native_skip_cases=source_cases,current_native_skip_cases=current_cases,relocated_native_skip_cases=target_cases,
            command_map=maps,all_target_commands=commands,total_speeches=len(speeches),unchanged_speeches=len(speeches)-len(texts),
            source_andtarget_complete_terminal_extent4=True,source_four_byte_header_andmetadata_preserved_except_length=True,
            full_predecessor_block_inverse_exact=True,complete_clean_command_order_preambles_relative_targets_andopaque_controls_exact=True,
            full_clean_block_inverse_not_claimed_other_previous_translations_preserved=True,external_references_complete=False))
        print('RELOCATION',number,len(old),'->',len(target),'logical',len(logical),'relative',len(fixups),'parity tails',sum(r['parity_space_added'] for r in texts),flush=True)
    assert not ctx.machines and sum(len(g['text_records']) for g in groups)==5
    target_archive=IlnkContainer(blocks).to_bytes();ap=ROOT/'SC2_Gerhard_RESEARCH_ONLY.DK4';ap.write_bytes(target_archive)
    parsed=IlnkContainer.parse(target_archive);assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[27,74]
    inverse_blocks=list(parsed.blocks)
    for g in groups:inverse_blocks[g['block']]=container.blocks[g['block']]
    assert IlnkContainer(inverse_blocks).to_bytes()==archive
    save(ROOT/'two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],file_path=doc['file_path'],source_archive_sha256=sha(archive),
        target_archive=str(ap),target_archive_sha256=sha(target_archive),groups=groups,exactly_blocks27_and74_changed=True,
        other_archive_blocks_exact=len(parsed.blocks)-2,all_full_predecessor_archive_bytes_reconstructed_exactly=True,
        source_relative_sites=sum(len(g['relative_fixups']) for g in groups),clean_native_skip_cases=total_source_cases,
        current_native_skip_cases=total_current_cases,target_native_skip_cases=total_target_cases,
        all_mapped_branch_targets_andnested_ancestor_scopes_preserved=True,all125_other_speeches_unchanged=sum(g['unchanged_speeches'] for g in groups)==125,
        all130_six_byte_preambles_andcomplete_terminals_preserved=True,
        research_archives_only_no_ROM_registration_orcredit=True,external_references_complete=False,
        full_clean_text_inverse_not_claimed_for_sparse_five_record_change=True,
        stored_fonts_end_valuecarry_fullreference_callers_loaders_actual_policy_production_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        ordinary_captain2_opening_context_no_unlock_orstate_fixture=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,MANUSCRIPT,PLAN,VIEW,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Sparse reconstruction pass;native clean/current/target skip cases',total_source_cases,total_current_cases,total_target_cases,'no ROM or new credit.')
