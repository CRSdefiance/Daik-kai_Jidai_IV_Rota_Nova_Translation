"""Expose only197 already-drafted speeches;the remaining342 older-English speeches stay unread."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
if __name__=='__main__':
    sealed=ROOT/'B61_B64_all197_sealed_drafts_v1.json';selected=ROOT/'B61_B64_selected_source_packet_v1.json';target=ROOT/'B61_B64_current_binding_source_v1.json'
    assert not any(p.exists() for p in [sealed,selected,target])
    paths=[ROOT/'B61_B63_77_logical_English_drafts_v1.json',ROOT/'B64_120_logical_English_drafts_v2.json']
    rows=[r for p in paths for r in load(p)['records']]
    assert len(rows)==197 and all(r['earlier_English_unconsulted'] and r['current_English_comparison_pending'] and not r['review']['formatting'] for r in rows)
    source=ROOT/'source_identity_event_andterm_checkpoint_v1.json';identity=load(source)
    meanings=[deepcopy(r) for r in identity['records'] if r['block'] in range(61,65)]
    assert {r['id'] for r in meanings}=={r['id'] for r in rows}
    save(sealed,dict(format='dk4-source-first-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',blocks=list(range(61,65)),records=rows,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        constituent_drafts={str(p):sha(p.read_bytes()) for p in paths},remaining342_speeches_not_exposed=True,
        all_fifth_formatting_gates_pending=True,new_credit=0,guide_photos=False))
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path);subset=deepcopy(packet)
    subset['groups']=[g for g in packet['groups'] if g['block'] in range(61,65)]
    subset.update(records=197,selected_from=str(packet_path),selected_from_sha256=sha(packet_path.read_bytes()))
    save(selected,subset)
    for row in meanings:row['current_ROM_English_unconsulted']=True
    save(target,dict(source_packet=str(selected),source_packet_sha256=sha(selected.read_bytes()),records=meanings,meanings=197,
        all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),no_blanket_prior_English_exposure_claim=True,
        complete_gloss=str(source),complete_gloss_sha256=sha(source.read_bytes()),
        remaining342_speeches_not_selected_or_exposed=True,new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Sealed197 drafts andfour complete source blocks for comparison;remaining342 older-English speeches remain unselected.',flush=True)
