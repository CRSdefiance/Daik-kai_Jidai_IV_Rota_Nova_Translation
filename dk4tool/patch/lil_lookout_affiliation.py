"""One source-bound B23 affiliation correction after the complete V1971 stack."""
import json
import struct
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH = '/data/SC2.DK4'
CONFIG = 'translations/lil_lookout_affiliation_release_v1.json'
IDENT = 'DK4_MES_B23_R0142'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require(test, message):
    if not test:
        raise ValueError('Lil Lookout '+message)


def apply_release(image, baseline, config_path=CONFIG):
    config = load(config_path)
    require(config.get('format') == 'dk4-lil-lookout-affiliation-release-v1','unknown release format')
    for name, expected in config['dependencies'].items():
        require(sha(Path(name).read_bytes()) == expected,'reviewed dependency differs: '+name)
    original_file, arm = image.read_file(PATH), image.read_file('/__arm9__.bin')
    require(sha(original_file) == config['source_SC2_sha256'],'current SC2 differs')
    require(sha(arm) == config['required_runtime_arm9_sha256'],'exact native runtime required')
    require(sha(baseline.read_file(PATH)) == config['canonical_SC2_sha256'],'canonical SC2 differs')
    clean_path = Path(config['clean_ROM'])
    require(sha(clean_path.read_bytes()) == config['clean_ROM_sha256'],'clean Japanese ROM differs')
    clean = NdsImage.open(clean_path).read_file(PATH)
    require(sha(clean) == config['clean_SC2_sha256'],'clean Japanese SC2 differs')
    doc, mapping = load(config['manuscript']), load(config['reference_map'])
    validate_natural_dialogue_batch(doc)
    require(doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
        and doc['encoder'] == 'dialogue-relocatable-v1' and doc['dialogue_profile'] == 'lil-opening-editorial-native-v1'
        and doc['formatting_review_pending'] is False and doc['required_runtime_ARM9_sha256'] == sha(arm),
        'complete source/native review required')
    require(len(doc['records']) == 1 and doc['records'][0]['id'] == IDENT,'one exact reviewed record required')
    require(mapping.get('format') == 'dk4-lil-lookout-source-relocation-map-v1'
        and mapping.get('external_references_complete') is True and mapping.get('entry_point_offset') == 8
        and mapping.get('preserve_record_parity') is True and mapping.get('required_runtime_ARM9_sha256') == sha(arm)
        and mapping.get('source_SC2_sha256') == sha(original_file)
        and mapping.get('target_SC2_sha256') == config['target_SC2_sha256'], 'complete current-source map required')
    for key in ('all55_nested_commands12_relative_sites_verified','all120_current_relocated_native_cases_verified',
        'current_EV2_block_index_loader_and_two_parent_modes_verified',
        'one_changed_progressive_record_actual_and_neighbor_transition_approved'):
        require(mapping.get(key) is True,'complete native/reference/actual contract required')
    actual = load(doc['actual_visual_review'])
    require(actual.get('changed_Lookout_two_holds_complete_native_actual_ink') is True
        and actual.get('preceding_and_following_Camille_four_holds_complete_native_actual_ink') is True
        and actual.get('all46_original_B23_command_results_and_mapped_targets_equal') is True
        and actual.get('one16_coordinate_byte_fixture_replay_exact') is True
        and actual.get('all_inputs_schedule_PNGs4MiB_snapshots_and_readonly_observers_host_restoration_pass') is True
        and actual.get('normal_Bruges_town_ID') == 3
        and actual.get('candidate_sha256') == config['tested_research_ROM_sha256'],'focused actual proof required')
    container, japanese = IlnkContainer.parse(original_file), IlnkContainer.parse(clean)
    block, jp = container.blocks[23], japanese.blocks[23]
    require(mapping['block'] == 23 and sha(block) == mapping['source_block_sha256']
        and sha(jp) == mapping['clean_block_sha256'],'exact current/clean B23 required')
    require(len(mapping['text_records']) == 1,'one exact mapped text required')
    ref, row = mapping['text_records'][0], doc['records'][0]
    require(ref['id'] == row['id'] == IDENT and row['file_path'] == PATH and row['block'] == 23,'record identity differs')
    source, old = bytes.fromhex(row['source_hex']), bytes.fromhex(row['current_text_hex'])
    ja, at = row['source_reference']['offset'], row['current_reference']['offset']
    require(jp[ja:ja+len(source)] == source and jp[ja+len(source)] == 0
        and block[at:at+len(old)] == old and block[at+len(old)] == 0,'complete clean/current paragraph differs')
    require(row['source_record_index'] == jp[:ja].count(b'\0') == 142
        and row['record_index'] == block[:at].count(b'\0') == 141,'distinct clean/current record indices differ')
    require(jp[ja-5:ja+1] == block[at-5:at+1] == bytes.fromhex('0040ffff0009')
        and row['source_complete_preamble_hex'] == '0040ffff0009'
        and row['native_display_consumer'] == 'original_progressive_54020','complete original progressive preamble differs')
    require(all(source.count(k.encode('ascii')) == row['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')),
        'runtime substitution count differs')
    compiled = encode_relocatable_dialogue(source,row['english'],get_dialogue_profile('lil-opening-editorial-native-v1'))
    fonts = load(doc['native_font_proof'])['cases']
    require(len(fonts) == 1 and fonts[0]['id'] == IDENT,'one complete native plane required')
    require(compiled.encoded.hex() == row['compiled_hex'] == fonts[0]['encoded_hex'] and not compiled.diagnostics,
        'reviewed native text or diagnostics differ')
    parity = len(compiled.encoded)%2 != len(old)%2
    value = compiled.encoded+(b' ' if parity else b'')
    require(at == ref['old_offset'] == ref['new_offset'] and len(old) == ref['old_length']
        and len(value) == ref['new_length'] and value.hex() == ref['target_hex']
        and parity == ref['parity_space_added'] and b'\0' not in value,'mapped target or compiler parity differs')
    end = 8+struct.unpack_from('<H',block,4)[0]
    require(end == mapping['source_logical_end'] and end <= len(block) and not any(block[end:]),'source extent differs')
    delta = len(value)-len(old)
    def mapped(offset):
        require(not at < offset < at+len(old),'unclassified interior reference')
        return offset+(delta if offset >= at+len(old) else 0)
    logical = bytearray(block[:at]+value+block[at+len(old):end])
    require(len(logical) == mapped(end) == mapping['research_logical_end'] and len(logical) < 0x2400,'target extent/cache differs')
    commands = mapping['mapped_native_commands']
    require(len(commands) == len({r['old_offset'] for r in commands}) == len({r['new_offset'] for r in commands}) == 55,
        'complete55 command map required')
    for command in commands:
        old_at, new_at = command['old_offset'], command['new_offset']
        require(new_at == mapped(old_at)
            and command['new_native_extent'] == mapped(old_at+command['old_native_extent'])-new_at
            and struct.unpack_from('<H',block,old_at)[0] == struct.unpack_from('<H',logical,new_at)[0] == command['word']
            and command['target_0100_ancestors'] == [mapped(a) for a in command['source_0100_ancestors']],
            'complete command boundary/extent/ancestor differs')
        if command['word'] == 0x4000:
            require(block[old_at:old_at+6] == logical[new_at:new_at+6],'complete speech preamble changed')
        if command['word'] not in (0x100,0x200,0x300) and old_at != at-5:
            require(block[old_at:old_at+command['old_native_extent']] == logical[new_at:new_at+command['new_native_extent']],
                'unowned speech/choice/opaque command changed')
    boundaries = {r['new_offset'] for r in commands}|{len(logical)}
    edges = mapping['relative_skip_fixups']
    require(len(edges) == 12,'complete12 relative spans required')
    for edge in edges:
        pos, target = mapped(edge['offset']), mapped(edge['matched_skip_target'])
        span = target-pos-4
        require(pos == edge['new_offset'] and target == edge['new_matched_skip_target']
            and pos+4 == edge['new_unmatched_next'] and target in boundaries and pos+4 in boundaries
            and 0 <= span <= 0xffff and span%2 == 0 and span == edge['target_span']
            and struct.unpack_from('<H',block,edge['offset']+2)[0] == edge['source_span']
            and struct.unpack_from('<H',logical,pos)[0] == edge['word'],'relative span or mapped destination differs')
        struct.pack_into('<H',logical,pos+2,span)
    struct.pack_into('<H',logical,4,len(logical)-8)
    target = bytes(logical)+bytes(-len(logical)%4)
    require(sha(target) == mapping['target_block_sha256'],'complete target B23 differs')
    restored = bytearray(logical)
    struct.pack_into('<H',restored,4,end-8)
    for edge in edges: struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
    restored[at:at+len(value)] = old
    require(bytes(restored) == block[:end],'inverse changed unowned logical bytes')
    container.blocks[23] = target
    result = container.to_bytes()
    require(sha(result) == config['target_SC2_sha256'],'complete target SC2 differs')
    image.replace_file(PATH,result)
    return {'manuscript':config['manuscript'],'reference_map':config['reference_map'],
        'source_SC2_sha256':sha(original_file),'target_SC2_sha256':sha(result),
        'changed_records':[{'id':IDENT,'file_path':PATH,'block':23,'source_record_index':142,'old_record_index':141,
            'old_offset':at,'new_offset':at,'old_bytes':len(old),'new_bytes':len(value),'parity_space_added':parity,
            'original_speaker_layout_controls_runtime_substitutions_and_opaque_bytes_preserved':True}],
        'blocks':[{'block':23,'source_bytes':len(block),'target_bytes':len(target),
            'growth_bytes':len(target)-len(block),'relative_operands':12}],
        'all55_native_command_mappings_and12_spans_verified':True,'all335_other_SC2_blocks_unchanged':True,
        'all59_other_lesson_targets_andfour_labels_unchanged':True,
        'native_runtime_fonts_graphics_and123040_staged_bytes_unchanged':True}
