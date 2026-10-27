"""Persist source-locked name allocation and reviewed native evidence."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.persistent_name_release import (
    BASE,
    HEAP_LOW,
    POOL,
    SOURCE,
    TARGET,
    apply_release,
)
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    source = NdsImage.open('out/all_routes_combined_v147_candidate.nds').read_file('/__arm9__.bin')
    target = Path('work/analysis/persistent_name_section_arm9.bin').read_bytes()
    if sha(source) != SOURCE or sha(target) != TARGET:
        raise ValueError('Exact V147 and verified persistent research required')
    proofs = {key: read('work/analysis/' + name + '.json') for key, name in {
        'persistent': 'persistent_name_section_proof',
        'consumers': 'persistent_name_consumers_proof',
        'pixels': 'persistent_square_shopkeeper_paired_name_context_proof',
        'references': 'persistent_name_reference_proof',
    }.items()}
    if any(proof['research_sha256'] != TARGET for proof in proofs.values()):
        raise ValueError('All native evidence must describe identical reserved bytes')
    visual = proofs['pixels']['native_ink_visual_review']
    if (visual['panels_reviewed'] != 10 or visual['rows_reviewed'] != 20
            or visual['complete_leading_and_final_glyphs'] is not True
            or visual['no_clipping_or_row_overlap'] is not True):
        raise ValueError('Complete reviewed native ink required')
    proofs['native_sheet_sha256'] = sha(Path(visual['sheet']).read_bytes())
    proofs['research_sha256'] = TARGET
    proofs['canonical_acceptance'] = False
    proofs['physical_gameplay_verified'] = False
    evidence = 'translations/persistent_name_native_review_v1.json'
    write(evidence, proofs)
    shop = read('work/analysis/joint_square_shopkeeper_native_proof.json')
    moves = [{
        'field': move['field'], 'source_hex': source[move['field']:move['field'] + 4].hex(),
        'runtime_pointer': struct.unpack_from('<I', target, move['field'])[0], 'text': move['text'],
    } for move in proofs['persistent']['placement']['moves']]
    allocation = 'translations/persistent_name_allocation_v1.json'
    write(allocation, {
        'format': 'dk4-persistent-name-allocation-v1',
        'runtime_base': POOL, 'heap_low': HEAP_LOW, 'used_bytes': 1480,
        'payload_hex': bytes(MainCodeFile(target, BASE).sections[3].data).hex(),
        'moves': moves,
        'shopkeeper': {
            'source_span': [0x15D088, 0x15D0A0],
            'source_hex': source[0x15D088:0x15D0A0].hex(),
            'references': [{'field': ref['field'],
                            'source_hex': source[ref['field']:ref['field'] + 4].hex()}
                           for ref in shop['references']],
        },
    })
    manuscripts = ['translations/square_shopkeeper_names_manuscript_v1.json',
                   'translations/shared_square_shopkeeper_name_review_v1.json']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for path in manuscripts:
        document = read(path)
        document['encoder'] = 'dialogue-fixed-v1'
        document['review_gates'] = ['source', 'context', 'localization', 'naturalness', 'formatting']
        document['review_evidence'] = evidence
        for row in document['records']:
            if 'pointer_field' in row:
                pointer = struct.unpack_from('<I', clean, row['pointer_field'])[0]
                if pointer != row['source_pointer']:
                    raise ValueError('Clean role pointer differs')
                at = pointer - BASE
            else:
                at = row['offset']
                if clean[at:at + row['capacity']] != bytes.fromhex(row['source_hex']):
                    raise ValueError('Clean shopkeeper owner differs')
            if clean[at:].split(b'\0', 1)[0].decode('cp932') != row['japanese']:
                raise ValueError('Clean Japanese role differs')
            row['review']['formatting'] = True
            row['localization_note'] = (
                'Complete natural American English retains both location and role. '
                'Twenty native paired-name rasters and ten inspected panels preserve '
                'all leading/final glyphs without clipping or overlap. Physical gameplay pending.')
        write(path, document)
    config = 'translations/persistent_name_release_v1.json'
    write(config, {'format': 'dk4-persistent-name-release-v1',
                   'source_arm9_sha256': SOURCE, 'target_arm9_sha256': TARGET,
                   'allocation': allocation, 'native_review': evidence, 'manuscripts': manuscripts,
                   'dependencies': {p: sha(Path(p).read_bytes())
                                    for p in [allocation, evidence, *manuscripts]}})
    saved, report = apply_release(source, config)
    if saved != target:
        raise ValueError('Production differs from verified native research')
    write('work/analysis/persistent_name_release_preparation.json', report)
    print('Strict persistent-name release prepared; combined ROM integration pending.')


if __name__ == '__main__':
    main()
