"""Seal all clean ordinary/style/caption meanings without consulting current dialogue."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B211_B230_clean_20261104')
VOICE = {
    0:'Conversational and politely helpful; ordinary ending.',
    1:'Respectful and formal, using a more formal word for a letter.',
    2:'Conversational, slightly casual but still polite.',
    3:'Gentle and polite, with the source feminine register; no invented relationship.',
    4:'Rougher familiar delivery with an assertive ending.',
    5:'Older-speaker diction and a familiar declarative ending.',
    6:'Childlike informal address and simple wording; do not force baby talk.',
    7:'Expansive adult polite delivery; preserve the source alias where slot2 also owns7.',
}

if __name__ == '__main__':
    target=ROOT/'complete_clean_meanings_checkpoint_v1.json'; combined=ROOT/'complete_clean_meanings_before_English.json'
    styles_out=ROOT/'all29_clean_style_meanings_before_English.json'; captions_out=ROOT/'all7_clean_caption_meanings_before_English.json'
    assert not any(p.exists() for p in [target,combined,styles_out,captions_out])
    packet_path=ROOT/'clean_source_packet.json'; choice_path=ROOT/'clean_choice_objects.json'; style_path=ROOT/'clean_style_objects.json'
    packet,choices,styles=map(load,[packet_path,choice_path,style_path])
    parts=[ROOT/(name+'_clean_meanings_before_English.json') for name in ['B211_B215','B216_B220','B221_B225','B226_B230']]
    ordinary=[r for p in parts for r in load(p)['records']]
    source={r['id']:r for g in packet['groups'] for r in g['records']}
    assert len(ordinary)==len(source)==241 and len({r['id'] for r in ordinary})==241
    for r in ordinary:
        assert all(r[k]==source[r['id']][k] for k in ['source_reference','source_hex','source_Japanese','source_complete_preamble_hex','source_selector'])
    contexts={g['block']:load(p)['source_fidelity_notes'].get(str(g['block']),[]) for p in parts for g in packet['groups'] if str(g['block']) in load(p)['source_fidelity_notes']}
    style_rows=[]
    for r in styles['records']:
        indices=r['source_style_indices']; assert indices and all(i in range(8) for i in indices)
        if r['block']==213 and r['source_command_offset']==702:
            if indices==[6]: meaning='The dynamic companion says the writing is so difficult that they cannot understand what it says.'
            else: meaning='The dynamic companion remarks that the writing is difficult and characteristic of Yukihisa.'
            context='After Yukihisa’s formal Muramasa letter; the selected companion personality reacts, with a separate Jam branch in ordinary dialogue.'
        else:
            author={213:'Yukihisa',218:'Jenas',226:'Ian'}[r['block']]
            meaning=f'The dynamic companion informs the admiral that a letter from {author} has arrived.'
            context=f'Before the complete letter scene in B{r["block"]}; preserve all eight original personality selector aliases without assigning actor208 a fictional static name.'
        style_rows.append(dict(**r,source_meaning=meaning,exchange_context=context,
            personality_voice_notes=[dict(source_index=i,register=VOICE[i]) for i in indices],
            no_current_ROM_English_intake_for_this_batch=True,source_only_not_localized_English=True))
    assert len(style_rows)==29 and styles['object_count']==4 and styles['style_alias_slots']==32
    save(styles_out,dict(records=style_rows,source_meanings=29,physical_objects=4,alias_slots=32,all_source_alias_memberships_preserved=True,
        source_reference=str(style_path),source_reference_sha256=sha(style_path.read_bytes()),no_current_English_intake=True,new_credit=0))
    caption_rows=[]
    for r in choices['records']:
        b,c,i=r['block'],r['source_command_offset'],r['source_index']
        if (b,c)==(216,64):
            meaning=['Affirm familiarity with Romance of the Three Kingdoms.','Say that the work is unfamiliar.'][i]
            context='First knowledge menu; the unfamiliar branch recommends reading, while familiarity leads to the favorite-commander menu.'
        elif (b,c)==(216,230):
            meaning=['Choose Zhao Yun as the favorite commander.','Choose Guan Yu as the favorite commander.','Choose Zhuge Liang as the favorite commander.'][i]
            context='Second menu in the complete novel conversation; only the matching Zhao Yun preference yields the legendary-spear lead.'
        else:
            assert (b,c)==(224,138)
            meaning=['Say that the Crusades are familiar.','Say that the Crusades are unfamiliar.'][i]
            context='Both knowledge branches retain their distinct opening before converging on the shopkeeper’s criticism and the Saladin discussion.'
        caption_rows.append(dict(**r,source_meaning=meaning,exchange_context=context,
            no_current_ROM_English_intake_for_this_batch=True,source_only_not_localized_English=True))
    assert len(caption_rows)==7 and choices['object_count']==3
    save(captions_out,dict(records=caption_rows,source_meanings=7,physical_objects=3,
        source_reference=str(choice_path),source_reference_sha256=sha(choice_path.read_bytes()),no_current_English_intake=True,new_credit=0))
    rows=ordinary+style_rows+caption_rows
    assert len(rows)==len({r['id'] for r in rows})==277
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=load(ledger_path)
    completed={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    overlap=completed & {(r['file_path'],r['id']) for r in rows};assert not overlap
    assert len(completed)==ledger['records_editorially_completed']==9933 and not ledger['full_goal_complete']
    empty=[g['block'] for g in packet['groups'] if not g['records'] and not any(o['block']==g['block'] for o in choices['objects']+styles['objects'])]
    assert empty==[222] and len(packet['groups'])==20
    evidence={str(p):sha(p.read_bytes()) for p in [packet_path,choice_path,style_path,ROOT/'clean_name_fields.json',*parts,styles_out,captions_out,Path(__file__)]}
    save(combined,dict(records=rows,speech_records=241,physical_personality_alternatives=29,caption_records=7,complete_blocks=20,
        source_parts=evidence,no_current_ROM_English_dialogue_extraction_in_this_intake=True,no_localized_drafts=True,
        no_blanket_before_any_historical_English_exposure_claim=True,native_identity_terms_localization_comparison_anddisplay_pending=True,new_credit=0))
    save(target,dict(total_editorial_objects=277,ordinary_speeches=241,physical_personality_alternatives=29,physical_style_objects=4,personality_alias_slots=32,
        typed_caption_records=7,typed_choice_objects=3,source_meanings_saved=277,remaining_ordinary_meanings=0,remaining_compound_meanings=0,
        localized_drafts=0,current_English_comparisons=0,complete_clean_meanings=str(combined),complete_clean_meanings_sha256=sha(combined.read_bytes()),
        complete_blocks=list(range(211,231)),control_only_blocks=empty,completed_overlap=[],completed_keys_checked=len(completed),completed_ledger_sha256=sha(ledger_path.read_bytes()),
        ordinary_actor_IDs=sorted({r['source_selector'] for r in ordinary if r['source_selector']<207}),special_selectors=[208,254],
        native_identity_andterms_still_pending=True,no_current_ROM_English_extraction_in_this_intake=True,no_all_prior_English_exposure_claim=True,
        source_cultural_claims_andcharacter_viewpoints_retained_not_historically_rewritten=True,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={**evidence,str(combined):sha(combined.read_bytes())}))
    print('Sealed277 clean meanings:241 ordinary,29 physical style alternatives,seven captions;zero completed overlaps. No English drafts/current extraction.')
