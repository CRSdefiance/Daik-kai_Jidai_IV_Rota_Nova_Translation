"""Bind all 68 Ian scene drafts to their clean source before reading current English."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B161_B180_clean_20261105')
PACKET = ROOT / 'clean_source_packet.json'
DRAFTS = ROOT / 'B169_clean_drafts_v1.json'
OUT = ROOT / 'B169_clean_first_v1'


def main():
    assert not OUT.exists()
    packet, drafts = map(load, (PACKET, DRAFTS))
    assert drafts['complete_blocks'] == [169] and drafts['records_count'] == 68
    assert drafts['no_current_English_extracted_for_this_intake_before_drafts'] and drafts['all_five_gates_pending']
    assert all(sha(Path(p).read_bytes()) == h for p, h in drafts['evidence'].items())
    groups = [g for g in packet['groups'] if g['block'] == 169]
    assert len(groups) == 1
    assert all(c['word'] not in (0x2100, 0x2200, 0x4100) for c in groups[0]['all_source_commands'])
    rows = drafts['records']
    assert len({row['id'] for row in rows}) == 68
    for original, row in zip(groups[0]['records'], rows, strict=True):
        assert all(row[k] == v for k, v in original.items()) and not any(row['review'].values())
    OUT.mkdir()
    bound, sealed = OUT / 'source_packet.json', OUT / 'sealed_drafts.json'
    save(bound, {**packet, 'groups': groups, 'records': 68, 'complete_source_packet': str(PACKET),
                 'complete_source_packet_sha256': sha(PACKET.read_bytes())})
    save(sealed, {**drafts, 'source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake': True})
    save(OUT / 'current_binding_meanings.json', dict(
        source_packet=str(bound), source_packet_sha256=sha(bound.read_bytes()),
        records=[{**r, 'current_ROM_English_unconsulted': True} for r in rows], meanings=68,
        all_drafts_sealed=str(sealed), all_drafts_sha256=sha(sealed.read_bytes()),
        no_blanket_prior_English_exposure_claim=True, new_credit=0,
    ))
    print('All 68 clean-first B169 inputs sealed for current binding.')


if __name__ == '__main__':
    main()
