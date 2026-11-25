"""Record the user's concrete plaque-material approval and Online scope reply."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.record_memory_streams_v682 import copy
from scripts.review_current_plaques_v714 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/plaque_acceptance_v715')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V715 Plaque material accepted')
DOC = Path('docs/plaque_acceptance_v715_checkpoint.md')
KEY = 'user_acceptance_of_current18_plaque_texture_borders_and_Online_exclusion_confirmed_v715'


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'acceptance.json').exists()
    native = read('work/analysis/plaque_review_v714/current_plaque_review_proof.json')
    assert native['candidate_sha256'] == sha(ROM.read_bytes())
    rom = NdsImage.open(ROM)
    groups = read('translations/source_plaque_grain_v1.json')['files']
    assets = {g['file_path']: sha(rom.read_file(g['file_path'])) for g in groups}
    plan = read('work/analysis/direct_equipment_v270/runtime_plan.json')
    pool = bytes(MainCodeFile(rom.read_file('/__arm9__.bin'), BASE).sections[3].data)
    off = plan['tile_pointer'] - POOL
    tile = pool[off:off + 1408]
    assert len(tile) == 1408
    sheets = native['sheets']
    assert len(sheets) == 2
    for row in sheets:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    original = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in original}
    save(ROOT / 'audits_before.json', before)
    release_paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'))
    release = {str(p): sha(p.read_bytes()) for p in release_paths}
    entry = {'recorded_UTC': '2026-10-17 14:04:51 UTC',
        'approval_source': 'Direct human message and structured answers in the current thread.',
        'direct_message': 'The textures appear acceptable',
        'material_answer': 'Texture and borders look acceptable',
        'Online_scope_answer': 'Keep the earlier exclusion',
        'plaque_material_gate': 'closed-user-accepted',
        'accepted_review_candidate': str(ROM), 'candidate_sha256': native['candidate_sha256'],
        'accepted_comparison_sheets': sheets, 'accepted_static_asset_sha256': assets,
        'accepted_equipment_backing_tile_pointer': plan['tile_pointer'],
        'accepted_equipment_backing_tile_bytes': len(tile), 'accepted_equipment_backing_tile_sha256': sha(tile),
        'scope': 'Wood texture and borders of the17 static plaques and equipment-hint backing shown in V714; all18 overall audit entries stay open.',
        'all18_overall_audit_entries_remain_incomplete': True,
        'four_low_resolution_Online_screenshot_bodies_remain_excluded': True,
        'Online_files': ['/_pxl/online/Online24.pxl', '/_pxl/online/Online27.pxl',
                         '/_pxl/online/Online31.pxl', '/_pxl/online/Online33.pxl'],
        'existing_Online_edits_and_source_preserved': True,
        'concealed_background_pixels_remain_documented_reconstruction': True,
        'not_canonical_ROM_acceptance_or_guide_publication_approval': True,
        'other_graphics_contexts_restoration_model_gaps_and_final_acceptance_remain_open': True,
        'older_record_based_checks_retained_after_full_goal': True,
        'release_hashes_unchanged': release, 'full_goal_complete': False}
    save(ROOT / 'acceptance.json', entry)
    for name, scope in original.items():
        path = Path('translations') / name
        current = read(path)
        assert current == before[name]
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        current[KEY] = {'documentation': str(DOC), 'record': str(ROOT / 'acceptance.json'),
            'record_sha256': sha((ROOT / 'acceptance.json').read_bytes()), **entry}
        save(path, current)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V715: user accepts current plaque textures and retains Online exclusion'
    text = ('The user explicitly accepts the V714 comparison sheets: "The textures appear acceptable" '
        'and "Texture and borders look acceptable." The current17 static plaque and equipment-backing '
        'texture/border material gate is closed, bound to both sheet hashes,two exact atlas files and '
        'the1408-byte backing tile. This does not promote V712 to the canonical ROM or approve guide '
        'publication. All18 overall plaque entries remain incomplete and22 historical objects exact. '
        'The user also answers "Keep the earlier exclusion": Online24/27/31/33 low-resolution bodies '
        'stay excluded,existing edits retained. Source reconstruction uncertainty remains documented. '
        'Other native contexts,legacy/comics,restoration,model gaps and final acceptance stay open; '
        'older record checks retained. No ROM/patch/registry/pointer changes. Full goal active. '
        'See [V715 acceptance](plaque_acceptance_v715_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*ROOT.glob('*.json'), Path(__file__), DOC):
        copy(path, ARCHIVE / path.name)
    for row in sheets:
        copy(row['path'], ARCHIVE / Path(row['path']).name)
    for name, scope in original.items():
        current = read(Path('translations') / name)
        current.pop(KEY)
        assert current == before[name]
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
    assert all(sha(Path(p).read_bytes()) == digest for p, digest in release.items())
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'human_material_acceptance_bound_to_current_artifacts': True,
        'Online_body_exclusion_reconfirmed': True, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    print('V715 user plaque-material approval and four Online exclusions recorded;18 overall entries still open; ROM exact.', flush=True)


if __name__ == '__main__':
    main()
