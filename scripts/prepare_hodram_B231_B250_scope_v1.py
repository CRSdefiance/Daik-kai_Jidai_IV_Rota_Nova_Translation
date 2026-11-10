"""Exclude the 18 exactly credited B237 source records without reopening their review."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B231_B250_clean_20261107')
PACKET=ROOT/'clean_source_packet.json'
SCOPE=ROOT/'clean_intake_scope_v1.json'
ELIGIBLE=ROOT/'eligible_clean_source_packet.json'
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('translations/papal_trade_contextual_final_review_v1.json')

def main():
    assert not SCOPE.exists() and not ELIGIBLE.exists()
    packet,styles,menus,ledger,prior=map(load,(PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',LEDGER,PRIOR))
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    ordinary=[r for g in packet['groups'] for r in g['records']]
    excluded=[r for r in ordinary if (r['file_path'],r['id']) in credited]
    assert len(excluded)==18 and {r['block'] for r in excluded}=={237}
    saved={(r['file_path'],r['id']):r for r in prior['records']}
    for row in excluded:
        old=saved[(row['file_path'],row['id'])]
        assert row['source_hex']==old['source_hex'] and row['source_reference']['offset']==old['source_reference']['offset']
        assert row['source_reference']['record_index']==old['source_reference']['record_index'] and all(old['review'].values())
    assert len(styles['records'])==14 and styles['object_count']==2 and styles['style_alias_slots']==16
    assert len(menus['records'])==2 and menus['object_count']==1
    eligible=deepcopy(packet);eligible['groups']=[g for g in eligible['groups'] if g['block']!=237]
    eligible.update(records=209,source_unfiltered_packet=str(PACKET),source_unfiltered_packet_sha256=digest(PACKET),
        excluded_already_credited_block=237,previous_source_reviews_reused=str(PRIOR),previous_source_reviews_sha256=digest(PRIOR))
    assert sum(len(g['records']) for g in eligible['groups'])==209
    rows=[r for g in eligible['groups'] for r in g['records']]+styles['records']+menus['records']
    assert len(rows)==225 and not any((r['file_path'],r['id']) in credited for r in rows)
    assert all(r['source_decode_error'] is None for r in ordinary)
    save(ELIGIBLE,eligible)
    save(SCOPE,dict(source_packet=str(ELIGIBLE),source_packet_sha256=digest(ELIGIBLE),raw_source_packet=str(PACKET),raw_source_packet_sha256=digest(PACKET),
        ordinary_speeches=209,physical_personality_alternatives=14,physical_style_objects=2,personality_alias_slots=16,
        typed_caption_records=2,typed_choice_objects=1,total_editorial_objects=225,control_only_blocks=[235],
        reviewed_block_numbers=[g['block'] for g in eligible['groups']],
        excluded_credited_records=[dict(id=r['id'],file_path=r['file_path'],source_reference=r['source_reference'],source_hex=r['source_hex']) for r in excluded],
        previous_review=str(PRIOR),previous_review_sha256=digest(PRIOR),all18_excluded_clean_source_positions_andbytes_exact=True,
        all_completed_exclusion_keys_checked=len(credited),remaining_source_meanings=225,remaining_clean_first_drafts=225,
        source_meanings_saved=0,localized_drafts_saved=0,contextual_comparisons=0,
        no_current_story_English_consulted_for_eligible_records=True,no_new_name_term_consumer_orformatting_approval=True,
        full_goal_complete=False,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in (PACKET,ROOT/'clean_style_objects.json',ROOT/'clean_choice_objects.json',LEDGER,PRIOR,Path(__file__))}))
    print('225 eligible source objects: 209 speeches, 14 voice alternatives, two captions. Eighteen exact prior B237 reviews preserved and excluded.')

if __name__=='__main__':main()
