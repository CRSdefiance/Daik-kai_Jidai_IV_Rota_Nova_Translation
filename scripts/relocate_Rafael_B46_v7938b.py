"""Research-only Rafael B46 reconstruction:24 speeches,two-choice object,four exact nested fixups andboth full inverses."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_relocation_v7938')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
SOURCE=Path('work/analysis/Rafael_next_clean_v7918/complete_clean_SC0_B46_EV0_andcoverage_before_current_English.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v2.json')
PLAN=Path('work/analysis/Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json')
NATIVE=Path('work/analysis/Rafael_B46_native_review_v7935/24_pages2_choices_full_native_review_individual_wrap_reasons.json')
BRANCH=Path('work/analysis/Rafael_B46_archive_tools_v7938/four_exact_source_current_relative_operands_bound_to20_native_cases.json')
INPUT=Path('work/analysis/current_V7911_Rafael_native_v7914/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();current,source,doc,plan,native,branches=map(read,[CURRENT,SOURCE,MANUSCRIPT,PLAN,NATIVE,BRANCH])
    assert plan['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes()) and native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes()) and all(not any(i['severity'] in ['warning','error'] for i in r['base_QA']['issues']) for r in plan['records'])
    im=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=im.read_file(doc['file_path']);assert sha(archive)==current['current_archive_sha256']
    container=IlnkContainer.parse(archive);arm=im.read_file('/__arm9__.bin');inventory,walker,fn=scoped_inventory()
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    blocks=list(container.blocks);groups=[]
    for spec,clean_spec in zip(current['groups'],source['groups'],strict=True):
        number=spec['block'];assert number==clean_spec['block']
        old=container.blocks[number];clean=bytes.fromhex(clean_spec['clean_block_hex'])
        oldend=spec['current_logical_end'];assert sha(old)==spec['current_block_sha256']
        patches=[];texts=[]
        for row in doc['records']:
            if row['block']!=number:continue
            at=row['current_reference']['offset'];oldraw=bytes.fromhex(row['current_hex']);p=next(r for r in plan['records'] if r['id']==row['id'])
            assert old[at:at+len(oldraw)+1]==oldraw+b'\0'
            value=bytes.fromhex(p['encoded_hex']);pad=len(value)%2!=len(oldraw)%2
            if pad:value+=b' '
            assert b'\0' not in value[1:] and value[0]==oldraw[0]==row['source_selector'] and len(value)%2==len(oldraw)%2
            patches.append(dict(start=at,end=at+len(oldraw),old=oldraw,value=value,source=bytes.fromhex(row['source_hex']),id=row['id']))
            texts.append(dict(id=row['id'],file_path=row['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],
                source_selector=row['source_selector'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
                old_offset=at,old_length=len(oldraw),old_hex=oldraw.hex(),compiled_hex=p['encoded_hex'],new_length=len(value),target_hex=value.hex(),parity_space_added=pad))
        choiceproof=read('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
        choice_rows=doc['typed_choice_records'];assert len(choice_rows)==2 and [r['option_index'] for r in choice_rows]==[0,1]
        oldmenu=next(c for c in spec['all_current_commands'] if c['word']==0x2100)
        sourcemenu=next(c for c in clean_spec['commands'] if c['word']==0x2100)
        at=oldmenu['offset'];oldvalue=bytes.fromhex(oldmenu['whole_command_hex']);sourcevalue=bytes.fromhex(sourcemenu['whole_command_hex'])
        value=bytes.fromhex(choiceproof['target_menu_object_hex'])
        assert choiceproof['manuscript_sha256']==sha(Path(doc['prior_manuscript']).read_bytes())
        assert len(oldvalue)==len(sourcevalue)==36 and len(value)==30 and old[at:at+36]==oldvalue and clean[at:at+36]==sourcevalue
        assert value[:2]==oldvalue[:2]==bytes.fromhex('0021') and len(value)%2==0
        patches.append(dict(start=at,end=at+36,old=oldvalue,value=value,source=sourcevalue,id='B46_menu256',kind='typed-menu'))
        menu_record=dict(old_offset=at,old_length=36,new_length=30,word=0x2100,count=2,target_hex=value.hex(),old_hex=oldvalue.hex(),clean_hex=sourcevalue.hex(),
            labels=[r['english'] for r in choice_rows],record_IDs=[r['id'] for r in choice_rows],source_references=[r['source_reference'] for r in choice_rows])
        assert len(patches)==25
        patches.sort(key=lambda p:p['start']);assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
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
        fixups=[]
        for edge in branches['operands_requiring_adjustment_when_resizing']:
            if edge['block']!=number:continue
            start=mapped(edge['offset']);end=mapped(edge['matched_skip_target']);span=end-start-4
            assert 0<=span<=0xFFFF and span%2==0 and struct.unpack_from('<H',logical,start)[0]==edge['word']
            struct.pack_into('<H',logical,start+2,span)
            fixups.append(dict(**edge,new_offset=start,new_unmatched_next=start+4,new_matched_skip_target=end,target_span=span))
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
        commands,speeches=inventory(arm,target);assert len(commands)==len(spec['all_current_commands']) and len(speeches)==len(texts)
        byoffset={c['offset']:c for c in commands};boundaries=set(byoffset)|{len(logical)};maps=[]
        for previous in spec['all_current_commands']:
            new=byoffset[mapped(previous['offset'])];word=previous['word']
            assert new['word']==word and new['native_extent']==mapped(previous['offset']+previous['native_extent'])-new['offset']
            assert new['ancestor_0100_offsets']==[mapped(a) for a in previous['ancestor_0100_offsets']]
            if word==0x4000:assert bytes.fromhex(previous['whole_command_hex'])[:6]==bytes.fromhex(new['whole_command_hex'])[:6]
            elif word in [0x100,0x200,0x300,0x400]:
                assert old[previous['offset']:previous['offset']+2]==target[new['offset']:new['offset']+2]
            elif word==0x2100:assert previous['whole_command_hex']==menu_record['old_hex'] and new['whole_command_hex']==menu_record['target_hex']
            else:assert previous['whole_command_hex']==new['whole_command_hex']
            maps.append(dict(word=word,old_offset=previous['offset'],new_offset=new['offset'],old_extent=previous['native_extent'],new_extent=new['native_extent'],
                source_0100_ancestors=previous['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
        skipcases=[]
        for fix in fixups:
            command=byoffset[fix['new_offset']];result=ctx.execute(native_skip,target,command);ctx.machines.pop()
            assert all(r['next_offset'] in boundaries for r in result['cases'])
            assert all(r['next_offset']==(fix['new_matched_skip_target'] if r['taken'] else fix['new_unmatched_next']) for r in result['cases'])
            skipcases.append(result)
        for row in texts:
            at=mapped(row['old_offset']);row.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
            assert target[at:at+row['new_length']+1]==bytes.fromhex(row['target_hex'])+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
        menu_record['new_offset']=mapped(menu_record['old_offset']);menu_record['label_references']=[]
        for row in choice_rows:
            at=menu_record['new_offset'];i=row['option_index'];relative=struct.unpack_from('<H',target,at+2+2*i)[0];start=at+6+relative
            value=row['english'].encode('ascii');assert target[start:start+len(value)+1]==value+b'\0'
            menu_record['label_references'].append(dict(id=row['id'],option_index=i,old_reference=row['current_reference'],
                source_reference=row['source_reference'],new_offset=start,new_length=len(value),new_record_index=target[:start].count(b'\0'),
                relative_table_field=at+2+2*i,relative_base=at+6,relative_offset=relative,target_hex=value.hex()))
        def inverse(clean_version):
            restored=bytearray(target[:len(logical)]);restored[:8]=(clean if clean_version else old)[:8]
            for fix in fixups:struct.pack_into('<H',restored,fix['new_offset']+2,fix['source_span'])
            for patch in reversed(patches):
                at=mapped(patch['start']);restored[at:at+len(patch['value'])]=patch['source'] if clean_version else patch['old']
            base=clean if clean_version else old;end=8+struct.unpack_from('<H',base,4)[0]
            return bytes(restored)+base[end:]
        assert inverse(False)==old and inverse(True)==clean
        terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4 and terminal['offset']+4==len(logical)
        bp=ROOT/f'SC0_block{number}_RESEARCH_ONLY.bin';bp.write_bytes(target);blocks[number]=target
        groups.append(dict(block=number,file_path=doc['file_path'],source_block_sha256=sha(old),clean_block_sha256=sha(clean),target_block=str(bp),target_block_sha256=sha(target),
            source_header_hex=old[:8].hex(),target_header_hex=target[:8].hex(),source_bytes=len(old),source_logical_end=oldend,source_tail_bytes=len(old)-oldend,
            target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),
            text_records=texts,choice_commands=[menu_record],relative_fixups=fixups,relocated_skip_cases=skipcases,command_map=maps,all_target_commands=commands,
            source_andtarget_complete_terminal_extent4=True,source_four_byte_header_andmetadata_preserved_except_length=True,
            source_current_andclean_block_inverse_exact=True,external_references_complete=False))
        print('RELOCATION',number,len(old),'->',len(target),'logical',len(logical),'tail',len(target)-len(logical),'fixups',len(fixups),'parityspaces',sum(r['parity_space_added'] for r in texts),flush=True)
    assert not ctx.machines and sum(len(g['text_records']) for g in groups)==24 and sum(len(g['relative_fixups']) for g in groups)==4
    target_archive=IlnkContainer(blocks).to_bytes();ap=ROOT/'SC0_B46_RESEARCH_ONLY.DK4';ap.write_bytes(target_archive)
    parsed=IlnkContainer.parse(target_archive)
    assert [i for i,(a,b) in enumerate(zip(container.blocks,parsed.blocks,strict=True)) if a!=b]==[46]
    inverse_blocks=list(parsed.blocks)
    for group in groups:inverse_blocks[group['block']]=container.blocks[group['block']]
    assert IlnkContainer(inverse_blocks).to_bytes()==archive
    save(ROOT/'one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],file_path=doc['file_path'],source_archive_sha256=sha(archive),
        target_archive=str(ap),target_archive_sha256=sha(target_archive),groups=groups,exactly_one_block_changed=True,other342_blocks_exact=len(parsed.blocks)==343,
        all_full_predecessor_archive_bytes_reconstructed_exactly=True,complete_clean_source_block_reconstructed_exactly=True,
        source_relative_sites=4,relocated_native_skip_cases=20,all_mapped_branch_targets_andnested_ancestor_scopes_preserved=True,
        all24_six_byte_preambles_two_choices_macros_selectors_complete_terminal_andseparate_tails_preserved=True,
        research_archives_only_no_ROM_registration_orcredit=True,external_references_complete=False,
        source_UI_effects_waits_A000_C200_wholecontrols_stored_fonts_census_actual_policy_production_andrelease_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),ordinary_captain0_opening_context_no_unlock_orstate_fixture=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE,MANUSCRIPT,PLAN,NATIVE,BRANCH,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Research archive:24 speeches/two choices/four relative sites/20 native cases;only B46 changes,342 others exact;both full block inverses andpredecessor archive exact. No ROM orcredit.')
