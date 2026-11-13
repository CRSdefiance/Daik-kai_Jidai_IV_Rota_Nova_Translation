"""Seal all clean drafts and source command bindings before reading Rafael2549 English."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT=Path('work/analysis/Rafael_B201_B220_clean_20261106')
PACKET=ROOT/'clean_source_packet.json'
CHOICES=ROOT/'clean_choice_objects.json'
STYLES=ROOT/'clean_style_objects.json'
DRAFTS=[ROOT/f'{name}_clean_drafts_v1.json' for name in (
    'B201_B203','B204_B206','B207_B208','B209_B210','B211_B213','B214_B217','B218_B220',
)]
OUT=ROOT/'sealed_all_clean_first_v1'


def digest(path):
    return sha(Path(path).read_bytes())


def main():
    assert not OUT.exists()
    packet,choices,styles=map(load,(PACKET,CHOICES,STYLES))
    blocks=list(range(201,221))
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert [g['block'] for g in packet['groups']]==blocks
    assert packet['records']==382 and choices['caption_count']==21 and choices['object_count']==10
    assert choices['source_packet_sha256']==styles['source_packet_sha256']==digest(PACKET)
    assert not styles['records'] and len(choices['label_free2000_controls'])==1
    drafts=list(map(load,DRAFTS))
    assert [d['records_count'] for d in drafts]==[47,35,56,41,81,78,65]
    assert [b for d in drafts for b in d['complete_blocks']]==blocks
    assert all(d['no_current_English_extracted_for_this_intake_before_drafts'] and d['all_five_gates_pending'] for d in drafts)
    assert all(digest(p)==h for d in drafts for p,h in d['evidence'].items())
    all_rows=[r for d in drafts for r in d['records']]
    byid={r['id']:r for r in all_rows}
    speeches=[r for g in packet['groups'] for r in g['records']]
    captions=choices['records']
    assert len(all_rows)==len(byid)==len(speeches)+len(captions)==403
    assert set(byid)=={r['id'] for r in speeches+captions}
    for original in speeches+captions:
        row=byid[original['id']]
        assert all(row[k]==v for k,v in original.items()) and not any(row['review'].values())
        assert row['earlier_English_unconsulted']
    ordered=[]
    for block in blocks:
        ordered.extend(sorted((byid[r['id']] for r in speeches+captions if r['block']==block),
            key=lambda row:row['source_reference']['offset']))
    OUT.mkdir()
    sealed=OUT/'sealed_drafts.json'
    save(sealed,dict(records=ordered,records_count=403,ordinary_speeches=382,typed_captions=21,typed_choice_objects=10,
        complete_blocks=blocks,source_contexts={k:v for d in drafts for k,v in d['source_contexts'].items()},
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in (PACKET,CHOICES,STYLES,*DRAFTS,Path(__file__))}))
    save(OUT/'current_binding_meanings.json',dict(source_packet=str(PACKET),source_packet_sha256=digest(PACKET),
        records=[{**byid[r['id']],'current_ROM_English_unconsulted':True} for r in speeches],meanings=382,
        all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True,new_credit=0))
    print('Sealed all 403 drafts with exact clean references, including all 21 typed captions.')


if __name__=='__main__':
    main()
