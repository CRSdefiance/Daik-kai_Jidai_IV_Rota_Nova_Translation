"""Bind the next clean-only Rafael intake and the first two complete exchanges."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.draft_rafael_B221_B222_clean_v1 import ROOT
from dk4tool.patch.grand_race_menu_release import sha


OUT=ROOT/'clean_source_census_v1.json'
LEDGER=Path('translations/editorial_review_current_v1.json')
INPUTS=[ROOT/f'{name}.json' for name in ('clean_source_packet','clean_style_objects','clean_choice_objects','B221_B222_clean_drafts_v1')]


def digest(path):
    return sha(Path(path).read_bytes())


def key(row):
    return row['file_path'],row['id']


def main():
    assert not OUT.exists()
    packet,styles,choices,drafts=map(load,INPUTS)
    assert packet['records']==234 and packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert [g['block'] for g in packet['groups']]==list(range(221,241))
    assert (styles['object_count'],styles['physical_alternatives'],styles['style_alias_slots'])==(4,29,32)
    assert (choices['object_count'],choices['caption_count'],len(choices['label_free2000_controls']))==(3,7,0)
    assert styles['source_packet_sha256']==choices['source_packet_sha256']==digest(INPUTS[0])
    rows=[r for g in packet['groups'] for r in g['records']]+styles['records']+choices['records']
    keys=set(map(key,rows))
    assert len(keys)==len(rows)==270
    assert not keys & set(map(key,load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']))
    assert {r['block'] for r in rows}==set(range(221,241))-{231}
    drafted=set(map(key,drafts['records']))
    assert len(drafted)==30 and drafted=={key(r) for r in rows if r['block'] in (221,222)}
    assert all(digest(p)==h for p,h in drafts['evidence'].items())
    save(OUT,dict(clean_speeches=234,typed_choice_captions=7,typed_choice_objects=3,
        physical_style_alternatives=29,native_style_objects=4,source_style_alias_slots=32,clean_objects=270,
        complete_blocks=list(range(221,241)),control_only_blocks=[231],zero_already_credited_keys=True,
        independently_drafted_records=30,complete_draft_blocks=[221,222],remaining_clean_drafts=240,
        remaining_current_comparisons=270,all_five_gates_pending=True,source_only_no_current_English_extracted=True,
        intake_ledger_sha256=digest(LEDGER),evidence={str(p):digest(p) for p in (*INPUTS,Path(__file__))},new_credit=0))
    print('270 clean source objects, 30 independent drafts and no prior credit overlap.')


if __name__=='__main__':
    main()

