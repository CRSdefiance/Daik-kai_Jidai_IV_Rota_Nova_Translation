"""Bind the directly viewed two-page correction and pin its Help-only research image."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_fleet66_amendment_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/HELP66_Command_amendment_20261104')
OUT = ROOT / 'preview_qualification_v1'

if __name__ == '__main__':
    assert not OUT.exists()
    plan_path, native_path = ROOT / 'automatic_plans_v1.json', ROOT / 'native_pages_v1/native_help_pages.json'
    plan, native = map(load, [plan_path, native_path])
    assert len(plan['pages']) == native['native_pages'] == 2 and native['complete_articles'] == 1
    assert native['plan_sha256'] == sha(plan_path.read_bytes()) and len(native['review_sheets']) == 1
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact']
    for sheet in native['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    doc = load(plan['manuscript'])
    parent, clean, base = [NdsImage.open(p) for p in [plan['current_ROM'], 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds']]
    assert sha(Path(plan['current_ROM']).read_bytes()) == plan['current_ROM_sha256']
    file = doc['file_path']
    args = [clean.read_file(file), base.read_file(file), parent.read_file(file)]
    resource, compiled = plan_articles(doc, *args, require_formatting=False)
    assert resource == Path(plan['research_resource']).read_bytes()
    assert compiled['compiler_generated_navigation_pairs'] == [dict(article=66, page_ids=[66,216])]
    old, target = [IlnkContainer.parse(p).blocks for p in [args[-1], resource]]
    assert len(target) == len(old) == 217 and [i for i in range(217) if old[i] != target[i]] == [66]
    rejected = []
    for case in ['old-stat-label', 'wrong-continuation', 'missing-localization-gate']:
        changed = deepcopy(doc)
        row = changed['records'][0]
        if case == 'old-stat-label':
            row['english'] = row['english'].replace('Command', 'Leadership')
            row['semantic_sections'] = [s.replace('Command', 'Leadership') for s in row['semantic_sections']]
        elif case == 'wrong-continuation':
            row['current_continuations'][0]['current_hex'] = '00'
        else:
            row['review']['localization'] = False
        try:
            plan_articles(changed, *args, require_formatting=False)
        except ValueError as error:
            rejected.append(dict(case=case, rejected=True, error=str(error)))
        else:
            raise AssertionError(case)
    OUT.mkdir()
    save(OUT / 'direct_visual_approval.json', dict(native_proof=str(native_path), native_proof_sha256=sha(native_path.read_bytes()),
        all_two_complete_pages_directly_viewed=True, sheets=native['review_sheets'],
        findings='Command matches the native stat. Complete at least150 phrase, complete funding/return paragraph, all original policy links and both navigation labels fit. Consistent glyphs and complete edge characters.',
        unchanged_continuation216_byte_exact=True, actual_gameplay=False, new_credit=0))
    image = deepcopy(parent)
    image.replace_file(file, resource)
    rom = OUT / 'HELP66_Command_RESEARCH_ONLY.nds'
    rom.write_bytes(bytes(image.rom.save()))
    reread = NdsImage.open(rom)
    assert [p for _,p,v in parent.iter_files() if reread.read_file(p) != v] == [file]
    assert all(reread.read_file(p) == v for p,v in parent.iter_components())
    inverse = deepcopy(reread)
    inverse.replace_file(file, args[-1])
    assert bytes(inverse.rom.save()) == Path(plan['current_ROM']).read_bytes()
    save(OUT / 'qualification.json', dict(parent=plan['current_ROM'], parent_sha256=plan['current_ROM_sha256'],
        research_ROM=str(rom), research_ROM_sha256=sha(rom.read_bytes()), source_articles=1, pages=2, target_topics=217,
        only_HELP_changed_all_other_components_exact_complete_parent_inverse=True, only_topic66_changed_continuation216_exact=True,
        new_formatter_andindividual_gate_rejections=rejected, all_two_native_anddirect_visual_pages_pass=True,
        actual_widgets_archive_load_navigation_andregistered_integration_pending=True, all_fifth_gates_pending=True, new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [plan_path, native_path, ROOT/'native_term_binding_v1.json', OUT/'direct_visual_approval.json', Path(__file__)]}))
    pins_path = Path('translations/rom_retention_pins.json')
    before = pins_path.read_bytes()
    pins = load(pins_path)
    (OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(r['path']).resolve() == rom.resolve() for r in pins)
    pins.append(dict(path=str(rom.resolve()), reason='Preserve Help66 Command terminology correction research image. SHA256 '+sha(rom.read_bytes())))
    staged = pins_path.with_name('rom_retention_pins.HELP66_Command_preview.pending.json')
    assert not staged.exists()
    save(staged, pins)
    assert pins_path.read_bytes() == before
    os.replace(staged, pins_path)
    save(ROOT/'focused_itinerary_v1.json', dict(start_frame=21400, required_topics=[66,216], actions=[
        dict(open=11), dict(open=44), dict(open=62), dict(open=66), dict(remember='fleet'), dict(open=216),
        dict(key='L'), dict(return_to='fleet'), dict(key='R'), dict(open=66), dict(return_to='fleet')]))
    print('Fleet66 native/direct view and three relevant rejection guards pass; pinned research image, no credit.')
