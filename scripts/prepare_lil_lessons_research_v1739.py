"""Two lesson blocks in a full V1711 copy; research only, no release registration."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_lessons_research_v1739')
PARENT = Path('out/all_routes_combined_v1711_candidate.nds')
ROM = ROOT / 'lil_lessons_V1711_derived_RESEARCH_ONLY.nds'

if __name__ == '__main__':
    assert not ROOT.exists()
    research = read('work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json')
    display = read('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
    choices = read('work/analysis/lil_lesson_choice_ui_v1735/original_choice_VM_geometry_and_native_pixels.json')
    digest = sha(PARENT.read_bytes())
    assert digest == research['candidate_sha256'] == display['candidate_sha256'] == choices['candidate_sha256']
    assert digest == read(PARENT.with_suffix('.manifest.json'))['candidate_sha256']
    assert display['all9_reviewed_FE_full_actual_context_native_planes_pass']
    assert choices['all12_original_selection_cancel_VM_cases_and_source_extents_verified']
    parent, image = NdsImage.open(PARENT), NdsImage.open(PARENT)
    archive = IlnkContainer.parse(parent.read_file('/data/SC2.DK4'))
    changes = []
    for spec in research['blocks']:
        number = spec['block']
        assert sha(archive.blocks[number]) == spec['source_block_sha256']
        target = Path(spec['research_block']).read_bytes()
        assert sha(target) == spec['research_block_sha256'] and len(target) <= 0x2400
        archive.blocks[number] = target
        changes.append({'block': number, 'old_bytes': spec['source_bytes'], 'new_bytes': len(target),
                        'old_sha256': spec['source_block_sha256'], 'new_sha256': sha(target)})
    assert sorted(r['block'] for r in changes) == [23, 120]
    target = archive.to_bytes()
    assert len(target) - len(parent.read_file('/data/SC2.DK4')) == 516
    image.replace_file('/data/SC2.DK4', target)
    ROOT.mkdir(parents=True)
    image.save(ROM)
    final = NdsImage.open(ROM)
    before = {p: b for _, p, b in parent.iter_files()}
    after = {p: b for _, p, b in final.iter_files()}
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/data/SC2.DK4']
    assert dict(parent.iter_components()) == dict(final.iter_components())
    original = IlnkContainer.parse(before['/data/SC2.DK4']).blocks
    revised = IlnkContainer.parse(after['/data/SC2.DK4']).blocks
    assert len(original) == len(revised) == 336
    assert [i for i, (a, b) in enumerate(zip(original, revised, strict=True)) if a != b] == [23, 120]
    save(ROOT / 'research_image_receipt.json', {
        'parent': str(PARENT), 'parent_sha256': digest, 'research_ROM': str(ROM),
        'research_ROM_sha256': sha(ROM.read_bytes()), 'SC2_sha256': sha(target),
        'ARM9_sha256': sha(final.read_file('/__arm9__.bin')), 'changed_blocks': changes,
        'only_changed_file': '/data/SC2.DK4', 'all334_other_SC2_blocks_exact': True,
        'all_other_files_components_code_fonts_art_and_staged_payload_exact': True,
        'external_reference_approval_and_actual_revised_gameplay_pending': True,
        'registered_candidate': False, 'not_for_user_handoff_or_new_parent': True,
        'relocation_research': 'work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    (ROOT / 'RESEARCH_ONLY.txt').write_text(
        'V1711-derived research only. Only SC2 B23/B120 changed. Not registered, not a release or parent.\n', encoding='utf-8')
    print({'research_ROM': str(ROM), 'sha256': sha(ROM.read_bytes()), 'changed_blocks': [23, 120]})
