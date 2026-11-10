"""Record the next complete clean-only intake and check for existing credit."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B181_B200_clean_20261105')
PACKET = ROOT / 'clean_source_packet.json'
CHOICES = ROOT / 'clean_choice_objects.json'
STYLES = ROOT / 'clean_style_objects.json'
DRAFT = ROOT / 'B181_B182_clean_drafts_v1.json'
LEDGER = Path('translations/editorial_review_current_v1.json')
OUT = ROOT / 'clean_source_census_v1.json'


def digest(p):
    return sha(Path(p).read_bytes())


def key(row):
    return row['file_path'], row['id']


def main():
    assert not OUT.exists()
    packet, choices, styles, draft, ledger = map(load, (PACKET,CHOICES,STYLES,DRAFT,LEDGER))
    assert packet['records'] == 384 and packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert [g['block'] for g in packet['groups']] == list(range(181,201))
    assert not choices['records'] and not styles['records']
    assert choices['source_packet_sha256'] == styles['source_packet_sha256'] == digest(PACKET)
    assert len(choices['label_free2000_controls']) == 2
    rows = [r for g in packet['groups'] for r in g['records']]
    credited = set(map(key,ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']))
    keys = set(map(key,rows))
    assert len(keys) == len(rows) == 384 and not keys & credited
    assert len(draft['records']) == 58 and draft['complete_blocks'] == [181,182]
    assert set(map(key,draft['records'])) == {key(r) for r in rows if r['block'] in (181,182)}
    assert draft['all_five_gates_pending'] and draft['no_current_English_extracted_for_this_intake_before_drafts']
    assert all(digest(p)==h for p,h in draft['evidence'].items())
    save(OUT, dict(clean_speeches=384, typed_choice_captions=0, physical_style_alternatives=0,
        distinct_label_free_2000_controls=2, complete_blocks=list(range(181,201)), zero_already_credited_keys=True,
        clean_drafts=58, complete_draft_blocks=[181,182], remaining_clean_drafts=326, remaining_current_comparisons=384,
        source_only_no_current_English_extracted=True, all_individual_five_gates_pending=True, new_credit=0,
        intake_ledger_sha256=digest(LEDGER), evidence={str(p):digest(p) for p in (PACKET,CHOICES,STYLES,DRAFT,Path(__file__))}))
    print('384 clean records across 20 complete blocks, 58 first drafts, zero earlier credit overlap.')


if __name__ == '__main__':
    main()
