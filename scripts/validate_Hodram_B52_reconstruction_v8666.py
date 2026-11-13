"""Exercise B52 production reconstruction and independent whole-archive inverses."""
import json
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_B52_reconstruction_v1 import reconstruct
from dk4tool.dialogue.hodram_B52_profile_v1 import validate_approved_batch
from dk4tool.dialogue.hodram_B52_choices_v1 import compile_choices
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_reconstruction_production_v8666')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
MAP = Path('work/analysis/Hodram_B52_relocation_v8642/reconstruction.json')
CURRENT = Path('work/analysis/Hodram_B52_current_v8631/current_effective.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, mapping, packet = read(DOC), read(MAP), read(CURRENT)['groups'][0]
    validate_approved_batch(doc)
    image = NdsImage.open(doc['current_ROM'])
    archive = image.read_file('/data/SC1.DK4')
    bank = IlnkContainer.parse(archive)
    old = bank.blocks[52]
    clean = bytes.fromhex(packet['clean_block_hex'])
    group = mapping['groups'][0]
    edges = []
    for command in packet['all_current_commands']:
        at, word = command['offset'], command['word']
        if word in [0x100, 0x200, 0x300, 0x400]:
            span = struct.unpack_from('<H', old, at+2)[0]
            edges.append(dict(block=52, offset=at, word=word, span_field_offset=at+2,
                 source_span=span, unmatched_next_offset=at+4, matched_skip_target=at+4+span,
                 ancestor_0100_offsets=command['ancestor_0100_offsets'], source_operand_hex=old[at:at+4].hex()))
    choices = compile_choices(doc['typed_choice_records'])

    def run(current=old, source=clean, g=group, p=packet, rows=doc['records'], es=edges, labels=doc['typed_choice_records'], typed=choices):
        return reconstruct(current, source, g, p, rows, es, labels, typed)

    result = run()
    assert result == Path(group['target_block']).read_bytes()
    assert sha(result) == group['target_block_sha256']
    blocks = list(bank.blocks)
    blocks[52] = result
    rebuilt = IlnkContainer(blocks).to_bytes()
    assert rebuilt == Path(mapping['target_archive']).read_bytes()
    independent = read('work/analysis/Hodram_B52_independent_v8644/independent_reconstruction.json')
    assert sha(rebuilt) == independent['target_archive_sha256']
    reversed_bank = IlnkContainer.parse(rebuilt)
    reversed_bank.blocks[52] = old
    assert reversed_bank.to_bytes() == archive
    negatives = []

    def reject(label, field, value, original):
        assert value != original
        try:
            run(**{field: value})
        except ValueError as error:
            negatives.append(dict(label=label, field=field, original_sha256=sha(json.dumps(original, sort_keys=True, default=repr).encode()),
                changed_sha256=sha(json.dumps(value, sort_keys=True, default=repr).encode()), diagnostic=str(error), actual_changed_input=True))
        else:
            raise AssertionError('Changed reconstruction input accepted:' + label)

    reject('source-word-changed', 'current', old[:8] + bytes([old[8]^1]) + old[9:], old)
    reject('clean-final-byte-changed', 'source', clean[:-1] + bytes([clean[-1]^1]), clean)
    for index in range(3):
        for field in ['compiled_hex', 'source_complete_preamble_hex']:
            changed = deepcopy(doc['records'])
            changed[index][field] += '20'
            reject('speech:' + str(index) + ':' + field, 'rows', changed, doc['records'])
    for index in range(4):
        for field in ['new_offset', 'new_matched_skip_target', 'target_span']:
            changed = deepcopy(group)
            changed['relative_fixups'][index][field] += 2
            reject('relative:' + str(index) + ':' + field, 'g', changed, group)
    for index in range(2):
        changed = deepcopy(group)
        changed['choice_commands'][0]['label_references'][index]['relative_offset'] += 2
        reject('choice-internal-offset:' + str(index), 'g', changed, group)
    reject('choice-count-order', 'labels', list(reversed(doc['typed_choice_records'])), doc['typed_choice_records'])
    reject('typed-count-opcode', 'typed', bytes([choices[0]^1]) + choices[1:], choices)
    for index in [6, 13]:
        assert packet['all_current_commands'][index]['word'] == 0
        changed = deepcopy(packet)
        changed['all_current_commands'][index]['whole_command_hex'] = '00000040'
        reject('complete-end-word:' + str(index), 'p', changed, packet)
    assert len(negatives) == 26
    ROOT.mkdir(parents=True)
    save(ROOT / 'production_reconstruction.json', dict(target_block_sha256=sha(result), target_archive_sha256=sha(rebuilt),
         all14_commands3_preambles4_relatives_twochoices4_opaque_controls_bothdistinct_ends_preserved=True,
         complete_clean_current_block_andwhole_archive_inverses_pass=True,
         exact_independent_command_atom_reconstruction_matches=True, negative_cases=negatives,
         every_negative_is_actual_changed_input_andoriginal_semantic_guard_rejection=True,
         native_probes_actual_captures_andprevious_producers_not_replayed=True,
         no_ROM_registry_orcredit_mutation=True, full_goal_complete=False,
         evidence={str(p): sha(Path(p).read_bytes()) for p in [DOC, MAP, CURRENT, __file__, 'dk4tool/patch/hodram_B52_reconstruction_v1.py']}))
    print('B52 production reconstruction: exact block/archive/independent/inverses;', len(negatives), 'changed-input rejections. No ROM mutation or credit.')
