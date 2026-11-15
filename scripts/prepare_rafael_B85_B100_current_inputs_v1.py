"""Adapt immutable261 clean-only drafts tothe proven255-speech catalogue extractor."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105')
SEALED=ROOT/'261_source_meanings_andindependent_drafts_v1.json'
OUT=ROOT/'current_extraction_inputs_v1'

if __name__=='__main__':
    assert not OUT.exists();doc=load(SEALED);packet_path=Path(doc['clean_source_packet']);packet=load(packet_path)
    assert sha(packet_path.read_bytes())==doc['clean_source_packet_sha256']
    assert doc['source_meanings_anddrafts_sealed_before_current_story_extraction'] and len(doc['records'])==261
    rows=[deepcopy(r) for r in doc['records'] if r['kind']!='typed-choice-label'];assert len(rows)==255
    assert all(r['earlier_English_unconsulted'] and r['current_English_comparison_pending'] for r in rows)
    for row in rows:row['current_ROM_English_unconsulted']=True
    OUT.mkdir();subset={**packet,'groups':[g for g in packet['groups'] if g['block']>=85],'records':255}
    source_view=OUT/'source_packet_view.json';save(source_view,subset)
    receipt=OUT/'sealed_drafts_receipt.json';save(receipt,dict(sealed=str(SEALED),sealed_sha256=sha(SEALED.read_bytes()),
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        claims_apply_to_this_intake_not_a_blanket_historical_screenshot_ortranslation_exposure_claim=True,new_credit=0))
    save(OUT/'meanings_view.json',dict(records=rows,meanings=255,source_packet=str(source_view),
        source_packet_sha256=sha(source_view.read_bytes()),all_drafts_sealed=str(receipt),all_drafts_sha256=sha(receipt.read_bytes()),
        no_blanket_prior_English_exposure_claim=True,source_draft_parent=str(SEALED),source_draft_parent_sha256=sha(SEALED.read_bytes()),
        no_source_orEnglish_wording_changed=True,new_credit=0))
    print('Prepared255-speech extraction view;all261 drafts andsix original choices remain sealed andunchanged.')
