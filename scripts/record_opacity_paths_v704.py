"""Record connected opacity leads without claiming the original comic viewer."""

from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.record_memory_streams_v682 import copy
from scripts.run_room_gender_v694 import ROM
from scripts.verify_opacity_paths_v704 import ROOT, SNAPSHOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V704 Original opacity paths')
DOC = Path('docs/opacity_paths_v704_checkpoint.md')
KEY = 'original_complete_portrait_palette_import_and_five_in_place_half_blends_not_raw_comic_import_v704'
SOURCES = ('scripts/scan_opacity_paths_v704.py', 'scripts/verify_opacity_paths_v704.py',
    'scripts/record_opacity_paths_v704.py', 'scripts/verify_opacity_archive_v704.py',
    'scripts/probe_button_prompt_native.py', 'scripts/trace_control_aliases_v688.py')
REFERENCES = ('work/analysis/titlemap_v221/native_proof.json',
    'work/analysis/legacy_descriptor_v547/descriptor_proof.json',
    'docs/titlemap_source_classification_v221.md', 'docs/legacy_descriptor_v547_checkpoint.md')


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'native_proof.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_opacity_paths_v704.py').read_bytes())
    assert len(proof['original_in_place_half_blend']['cases']) == 5
    assert proof['portrait_palette_initializer']['actual_changed_highbits'] == 227
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    # Retain the exact source of the one register-mask lead; this is disassembly,
    # not proof that the function executes in an ordinary comic scene.
    u = machine(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    original = machine(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    lo, hi = 0x020F4120, 0x020F4260
    data = bytes(u.mem_read(lo, hi - lo))
    assert data == bytes(original.mem_read(lo, hi - lo))
    save(ROOT / 'register_mask_context.json', {'start': lo, 'end': hi, 'code_sha256': sha(data),
        'current_clean_exact': True, 'disassembly': [
            {'PC': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
            for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(data, lo)],
        'structured_field_packing_stride8_writes_not_a_proven_raw_import': True})
    save(ROOT / 'related_evidence.json', {'existing_source_bound_evidence_not_repeated_as_new_coverage': {
        path: sha(Path(path).read_bytes()) for path in REFERENCES},
        'no_new_GPU_or_ordinary_comic_scene_credit': True})
    entry = {'documentation': str(DOC), 'proof': str(ROOT / 'native_proof.json'),
        'proof_sha256': sha((ROOT / 'native_proof.json').read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'full_original_47B18_portrait_and_item_palette_initializer_return_ABI_source_IO_and16_descriptors_pass': True,
        'all256_palette_low15_RGB_preserved227_actual_opacity_bit_changes': True,
        'five_original_half_blends983040_framebuffer_bytes_and_whole_outside_RAM_exact': True,
        'half_blend_changes_RGB_and_is_not_a_raw_image_opacity_import': True,
        'TITLEMAP_conversion_is_prior_V221_coverage_not_a_new_comic_consumer': True,
        'bounded_immediate_word_literal_and_byte_mask_leads_not_global_import_exclusion': True,
        'previous_goal_turn_status_only_no_progress_revalidated_native_work_resumed': True,
        'original_comic_import_viewer_normal_geometry_readability_and_restoration_open': True,
        'all18_plaques_incomplete22_historical_requirements_exact': True,
        'production_ROM_patch_manifest_registry_canonical_release_pointers_unchanged': True,
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
    heading = '## V704: original portrait opacity import and framebuffer half blend'
    addition = (
        'The previous status-only goal turn made no progress. Complete original47B18 '
        'now returns with exact ABI using real V703 baseline RAM and only ROM-backed '
        'SDK filesystem bridges. Actual CMMNIMG.000 and item.pxl reads bind all256 '
        'portrait palette colours,227 opacity changes and16 item descriptors; '
        'all239 native words are clean-original and whole main-RAM changes stay '
        'inside declared buffers/filesystem globals. Five complete original overlay '
        'half blends compare983040 framebuffer bytes and all outside RAM/guards; '
        '49296 pixels reject an opacity-only model. The routine changes existing '
        'RGB,not an external image import. TITLEMAP conversion is existing V221 '
        'coverage. Bounded word/literal/byte-mask searches do not establish the '
        'raw-comic importer or global non-use. Original comic viewer,normal scenes,'
        'geometry/readability/restoration remain open. No art/alpha/ROM/patch/'
        'registry/pointer changes,no guide claim. All18 plaques incomplete,'
        '22 historical scopes exact;full goal active. See '
        '[V704 checkpoint](opacity_paths_v704_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC, *map(Path, REFERENCES)):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': {str(SNAPSHOT): sha(SNAPSHOT.read_bytes())},
        'source_bound_native_contracts_not_normal_comic_scene_or_global_opacity_fix': True,
        'full_goal_complete': False})
    print('V704 opacity leads recorded and archived; original comic import and full goal remain open.', flush=True)


if __name__ == '__main__':
    main()
