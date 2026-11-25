"""Replan only two wide-I records; reuse the other 222 reviewed plans exactly."""
import argparse
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import plan_Hodram_B61_B70_v8893 as previous
from scripts.audit_story_glyph_consistency import independent_pixels, load, save
from scripts.verify_fixed_name_glyphs_v279 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster
from scripts.verify_ordinary_name_fidelity_research import initialized

OLD_DOC = Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')
OLD_PLAN = Path('work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json')
NEW_DOC = Path('translations/hodram_B61_B70_editorial_manuscript_v2.json')
IDS = {'DK4_MES_B67_R0089', 'DK4_MES_B69_R0011'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists() and not NEW_DOC.exists()
    doc, old_plans = load(OLD_DOC), load(OLD_PLAN)
    assert old_plans['manuscript_sha256'] == sha(OLD_DOC.read_bytes())
    registry = load('translations/release_stack.json')
    profile = registry['profiles']['lisbon-guild-hover-fix-20261101']
    runtime = load(profile['ascii_glyph_right_bounds'])
    current = Path('out/all_routes_combined_lisbon_guild_fixed_20261101.nds')
    assert sha(current.read_bytes()) == runtime['target_ROM_sha256']
    image = NdsImage.open(current)
    arm = image.read_file('/__arm9__.bin')
    assert sha(arm) == runtime['target_ARM9_sha256']
    restored = bytearray(arm)
    for patch in runtime['proof']['patches']:
        at = patch['offset']
        old, new = bytes.fromhex(patch['before_hex']), bytes.fromhex(patch['after_hex'])
        assert len(old) == len(new) and restored[at:at + len(new)] == new
        restored[at:at + len(old)] = old
    assert sha(restored) == doc['current_ARM9_sha256']
    predecessor = NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes()) == doc['current_ROM_sha256']
    assert bytes(restored) == predecessor.read_file('/__arm9__.bin')
    assert all(image.read_file(p) == value for _, p, value in predecessor.iter_files())
    assert image.read_file('/__arm7__.bin') == predecessor.read_file('/__arm7__.bin')
    doc = deepcopy(doc)
    doc.update(current_ROM=str(current), current_ROM_sha256=sha(current.read_bytes()),
               current_ARM9_sha256=sha(arm), previous_manuscript=str(OLD_DOC),
               previous_manuscript_sha256=sha(OLD_DOC.read_bytes()),
               glyph_only_revisions=sorted(IDS), new_credit=0)
    args.out.mkdir(parents=True)
    cpu = initialized(arm)
    plans = []
    changed = []
    pictures = []
    for row, old_plan in zip(doc['records'], old_plans['records'], strict=True):
        assert row['id'] == old_plan['id']
        if row['id'] not in IDS:
            plans.append(deepcopy(old_plan))
            continue
        before = deepcopy(row)
        assert '\uff29' in row['english']
        for key in ['english', 'logical_English', 'planned_English_markup']:
            row[key] = row[key].replace('\uff29', 'I')
        row['glyph_consistency_revision'] = dict(previous_english=before['english'],
            reason='Keep the established prose; use normal ASCII I with the validated native literal-prefix policy.',
            source_context_andprose_decision_reused=True, formatting_andintegration_pending=True)
        planning = dict(row)
        planning['english'] = row['planned_English_markup']
        plan = previous.plan(planning)
        plan.update(file_path=row['file_path'], block=row['block'],
                    source_record_index=row['source_record_index'], source_selector=row['source_selector'],
                    kind=row['kind'], logical_English=row['english'], planning_record=planning,
                    base_QA=previous.base_qa(planning, plan),
                    original_consumer_usable_text_width_px=216,
                    original_consumer_bitmap_width_px=216)
        assert not any(i['severity'] in ('warning', 'error') for i in plan['base_QA']['issues'])
        assert ' '.join(plan['lines']) == row['english']
        raw = bytes.fromhex(plan['encoded_hex'])
        assert raw[0] == row['source_selector']
        body = raw[1:]
        assert all(c < 128 for c in body) and not any(m in body for m in (b'FI', b'FA', b'FO'))
        assert expand(cpu, body) == body
        pixels, events, font = raster(arm, body)
        assert pixels == independent_pixels(arm, font, events)
        visible = [e for e in events if e['code'] != 32]
        assert all(e['kind'] == 'ascii' for e in events)
        assert [e['code'] for e in visible] == [c for c in body if c not in (10, 32)]
        assert [visible[0]['x'], visible[0]['y']] == [0, 0]
        picture = Image.new('RGB', (216, 64))
        colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
        picture.putdata([colors[v] for v in pixels])
        path = args.out / (row['id'] + '.png')
        picture.save(path)
        pictures.append((row['id'], picture))
        changed.append(dict(id=row['id'], old_English=before['english'], new_English=row['english'],
            old_lines=old_plan['lines'], new_lines=plan['lines'], compiled_hex=raw.hex(),
            native_parser_output_exact=True, complete_native_glyphs_pixels_bounds_andcanaries=True,
            preview=str(path), preview_sha256=sha(path.read_bytes())))
        plans.append(plan)
    assert len(changed) == 2 and len(plans) == 224
    assert sum(r['expected_native_pages'] for r in plans) == 229
    assert all(a == b for a, b in zip(plans, old_plans['records'], strict=True) if a['id'] not in IDS)
    save(NEW_DOC, doc)
    plan_path = args.out / 'automatic_plans.json'
    save(plan_path, dict(manuscript=str(NEW_DOC), manuscript_sha256=sha(NEW_DOC.read_bytes()),
        records=plans, failures=[], reused_plan_count=222, regenerated_plan_count=2,
        prior_plan=str(OLD_PLAN), prior_plan_sha256=sha(OLD_PLAN.read_bytes()),
        glyph_only_changes=changed, prose_wording_preserved=True, original_QA_not_relaxed=True,
        source_owned_planner=old_plans['source_owned_planner'], new_credit=0))
    sheet = Image.new('RGB', (648, 440), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (label, picture) in enumerate(pictures):
        draw.text((5, i * 220 + 4), label + ' - offline native', fill='white')
        sheet.paste(picture.resize((648, 192), Image.Resampling.NEAREST), (0, i * 220 + 24))
    sheet_path = args.out / 'two_glyph_pages.png'
    sheet.save(sheet_path)
    save(args.out / 'glyph_review.json', dict(current_ROM=str(current), current_ROM_sha256=sha(current.read_bytes()),
        current_ARM9_sha256=sha(arm), runtime_inverse_exact_to_previous_reviewed_ARM9=True,
        every_other_predecessor_file_andARM7_exact=True, changed=changed,
        reused_unaffected_records_andplans=222, total_pages=229, review_sheet=str(sheet_path),
        review_sheet_sha256=sha(sheet_path.read_bytes()), direct_view_pending=True,
        manuscript=str(NEW_DOC), manuscript_sha256=sha(NEW_DOC.read_bytes()),
        plan=str(plan_path), plan_sha256=sha(plan_path.read_bytes()),
        formatting_gates_still_false=True, actual_gameplay_andintegration_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()), new_credit=0))
    print('Two wide-I records corrected and natively checked; 222 exact plans reused; 229 pages total.')


if __name__ == '__main__':
    main()
