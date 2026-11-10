"""Use the generic current-text binder after all557 independent drafts are sealed."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    root=Path('work/analysis/Rafael_B141_B160_clean_20261105')
    drafts_path=root/'all557_meanings_andindependent_drafts_v2.json'
    packet_path=root/'clean_source_packet.json';sealed=root/'all557_sealed_for_current_binding_v1.json'
    target=root/'current_binding_meanings_v1.json'
    assert not sealed.exists() and not target.exists()
    draft,packet=map(load,[drafts_path,packet_path])
    assert len(draft['records'])==557 and draft['all_individual_clean_meanings_andindependent_drafts_saved']
    source_rows=[r for g in packet['groups'] for r in g['records']]
    selected={r['id']:r for r in draft['records'] if 'source_selector' in r}
    assert set(selected)=={r['id'] for r in source_rows} and len(selected)==549
    save(sealed,dict(source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        original_drafts=str(drafts_path),original_drafts_sha256=sha(drafts_path.read_bytes()),source_objects=557,
        no_blanket_historical_exposure_claim=True,new_credit=0))
    rows=[]
    for original in source_rows:
        row=deepcopy(selected[original['id']]);assert all(row[k]==v for k,v in original.items())
        row['current_ROM_English_unconsulted']=True;rows.append(row)
    save(target,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),
        records=rows,meanings=549,all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),
        no_blanket_prior_English_exposure_claim=True,source_drafts=str(drafts_path),
        source_drafts_sha256=sha(drafts_path.read_bytes()),new_credit=0,guide_photos=False))
    print('549 speech inputs bound to557 sealed independent drafts;current extraction nowready. No approval orcredit.')
