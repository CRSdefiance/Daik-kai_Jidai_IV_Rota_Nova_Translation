"""Seal the next clean source census and the eight drafted blocks."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


ROOT = Path('work/analysis/Rafael_B201_B220_clean_20261106')
PACKET = ROOT/'clean_source_packet.json'
CHOICES = ROOT/'clean_choice_objects.json'
STYLES = ROOT/'clean_style_objects.json'
DRAFTS = [ROOT/f'{label}_clean_drafts_v1.json' for label in ('B201_B203','B204_B206','B207_B208')]
OUT = ROOT/'clean_source_census_v1.json'
LEDGER = Path('translations/editorial_review_current_v1.json')


def digest(path):
    return sha(Path(path).read_bytes())


def key(row):
    return row['file_path'],row['id']


def main():
    assert not OUT.exists()
    packet,choices,styles,ledger=map(load,(PACKET,CHOICES,STYLES,LEDGER))
    assert packet['records']==382 and packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert [g['block'] for g in packet['groups']]==list(range(201,221))
    assert choices['caption_count']==21 and choices['object_count']==10 and len(choices['label_free2000_controls'])==1
    assert not styles['records']
    assert choices['source_packet_sha256']==styles['source_packet_sha256']==digest(PACKET)
    rows=[r for g in packet['groups'] for r in g['records']]+choices['records']
    keys=set(map(key,rows))
    assert len(keys)==len(rows)==403
    credited=set(map(key,ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']))
    assert not keys&credited
    drafts=list(map(load,DRAFTS))
    assert [p['records_count'] for p in drafts]==[47,35,56]
    assert [b for d in drafts for b in d['complete_blocks']]==list(range(201,209))
    assert sum(d['typed_captions'] for d in drafts)==12
    assert all(d['all_five_gates_pending'] and d['no_current_English_extracted_for_this_intake_before_drafts'] for d in drafts)
    assert all(digest(p)==h for d in drafts for p,h in d['evidence'].items())
    drafted={key(r) for d in drafts for r in d['records']}
    assert len(drafted)==138 and drafted=={key(r) for r in rows if r['block']<=208}
    save(OUT,dict(clean_speeches=382,typed_choice_captions=21,typed_choice_objects=10,physical_style_alternatives=0,
        label_free_2000_controls=1,clean_objects=403,complete_blocks=list(range(201,221)),zero_already_credited_keys=True,
        independent_drafts=138,clean_draft_speeches=126,clean_draft_captions=12,complete_draft_blocks=list(range(201,209)),
        remaining_clean_drafts=265,remaining_current_comparisons=403,
        all_individual_five_gates_pending=True,source_only_no_current_English_extracted=True,
        intake_ledger_sha256=digest(LEDGER),evidence={str(p):digest(p) for p in (PACKET,CHOICES,STYLES,*DRAFTS,Path(__file__))},new_credit=0))
    print('403 clean objects in 20 complete blocks, 138 drafts, and zero earlier credit overlap.')


if __name__=='__main__':
    main()
