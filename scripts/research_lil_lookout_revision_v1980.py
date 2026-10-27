"""Current-source B23 one-paragraph relocation, native skips and exact inverse."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_name_catalog_glyphs_v278 import raster, expected_pixels
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Lookout_relocation_v1980')
PARENT = Path('out/all_routes_combined_v1971_candidate.nds')
ROM = ROOT/'lil_Lookout_V1971_derived_RESEARCH_ONLY.nds'
PLAN = ROOT/'current_B23_typed_relocation_research.json'
PACKET = Path('work/analysis/lil_lessons_contextual_v1977/all64_clean_current_full_exchange_and_native_commands.json')
FONT = Path('work/analysis/lil_Lookout_affiliation_fonts_v1978/one_changed_native_macros_and_complete_font_plane.json')
DOC = Path('translations/lil_lessons_editorial_manuscript_v6.json')
CHANGED = 'DK4_MES_B23_R0142'
OWNER, STREAM, RESULT, LENGTH = 0x02650000, 0x02660000, 0x02668000, 0x02668100

if __name__ == '__main__':
    assert not ROOT.exists()
    packet, font, doc = map(read,(PACKET,FONT,DOC))
    assert font['manuscript_sha256'] == sha(DOC.read_bytes())
    assert sha(PARENT.read_bytes()) == packet['candidate_sha256'] == font['candidate_sha256'] == doc['current_ROM_sha256']
    parent, image, clean = map(NdsImage.open,(PARENT,PARENT,'work/clean.nds'))
    arm = image.read_file('/__arm9__.bin')
    assert sha(arm) == packet['ARM9_sha256'] == font['ARM9_sha256']
    original_arm = clean.read_file('/__arm9__.bin')
    assert all(arm[a:b] == original_arm[a:b] for a,b in ((0x2A414,0x2A530),(0x24048,0x24118)))
    container = IlnkContainer.parse(image.read_file('/data/SC2.DK4'))
    source = container.blocks[23]
    jp = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[23]
    context = next(r for r in packet['blocks'] if r['block'] == 23)
    assert sha(source) == context['current_block_sha256']
    assert sha(jp) == context['clean_block_sha256']
    row = next(r for r in doc['records'] if r['id'] == CHANGED)
    case = font['cases'][0]
    assert case['id'] == CHANGED and not font['failures'] and font['native_macro_calls'] == 8
    start, old = row['current_reference']['offset'], bytes.fromhex(row['current_text_hex'])
    ja, japanese = row['source_reference']['offset'], bytes.fromhex(row['source_hex'])
    assert start == 2095 and ja == 1845 and len(old) == 99
    assert row['record_index'] == 141 and row['source_record_index'] == 142
    assert source[start:start+len(old)] == old and source[start+len(old)] == 0
    assert jp[ja:ja+len(japanese)] == japanese and jp[ja+len(japanese)] == 0
    assert source[start-5:start+1] == jp[ja-5:ja+1] == bytes.fromhex('0040ffff0009')
    compiled = bytes.fromhex(case['encoded_hex'])
    value = compiled + (b' ' if len(compiled)%2 != len(old)%2 else b'')
    assert value[:1] == old[:1] == japanese[:1] == b'\x09' and b'\0' not in value
    assert len(value)%2 == len(old)%2
    pixels, glyphs, kanji = raster(arm,value[1:])
    assert pixels == expected_pixels(arm,kanji,glyphs)
    assert sha(pixels) == case['native_font_plane_sha256']
    delta = len(value)-len(old)
    end = 8+struct.unpack_from('<H',source,4)[0]
    assert end <= len(source) and not any(source[end:])
    def mapped(offset):
        assert not start < offset < start+len(old),('Unclassified interior reference',offset)
        return offset+(delta if offset >= start+len(old) else 0)
    target = bytearray(source[:start]+value+source[start+len(old):end])
    assert len(target) == mapped(end) and len(target) < 0x2400
    commands = context['all_current_native_commands']
    assert len(commands) == 55
    source_boundaries = {r['offset'] for r in commands}|{end}
    fixups = []
    for command in commands:
        if command['word'] not in (0x100,0x200,0x300): continue
        at = command['offset']
        span = struct.unpack_from('<H',source,at+2)[0]
        old_target = at+4+span
        assert at+4 in source_boundaries and old_target in source_boundaries
        new_at, new_target = mapped(at), mapped(old_target)
        new_span = new_target-new_at-4
        assert 0 <= new_span <= 0xffff and new_span%2 == 0
        struct.pack_into('<H',target,new_at+2,new_span)
        fixups.append(dict(offset=at,word=command['word'],span_field_offset=at+2,source_span=span,
            unmatched_next_offset=at+4,matched_skip_target=old_target,new_offset=new_at,
            new_unmatched_next=new_at+4,new_matched_skip_target=new_target,target_span=new_span))
    assert len(fixups) == 12
    struct.pack_into('<H',target,4,len(target)-8)
    logical_end = len(target)
    target = bytes(target)+bytes(-len(target)%4)
    target_commands, target_speeches = inventory(arm,target)
    assert len(target_commands) == 55 and len(target_speeches) == 33
    by_offset = {r['offset']:r for r in target_commands}
    mapped_commands = []
    for command in commands:
        old_at, new_at = command['offset'], mapped(command['offset'])
        new = by_offset[new_at]
        assert new['word'] == command['word']
        assert new['native_extent'] == mapped(old_at+command['native_extent'])-new_at
        assert new['ancestor_0100_offsets'] == [mapped(a) for a in command['ancestor_0100_offsets']]
        if command['word'] not in (0x100,0x200,0x300) and old_at != start-5:
            assert command['whole_command_hex'] == new['whole_command_hex']
        if command['word'] == 0x4000:
            assert source[old_at:old_at+6] == target[new_at:new_at+6]
        mapped_commands.append(dict(word=command['word'],old_offset=old_at,new_offset=new_at,
            old_native_extent=command['native_extent'],new_native_extent=new['native_extent'],
            source_0100_ancestors=command['ancestor_0100_offsets'],target_0100_ancestors=new['ancestor_0100_offsets']))
    assert target[start:start+len(value)] == value and target[start+len(value)] == 0
    cpu = machine(arm)
    native_cases = []
    for label, data in (('current',source),('research',target)):
        cpu.mem_write(STREAM-16,b'\xa5'*(len(data)+32))
        cpu.mem_write(STREAM,data)
        for edge in fixups:
            at = edge['offset'] if label == 'current' else edge['new_offset']
            span = edge['source_span'] if label == 'current' else edge['target_span']
            for previous in (0,1,2,3,0xffffffff):
                cpu.mem_write(OWNER-16,b'\xa5'*64)
                cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0))
                owner_before = bytes(cpu.mem_read(OWNER-16,64))
                cpu.mem_write(RESULT-16,b'\xa5'*80)
                cpu.mem_write(RESULT,bytes(24))
                cpu.mem_write(LENGTH-16,b'\xa5'*36)
                cpu.mem_write(LENGTH,bytes(4))
                call(cpu,0x2A510,(RESULT,OWNER,LENGTH,previous))
                taken = edge['word'] == 0x100 or (edge['word'] == 0x200 and previous == 0) or (edge['word'] == 0x300 and previous == 1)
                extent = struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                assert extent == 4+(span if taken else 0)
                assert struct.unpack('<6I',cpu.mem_read(RESULT,24)) == (3,0,0,0,0,0)
                assert bytes(cpu.mem_read(STREAM,len(data))) == data
                assert bytes(cpu.mem_read(OWNER-16,64)) == owner_before
                for guard in (STREAM-16,STREAM+len(data),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4):
                    assert bytes(cpu.mem_read(guard,16)) == b'\xa5'*16
                native_cases.append(dict(version=label,offset=at,word=edge['word'],previous_result=previous,
                    taken=taken,native_extent=extent,source_target_preserved=True,ABI_input_owner_and_output_guards_exact=True))
    assert len(native_cases) == 120
    restored = bytearray(target[:logical_end])
    struct.pack_into('<H',restored,4,end-8)
    for edge in fixups: struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    restored[start:start+len(value)] = old
    assert bytes(restored) == source[:end]
    container.blocks[23] = target
    image.replace_file('/data/SC2.DK4',container.to_bytes())
    ROOT.mkdir(parents=True)
    (ROOT/'SC2_block023_RESEARCH_ONLY.bin').write_bytes(target)
    image.save(ROM)
    result = NdsImage.open(ROM)
    assert [p for _,p,data in parent.iter_files() if result.read_file(p) != data] == ['/data/SC2.DK4']
    for path,data in parent.iter_components(): assert result.read_file(path) == data,path
    before, after = (IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in (parent,result))
    assert len(before) == len(after) == 336
    assert [n for n,(a,b) in enumerate(zip(before,after,strict=True)) if a != b] == [23]
    changed = dict(id=CHANGED,block=23,source_record_index=142,current_source_record_index=141,
        source_Japanese_offset=ja,old_offset=start,new_offset=start,old_length=len(old),new_length=len(value),
        encoded_hex=compiled.hex(),target_hex=value.hex(),parity_space_added=len(value)!=len(compiled),
        complete_final_target_native_plane_equals_reviewed_plane=True,native_plane_sha256=sha(pixels))
    save(PLAN,dict(parent=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),ARM9_sha256=sha(arm),
        source_SC2_sha256=sha(parent.read_file('/data/SC2.DK4')),target_SC2_sha256=sha(result.read_file('/data/SC2.DK4')),
        block=23,source_block_sha256=sha(source),research_block_sha256=sha(target),clean_block_sha256=sha(jp),
        source_bytes=len(source),research_bytes=len(target),source_logical_end=end,research_logical_end=logical_end,
        text_records=[changed],relative_skip_fixups=fixups,mapped_native_commands=mapped_commands,
        all55_current_and_target_native_commands_and_opaque_bytes_preserved=True,
        unchanged_B23_speech_commands=32,unchanged_B120_speech_objects=27,
        unchanged_original_B23_two_label_choice_preserved=True,all_other335_SC2_blocks_and_all_other_files_components_exact=True,
        current_and_relocated_native_skip_cases=native_cases,all12_relative_sites_120_cases_preserve_targets=True,
        inverse_restores_every_original_logical_byte=True,entry_point_offset=8,
        original_runtime_and_overlay_files_unchanged_prior_shipped24070_entry_census_inherited_not_rerun=True,
        full_loader_reference_revised_actual_and_registered_release_approval_pending=True,not_a_release_relocation_map=True,
        evidence={str(p):sha(p.read_bytes()) for p in (PACKET,FONT,DOC,
            Path('work/analysis/lil_lessons_native_checkpoint_v1979b/all60_source_bound_native_font_inheritance.json'))},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        COMMON_sha256=sha(result.read_file('/COMMON/MESFILE.DK4')),SC2_sha256=sha(result.read_file('/data/SC2.DK4')),
        only_changed_blocks=[23],block_growth_bytes={'23':len(target)-len(source)},only_changed_id=CHANGED,
        all335_other_SC2_blocks_every_other_file_and_native_component_exact=True,source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        registered_candidate=False,not_for_user_handoff_or_new_parent=True,full_goal_complete=False))
    print(dict(research_ROM_sha256=sha(ROM.read_bytes()),only_changed_id=CHANGED,block_growth=len(target)-len(source),
        mapped_commands=55,relative_sites=12,native_cases=120,inverse_exact=True,final_parity_plane_exact=True))
