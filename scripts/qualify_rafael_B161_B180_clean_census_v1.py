"""Bind the next complete source packet to unique uncredited records."""
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B161_B180_clean_20261105')
OUT=ROOT/'clean_source_census_v1.json'
LEDGER=Path('translations/editorial_review_current_v1.json')
PENDING=Path('translations/rafael_B141_B160_final_review_v1.json')

if __name__=='__main__':
    assert not OUT.exists()
    packetpath,choicepath,draftpath=[ROOT/p for p in ['clean_source_packet.json','clean_choice_objects.json','B180_sailing_lesson_clean_drafts_v1.json']]
    packet,choice,drafts,pending,ledger=map(load,[packetpath,choicepath,draftpath,PENDING,LEDGER])
    assert choice['source_packet_sha256']==sha(packetpath.read_bytes())
    assert [g['block'] for g in packet['groups']]==list(range(161,181))
    speeches=[r for g in packet['groups'] for r in g['records']]
    captions=choice['records'];rows=speeches+captions
    assert (len(speeches),len(captions),choice['object_count'],len(choice['label_free2000_controls']))==(733,8,4,14)
    assert not any(c['word']==0x4100 for g in packet['groups'] for c in g['all_source_commands'])
    key=lambda r:(r['file_path'],r['id'])
    keys={key(r) for r in rows};assert len(keys)==741
    integrated=ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
    assert len({key(r) for r in integrated})==ledger['records_editorially_completed']
    assert not keys&{key(r) for r in integrated} and not keys&{key(r) for r in pending['records']}
    assert {key(r) for r in drafts['records']}=={key(r) for r in rows if r['block']==180} and drafts['records_count']==29
    assert all(not any(r['review'].values()) for r in drafts['records'])
    source_macros=Counter()
    for r in speeches:
        body=bytes.fromhex(r['source_hex'])[1:]
        source_macros.update({m.decode():body.count(m) for m in [b'FI',b'FA',b'FO',b'FU']})
    assert source_macros['FU']==1
    save(OUT,dict(source_objects=741,speeches=733,choice_captions=8,complete_blocks=list(range(161,181)),zero_already_credited_keys=True,
        zero_overlap_with_pending_or_integrated_B141_B160=True,completed_ledger_count_at_intake=ledger['records_editorially_completed'],
        source_only_no_current_English_extracted=True,source_macros=dict(source_macros),
        clean_meanings_andindependent_drafts=29,draft_blocks=[180],remaining_clean_meanings_anddrafts=712,
        all_five_gates_pending=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [packetpath,choicepath,draftpath,PENDING,Path(__file__)]},
        intake_ledger_sha256=sha(LEDGER.read_bytes())))
    print('741 unique clean source records, no overlap; the 29-record sailing lesson has independent drafts.')
