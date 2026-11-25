"""Bind the 67 independent drafts to their exact clean source before current extraction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT=Path('work/analysis/Rafael_B161_B180_clean_20261105')
PACKET=ROOT/'clean_source_packet.json'
DRAFTS=ROOT/'B161_B165_clean_drafts_v1.json'
OUT=ROOT/'B161_B165_clean_first_v1'

if __name__=='__main__':
    assert not OUT.exists()
    packet,drafts=map(load,[PACKET,DRAFTS])
    groups=[g for g in packet['groups'] if 161<=g['block']<=165]
    assert [g['block'] for g in groups]==list(range(161,166))
    source=[r for g in groups for r in g['records']]
    byid={r['id']:r for r in drafts['records']}
    assert len(byid)==len(source)==67 and set(byid)=={r['id'] for r in source}
    assert all(c['word'] not in (0x2100,0x2200,0x4100) for g in groups for c in g['all_source_commands'])
    for original in source:
        row=byid[original['id']]
        assert all(row[k]==v for k,v in original.items()) and not any(row['review'].values())
    OUT.mkdir()
    bound=OUT/'source_packet.json'
    save(bound,{**packet,'groups':groups,'records':len(source),'complete_source_packet':str(PACKET),
        'complete_source_packet_sha256':sha(PACKET.read_bytes())})
    save(OUT/'current_binding_meanings.json',dict(source_packet=str(bound),source_packet_sha256=sha(bound.read_bytes()),
        records=[{**byid[r['id']],'current_ROM_English_unconsulted':True} for r in source],meanings=len(source),
        all_drafts_sealed=str(DRAFTS),all_drafts_sha256=sha(DRAFTS.read_bytes()),
        no_blanket_prior_English_exposure_claim=True,new_credit=0))
    print('67 exact source-first speech inputs ready for current binding.')
