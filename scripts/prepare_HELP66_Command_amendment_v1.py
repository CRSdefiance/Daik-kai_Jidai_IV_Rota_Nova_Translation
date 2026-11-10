"""Reopen one terminology finding without invalidating the other Help reviews or evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_fleet66_amendment_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/HELP66_Command_amendment_20261104')
FINAL = Path('translations/help_shipyard37_contextual_final_review_v3.json')
PREP = Path('work/analysis/Shipyard_HELP37_release_v2_20261104/registered_preparation.json')
TOWN = Path('work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    prep, final, verified = map(load, [PREP, FINAL, TOWN])
    parent = Path(prep['final_ROM'])
    assert sha(parent.read_bytes()) == prep['target_ROM_sha256']
    image, clean, base = [NdsImage.open(p) for p in [parent, Path('work/clean.nds'), Path('out/raphael_natural_v2_accepted_base.nds')]]
    file = '/COMMON/HELP.DK4'
    raw, source, canonical = [p.read_file(file) for p in [image, clean, base]]
    current, original, baseline = [IlnkContainer.parse(p).blocks for p in [raw, source, canonical]]
    assert len(current) == 217 and len(original) == len(baseline) == 202
    town = NdsImage.open(verified['candidate'])
    arm, source_arm = [p.read_file('/__arm9__.bin') for p in [image, clean]]
    assert all(image.read_file(p) == town.read_file(p) for p in ['/__arm9__.bin', '/COMMON/MESFILE.DK4', '/GRP/KANJI.FNT'])
    labels = []
    for at in [0x131EB4, 0x148324]:
        jp = source_arm[at:].split(b'\0', 1)[0]
        en = arm[at:].split(b'\0', 1)[0]
        assert jp.decode('cp932') == '統率力' and en == b'Command'
        labels.append(dict(ARM9_offset=at, source_hex=jp.hex(), source_Japanese=jp.decode('cp932'), current_hex=en.hex(), current_English=en.decode('ascii')))
    old = next(r for r in final['records'] if r['topic_id'] == 66)
    assert '統率力１５０以上' in old['source_Japanese_with_link_IDs']
    row = deepcopy(old)
    row['english'] = old['english'].replace('Leadership of at least 150.', 'Command of at least 150.')
    assert row['english'] != old['english']
    row['semantic_sections'] = [s.replace('Leadership of at least 150.', 'Command of at least 150.') for s in old['semantic_sections']]
    row['review'] = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    row['finding'] = 'Use Command for 統率力, matching both current native stat labels. Preserve the source threshold of at least 150 and every fleet/funding/policy/commander-return fact. Earlier Leadership wording was a missed terminology defect.'
    row['localization_note'] = row['finding']
    row['source_meaning'] = old['source_meaning'].replace('Leadership>=150', 'Command>=150')
    row['current_reference'] = dict(file_path=file, block=66, archive_offset=int.from_bytes(raw[272:276], 'little'), bytes=len(current[66]), offset_table_slot=272)
    row['comparison_current_reference'] = row['current_reference']
    row['current_hex'] = row['current_source_hex'] = current[66].hex()
    row['current_continuations'] = [dict(topic_id=216, current_hex=current[216].hex())]
    row['current_English'] = current[66].decode('ascii', errors='backslashreplace')
    row['planned_stored_pages'] = []
    row['fresh_display_allocation_widgets_andintegration_pending'] = True
    row['registered_integration_pending'] = True
    row['new_credit'] = 0
    doc = dict(format='dk4-help66-command-terminology-amendment-v1', translation_policy='natural-dialogue-v2', target_locale='en-US', file_path=file,
        current_ROM=str(parent), current_ROM_sha256=sha(parent.read_bytes()), source_clean_HELP_sha256=sha(source),
        source_canonical_HELP_sha256=sha(canonical), source_current_HELP_sha256=sha(raw), current_topic_count=217, source_topic_count=202,
        records=[row], no_authored_wraps=True, all_four_prose_gates_pass=True, all_fifth_gates_pending=True, new_credit=0,
        original37_manuscript_preserved=str(FINAL), original37_manuscript_sha256=sha(FINAL.read_bytes()),
        prior36_editorial_reviews_andall_unaffected_pages_preserved=True, registered_parent_build_pending=True)
    resource, plan = plan_articles(doc, source, canonical, raw, require_formatting=False)
    target = IlnkContainer.parse(resource).blocks
    assert len(plan['pages']) == 2 and plan['owned_topic_ids'] == [66, 216] and len(target) == 217
    assert target[216] == current[216] and [i for i in range(217) if target[i] != current[i]] == [66]
    ROOT.mkdir()
    save(ROOT / 'native_term_binding_v1.json', dict(labels=labels, source_HELP_reference=old['source_reference'],
        source_HELP_hex=old['source_hex'], source_HELP_Japanese=old['source_Japanese_with_link_IDs'],
        current_ARM9_sha256=sha(arm), source_ARM9_sha256=sha(source_arm), current_verified_release=str(TOWN), current_verified_release_sha256=sha(TOWN.read_bytes()),
        planned_parent_runtime_COMMON_font_exact_to_verified_Town=True, finding=row['finding'], actual_new_gameplay=False, new_credit=0))
    manuscript = ROOT / 'formatting_input_v1.json'
    save(manuscript, doc)
    output = ROOT / 'HELP66_Command_RESEARCH_ONLY.DK4'
    output.write_bytes(resource)
    save(ROOT / 'automatic_plans_v1.json', dict(**plan, manuscript=str(manuscript), manuscript_sha256=sha(manuscript.read_bytes()),
        research_resource=str(output), current_ROM=str(parent), current_ROM_sha256=sha(parent.read_bytes()),
        source_terminology_binding=str(ROOT / 'native_term_binding_v1.json'), source_terminology_binding_sha256=sha((ROOT / 'native_term_binding_v1.json').read_bytes()),
        one_changed_page_one_exact_continuation=True, all_native_actual_visual_andfifth_gates_pending=True, new_credit=0))
    print('Fleet66 Command correction source-bound; one changed page, same continuation216, no new credit.')
    for page in plan['pages']:
        print(page['topic_id'], '/'.join(page['visible_lines']))
