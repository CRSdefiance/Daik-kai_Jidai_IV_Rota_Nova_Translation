"""Project the unified clean intake into existing speech/style/menu binder schemas."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    root = Path('work/Maria_B0_B32_clean_20261109')
    out = root / 'binding_inputs_v1'
    assert not out.exists()
    original = root / 'clean_source_packet.json'
    sealed = root / 'all301_clean_meanings_andindependent_drafts_v1.json'
    packet, drafts = map(load, [original, sealed])
    assert drafts['records_count'] == 301 and drafts['current_English_unconsulted']
    assert drafts['source_meanings_andlogical_drafts_all_saved_before_current_English_intake']
    rows = deepcopy(drafts['records'])
    for row in rows:
        assert row['current_English_unconsulted'] and not any(row['review'].values())
        row.update(earlier_English_unconsulted=True, current_ROM_English_unconsulted=True)
    speech = [r for r in rows if r['kind'] == 'ordinary-speech']
    styles = [r for r in rows if r['kind'] == 'physical-style-alternative']
    choices = [r for r in rows if r['kind'] == 'typed-menu-caption']
    assert (len(speech), len(styles), len(choices)) == (292, 7, 2)
    projected = deepcopy(packet)
    for group in projected['groups']:
        group['records'] = [r for r in speech if r['block'] == group['block']]
    out.mkdir()
    projected_path = out / 'clean_source_packet.json'
    save(projected_path, projected)
    sealed_projection = out / 'sealed_drafts.json'
    save(sealed_projection, dict(records=rows,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        original_sealed_drafts=str(sealed), original_sealed_drafts_sha256=digest(sealed),
        source_schema_projection_only_no_meaning_draft_orcontrol_changes=True, new_credit=0))
    save(out / 'meanings_view.json', dict(records=speech, meanings=292,
        source_packet=str(projected_path), source_packet_sha256=digest(projected_path),
        all_drafts_sealed=str(sealed_projection), all_drafts_sha256=digest(sealed_projection),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    for name, records in [('clean_style_objects.json', styles), ('clean_choice_objects.json', choices)]:
        save(out / name, dict(records=records, source_packet_sha256=digest(projected_path),
            original_source_packet_sha256=digest(original), current_English_unconsulted=True,
            all_drafts_sealed=str(sealed_projection), all_drafts_sha256=digest(sealed_projection), new_credit=0))
    save(out / 'projection_qualification.json', dict(source_objects=301, ordinary_speeches=292,
        physical_style_alternatives=7, captions=2, complete_blocks=32,
        all_source_commands_retained=True, all301_meanings_anddrafts_unchanged=True,
        no_current_English_yet_extracted=True, all_five_gates_pending=True, new_credit=0,
        evidence={str(p): digest(p) for p in [original, sealed, projected_path, sealed_projection, Path(__file__)]}))
    print('Projected301 sealed drafts for unchanged native binders:292 speech/seven style/two menu;zero credit.')


if __name__ == '__main__':
    main()
