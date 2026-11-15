"""Bind the complete clean drafts to a four-block subset before current extraction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B161_B180_clean_20261105')
BLOCKS={177,178,179,180}
PACKET=ROOT/'clean_source_packet.json'
CHOICES=ROOT/'clean_choice_objects.json'
DRAFTS=[ROOT/name for name in ['B177_Elysion_ship_lesson_clean_drafts_v1.json','B178_Fernando_coin_game_clean_drafts_v1.json',
    'B179_Manuel_refit_lesson_clean_drafts_v1.json','B180_sailing_lesson_clean_drafts_v1.json']]

if __name__=='__main__':
    packet,choices=map(load,[PACKET,CHOICES])
    groups=[g for g in packet['groups'] if g['block'] in BLOCKS]
    speeches=[r for g in groups for r in g['records']]
    captions=[r for r in choices['records'] if r['block'] in BLOCKS]
    inputs=[r for path in DRAFTS for r in load(path)['records']]
    byid={r['id']:r for r in inputs}
    assert len(inputs)==len(byid)==183 and (len(speeches),len(captions))==(175,8)
    assert set(byid)=={r['id'] for r in speeches+captions}
    for r in speeches+captions:
        row=byid[r['id']]
        assert all(row[k]==v for k,v in r.items()) and not any(row['review'].values())
    out=ROOT/'B177_B180_clean_first_v1';assert not out.exists();out.mkdir()
    sub=out/'source_packet.json';caption=out/'source_choices.json';sealed=out/'sealed_drafts.json'
    save(sub,{**packet,'groups':groups,'records':175,'complete_source_packet':str(PACKET),'complete_source_packet_sha256':sha(PACKET.read_bytes())})
    save(caption,{**choices,'records':captions,'label_free2000_controls':[r for r in choices['label_free2000_controls'] if r['block'] in BLOCKS],
        'source_packet':str(sub),'source_packet_sha256':sha(sub.read_bytes())})
    save(out/'source_styles.json',dict(records=[],objects=[],scope='No 4100 commands in the complete four-block inventory.',new_credit=0))
    assert not any(c['word']==0x4100 for g in groups for c in g['all_source_commands'])
    save(sealed,dict(records=inputs,complete_blocks=sorted(BLOCKS),records_count=183,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PACKET,CHOICES,*DRAFTS,Path(__file__)]}))
    save(out/'current_binding_meanings.json',dict(source_packet=str(sub),source_packet_sha256=sha(sub.read_bytes()),
        records=[{**byid[r['id']],'current_ROM_English_unconsulted':True} for r in speeches],meanings=175,
        all_drafts_sealed=str(sealed),all_drafts_sha256=sha(sealed.read_bytes()),no_blanket_prior_English_exposure_claim=True,new_credit=0))
    print('Sealed 183 independent drafts over all four exchanges; 175 speech inputs and eight exact typed captions.')
