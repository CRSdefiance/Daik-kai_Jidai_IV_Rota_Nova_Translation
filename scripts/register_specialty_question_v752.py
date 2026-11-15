"""Register a hash-pinned, gameplay-pending specialty question candidate."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.specialty_question_editorial import transform
from dk4tool.rom.nds import NdsImage
from scripts.prepare_specialty_question_v752 import MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    rom = NdsImage.open('out/all_routes_combined_v751_candidate.nds')
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    target_common, target_arm, proof = transform(common, arm, read(MANUSCRIPT))
    (ROOT / 'research_COMMON.bin').write_bytes(target_common)
    (ROOT / 'integrated_research_ARM9.bin').write_bytes(target_arm)
    save(ROOT / 'repack_proof.json', proof)
    config = Path('translations/specialty_question_editorial_release_v1.json')
    assert not config.exists()
    save(config, {'format': 'dk4-specialty-question-editorial-v1',
        'source_common_sha256': sha(common), 'source_arm9_sha256': sha(arm),
        'target_common_sha256': sha(target_common), 'target_arm9_sha256': sha(target_arm),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in (Path('dk4tool/patch/specialty_question_editorial.py'),
            Path('dk4tool/script/common_native_repack.py'), ROOT / 'native_review.json', ROOT / 'runtime_names.json')}})
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v752' not in registry['profiles']
    save(ROOT / 'release_stack_before_V752.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v751'])
    profile.update({'specialty_question_editorial': str(config), 'status': 'experimental',
        'description': 'Complete V751 plus number-neutral specialty question742 and original-Yes/No-only runtime wrap. Gameplay verification pending;730 and broad editorial inventory remain open.'})
    registry['profiles']['all-routes-unified-v752'] = profile
    save(registry_path, registry)
    print('Registered V752 experimental specialty question; gameplay verification pending.', flush=True)


if __name__ == '__main__':
    main()
