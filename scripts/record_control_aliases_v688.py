"""Retain bounded alias evidence without claiming missing gameplay contexts."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.trace_control_aliases_v688 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V688 Control owner aliases')
DOC = Path('docs/control_aliases_v688_checkpoint.md')
KEY = 'bounded_control_aliases_exact20_byte_owners100_native_loads_no_new_parent_v688'
SCRIPTS = tuple('scripts/' + p for p in (
    'trace_control_aliases_v688.py', 'verify_control_owners_v688.py',
    'verify_control_aliases_v688.py', 'record_control_aliases_v688.py',
    'verify_control_aliases_archive_v688.py'))


def main():
    pre = read(ROOT / 'preflight.json')
    pp = ROOT / 'proof.json'
    proof = read(pp)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_control_aliases_v688.py').read_bytes())
    assert proof['no_additional_computed_owner_lead_in_supported_bounded_ARM_constant_flow']
    assert len(proof['all100_source_current_literal_load_instructions_verified']) == 100
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': 'out/all_routes_combined_v685_candidate.nds',
        'candidate_sha256': pre['release_hashes']['out/all_routes_combined_v685_candidate.nds'],
        'two_original_complete_initializers2864_distinct_instructions_each_no_bridges': True,
        'exact20_byte_owners_neighbor_plate4016_and_Marker_are_separate_resources': True,
        'all100_known_original_current_literal_loads_native_verified': True,
        'bounded_constant_arithmetic_and_table_analysis_finds_no_new_alias_parent': True,
        'actual_dynamic_Thumb_cross_call_and_other_readers_not_globally_excluded': True,
        'initial24_byte_owner_assumption_and_register_alias_failure_retained': True,
        'six_actual_control_contexts_still_open_no_new_rendering_or_global_nonuse_credit': True,
        'all18_plaques_incomplete22_historical_requirements_exact_other_graphics_open': True,
        'ROM_manifest_patch_registry_canonical_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V688: bounded control aliases and exact resource-owner boundaries'
    addition = (
        'Bounded ARM constant arithmetic and mapped pointer-table analysis '
        'includes staged and verified live POOL views. It finds only the known '
        'two Confirm and48 Frame owner loads per version;100 original/current '
        'loads execute with RAM/other registers intact. Two complete original '
        'initializers execute2864 distinct instructions each without bridges. '
        'Exact20-byte objects exclude the separate plate4016 and Marker owners; '
        'the initial24-byte window and register-alias diagnostics remain retained. '
        'No new control parent is found. Thumb,dynamic aliases,cross-call/branch '
        'flows and other readers remain outside this bounded result. Do not repeat '
        'this owner census or count adjacent-resource rendering as control credit. '
        'Six contexts,all18 plaques and22 original scopes remain open/exact; '
        'ROM/manifest/patch/registry/pointers unchanged. Evidence on E,no new '
        'screenshot or guide credit. See '
        '[V688 checkpoint](control_aliases_v688_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for p in (DOC, *map(Path, SCRIPTS)):
        copy(p, ARCHIVE / 'sources' / p.name)
    for p in ROOT.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'analysis' / p.relative_to(ROOT))
    save(ARCHIVE / 'provenance.json', {
        'scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'full_goal_complete': False})
    print('V688 bounded alias evidence recorded on E; no new gameplay context claimed.', flush=True)


if __name__ == '__main__':
    main()
