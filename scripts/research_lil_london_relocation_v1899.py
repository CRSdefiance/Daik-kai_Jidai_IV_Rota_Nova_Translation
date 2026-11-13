"""Rebuild reviewed B26 with92 typed spans; research only until final approval."""
import struct
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.lil_london_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_relocation_v1899')
ROM=Path('out/all_routes_combined_v1875_candidate.nds')
DOC=Path('translations/lil_london_editorial_manuscript_v4.json')
SOURCE=Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
BRANCHES=Path('work/analysis/lil_London_branches_v1885/original_relative_skip_operand_proof.json')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100

if __name__=='__main__':
    assert not ROOT.exists()
    image=NdsImage.open(ROM)
    arm=image.read_file('/__arm9__.bin')
    source=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[26]
    doc,packet,branches=map(read,(DOC,SOURCE,BRANCHES))
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']==packet['candidate_sha256']
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    assert len(doc['records'])==len(fonts)==111
    assert len(packet['all_current_native_commands'])==262
    assert not any(r['word']==0x2100 for r in packet['all_current_native_commands'])
    profiles={k:profile_for(arm,source,k) for k in ('progressive','FE-paper')}
    old_end=8+struct.unpack_from('<H',source,4)[0]
    patches,texts=[],[]
    for row in doc['records']:
        at=row['current_reference']['offset']
        old=bytes.fromhex(row['current_text_hex'])
        assert source[at:at+len(old)]==old
        compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),
            profiles['FE-paper' if row['source_presentation_prefix_hex']=='fe' else 'progressive'])
        assert compiled.encoded.hex()==row['compiled_hex']==fonts[row['id']]['encoded_hex']
        value=compiled.encoded
        pad=len(value)%2!=len(old)%2
        if pad:value+=b' '
        assert value[:1]==old[:1] and b'\0' not in value and len(value)%2==len(old)%2
        if value[:1]!=b'\xfe':
            expanded=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            pixels,events,_=raster(arm,expanded)
            assert sha(pixels)==fonts[row['id']]['native_font_plane_sha256']
            assert all(e['y']<=48 for e in events)
        patches.append(dict(start=at,end=at+len(old),old=old,value=value,id=row['id']))
        texts.append(dict(id=row['id'],record_index=row['record_index'],old_offset=at,old_length=len(old),
            new_length=len(value),parity_space_added=pad,target_hex=value.hex(),
            consumer='original_FE_modal_5473C_mode1' if value[:1]==b'\xfe' else 'original_progressive_54020'))
    patches.sort(key=lambda p:p['start'])
    assert all(a['end']<=b['start'] for a,b in zip(patches,patches[1:]))
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            if p['start']<offset<p['end']:raise ValueError('Unclassified interior reference')
            if offset==p['start']:return offset+delta
            delta+=len(p['value'])-len(p['old'])
        return offset+delta
    parts,last=[],0
    for p in patches:
        parts.extend((source[last:p['start']],p['value']))
        last=p['end']
    parts.append(source[last:old_end])
    logical=bytearray(b''.join(parts))
    assert len(logical)==mapped(old_end) and len(logical)<0x2400
    fixups=[]
    for edge in branches['operands_requiring_adjustment_when_resizing']:
        assert edge['block']==26
        start=mapped(edge['offset'])
        target=mapped(edge['matched_skip_target'])
        span=target-start-4
        assert 0<=span<=0xffff and span%2==0
        assert struct.unpack_from('<H',logical,start)[0]==edge['word']
        old_span=struct.unpack_from('<H',source,edge['span_field_offset'])[0]
        struct.pack_into('<H',logical,start+2,span)
        fixups.append(dict(**edge,new_offset=start,new_unmatched_next=start+4,new_matched_skip_target=target,
            source_span=old_span,target_span=span))
    assert len(fixups)==92
    struct.pack_into('<H',logical,4,len(logical)-8)
    target=bytes(logical)+b'\0'*(-len(logical)%4)
    commands,speeches=inventory(arm,target)
    assert len(commands)==262 and len(speeches)==111
    by_offset={r['offset']:r for r in commands}
    mapped_commands=[]
    for old in packet['all_current_native_commands']:
        new=by_offset[mapped(old['offset'])]
        assert new['word']==old['word']
        assert new['ancestor_0100_offsets']==[mapped(a) for a in old['ancestor_0100_offsets']]
        assert mapped(old['offset']+old['native_extent'])-mapped(old['offset'])==new['native_extent']
        if old['word'] not in (0x100,0x200,0x300,0x4000):
            assert source[old['offset']:old['offset']+old['native_extent']]==target[new['offset']:new['offset']+new['native_extent']]
        mapped_commands.append(dict(word=old['word'],old_offset=old['offset'],new_offset=new['offset'],
            old_native_extent=old['native_extent'],new_native_extent=new['native_extent'],
            original_0100_ancestors=old['ancestor_0100_offsets'],relocated_0100_ancestors=new['ancestor_0100_offsets']))
    boundaries=set(by_offset)|{len(logical)}
    cpu=machine(arm)
    cpu.mem_write(STREAM-16,b'\xa5'*(len(target)+32))
    cpu.mem_write(STREAM,target)
    native_cases=[]
    for edge in fixups:
        assert edge['new_unmatched_next'] in boundaries and edge['new_matched_skip_target'] in boundaries
        for choice in (0,1,2,3,0xffffffff):
            cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+edge['new_offset'],0,0))
            cpu.mem_write(RESULT,bytes(24))
            cpu.mem_write(LENGTH,bytes(4))
            call(cpu,0x2A510,(RESULT,OWNER,LENGTH,choice))
            extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
            take=edge['word']==0x100 or (edge['word']==0x200 and choice==0) or (edge['word']==0x300 and choice==1)
            assert edge['new_offset']+extent==(edge['new_matched_skip_target'] if take else edge['new_unmatched_next'])
            assert struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
            assert bytes(cpu.mem_read(STREAM,len(target)))==target
            native_cases.append(dict(new_offset=edge['new_offset'],last_result=choice,native_extent=extent,
                original_destination_preserved_at_mapped_native_boundary=True))
    assert len(native_cases)==460
    for row in texts:
        row['new_offset']=mapped(row['old_offset'])
        at=row['new_offset']
        assert target[at-5:at+1]==source[row['old_offset']-5:row['old_offset']+1]
        assert target[at:at+row['new_length']].hex()==row['target_hex'] and target[at+row['new_length']]==0
    inverse=bytearray(logical)
    for edge in fixups:struct.pack_into('<H',inverse,edge['new_offset']+2,edge['source_span'])
    for p in reversed(patches):inverse[mapped(p['start']):mapped(p['start'])+len(p['value'])]=p['old']
    struct.pack_into('<H',inverse,4,old_end-8)
    assert bytes(inverse)==source[:old_end]
    ROOT.mkdir(parents=True)
    file=ROOT/'SC2_block026_RESEARCH_ONLY.bin'
    file.write_bytes(target)
    save(ROOT/'nested_source_relocation_research.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_block_sha256=sha(source),
        research_block_sha256=sha(target),source_bytes=len(source),research_bytes=len(target),
        source_logical_end=old_end,research_logical_end=len(logical),text_records=texts,
        relative_skip_fixups=fixups,mapped_commands=mapped_commands,target_native_skip_cases=native_cases,
        all262_nested_commands_111_complete_preambles_and_92_typed_spans_preserved=True,
        all460_relocated_native_skip_cases_match_original_mapping=True,
        inverse_restoration_recovers_every_original_logical_byte=True,
        all108_progressive_parity_space_native_planes_equal_reviewed=True,
        FE_parity_space_native_recheck_pending=True,
        source_branch_proof=str(BRANCHES),source_branch_proof_sha256=sha(BRANCHES.read_bytes()),
        research_block=str(file),external_references_complete=False,not_a_release_relocation_map=True,
        loader_external_census_revised_gameplay_andregistered_release_pending=True,
        no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_bytes=len(source),research_bytes=len(target),growth=len(target)-len(source),
        complete_preambles=111,commands=262,typed_spans=92,target_native_cases=460,exact_inverse=True))
