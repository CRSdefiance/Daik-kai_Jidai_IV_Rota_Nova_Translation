"""Seal all 175 logical drafts before exposing the matching current dialogue."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')

if __name__=='__main__':
    target=ROOT/'B36_B41_current_binding_source_v1.json'
    sealed=ROOT/'B36_B41_all175_sealed_drafts_v1.json'
    selected=ROOT/'B36_B41_selected_source_packet_v1.json'
    assert not any(p.exists() for p in [target,sealed,selected])
    sources=[ROOT/'B36_B37_92_logical_English_drafts_v1.json',ROOT/'B38_B41_83_logical_English_drafts_v1.json']
    drafts=[r for p in sources for r in load(p)['records']]
    gloss_path=ROOT/'B36_B41_175_complete_clean_meanings_v1.json'
    packet_path=ROOT/'clean_source_packet.json'
    gloss,packet=map(load,[gloss_path,packet_path])
    assert len(drafts)==175 and {r['id'] for r in drafts}=={r['id'] for r in gloss['records']}
    assert all(r['current_English_comparison_pending'] and not r['review']['formatting'] for r in drafts)
    save(sealed,dict(format='dk4-source-first-logical-English-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/data/SC0.DK4',blocks=list(range(36,42)),records=drafts,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        constituent_drafts={str(p):sha(p.read_bytes()) for p in sources},all_fifth_formatting_gates_pending=True,new_credit=0,guide_photos=False))
    subset=deepcopy(packet)
    subset['groups']=[g for g in packet['groups'] if g['block'] in range(36,42)]
    subset.update(records=175,selected_from=str(packet_path),selected_from_sha256=sha(packet_path.read_bytes()))
    save(selected,subset)
    rows=deepcopy(gloss['records'])
    for row in rows:row['current_ROM_English_unconsulted']=True
    save(target,dict(source_packet=str(selected),source_packet_sha256=sha(selected.read_bytes()),records=rows,meanings=175,
        all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),no_blanket_prior_English_exposure_claim=True,
        complete_gloss=str(gloss_path),complete_gloss_sha256=sha(gloss_path.read_bytes()),new_credit=0,guide_photos=False))
    print('175 complete source-first drafts sealed;current-English binding is now authorized for the six complete blocks.')
