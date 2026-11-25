"""Seal both new complete Rafael blocks before opening current English."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B161_B180_clean_20261105')
PACKET = ROOT / 'clean_source_packet.json'
DRAFTS = [ROOT / f'B{n}_clean_drafts_v1.json' for n in (166,167)]
OUT = ROOT / 'B166_B167_clean_first_v1'


def digest(path):
    return sha(path.read_bytes())


def main():
    assert not OUT.exists()
    packet = load(PACKET)
    drafts = list(map(load, DRAFTS))
    assert [d['complete_blocks'] for d in drafts] == [[166], [167]]
    assert [d['records_count'] for d in drafts] == [136, 50]
    assert all(d['no_current_English_extracted_for_this_intake_before_drafts'] and d['all_five_gates_pending'] for d in drafts)
    assert all(digest(Path(path)) == expected for d in drafts for path,expected in d['evidence'].items())
    groups = [g for g in packet['groups'] if g['block'] in (166,167)]
    assert [g['block'] for g in groups] == [166,167]
    source = [r for g in groups for r in g['records']]
    rows = [r for d in drafts for r in d['records']]
    assert len(source) == len(rows) == len({r['id'] for r in rows}) == 186
    assert all(c['word'] not in (0x2100,0x2200,0x4100) for g in groups for c in g['all_source_commands'])
    for original, row in zip(source,rows,strict=True):
        assert all(row[k] == v for k,v in original.items()) and not any(row['review'].values())
    OUT.mkdir()
    bound, sealed = OUT/'source_packet.json', OUT/'sealed_drafts.json'
    save(bound, {**packet, 'groups':groups, 'records':186, 'complete_source_packet':str(PACKET),
        'complete_source_packet_sha256':digest(PACKET)})
    save(sealed, dict(records=rows, records_count=186, complete_blocks=[166,167],
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        source_proof={str(p):digest(p) for p in [PACKET,*DRAFTS,Path(__file__)]}, new_credit=0))
    save(OUT/'current_binding_meanings.json', dict(source_packet=str(bound), source_packet_sha256=digest(bound),
        records=[{**r,'current_ROM_English_unconsulted':True} for r in rows], meanings=186,
        all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    print('186 clean-first source inputs sealed for current binding.')


if __name__ == '__main__':
    main()
