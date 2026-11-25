"""Seal the seven complete clean-first blocks together before current comparison."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B161_B180_clean_20261105')
PACKET = ROOT / 'clean_source_packet.json'
DRAFTS = [ROOT / f'B{b}_clean_drafts_v1.json' for b in (170, 171, 172)] + [ROOT / 'B173_B176_clean_drafts_v1.json']
OUT = ROOT / 'B170_B176_clean_first_v1'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUT.exists()
    packet, drafts = load(PACKET), list(map(load, DRAFTS))
    assert [d['records_count'] for d in drafts] == [75, 25, 35, 55]
    assert [b for d in drafts for b in d['complete_blocks']] == list(range(170, 177))
    assert all(d['no_current_English_extracted_for_this_intake_before_drafts'] and d['all_five_gates_pending'] for d in drafts)
    assert all(digest(p) == h for d in drafts for p, h in d['evidence'].items())
    groups = [g for g in packet['groups'] if 170 <= g['block'] <= 176]
    assert [g['block'] for g in groups] == list(range(170, 177))
    assert all(c['word'] not in (0x2100, 0x2200, 0x4100) for g in groups for c in g['all_source_commands'])
    records = [r for d in drafts for r in d['records']]
    for row, original in zip(records, (r for g in groups for r in g['records']), strict=True):
        assert all(row[k] == v for k, v in original.items()) and not any(row['review'].values())
    assert len(records) == len({r['id'] for r in records}) == 190
    assert {r['id'] for r in records if r['source_selector'] == 254} == {
        'DK4_MES_B170_R0241', 'DK4_MES_B170_R0244', 'DK4_MES_B171_R0044', 'DK4_MES_B171_R0047', 'DK4_MES_B171_R0061', 'DK4_MES_B171_R0064',
    }
    OUT.mkdir()
    bound, sealed = OUT / 'source_packet.json', OUT / 'sealed_drafts.json'
    proof = {str(p): digest(p) for p in (PACKET, *DRAFTS, Path(__file__))}
    save(bound, {**packet, 'groups': groups, 'records': 190, 'complete_source_packet': str(PACKET),
                 'complete_source_packet_sha256': digest(PACKET)})
    save(sealed, dict(records=records, records_count=190, complete_blocks=list(range(170, 177)),
        source_contexts={k: v for d in drafts for k, v in d['source_contexts'].items()}, all_five_gates_pending=True,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        four_B171_audience_reaction_modals_require_source_layout_check=True, source_proof=proof, new_credit=0))
    save(OUT / 'current_binding_meanings.json', dict(source_packet=str(bound), source_packet_sha256=digest(bound),
        records=[{**r, 'current_ROM_English_unconsulted': True} for r in records], meanings=190,
        all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    print('190 clean drafts from seven complete blocks are sealed with six source modal records.')


if __name__ == '__main__':
    main()
