"""Select complete clean-source blocks and reconcile all object keys against credited coverage."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['packet','styles','choices','names','out']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--blocks',type=int,nargs='+',required=True)
    a=p.parse_args();assert not a.out.exists() and len(set(a.blocks))==len(a.blocks)
    packet,styles,choices,names=map(load,[a.packet,a.styles,a.choices,a.names])
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert styles['source_packet_sha256']==choices['source_packet_sha256']==names['source_packet_sha256']==digest(a.packet)
    selected=set(a.blocks);groups=[deepcopy(g) for g in packet['groups'] if g['block'] in selected]
    assert [g['block'] for g in groups]==a.blocks
    ordinary=[r for g in groups for r in g['records']]
    sr=[deepcopy(r) for r in styles['records'] if r['block'] in selected]
    so=[deepcopy(o) for o in styles['objects'] if o['block'] in selected]
    cr=[deepcopy(r) for r in choices['records'] if r['block'] in selected]
    co=[deepcopy(o) for o in choices['objects'] if o['block'] in selected]
    rows=ordinary+sr+cr
    keys={(r['file_path'],r['id']) for r in rows};assert len(keys)==len(rows)
    assert all(r['source_decode_error'] is None for r in ordinary)
    assert all(r['earlier_English_unconsulted'] for r in rows)
    ledgerpath=Path('translations/editorial_review_current_v1.json');ledger=load(ledgerpath)
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(credited)==ledger['records_editorially_completed'] and not keys&credited
    actors={r['source_selector'] for r in ordinary+sr if r['source_selector']<207}
    named=[deepcopy(r) for r in names['records'] if r['actor_ID'] in actors]
    assert {r['actor_ID'] for r in named}==actors
    a.out.mkdir(parents=True);target=a.out/'clean_source_packet.json'
    subset={**packet,'groups':groups,'records':len(ordinary),'source_parent_packet':str(a.packet),
        'source_parent_packet_sha256':digest(a.packet),'selected_complete_block_numbers':a.blocks,
        'scope_selector':__file__,'scope_selector_sha256':digest(__file__)}
    save(target,subset)
    shared=dict(source_packet=str(target),source_packet_sha256=digest(target))
    save(a.out/'clean_style_objects.json',{**styles,**shared,'objects':so,'records':sr,'object_count':len(so),
        'physical_alternatives':len(sr),'style_alias_slots':8*len(so),'source_parent_objects':str(a.styles),
        'source_parent_objects_sha256':digest(a.styles)})
    save(a.out/'clean_choice_objects.json',{**choices,**shared,'objects':co,'records':cr,'object_count':len(co),
        'caption_count':len(cr),'label_free2000_controls':[v for v in choices['label_free2000_controls'] if v['block'] in selected],
        'source_parent_objects':str(a.choices),'source_parent_objects_sha256':digest(a.choices)})
    selectors={r['source_selector'] for r in ordinary+sr}
    save(a.out/'clean_name_fields.json',{**names,**shared,'records':named,
        'special_selectors_outside_ordinary_actor_table':sorted(v for v in selectors if v>=207),
        'source_parent_names':str(a.names),'source_parent_names_sha256':digest(a.names)})
    styleblocks={o['block'] for o in so};choiceblocks={o['block'] for o in co}
    control=[g['block'] for g in groups if not g['records'] and g['block'] not in styleblocks|choiceblocks]
    save(a.out/'clean_intake_scope_v1.json',dict(source_packet=str(target),source_packet_sha256=digest(target),
        ordinary_speeches=len(ordinary),physical_personality_alternatives=len(sr),physical_style_objects=len(so),
        personality_alias_slots=8*len(so),typed_caption_records=len(cr),typed_choice_objects=len(co),
        total_editorial_objects=len(rows),reviewed_block_numbers=a.blocks,control_only_blocks=control,
        excluded_credited_records=[],all_completed_exclusion_keys_checked=len(credited),source_key_overlap_with_completed_credit=0,
        source_parent_unselected_blocks=[g['block'] for g in packet['groups'] if g['block'] not in selected],
        no_current_English_dialogue_consulted_for_eligible_records=True,source_meanings_pending=True,
        all_five_review_gates_pending=True,new_credit=0,full_goal_complete=False,
        evidence={str(q):digest(q) for q in [a.packet,a.styles,a.choices,a.names,ledgerpath,Path(__file__)]}))
    print(dict(ordinary=len(ordinary),style_alternatives=len(sr),captions=len(cr),total=len(rows),
        voice_objects=len(so),menus=len(co),control_only_blocks=control,credited_overlap=0))

if __name__=='__main__':main()
