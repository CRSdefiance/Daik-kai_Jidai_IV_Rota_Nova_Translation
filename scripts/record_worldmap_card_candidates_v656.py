"""Archive typed terrain ownership without claiming ordinary card reachability."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/worldmap_card_candidates_v656')
DOC = Path('docs/worldmap_card_candidates_v656_checkpoint.md')
KEY = 'all16_WORLDMAP_village_card_byte_candidates_owned_by_original_compressed_terrain_pages_v656'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V656 Terrain byte candidates')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    script = Path('scripts/trace_worldmap_card_candidates_v656.py')
    assert proof['script_sha256'] == sha(script.read_bytes())
    assert len(proof['all16_original_byte_candidates_have_exact_compressed_page_owners']) == 16
    assert len(proof['twenty_original_pathname_open_prefixes']) == 20
    assert len(proof['fiftytwo_original_native_page_decodes_clean_current']) == 26
    assert proof['all64_candidate_bytes_read_as_compressed_input_by_original_ITCM_decoder']
    assert not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, script, Path(__file__), *ROOT.glob('*.json'), *ROOT.glob('*.txt')]:
        checked_copy(source, ARCHIVE / source.name)
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'all10_archive_blocks2500_page_headers_and1037_contiguous_compressed_streams_typed': True,
        'all16_village_card_byte_candidates_are_wholly_in_compressed_terrain_streams': True,
        'all64_candidate_bytes_read_by_original_decompressor_not_script_dispatch': True,
        'fiftytwo_full_clean_current_2500_byte_page_decodes_and_ABI_guards_exact': True,
        'ten_uniform_pages_match_independent1250_word_model': True,
        'twenty_original_native_filename_open_prefixes_stop_before_filesystem': True,
        'no_new_emulator_GPU_ordinary_village_trigger_or_global_unused_art_claim': True,
        'eight_village_card_ordinary_usage_and_other_readers_remain_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_manifest_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V656: village-card byte candidates classified through the original terrain reader'
    addition = ('All16 V589 WorldMap byte candidates are wholly owned by compressed terrain '
        'streams,not established script records. All10 blocks/2500 page headers/1037 '
        'contiguous streams are typed. Original pathname prefixes identify '
        'DATA/WORLDMAP.DK4;20 clean/current cases stop before Open. Original page '
        'selection and decompression execute52 full clean/current cases for16 '
        'candidate pages plus10 uniform controls. All64 candidate bytes are read '
        'by the original flag/literal/bit readers;whole2500-byte outputs and ABI '
        'guards pass. Uniform controls independently match1250 words each. This '
        'removes a concrete false trigger lead,not global unused-art proof or '
        'ordinary village-card reachability. No ROM/patch/registry/pointer change; '
        'all18 plaques incomplete and22 scopes exact. Evidence on E;full goal active. '
        'See [V656 checkpoint](worldmap_card_candidates_v656_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'no_screenshot_or_gameplay_or_guide_credit': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in (script, Path(__file__))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V656 typed candidate evidence archived; three audits/four progress documents updated; full scope remains active.')


if __name__ == '__main__':
    main()
