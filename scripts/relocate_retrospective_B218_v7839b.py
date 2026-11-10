"""Rebuild only the automatic wrap in B218; bind all13 speeches and both complete inverses."""
import struct
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_relocation_v7839b')
DOC=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
PLAN=Path('work/analysis/retrospective_B218_predicate_plan_v7833/one_changed_automatic_plan12_exact_reuses_all13_unmodified_base_QA.json')
LEADS=Path('work/analysis/completed_contraction_wrap_leads_v7831/completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json')
NATIVE=Path('work/analysis/retrospective_B218_native_v7838/one_changed_wrap12_alignments_two_complete_current_native_planes.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,leads,native=map(read,[DOC,PLAN,LEADS,NATIVE])
    assert native['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes())
    image=NdsImage.open(doc['current_ROM']);clean_image=NdsImage.open('work/clean.nds')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==leads['candidate_sha256']
    path='/data/SC2.DK4';archive=image.read_file(path);container=IlnkContainer.parse(archive)
    before=container.blocks[218];clean=IlnkContainer.parse(clean_image.read_file(path)).blocks[218]
    lead=next(g for g in leads['source_current_native_groups'] if g['file_path']==path and g['block']==218)
    assert sha(before)==lead['current_block_sha256'] and sha(clean)==lead['source_block_sha256']
    assert len(container.blocks)==336
    inventory,walker,fn=scoped_inventory();arm=image.read_file('/__arm9__.bin')
    cc,cs=inventory(arm,before);sc,ss=inventory(clean_image.read_file('/__arm9__.bin'),clean)
    assert len(cc)==len(sc)==15 and len(cs)==len(ss)==13
    assert [c['word'] for c in cc]==[c['word'] for c in sc]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400] for c in cc)
    assert all(not c['ancestor_0100_offsets'] for c in cc)
    rows=[];patches=[];refs=[]
    for source_speech,current_speech in zip(ss,cs,strict=True):
        ja,at=source_speech['offset']+5,current_speech['offset']+5
        source_raw=clean[ja:clean.index(0,ja+1)];old=before[at:before.index(0,at+1)]
        source_index=clean[:ja].count(b'\0');ident=f'DK4_MES_B218_R{source_index:04d}'
        row=deepcopy(next(r for r in doc['records'] if r['id']==ident))
        p=next(p for p in plan['records'] if p['id']==ident);compiled=bytes.fromhex(p['proposed']['encoded_hex'])
        value=compiled;pad=len(compiled)%2!=len(old)%2
        if pad:value+=b' '
        assert b'\0' not in value and source_raw[0]==old[0]==value[0]
        assert clean[ja-5:ja+1]==before[at-5:at+1]
        if ident!='DK4_MES_B218_R0027':assert value==old
        row.update(source_hex=source_raw.hex(),source_selector=source_raw[0],compiled_hex=compiled.hex(),current_hex=old.hex(),
            source_reference=dict(file_path=path,block=218,offset=ja,record_index=source_index,bytes=len(source_raw)),
            current_reference=dict(file_path=path,block=218,offset=at,record_index=before[:at].count(b'\0'),bytes=len(old)),
            current_record_index=before[:at].count(b'\0'),source_complete_preamble_hex=clean[ja-5:ja+1].hex())
        ref=dict(id=ident,file_path=path,block=218,source_reference=row['source_reference'],current_reference=row['current_reference'],
            old_offset=at,old_length=len(old),old_hex=old.hex(),compiled_hex=compiled.hex(),target_hex=value.hex(),
            source_selector=source_raw[0],source_complete_preamble_hex=row['source_complete_preamble_hex'],
            new_length=len(value),parity_space_added=pad)
        rows.append(row);refs.append(ref);patches.append(dict(start=at,end=at+len(old),old=old,source=source_raw,value=value,id=ident))
    assert len(rows)==13
    patches.sort(key=lambda p:p['start']);assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    oldend=8+struct.unpack_from('<H',before,4)[0]
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            assert not p['start']<at<p['end']
            if at==p['start']:return at+delta
            delta+=len(p['value'])-len(p['old'])
        return at+delta
    parts=[];last=0
    for p in patches:parts.extend([before[last:p['start']],p['value']]);last=p['end']
    parts.append(before[last:oldend]);logical=bytearray(b''.join(parts))
    assert len(logical)==mapped(oldend)<0x2400
    struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+bytes(-len(logical)%4)
    tc,ts=inventory(arm,target);assert len(tc)==15 and len(ts)==13
    command_map=[]
    for old,new,original in zip(cc,tc,sc,strict=True):
        assert old['word']==new['word']==original['word'] and new['offset']==mapped(old['offset'])
        assert new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
        if old['word']==0x4000:assert before[old['offset']:old['offset']+6]==target[new['offset']:new['offset']+6]
        else:assert old['whole_command_hex']==new['whole_command_hex']==original['whole_command_hex']
        command_map.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],
            old_extent=old['native_extent'],new_extent=new['native_extent'],
            source_0100_ancestors=old['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    assert tc[-1]['word']==0 and tc[-1]['native_extent']==4 and tc[-1]['offset']+4==len(logical)
    for r in refs:
        at=mapped(r['old_offset']);r.update(new_offset=at,new_record_index=target[:at].count(b'\0'))
        assert target[at:at+r['new_length']+1]==bytes.fromhex(r['target_hex'])+b'\0'
    group=dict(file_path=path,block=218,source_block_sha256=sha(before),clean_block_sha256=sha(clean),
        source_bytes=len(before),source_logical_end=oldend,source_tail_bytes=len(before)-oldend,
        target_bytes=len(target),target_logical_end=len(logical),target_tail_bytes=len(target)-len(logical),
        target_block_sha256=sha(target),target_header_hex=target[:8].hex(),
        text_records=refs,relative_fixups=[],command_map=command_map,all_target_commands=tc)
    packet=dict(file_path=path,block=218,current_block_sha256=sha(before),clean_block_sha256=sha(clean),
        current_logical_end=oldend,all_current_commands=cc)
    ROOT.mkdir(parents=True)
    provenance=read('work/analysis/retrospective_B218_relocation_repair_v7839b/provenance.json')['helper_derivation']
    from dk4tool.patch.retrospective_SC2_reconstruction_v2 import reconstruct
    assert reconstruct(before,clean,group,packet,rows,[])==target
    blocks=list(container.blocks);blocks[218]=target;newarchive=IlnkContainer(blocks).to_bytes()
    assert [i for i,(a,b) in enumerate(zip(container.blocks,IlnkContainer.parse(newarchive).blocks,strict=True)) if a!=b]==[218]
    restored=IlnkContainer.parse(newarchive);restored.blocks[218]=before
    assert restored.to_bytes()==archive
    bp=ROOT/'SC2_B218_RESEARCH_ONLY.bin';bp.write_bytes(target)
    ap=ROOT/'SC2_RESEARCH_ONLY.DK4';ap.write_bytes(newarchive)
    for p in patches:assert p['old']!=p['value'] if p['id']=='DK4_MES_B218_R0027' else p['old']==p['value']
    save(ROOT/'all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        file_path=path,block=218,source_archive_sha256=sha(archive),target_archive=str(ap),target_archive_sha256=sha(newarchive),
        target_block=str(bp),groups=[group],current_packet=packet,records=rows,
        only_changed_record_ID='DK4_MES_B218_R0027',other12_stored_speeches_exact=True,
        all335_other_blocks_exact=True,complete_clean_andpredecessor_blocks_inverse_exact=True,
        full_predecessor_archive_inverse_exact=True,all15_original_commands13_preambles_zero_macros_A000_andcomplete_end_preserved=True,
        relative_andinblock_predicate_commands=0,native_inventory_walker=walker,native_inventory_function=fn,
        unchanged_reconstruction_native_guards=provenance,
        stored_native_fonts_loader_caller_actual_policy_andrelease_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,LEADS,NATIVE,Path(__file__)]},full_goal_complete=False))
    print('B218 only R27 stored changes;',len(before),'->',len(target),'bytes;15commands/13preambles/no relative sites;clean+predecessor block andfull predecessor archive inverses exact.')
