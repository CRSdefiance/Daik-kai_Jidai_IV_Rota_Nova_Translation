"""Register the complete V685 stack plus the original Captain filter caption."""

import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.navigator_captain_filter import transform
from dk4tool.rom.nds import NdsImage
from scripts.trace_deck_gender_v692 import ROOT
from scripts.verify_village_wrap_v608 import read, save


def main():
    assert not (ROOT / 'build_preflight.json').exists()
    old = Path('out/all_routes_combined_v685_candidate.nds')
    registry = Path('translations/release_stack.json')
    stack = read(registry)
    original_registry = ROOT / 'source_release_stack.json'
    original_registry.write_bytes(registry.read_bytes())
    source = NdsImage.open(old).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    target, plan = transform(source, clean)
    config = Path('translations/navigator_captain_filter_v1.json')
    save(config, {'format': 'dk4-navigator-captain-filter-v1',
        'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
        'Japanese': '艦長', 'English': 'Captain', 'localization_reason':
        'The original navigator filter selects ship captains. Captain matches the existing role glossary; no rank or character identity is changed.',
        'source_slot_hex': source[0x14F33C:0x14F344].hex(),
        'original_source_and_enabled_descriptor_preserved_except_caption_bytes': True,
        'status': 'experimental'})
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v685'])
    profile['description'] = 'Experimental full V685 stack plus the source-verified navigator Captain filter caption in its original eight-byte allocation.'
    profile['navigator_captain_filter'] = str(config)
    stack['profiles']['all-routes-unified-v692'] = profile
    save(ROOT / 'build_preflight.json', {'source_candidate': str(old), 'source_candidate_sha256': sha(old.read_bytes()),
        'source_registry': str(original_registry), 'source_registry_sha256': sha(original_registry.read_bytes()),
        'source_profile': 'all-routes-unified-v685', 'profile': 'all-routes-unified-v692',
        'config': str(config), 'config_sha256': sha(config.read_bytes()), 'repair_plan': plan,
        'all_original_audits_before': read(ROOT / 'preflight.json')['all_original_audits_before'],
        'canonical_sha256': stack['canonical_baseline']['sha256'],
        'initial_observer_failure': 'Original return target may be reached without entering the gender helper; initial observer asserted instead of classifying that original bypass. No game state was written. Failed run/events retained; no actual gender-helper coverage claimed.',
        'previous_status_turn_no_progress_followed_by_new_actual_Japanese_caption_discovery': True,
        'full_goal_complete': False})
    save(registry, stack)
    save(ROOT / 'registration.json', {'registry_sha256': sha(registry.read_bytes()),
        'config_sha256': sha(config.read_bytes()), 'module_sha256': sha(Path('dk4tool/patch/navigator_captain_filter.py').read_bytes()),
        'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),
        'all_existing_profiles_and_accepted_layers_retained': True, 'full_goal_complete': False})
    print('V692 full V685 stack plus source-locked Captain filter registered.', flush=True)


if __name__ == '__main__':
    main()
