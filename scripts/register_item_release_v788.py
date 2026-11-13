"""Register the native-reviewed experimental layer; keep frozen inputs intact."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import item_diplomacy_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_item_diplomacy_v784 import CURRENT
from scripts.review_item_diplomacy_v784 import MANUSCRIPT as DRAFT
from scripts.verify_village_wrap_v608 import read, save

ROOT = owned.ROOT
MANUSCRIPT = Path('translations/item_diplomacy_editorial_manuscript_v2.json')
CONFIG = Path('translations/item_diplomacy_editorial_release_v1.json')


def main():
    assert not CONFIG.exists() and not MANUSCRIPT.exists()
    plan, layout = read(ROOT/'prospective_common_repack.json'), read(ROOT/'production_layout/verification.json')
    assert layout['native_layouts'] == 2774 and not layout['findings']
    assert len(layout['all76_complete_native_font_planes_exact_to_visually_reviewed_images']) == 76
    assert layout['manuscript_sha256'] == sha(DRAFT.read_bytes())
    manuscript = deepcopy(read(DRAFT))
    for row in manuscript['records']:
        assert all(row['review'][g] for g in ('source', 'context', 'localization', 'naturalness'))
        assert not row['review']['formatting']
        row['review']['formatting'] = True
        row['status'] = 'native-reviewed-actual-revised-scenes-and-full-eligibility-pending'
        row['context'] += (' V786 source/captured Guild role5 resolves the regional Guildmaster; V788 original wrappers verify actual First Mate/Purser actors,portrait core,argument order and template binding. Native layout/font checks pass; representative revised in-game scenes and full branch eligibility remain pending.')
    manuscript.update({'status': 'native-reviewed-registered-experimental-actual-scenes-pending',
        'required_letter_type_localization': 'work/analysis/item_diplomacy_runtime_v785/letter_type_localization_DRAFT_v2.json',
        'reviewed_research_manuscript': str(DRAFT), 'reviewed_research_manuscript_sha256': sha(DRAFT.read_bytes()),
        'consumer_routing_proof': str(ROOT/'consumer_routing.json'),
        'production_layout_proof': str(ROOT/'production_layout/verification.json'),
        'remaining_gates': ['Actual revised item buy/sell/bargain and diplomacy scenes',
                           'Complete diplomatic branch eligibility and document lifecycle',
                           'Actual SDK/GPU selector menu and remaining name consumers', 'Ordinary cold-boot/startup regression'],
        'whole_batch_completion_credit': False})
    save(MANUSCRIPT, manuscript)
    rom = NdsImage.open(CURRENT)
    c, a, proof = owned.transform(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), manuscript)
    assert c == (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    assert a == (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    save(ROOT/'native_integration.json', {'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a),
        'proof': proof, 'actual_gameplay_pending': True})
    paths = [Path(p) for p in (
        'dk4tool/patch/item_diplomacy_editorial.py', 'dk4tool/patch/item_diplomacy_runtime.py',
        'dk4tool/patch/tavern_schemes_editorial.py', 'dk4tool/script/common_message_table.py',
        'scripts/prepare_item_common_v788.py', 'scripts/prepare_recruitment_common_v772.py',
        'scripts/verify_item_consumers_v788.py', 'scripts/verify_item_copies_v788.py',
        'scripts/probe_item_production_v788.py', str(DRAFT),
        'work/analysis/item_diplomacy_runtime_v785/runtime_plan.json',
        'work/analysis/item_diplomacy_runtime_v785/scope_proof.json',
        'work/analysis/item_diplomacy_runtime_v785/status_contracts.json',
        'work/analysis/item_diplomacy_runtime_v785/source_tail_ownership.json',
        'work/analysis/item_diplomacy_runtime_v785/private_reference_census.json',
        'work/analysis/item_diplomacy_runtime_v785/Thumb_ISA_audit.json',
        'work/analysis/item_diplomacy_runtime_v785/type_phrase_storage_research.json',
        'work/analysis/item_diplomacy_runtime_v785/letter_type_localization_DRAFT_v2.json',
        'work/analysis/item_diplomacy_context_v786/nominal_provider_research.json',
        'work/analysis/item_diplomacy_context_v786/Guild_context_verification.json',
        'work/analysis/item_diplomacy_context_v786/provider_layouts/verification.json',
        'work/analysis/item_diplomacy_context_v786/provider_layouts/visual_review.json',
        'work/analysis/scheme_name_width_v787/native_width_verification.json',
        'work/analysis/scheme_name_width_v787/selector_entry_closure.json',
        'work/analysis/scheme_name_width_v787/visual_review.json')]
    paths += [ROOT/p for p in ('prospective_common_repack.json', 'consumer_routing.json',
        'production_layout/verification.json', 'production_layout/effective_format_case.py', 'native_integration.json')]
    paths += [ROOT/f'native_copies/native_copies_block_{n:02d}.json' for n in range(41)]
    # Preserve all existing stage pins. A versioned, exact-directory reader in
    # this new module eliminates the historical need to rewrite old configs.
    registry_path = Path('translations/release_stack.json')
    registry = read(registry_path)
    assert 'all-routes-unified-v788' not in registry['profiles'] and len(registry['accepted_layers']) == 114
    inherited = deepcopy(registry['profiles']['all-routes-unified-v783'])
    frozen = {'dk4tool/script/common_message_table.py': sha(Path('dk4tool/script/common_message_table.py').read_bytes())}
    for value in inherited.values():
        if isinstance(value, str) and value.endswith('.json') and Path(value).exists():
            cfg = read(value)
            frozen[value] = sha(Path(value).read_bytes())
            for p, h in cfg.get('dependencies', {}).items():
                assert sha(Path(p).read_bytes()) == h, p
                frozen[p] = h
    save(ROOT/'release_stack_before_v788.json', registry)
    save(ROOT/'frozen_prior_dependencies.json', frozen)
    save(CONFIG, {'format': 'dk4-item-diplomacy-editorial-v1',
        'source_common_sha256': sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'source_arm9_sha256': sha(rom.read_file('/__arm9__.bin')),
        'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'dependencies': {str(p): sha(p.read_bytes()) for p in paths}})
    profile = deepcopy(inherited)
    profile.update({'item_diplomacy_editorial': str(CONFIG), 'status': 'experimental',
        'description': 'V783 full stack plus76 native-reviewed item/diplomacy paragraphs, six full nominal names and24-cell shared name width; actual revised scenes and eligibility remain pending.'})
    registry['profiles']['all-routes-unified-v788'] = profile
    save(registry_path, registry)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), CONFIG)[:2] == (c, a)
    print('V788 experimental layer registered; frozen parser and all prior stage inputs preserved. Actual scenes remain pending.', flush=True)


if __name__ == '__main__':
    main()
