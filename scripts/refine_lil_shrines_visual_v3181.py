"""Resolve three observed native wrap findings without editing predecessors."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Shrines_Temples_refinement_v3181')
OLD = Path('translations/lil_shrines_temples_editorial_manuscript_v3.json')
NEW = Path('translations/lil_shrines_temples_editorial_manuscript_v4.json')
FORMATTER = Path('dk4tool/dialogue/lil_shrines_temples_layout_v2.py')
PLANNER = Path('scripts/prepare_lil_shrines_layout_v3182.py')

if __name__ == '__main__':
    assert not any(p.exists() for p in [ROOT, NEW, FORMATTER, PLANNER])
    doc = deepcopy(read(OLD))
    row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B108_R0030')
    before = row['english']
    row['prior_prose_before_native_visual_refinement'] = before
    row['english'] = "{SPEAKER:A0}Our village has passed this lamp down since ancient times. They say it's essential to anyone seeking the Proof. I entrust it to you."
    # Strip the previous row-count note before adding a new editorial note.
    # The next complete QA pass will independently regenerate any such note.
    for r in doc['records']:
        reason = r.pop('qa_waiver_reason', None)
        if reason:
            assert r['localization_note'].endswith(' ' + reason)
            r['localization_note'] = r['localization_note'][:-len(reason)-1]
        r.pop('qa_waivers', None)
    note = ("The viewed native plane split need from it. Essential to anyone seeking the Proof preserves the community's hearsay and necessity while keeping the lamp, ancient transmission and entrusting intact. No source fact or uncertain status changes.")
    row['localization_note'] += ' ' + note
    assert row['editorial_decision'] == 'revise'
    doc.update(previous_manuscript=str(OLD), previous_manuscript_sha256=sha(OLD.read_bytes()),
        native_visual_refinement_note=note, formatting_approval_not_granted=True)
    old_formatter = Path('dk4tool/dialogue/lil_shrines_temples_layout_v1.py')
    text = old_formatter.read_text(encoding='utf-8')
    assert text.count("'i','you','he','she','it','we','they','my'") == 1
    assert text.count("PROTECTED_BOUNDARIES=frozenset({") == 1
    text = text.replace("'i','you','he','she','it','we','they','my'",
                        "'i','you','he','she','it','its','we','they','my'")
    text = text.replace("PROTECTED_BOUNDARIES=frozenset({",
                        "PROTECTED_BOUNDARIES=frozenset({('nice','work'),")
    FORMATTER.write_text(text, encoding='utf-8')
    old_planner = Path('scripts/prepare_lil_shrines_layout_v3178.py')
    text = old_planner.read_text(encoding='utf-8')
    changes = {
        'lil_shrines_temples_layout_v1': 'lil_shrines_temples_layout_v2',
        'lil_Shrines_Temples_layout_v3178': 'lil_Shrines_Temples_layout_v3182',
        "SPEECH = Path('translations/lil_shrines_temples_editorial_manuscript_v2.json')":
        "SPEECH = Path('translations/lil_shrines_temples_editorial_manuscript_v4.json')",
        "VOICE = Path('translations/lil_shrines_temples_actor_style_manuscript_v1.json')":
        "VOICE = Path('translations/lil_shrines_temples_actor_style_manuscript_v2.json')",
        "Path('translations/lil_shrines_temples_editorial_manuscript_v3.json')":
        "Path('translations/lil_shrines_temples_editorial_manuscript_v5.json')",
        "Path('translations/lil_shrines_temples_actor_style_manuscript_v2.json')]":
        "Path('translations/lil_shrines_temples_actor_style_manuscript_v3.json')]",
    }
    # One simultaneous replacement prevents the old voice input becoming output.
    import re
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes, key=len, reverse=True)),
                  lambda m: changes[m.group()], text)
    anchor = "            raw = bytes.fromhex(row['source_hex'])"
    assert text.count(anchor) == 1
    text = text.replace(anchor, """            old_reason = row.pop('qa_waiver_reason', None)
            if old_reason:
                assert row['localization_note'].endswith(' ' + old_reason)
                row['localization_note'] = row['localization_note'][:-len(old_reason)-1]
            row.pop('qa_waivers', None)
""" + anchor)
    PLANNER.write_text(text, encoding='utf-8')
    ROOT.mkdir(parents=True)
    save(NEW, doc)
    prior = Path('work/analysis/lil_Shrines_Temples_fonts_v3179/current_macro_QA_and_progressive_font_proof.json')
    fe = Path('work/analysis/lil_Shrines_Temples_FE_v3180/current_FE_macro_font_and_typed_paper_proof.json')
    pictures = read(prior)['review_sheets'] + read(fe)['review_sheets']
    assert len(pictures) == 28
    for p in pictures:
        assert sha(Path(p['path']).read_bytes()) == p['sha256']
    save(ROOT / 'native_visual_findings_and_successor_receipt.json', dict(
        viewed_sheets=pictures, all24_progressive_and4_FE_sheets_viewed=True,
        findings=[
            dict(id='DK4_MES_B101_R0072', finding='its split from two Map Keys', resolution='local v2 possessive weak-boundary rule'),
            dict(id='DK4_MES_B108_R0030', finding='need split from it', before=before, after=row['english'], resolution=note),
            dict(id='DK4_MES_B109_R0266', finding='Nice split from work', resolution='local v2 idiom pair; effective current wording retained')],
        previous_manuscript=str(OLD), previous_manuscript_sha256=sha(OLD.read_bytes()),
        manuscript=str(NEW), manuscript_sha256=sha(NEW.read_bytes()),
        previous_formatter=str(old_formatter), previous_formatter_sha256=sha(old_formatter.read_bytes()),
        formatter=str(FORMATTER), formatter_sha256=sha(FORMATTER.read_bytes()),
        next_QA_producer=str(PLANNER), next_QA_producer_sha256=sha(PLANNER.read_bytes()),
        no_global_helper_source_control_gloss_or_review_gate_change=True,
        no_ROM_registry_ledger_or_editorial_credit=True, new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('All28native sheets viewed;three concrete flow findings resolved in successors;complete QA next.')
