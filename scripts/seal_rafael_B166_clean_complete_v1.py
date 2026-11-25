"""Bind the three full B166 draft exchanges and document the clean FE display leads."""
import re
from collections import Counter
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B161_B180_clean_20261105')
OUT = ROOT / 'B166_clean_drafts_v1.json'
INTAKE = ROOT / 'clean_source_packet.json'
PARTS = [ROOT / f'B166_{name}_clean_drafts_v1.json' for name in ('opening_audience', 'post_audience', 'charlotte_letter')]
REFINEMENTS = {
    193: "I've never felt at home in stiff places like that...",
    196: "Heh heh... I can see that.",
    610: "He didn't go over to Spain. He's a military man. He was loyal to the King of Spain. The king was our sovereign at the time.",
}


def main():
    assert not OUT.exists()
    original = next(g['records'] for g in load(INTAKE)['groups'] if g['block'] == 166)
    packets = list(map(load, PARTS))
    assert all(p['all_five_gates_pending'] and p['no_current_English_extracted_for_this_intake_before_drafts'] for p in packets)
    records = [row for p in packets for row in p['records']]
    assert [p['records_count'] for p in packets] == [26, 76, 34]
    assert len(original) == len(records) == len({r['id'] for r in records}) == 136
    for raw, row in zip(original, records, strict=True):
        assert all(row[k] == value for k, value in raw.items())
        idx = raw['source_reference']['record_index']
        if idx in REFINEMENTS:
            row['prior_independent_English'] = row['independent_English']
            row['independent_English'] = REFINEMENTS[idx]
        assert all(row['independent_English'].count(t) == n for t,n in row['native_literal_token_counts'].items())
        assert row['current_English_comparison_pending'] and not any(row['review'].values())
        if row['source_selector'] == 254:
            japanese = raw['source_Japanese']
            if japanese.startswith('＜エイレネ＞'):
                row['clean_FE_presentation_lead'] = 'Eirene heading separate from body'
            elif re.match(r'^\n', japanese):
                row['clean_FE_presentation_lead'] = 'Original staged blank rows or indentation and alternating scene alignment'
            elif idx in {787,791,794,797}:
                row['clean_FE_presentation_lead'] = 'Charlotte letter sequence with original Portuguese, pronunciation and separate translated reading'
            else:
                row['clean_FE_presentation_lead'] = 'Other FE speech, source consumer and exact layout pending'
    lead_counts = Counter(r.get('clean_FE_presentation_lead') for r in records if r['source_selector'] == 254)
    assert None not in lead_counts and lead_counts['Charlotte letter sequence with original Portuguese, pronunciation and separate translated reading'] == 4
    save(OUT, dict(records=records, records_count=136, ordinary_speeches=136, typed_captions=0, complete_blocks=[166],
        source_contexts={166: 'Opening audience, Claudio and Eirene after the audience, expedition and Charlotte letter.'},
        complete_exchange_parts=[dict(path=str(path), sha256=sha(path.read_bytes()), records=p['records_count'])
            for path,p in zip(PARTS,packets,strict=True)],
        individual_read_aloud_refinements=sorted(REFINEMENTS), clean_FE_display_leads=dict(lead_counts),
        all_five_gates_pending=True, no_current_English_extracted_for_this_intake_before_drafts=True,
        no_blanket_claim_of_historical_unexposure=True, all_source_literal_F_tokens_preserved_not_an_approval_of_their_native_consumers=True,
        no_ROM_or_registry_changes=True, new_credit=0, guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [INTAKE,*PARTS,Path(__file__)]}))
    print('136 unique B166 clean drafts sealed. Exact source ranges and FE presentation leads retained.')


if __name__ == '__main__':
    main()
