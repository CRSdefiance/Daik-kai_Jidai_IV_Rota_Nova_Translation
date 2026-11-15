"""Seal321 individual prose decisions and24 scoped names; formatting remains blocked."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B196_B215_clean_20261110')
OUT=Path('translations/maria_B196_B215_contextual_review_v1.json')
NAMES=Path('translations/maria_B196_B215_scoped_names_v1.json')
GATES=['source','context','localization','naturalness','formatting']
NAME_REASONS={
3:'Retain approved Maria Li and full Maria Huamei Li. Her practical skepticism, compassion and command belong to the same source captain; they add no marriage, noble title or religious biography.',
4:'Retain Janus Pasar. His mast-fitting injury and modest explanation establish no new rank or relationship to the port worker.',
6:'Retain Julio Erneco, matching フリオ/エルネコ. Keep his reluctant figurehead assistance distinct from Maria; conventional Father addresses the priest, not a newly invented relative.',
10:'Retain Xien Yan. His cautious distinction between a swindler and a proven thief, and his glass identification, add no grandfather kinship or official judicial rank.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. Repair the letter signature Ludwayer to this exact full consumer. His gambling joke neither adds a new name nor confirms the statue works.',
13:'Retain established Cesare Tony, source チェザーレ/トーニ. His Russian-history explanation and officious arrow-rumor rant are not Carlo or Samwell; no military title is added to the nameplate.',
16:'Retain Gerhard Adernkatz. His confident historical explanation and compliment to Maria are character speech, not a new historical identity or noble rank.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort. The existing full signature already agrees with the native name. Reporting sailors in West Africa adds neither an eyewitness claim nor a new occupation.',
19:'Retain Carlo Sinat. His Herophilus-book account and uncertain memory do not make him an officially titled physician or another source actor.',
20:'Retain Fernando Dias, distinct from Fernan Silveira. Jam names Fernando in the gambling joke, and the boast about500 years belongs to this actor.',
21:'Retain Ian Dukov. Restore Ian in familiar letter announcements and the complete Ian Dukov signature. Cesare explaining Russian history does not expand Ian into a new royal or scholarly title.',
22:'Retain Samwell Khan and full Samwell da Khan. His repeated equipment pitches and pride in research do not invent an occupation, family relationship or biography from the middle component.',
23:'Retain Manuel Almeida. His Attila lesson, library discovery and artist-tool joke do not create a poet, priest or official historian nameplate.',
25:'Retain Yifa Sol. Martial-arts practice and reference to a personal teacher do not assign that teacher to Maria or supply an unsupported new rank.',
26:'Retain Julian Lopes for actor26. His teasing conversation with Safia does not merge him with actor63 Julian Vermeer or establish a romance as fact.',
67:'Retain established Gabriel Cardocci, source ガブリエル/カルドッチ. The glass fraud and escape supply no reason to impose a speculative historical spelling, rename him generically or invent a completed arrest.',
92:'Retain Barkeep for the reusable tavern role. Francisca explicitly mentions her father, but the barkeep is not identified as that father; do not turn regional metadata into a surname or treat reuse as one person across towns.',
113:'Retain Port Worker. The familiar address to Janus is not brotherhood; the lost-gloves boast supplies no personal name or new rank.',
139:'Retain Priest for 神父. Father is an appropriate direct religious address in the church exchange, not evidence of family kinship.',
151:'Retain Sailor on the progressive nameplate and Retainer in the separate catalogue. The hero-play opponent uses this source selector; the Boy label belongs to actor162 and must not be propagated by guesswork.',
156:'Retain current-fallback Sailor/Retainer forms. Source208 is unassigned in the observed startup and falls back to156/voice4; this is not proof of a future conditional crew assignment or a new personal identity.',
162:'Retain Boy for the explicitly 男の子 role playing Charles Martel. Do not infer an additional personal name or relabel the other actor solely from the game discussion.',
186:'Retain Francisca. Stockholm is regional metadata, not her surname. The stolen ornament is explicitly a gift from her father; gratitude supplies no romance or new family tie to the barkeep.',
197:'Retain Safia. Basra is regional metadata, not a surname. Covered hair and mutual teasing do not establish a religion, marriage or confirmed relationship with Julian.',
}
AMENDMENTS={
'SC3_B196_STYLE_8_192':("Admiral, a letter's come in from Ian.",'Place the contraction naturally after letter rather than risk a misleading possessive reading of Ian\'s.'),
'DK4_MES_B197_R0025':("I had that story about the Medusa Shield on my mind. They say it's in the Tasman Sea. Looking into your eyes reminded me of it.",'Use the exact installed Medusa Shield label while retaining the rumor and flirtatious transition.'),
'DK4_MES_B201_R0020':("Well, apparently someone once made a shield from its hide. They called it Armadillo Hide.",'Use the installed Armadillo Hide name; the preceding iron-hard-hide description preserves the source material claim.'),
'DK4_MES_B209_R0032':("It's about a statue of a spirit beast made during the Gupta dynasty. Apparently it can see the future.",'Use the registered spirit-beast noun naturally without inserting an unspoken formal catalogue title or asserting the power is real.'),
'DK4_MES_B213_R0107':("Take it back to its rightful owner. I'll bet that scoundrel's up to other crooked business too. Next time I see him, I'll turn him over to the governor's office!",'Treat governor\'s office as the descriptive authority in the barkeep\'s threat, not an invented capitalized UI instruction.'),
'DK4_MES_B215_R0086':('You can head back first.','Keep the corrected Maria-to-Julio direction in natural speech without the repetitive head-back-ahead phrase.'),
}


def main():
    proof_path=ROOT/'prose_gates_v1.json'
    assert not any(p.exists() for p in [OUT,NAMES,proof_path])
    paths=[ROOT/n for n in ['contextual_comparisons_v1.json','scoped_names_macros_reference_v2.json',
        'scoped_terms_reference_v1.json','dynamic_roles_current_v1.json','current_objects_v1/current_objects.json']]
    proposals,names,terms,roles,objects=map(load,paths);runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,terms,roles,objects])
    assert (proposals['records_count'],proposals['revised'],proposals['retained'])==(321,171,150)
    assert {r['actor_ID'] for r in names['records']}==set(NAME_REASONS) and len(names['records'])==24
    assert names['original_native_name_getters']==48 and roles['source_selectors']==[208]
    native_roles={r['source_selector']:r for r in roles['native_roles']['rows']}
    assert native_roles[207]['resolved_actor_ID']==3 and native_roles[208]['resolved_actor_ID']==156 and native_roles[208]['source_voice_class']==4
    assert len(objects['style_records'])==21 and len(objects['choice_records'])==4
    assert len(terms['items'])==13 and terms['UI'][0]['current']['text']=='Spirit'
    item_forms={r['source']['text']:r['current']['text'] for r in terms['items']}
    assert item_forms['メデューサの盾']=='Medusa Shield' and item_forms['アルマジロの鉄皮']=='Armadillo Hide'
    forms={};scoped=[]
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=NAME_REASONS[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B196_B215_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean/current Maria B196–B215 exchanges; exact scoped name and role consumers only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=runtime['candidate'],candidate_sha256=runtime['candidate_sha256'],actor_ID=actor,
                original_consumers=row['current_consumers']),finding=reason,localization_note=reason,retention_reason=reason,
            decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    rows=deepcopy(proposals['records']);changes=[]
    for row in rows:
        before=text=row['proposed_English']
        if row['id'] in AMENDMENTS:
            text,note=AMENDMENTS[row['id']];assert before!=text
            changes.append(dict(id=row['id'],before=before,after=text,reason=note,source_reference=row['source_reference'],current_reference=row['current_reference']))
            row['finding']+=' '+note;row['localization_note']=row['finding'];row.update(decision='revision',retention_reason='')
        assert text.isascii() and text.strip()==text and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert all(text.count(t)==row['source_macros'].get(t,0) for t in ['FI','FA','FO','FU'])
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention')
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        assert not any(row['review'].values())
        if row['decision']=='retention':assert row['retention_reason']
        source_kind,selector=row['kind'],row.get('source_selector')
        if source_kind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response in the original conditional exchange'
        elif source_kind=='physical-style-alternative':
            assert selector==208
            kind,speaker='progressive',f'Dynamic style selector208; original voice slots{row["source_style_indices"]}; future assignment unvisited'
            obj=next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
            row.update(native_object_kind='4100-style-alternative',source_object_hex=obj['source_object_hex'],
                source_choice_object_hex=obj['source_object_hex'],virtual_formatter_prefix_not_in_stored_body=True,
                current_record_index=row['current_reference']['physical_record_index'])
        else:
            assert source_kind=='ordinary-speech'
            if selector==254:
                assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_hex'].startswith('fe')
                kind,speaker='system-FE','FE system message; no actor nameplate'
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            else:
                assert selector in forms
                kind,speaker='progressive',forms[selector]
        row.update(english=text,logical_English=text,proposed_English=text,original_source_kind=source_kind,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},names_terms_consumers_andfresh_display_approval_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,scoped_prose_name_term_references=[str(NAMES),str(paths[2]),str(paths[3])],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts,kinds=Counter(r['decision'] for r in rows),Counter(r['kind'] for r in rows)
    assert counts=={'revision':171,'retention':150} and kinds=={'progressive':315,'system-FE':2,'typed-choice-label':4}
    assert len(changes)==6 and len(rows)==321
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=proposals['blocks'],records=rows,
        source_objects=321,complete_exchanges=18,proposed_revisions=171,justified_retentions=150,runtime=runtime,
        current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],scoped_name_term_andreadaloud_amendments=changes,
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        all321_paragraphs_read_in18_complete_exchanges=True,native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed release gate')
    save(NAMES,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=scoped,runtime=runtime,scoped_actors=24,individual_name_retentions=24,first_four_gates_pass=True,
        formatting_gates_pending=True,no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [*paths,Path(__file__)]}))
    doc['evidence'][str(NAMES)]=digest(NAMES);save(OUT,doc)
    save(proof_path,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=321,complete_exchanges=18,
        revisions=171,retentions=150,scoped_name_retentions=24,first_four_individual_gates_pass=True,all_fifth_gates_false=True,
        exact_macro_counts={t:sum(r['source_macros'].get(t,0) for r in rows) for t in ['FI','FA','FO','FU']},
        structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,amendments=changes,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed321 four-gate prose reviews:171 revisions/150 retentions,24 scoped names; fresh formatting/release remain.')


if __name__=='__main__':main()
