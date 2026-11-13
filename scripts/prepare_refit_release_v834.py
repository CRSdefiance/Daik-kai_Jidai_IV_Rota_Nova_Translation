"""Verify complete native copies and register the complete V834 stack."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import CONFIG, plan
from dk4tool.patch.refit_help_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_dialogue_v834')
MANUSCRIPT = Path('translations/refit_dialogue_editorial_manuscript_v2.json')
OLD = Path('out/all_routes_combined_v831_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not Path(CONFIG).exists()
    registry_path = Path('translations/release_stack.json')
    save(ROOT / 'registry_before.json', read(registry_path))
    rom = NdsImage.open(OLD)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    c, a, proof = plan(common, arm, read(MANUSCRIPT))
    (ROOT / 'target_COMMON.bin').write_bytes(c)
    (ROOT / 'target_ARM9.bin').write_bytes(a)
    save(ROOT / 'repack_plan.json', proof)
    print('Refit dialogue repack:', proof['repacked_block_range'], 'existing native IDs:', len(proof['repacked_native_IDs']), flush=True)
    expected = {e.message_id: e.text for e in current_entries(common, arm)}
    expected.update({r['message_id']: b' ' + r['english'].encode('ascii') for r in read(MANUSCRIPT)['records']})
    before_factory = loader.machine_for
    loader.machine_for = arm946_machine
    cases = []
    try:
        for number in range(3668):
            outputs = [loader.warm_copy(a, c, number, expected[number], cold_cache=cold) for cold in (False, True)]
            cases.append({'message_id': number, 'text_sha256': sha(expected[number]),
                          'warm_and_cold_complete_native_copy_and_guards_pass': True,
                          'warm_copy_bytes': outputs[0]['copied_bytes'],
                          'cold_host_file_contract_reads': outputs[1]['host_file_contract_reads']})
            if number % 500 == 0:
                print('Native warm/cold:', number, '/3668', flush=True)
    finally:
        loader.machine_for = before_factory
    copies = ROOT / 'native_copy_proof.json'
    save(copies, {'COMMON_sha256': sha(c), 'ARM9_sha256': sha(a),
                  'all3668_native_IDs_warm_and_cold7336_complete_copies': cases,
                  'native_loader_cache_and_aligned_copy_execute': True,
                  'host_ILNK_read_bridge_not_hardware_or_gameplay': True,
                  'producer_sha256': sha(Path(__file__).read_bytes())})
    research = Path('work/analysis/refit_dialogue_v833')
    deps = [Path('dk4tool/patch/refit_dialogue_editorial.py'), Path('scripts/refit_dialogue_runtime_v833.py'),
            Path('scripts/prepare_item_common_v788.py'), Path('scripts/prepare_recruitment_common_v772.py'),
            copies, research / 'native_runtime_verification.json', research / 'native_font_proof.json',
            research / 'quantity_equivalence.json', research / 'modal_equivalence.json',
            research / 'status_phrase_contracts.json', research / 'storage_and_quantity_closure.json',
            research / 'research_scope/scope_proof.json', research / 'scope_delta.json']
    config = {'format': 'dk4-refit-dialogue-editorial-v1', 'source_common_sha256': sha(common),
              'source_arm9_sha256': sha(arm), 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
              'directory_sha256': proof['directory_sha256'], 'manuscript': str(MANUSCRIPT),
              'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'native_copy_proof': str(copies),
              'dependencies': {str(p): sha(p.read_bytes()) for p in deps}}
    save(CONFIG, config)
    registry = read(registry_path)
    assert registry == read(ROOT / 'registry_before.json') and 'all-routes-unified-v834' not in registry['profiles']
    profile = deepcopy(registry['profiles']['all-routes-unified-v831'])
    profile.update(refit_dialogue_editorial=CONFIG, status='experimental',
                   description='Complete V831 stack plus12 natural Refit dialogue entries,exact selector compaction and scoped day/days unit.',
                   note='Preserve all earlier profiles and source locks. Native layout/copy/scope/ABI gates pass;actual scene evidence is recorded separately before handoff. Canonical promotion requires explicit human acceptance.')
    registry['profiles']['all-routes-unified-v834'] = profile
    save(registry_path, registry)
    print('All7336 native copies pass;V834 full profile registered. Build and actual revised scenes remain.', flush=True)


if __name__ == '__main__':
    main()
