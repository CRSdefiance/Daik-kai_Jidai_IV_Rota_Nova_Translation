"""Typed182-command B44 research relocation, with explicit inherited span repair.

This writes a preserved research ROM only. FE/choice display, loader/external
references, representative gameplay and registered integration remain pending.
"""
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.census_native_storylines_v1995 import complete_walk,choices
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_relocation_v2001')
PARENT=Path('out/all_routes_combined_v1986_candidate.nds')
ROM=ROOT/'rafael_opening_V1986_derived_RESEARCH_ONLY.nds'
DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v2.json')
FONT=Path('work/analysis/rafael_opening_fonts_v1998/all114_progressive_native_macros_and_complete_font_planes.json')
SPAN=Path('work/analysis/rafael_opening_span_v1999/current_B44_final_span_diagnosis.json')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100

if __name__=='__main__':
    assert not ROOT.exists()
    doc,font,span=map(read,(DOC,FONT,SPAN))
    assert not font['failures'] and font['manuscript_sha256']==sha(DOC.read_bytes())
    assert sha(PARENT.read_bytes())==font['candidate_sha256']
    image=NdsImage.open(PARENT);arm=image.read_file('/__arm9__.bin')
    container=IlnkContainer.parse(image.read_file('/data/SC0.DK4'));source=container.blocks[44]
    assert sha(source)==span['current_block_sha256']
    normalized=bytearray(source);struct.pack_into('<H',normalized,6606,76)
    assert sha(normalized)==span['one_byte_normalized_copy_sha256']
    commands=span['corrected_in_memory_native']['commands'];assert len(commands)==182
    command_by_offset={r['offset']:r for r in commands}
    font_by_ID={r['id']:r for r in font['cases']}
    patches=[];text_records=[]
    for row in doc['records']:
        start=row['current_reference']['header_offset'];command=command_by_offset[start]
        assert command['word']==0x4000
        old=source[start:start+command['native_extent']]
        assert old[:6].hex()==row['source_complete_preamble_hex']
        original=bytes.fromhex(row['current_text_hex']);at=row['current_reference']['offset']
        assert source[at:at+len(original)]==original and source[at+len(original)]==0
        if row['source_presentation_prefix_hex']=='fe':
            text_records.append(dict(id=row['id'],old_command_offset=start,old_native_extent=len(old),
                source_preamble_hex=old[:6].hex(),target_hex=old.hex(),unchanged_FE_separate_display_pending=True))
            continue
        case=font_by_ID[row['id']]
        payload=bytes.fromhex(case['encoded_text_excluding_speaker_hex'])
        # Preserve old text parity explicitly; this is encoder-owned structural
        # padding, not authored layout or a native command separator.
        old_payload=source[start+6:at+len(original)]
        parity_space=len(payload)%2!=len(old_payload)%2
        value=payload+(b' 'if parity_space else b'')
        assert len(value)%2==len(old_payload)%2 and b'\0'not in value
        new=old[:6]+value+b'\0';new+=b'\0'*(-len(new)%2)
        expanded=value.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        pixels,glyphs,font_data=raster(arm,expanded)
        assert pixels==expected_pixels(arm,font_data,glyphs) and sha(pixels)==case['native_font_plane_sha256']
        assert all(0<=g['x']<=210 and 0<=g['y']<=48 for g in glyphs)
        patches.append(dict(start=start,end=start+len(old),old=old,new=new))
        text_records.append(dict(id=row['id'],old_command_offset=start,old_native_extent=len(old),
            source_preamble_hex=old[:6].hex(),target_hex=new.hex(),text_hex=value.hex(),
            source_record_index=row['source_record_index'],current_source_record_index=row['record_index'],
            parity_space_added=parity_space,final_parity_native_plane_equals_reviewed_plane=True,
            native_plane_sha256=sha(pixels)))
    assert len(patches)==114 and len(text_records)==115
    patches.sort(key=lambda r:r['start'])
    def mapped(offset):
        shift=0
        for p in patches:
            assert not p['start']<offset<p['end'],('unclassified interior reference',offset,p['start'])
            if offset>=p['end']:shift+=len(p['new'])-len(p['old'])
        return offset+shift
    end=8+struct.unpack_from('<H',source,4)[0]
    output=[];last=0
    for p in patches:output.extend((source[last:p['start']],p['new']));last=p['end']
    output.append(source[last:end]);target=bytearray(b''.join(output))
    assert len(target)==mapped(end) and len(target)<0x2400
    boundaries={r['offset']for r in commands}|{end};edges=[]
    for command in commands:
        if command['word']not in(0x100,0x200,0x300,0x400):continue
        at=command['offset'];actual_span=struct.unpack_from('<H',source,at+2)[0]
        intended_span=struct.unpack_from('<H',normalized,at+2)[0]
        old_target=at+4+intended_span
        assert at+4 in boundaries and old_target in boundaries
        new_at,new_target=mapped(at),mapped(old_target);new_span=new_target-new_at-4
        assert new_span%2==0 and 0<=new_span<=0xffff
        struct.pack_into('<H',target,new_at+2,new_span)
        edges.append(dict(offset=at,word=command['word'],actual_source_span=actual_span,
            classified_intended_source_span=intended_span,actual_source_matched_target=at+4+actual_span,
            intended_source_matched_target=old_target,source_unmatched_next=at+4,
            inherited_stale_span_explicitly_repaired=actual_span!=intended_span,
            new_offset=new_at,new_matched_skip_target=new_target,new_unmatched_next=new_at+4,target_span=new_span))
    assert len(edges)==4 and sum(e['inherited_stale_span_explicitly_repaired']for e in edges)==1
    struct.pack_into('<H',target,4,len(target)-8);logical_end=len(target)
    target=bytes(target)+b'\0'*(-len(target)%4)
    parsed=complete_walk(arm,target);assert not parsed['errors']
    assert len(parsed['commands'])==182
    target_commands={r['offset']:r for r in parsed['commands']};mapped_commands=[]
    for command in commands:
        old_at=command['offset'];new_at=mapped(old_at);new=target_commands[new_at]
        assert new['word']==command['word']
        assert new['native_extent']==mapped(old_at+command['native_extent'])-new_at
        assert new['ancestor_0100_offsets']==[mapped(a)for a in command['ancestor_0100_offsets']]
        if command['word']not in(0x100,0x200,0x300,0x400,0x4000):assert new['whole_command_hex']==command['whole_command_hex']
        if command['word']==0x4000:assert source[old_at:old_at+6]==target[new_at:new_at+6]
        mapped_commands.append(dict(word=command['word'],old_offset=old_at,new_offset=new_at,
            old_native_extent=command['native_extent'],new_native_extent=new['native_extent'],
            source_0100_ancestors=command['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    menu,menu_errors=choices(machine(arm),target,parsed['commands']);assert not menu_errors and len(menu)==1
    assert [bytes.fromhex(r['hex'])for r in menu[0]['labels']]==[b'Ask him.',b'Prepare alone.']
    for text in text_records:
        text['new_command_offset']=mapped(text['old_command_offset'])
        text['new_offset']=text['new_command_offset']+5
        text['new_record_index']=target[:text['new_offset']].count(b'\0')+int(target[text['new_offset']]==0)
        assert target[text['new_command_offset']:text['new_command_offset']+len(bytes.fromhex(text['target_hex']))].hex()==text['target_hex']
    # Restore actual current source, including its explicitly diagnosed defect.
    restored=bytearray(target[:logical_end]);struct.pack_into('<H',restored,4,end-8)
    for edge in edges:struct.pack_into('<H',restored,edge['new_offset']+2,edge['actual_source_span'])
    for p in reversed(patches):
        at=mapped(p['start']);restored[at:at+len(p['new'])]=p['old']
    assert bytes(restored)==source[:end]
    cpu=machine(arm);native_cases=[]
    for version,data in [('actual-current',source),('normalized-current-analysis-only',bytes(normalized)),('research-target',target)]:
        cpu.mem_write(STREAM-16,b'\xa5'*(len(data)+32));cpu.mem_write(STREAM,data)
        for edge in edges:
            at=edge['new_offset']if version=='research-target'else edge['offset']
            field=struct.unpack_from('<H',data,at+2)[0]
            for previous in (0,1,2,3,0xffffffff):
                cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0))
                owner=bytes(cpu.mem_read(OWNER-16,64));cpu.mem_write(RESULT-16,b'\xa5'*80);cpu.mem_write(RESULT,b'\0'*24)
                cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,b'\0'*4)
                call(cpu,0x2A510,(RESULT,OWNER,LENGTH,previous))
                taken=edge['word']==0x100 or previous=={0x200:0,0x300:1,0x400:2}.get(edge['word'],-1)
                extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0];assert extent==4+(field if taken else 0)
                assert bytes(cpu.mem_read(OWNER-16,64))==owner and bytes(cpu.mem_read(STREAM,len(data)))==data
                assert bytes(cpu.mem_read(RESULT,24))==struct.pack('<6I',3,0,0,0,0,0)
                for guard in (STREAM-16,STREAM+len(data),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4):assert bytes(cpu.mem_read(guard,16))==b'\xa5'*16
                native_cases.append(dict(version=version,offset=at,previous_result=previous,taken=taken,native_extent=extent,
                    actual_current_stale_target_disclosed=version=='actual-current'and edge['inherited_stale_span_explicitly_repaired'],
                    whole_native_ABI_owner_input_output_guards_exact=True))
    assert len(native_cases)==60
    ROOT.mkdir(parents=True)
    (ROOT/'SC0_block044_RESEARCH_ONLY.bin').write_bytes(target)
    before_file=image.read_file('/data/SC0.DK4');container.blocks[44]=target;image.replace_file('/data/SC0.DK4',container.to_bytes());image.save(ROM)
    parent=NdsImage.open(PARENT);result=NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files()if result.read_file(p)!=data]==['/data/SC0.DK4']
    assert all(result.read_file(p)==data for p,data in parent.iter_components())
    assert [n for n,(a,b)in enumerate(zip(IlnkContainer.parse(before_file).blocks,IlnkContainer.parse(result.read_file('/data/SC0.DK4')).blocks,strict=True))if a!=b]==[44]
    save(ROOT/'current_B44_typed_relocation_research.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(arm),source_SC0_sha256=sha(before_file),target_SC0_sha256=sha(result.read_file('/data/SC0.DK4')),
        source_block_sha256=sha(source),target_block_sha256=sha(target),old_bytes=len(source),new_bytes=len(target),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        text_records=text_records,mapped_native_commands=mapped_commands,relative_skip_fixups=edges,native_cases=native_cases,
        all182_typed_command_words_preambles_extents_and_ancestors_verified=True,
        all114_final_parity_native_planes_exact=True,all4_relative_sites60_native_cases_pass=True,
        explicit_inherited_stale_span_repair=True,exact_inverse_restores_actual_current_source_including_old_stale_span=True,
        typed_choice_object_and_both_original_labels_unchanged=True,typed_target_choices=menu,
        only_B44_changes_all342_other_blocks_all_other_files_components_exact=True,
        external_entry_loader_and_actual_scene_proofs_pending=True,FE_and_choices_final_display_proofs_pending=True,
        registered_integration_and_clean_patch_pending=True,not_a_playable_user_handoff=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(commands=182,texts=115,changed_progressive=114,relative_sites=4,native_cases=60,old_bytes=len(source),new_bytes=len(target),research_only=True))
