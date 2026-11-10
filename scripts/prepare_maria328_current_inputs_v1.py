"""Project sealed drafts for existing guarded current-text andmixed-object binders."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out = ROOT/'current_inputs_v1'
    assert not out.exists()
    draft_path = ROOT/'all328_independent_drafts_v1.json'
    source_path = ROOT/'clean_source_packet.json'
    drafts, source = map(load, [draft_path, source_path])
    assert drafts['current_English_not_consulted'] and drafts['whole_clean_exchanges_read_before_drafting']
    assert len(drafts['records']) == source['records'] == 328
    assert all(not any(r['review'].values()) and r['current_English_comparison_pending'] for r in drafts['records'])
    assert {r['id'] for r in drafts['records']} == {r['id'] for g in source['groups'] for r in g['records']}
    out.mkdir()
    sealed = out/'sealed_drafts.json'
    save(sealed, dict(source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        source_meanings=drafts['source_meanings'], source_meanings_sha256=drafts['source_meanings_sha256'],
        independent_drafts=str(draft_path), independent_drafts_sha256=digest(draft_path),
        no_blanket_historical_English_exposure_claim=True, no_new_gates_orcredit=True, new_credit=0))
    grouped = {'speech':[], 'styles':[], 'choices':[]}
    for original in drafts['records']:
        row = deepcopy(original)
        row.update(earlier_English_unconsulted=True, current_ROM_English_unconsulted=True)
        if row['kind'] == 'ordinary-speech':
            group = 'speech'
        elif row['kind'] == '4100-style-alternative':
            group = 'styles'
        else:
            assert row['kind'] == 'typed-choice-label', row['kind']
            group = 'choices'
        grouped[group].append(row)
    assert tuple(len(grouped[k]) for k in ['speech','styles','choices']) == (289,24,15)
    for name, rows in grouped.items():
        save(out/(name+'_meanings.json'), dict(records=rows, meanings=len(rows), source_packet=str(source_path),
            source_packet_sha256=digest(source_path), all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed),
            no_blanket_prior_English_exposure_claim=True, source_only_not_current_story_English=True,
            all_review_gates_pending=True, new_credit=0))
    save(out/'projection.json', dict(source_objects=328, groups={k:len(v) for k,v in grouped.items()},
        all_source_glosses_drafts_controls_andreferences_unchanged=True,
        dynamic_source_selectors=Counter(r['source_selector'] for r in grouped['speech'] if r['source_selector'] in [207,208]),
        FE_source_panels=sum(r['source_selector']==254 for r in grouped['speech']),
        source_meanings_preceded_drafts_andcurrent_intake=True, no_new_gates_orcredit=True, new_credit=0,
        evidence={str(p):digest(p) for p in [draft_path,source_path,sealed,Path(__file__)]}))
    print('Prepared289 speech,24 style and15 caption input views;all328 sealed drafts unchanged.')


if __name__ == '__main__':
    main()
