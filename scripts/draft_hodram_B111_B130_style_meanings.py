"""Read all48 clean personality alternatives incontext before any current English."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Hodram_B111_B130_clean_20261101')
SOURCE=ROOT/'clean_style_objects.json'
MEANINGS={
(113,10):[
'Politely ask the admiral tolook at this,with excited emphasis;shared source slots0/1.',
'Ask the admiral tolook at this in a lighter familiar voice;shared slots2/3.',
'Ask the admiral tolook at this in a rough familiar voice.',
'Ask the admiral tolook at this with a gruff/older imperative.',
'Call out to the admiral in a youthful,elongated,excited voice andask him tolook.',
'Respectfully ask the admiral tolook with an older-fashioned verbal manner.',
],
(119,16):[
'Politely inform the admiral that this is a dead end,with explanatory emphasis.',
'Plainly andpolitely state that this is a dead end,addressing the admiral.',
'React with mild surprise andnote the dead end in a light familiar voice.',
'Tell the admiral this is a dead end in a conversational feminine-coded source voice;do not invent a relationship.',
'React roughly andcasually tothe dead end.',
'Tell the admiral it is a dead end with an older-fashioned conversational ending.',
'Call out tothe admiral youthfully andsay it is a dead end.',
'React with composed older/formal surprise andstate that it is a dead end.',
],
(121,64):[
'Notice someone on a river sandbar/islet with a masculine conversational reaction;one physical string shared byslots0/1/2/4/7. The text does not yet identify the person.',
'Notice someone on a river sandbar/islet in a feminine conversational voice.',
'Notice someone on a river sandbar/islet in an older-fashioned voice.',
'Youthfully notice that someone is there;this variant omits the sandbar detail,so do not mechanically add it.',
],
(121,324):[
'Volunteer confidently andpolitely tohandle the rescue;one physical string shared byslots0/1/7.',
'Volunteer tohandle the rescue in a short familiar voice.',
'Say that the speaker will go torescue the child,in a feminine conversational voice.',
'Tell the party toleave it tothe speaker,in a rough confident voice.',
'Tell the party toleave it tothe speaker,in an older-fashioned emphatic voice.',
'Say the speaker will go,in a youthful familiar voice.',
],
(122,16):[
'Draw the admiral\'s attention tothe object with a short imperative;shared slots0/1/4/5/7.',
'Ask the admiral tolook;shared slots2/3.',
'Address the admiral youthfully andpoint out this object.',
],
(123,16):[
'Politely andexcitedly ask the admiral tolook at the object;shared slots0/1/7.',
'Ask the admiral tolook in a light familiar voice;shared slots2/3.',
'Ask the admiral tolook in a rough familiar voice.',
'Tell the admiral tolook with an emphatic older-fashioned ending.',
'Youthfully address the admiral andask him tolook.',
],
(125,54):[
'Tentatively andpolitely observe that the statue\'s form does not suit this building.',
'Politely say the form seems incongruous with the building;retain the slightly measured/formal manner.',
'Conversationally say the object looks outofplace inthis building.',
'Casually call the object a mismatch with the building,in a feminine conversational voice.',
'Roughly ask whether the admiral agrees that the object does not fit the building.',
'Tentatively say it seems unsuitable forthe building,in an older-fashioned voice.',
'Youthfully say it feels as though the object does not fit the building.',
'Ask politely whether the form seems incongruous with the building;preserve the confirming-question force.',
],
(125,450):[
'Say the object is shaped like a ship\'s figurehead,then wonder whether it was originally one;polite tentative deduction.',
'Note the figurehead shape,then reconsider whether it is actually a figurehead;measured tentative deduction.',
'Lightly ask whether it looks like a figurehead,then suggest that perhaps it actually is one.',
'Hesitantly compare it toa figurehead,then wonder whether it was one originally;feminine conversational voice.',
'Roughly observe that it looks like a figurehead andtentatively suggest that it actually is one,with a trailing thought.',
'In an older-fashioned voice,first compare the shape toa figurehead,then positively conclude that it was originally a figurehead. Preserve the stronger conclusion inthis variant.',
'Youthfully say that the object can be used as a figurehead anddraw attention toit. Do not replace this with the other variants\' claim about its original purpose.',
'In a composed older/formal voice,compare the shape toa figurehead,then ask whether it was originally one.',
],
}

if __name__=='__main__':
    out=ROOT/'all48_clean_style_meanings_before_English.json';assert not out.exists()
    source=load(SOURCE);rows=[]
    for obj in source['objects']:
        originals=[r for r in source['records'] if (r['block'],r['source_command_offset'])==(obj['block'],obj['offset'])]
        glosses=MEANINGS[obj['block'],obj['offset']];assert len(originals)==len(glosses)
        for original,gloss in zip(originals,glosses,strict=True):
            row=deepcopy(original);row.update(source_meaning_gloss=gloss,meaning_read_in_complete_clean_exchange=True,style_slots_are_personality_aliases_not_distinct_actor_IDs=True,localization_andfive_gate_approval_pending=True);rows.append(row)
    assert len(rows)==48 and sum(len(r['source_style_indices']) for r in rows)==64
    save(out,dict(source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),records=rows,meanings=48,objects=8,aliases=64,
        source_only_before_old_English=True,existing_Lil4100_consumer_proof_toqualify_for_current_dependencies=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    old=ROOT/'all260_clean_meanings_before_English.json';speech=deepcopy(load(old))
    for row in speech['records']:
        if row['id']=='DK4_MES_B125_R0032':
            row['source_meaning_gloss']='Hodram recognizes the preceding personality-selected observation that the statue looks incongruous with the building. The full source4100 variants now supply the context.'
        elif row['id']=='DK4_MES_B125_R0053':
            row['source_meaning_gloss']='Hodram understands the preceding personality-selected figurehead observation. Most variants infer that it originally was a figurehead;the youthful variant instead says it can be used as one.'
        if row['block'] in [113,119,121,122,123,125]:row['additional_clean_style_context']=str(out)
    speech.update(previous_meanings=str(old),previous_meanings_sha256=sha(old.read_bytes()),full_style_context_meanings=str(out),full_style_context_meanings_sha256=sha(out.read_bytes()),
        revised_glosses=['DK4_MES_B125_R0032','DK4_MES_B125_R0053'],source_context_refinement_before_English=True)
    updated=ROOT/'all260_clean_meanings_before_English_v2.json';assert not updated.exists();save(updated,speech)
    save(ROOT/'intake_scope_checkpoint.json',dict(source_packet=str(ROOT/'clean_source_packet.json'),speech_meanings=str(updated),style_meanings=str(out),choice_meanings=str(ROOT/'fifteen_clean_choice_meanings_before_English.json'),clean_names=str(ROOT/'clean_name_fields.json'),
        ordinary_speeches=260,physical_style_alternatives=48,style_alias_slots=64,style_objects=8,choice_labels=15,choice_objects=5,total_prose_objects=323,control_only_blocks=[128],
        all_clean_meanings_precede_earlier_English_comparison=True,all_native_bindings_contextual_localization_andformatting_pending=True,
        source_virtual_selectors=[207,208,209,214,215,220,254],selector0_is_source_Rafael_actor_not_terminator=True,
        no_global_character_identity_orfuture_dynamic_role_assignment_approval=True,new_credit=0,full_goal_complete=False))
    print('Complete source intake:260 speeches +48 physical personality alternatives/64 aliases +15 choices =323 prose objects;all meanings precede earlier English;no credit.')
