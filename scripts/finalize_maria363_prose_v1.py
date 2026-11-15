"""Seal363 individually reviewed prose decisions and29 scoped names; no display approval."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B216_B252_clean_20261110')
OUT=Path('translations/maria_B216_B252_contextual_review_v1.json')
NAMES=Path('translations/maria_B216_B252_scoped_names_v1.json')
GATES=['source','context','localization','naturalness','formatting']
REASONS={
3:'Retain approved Maria Li and full Maria Huamei Li. Her command, dry wit, compassion and calculated lure do not confer a noble title, marriage or male identity. Correct the man-like-you reference in prose.',
10:'Retain Xien Yan. His order to seize Plett identifies a crew intervention, not a newly invented judicial rank or family relationship.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. The theft-frame grievance and angry recognition belong to Jam; no alternate name or invented previous partnership with Plett is established.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His command to drop the sword supplies no Lord title or new familial relationship.',
13:'Retain Cesare Tony. His earnest figurehead admiration, private reflections and Luck/Charm notices consistently identify Cesare, without a newly named deity or religious office.',
14:'Retain Emilio Ferog. Maria calls him Emilio, followed by his sleep sound; the joke does not justify a different surname spelling or child role label.',
20:'Retain Fernando Dias, distinct from Fernan Silveira. His puzzled and frightened figurehead reactions do not establish a confirmed curse, supernatural identity or new rank.',
22:'Retain Samwell Khan and full Samwell da Khan. His man-eater warning is speculation in the bear encounter, not proof of expertise, biography or a new surname component.',
64:'Retain Yuris Huygens, matching the established source-bound identity. Reconcile Huigen in dialogue. Noble status is explicit, but no particular hereditary title or penniless condition is supported.',
65:'Retain Plett Perrault. Familiar address to Maria is not kinship; the source criminal identity and past framing incident do not establish friendship or a specific final sentence.',
66:'Retain Jean Ramusio. Reconcile Ramgio and independent provisional Ramzio to this installed identity. His French origin is explicit, while his self-praise remains character speech.',
67:'Retain Gabriel Cardocci for source Karudotchi. Reconcile Carducci in dialogue; no speculative historical identity or extra rank is justified by his agreement violations.',
68:'Retain Jacob Portunto. The wanted Dutch smuggler and cargo complaint identify the same actor; neither the nameplate nor fleet requires an invented additional title.',
69:'Retain Peralonso Aguirre. His womanizing and Spanish-spy request identify him without inventing romance, marriage or sisterhood with Maria.',
71:'Retain William Clive. English piracy is explicit; wild shrieks do not make him an animal, prove magic or support a mental-health diagnosis.',
72:'Retain Hernan Berio. Reconcile the independent provisional Berrio to Berio. Self-aggrandizing sama supports great in dialogue, not an invented Lord title.',
92:'Retain Barkeep for the tavern role. Oyaji and Master in these exchanges do not mean father or a new personal name; European regional metadata is not a surname.',
147:'Retain Guildmaster for this local guild role. European metadata is not a surname and reuse across cities does not establish a single travelling person.',
148:'Retain Guildmaster for this local guild role. Islamic-region metadata does not authorize a religious title, personal name or biography.',
149:'Retain Guildmaster for the Chinese-region guild role. Familiar jiesan for Maria is not sisterhood, and region metadata is not a surname.',
154:'Retain Sailor on the progressive nameplate and Retainer in the catalogue. The subordinate complaining about Jean is not assigned a new personal identity or nationality from regional metadata.',
156:'Retain Sailor/Retainer as the two current fallback consumers. Source roles208/211/215/216 are unassigned at startup and resolve to156; this is not a future conditional crew assignment or observed forest participation.',
188:'Retain Margrete, a supported existing form of Marugurete. Hamburg is regional metadata, not her surname; the romantic gold-river image does not establish a relationship with Maria.',
189:'Retain Wanda. Amsterdam is regional metadata, not a surname; regret about local ruins adds no personal biography or relationship.',
190:'Retain Julia. Lisbon is regional metadata, not a surname. Do not merge her with Julian or turn her brief welcome into an invented relationship.',
193:'Retain Myrine for the existing source Myurine identity. Athens metadata is not a surname or proof of a historical/mythological identity.',
195:'Retain Nelly. Alexandria is regional metadata, not her surname; offering directions does not imply that she accompanies Maria to the pyramid.',
196:'Retain Hatra. Sofala is regional metadata, not a surname; the picnic-weather suggestion does not invent a shared outing or romance.',
200:'Retain Titis. Jakarta is regional metadata, not her surname; the personal exception about telling foreigners supplies neither a new ethnicity nor a mythological identity.',
}


def main():
    comparison=ROOT/'contextual_comparisons_v1.json';terms_path=ROOT/'scoped_terms_reference_v1.json';proof_path=ROOT/'prose_gates_v1.json'
    assert not any(p.exists() for p in [OUT,NAMES,comparison,terms_path,proof_path])
    pp=ROOT/'clean_source_packet.json';packet=load(pp);selected=[r for g in packet['groups'] for r in g['records']]
    cp=ROOT/'current_v1/current_effective.json';op=ROOT/'current_objects_v1/current_objects.json'
    np=ROOT/'scoped_names_macros_reference_v2.json';rp=ROOT/'dynamic_roles_current_v1.json'
    current,objects,names,roles=map(load,[cp,op,np,rp]);runtime=current['runtime']
    assert all(x['runtime']==runtime for x in [objects,names,roles])
    assert current['current_ROM_sha256']==runtime['candidate_sha256'] and digest(current['current_ROM'])==runtime['candidate_sha256']
    rows=[];parts=[]
    for part in ['B216_B226','B227_B251','B252']:
        path=ROOT/f'contextual_{part}_v1.json';doc=load(path)
        assert doc['all_five_gates_still_pending'] and doc['runtime']==runtime
        assert doc['source_clean_meanings_andindependent_drafts_preceded_current_intake']
        rows.extend(deepcopy(doc['records']));parts.append(path)
    assert len(rows)==len({r['id'] for r in rows})==len(selected)==363
    for a,b in zip(selected,rows,strict=True):
        assert all(a[k]==b[k] for k in ['id','source_hex','source_reference','source_Japanese'])
        assert b['contextual_comparison_saved'] and b['finding'] and not any(b['review'].values())
        assert bool(b['retention_reason'])==(b['decision']=='retention')
    counts=Counter(r['decision'] for r in rows);assert counts=={'revision':203,'retention':160}
    evidence={str(p):digest(p) for p in [pp,cp,op,np,rp,*parts,ROOT/'clean_draft_seal_v1.json',Path(__file__)]}
    save(comparison,dict(records=rows,records_count=363,complete_exchanges=37,blocks=packet['selected_blocks'],runtime=runtime,
        revised=203,retained=160,all_individual_findings_andretention_reasons_saved=True,all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(current['current_ROM']).read_file('/__arm9__.bin')
    registry_path=Path('translations/deck_view_arm9_v2.json');registry=load(registry_path)
    terms=[]
    for offset,japanese,english in [(1344220,'魅力','Charm'),(1344236,'運勢','Luck')]:
        source=clean[offset:offset+8];target=arm[offset:offset+8]
        registered=next(r for r in registry['records'] if r['offset']==offset)
        assert source.hex().lower()==registered['source_hex'].lower() and registered['english']==english
        assert source.split(b'\0')[0].decode('cp932')==japanese and target.split(b'\0')[0].decode('ascii')==english
        terms.append(dict(offset=offset,length=8,source_hex=source.hex(),current_hex=target.hex(),
            source_Japanese=japanese,current_English=english,registered_record=registered['id']))
    save(terms_path,dict(runtime=runtime,UI=terms,unnamed_figureheads_ruins_andstatues_remain_descriptive=True,
        no_unspoken_catalogue_item_titles_added=True,source_notices_not_executed_stat_effect_proof=True,new_credit=0,
        evidence={str(p):digest(p) for p in [registry_path,cp,Path(__file__)]}))
    assert {r['actor_ID'] for r in names['records']}==set(REASONS) and names['original_native_name_getters']==58
    assert roles['source_selectors']==[207,208,211,215,216]
    resolved={r['source_selector']:r for r in roles['native_roles']['rows']}
    assert resolved[207]['resolved_actor_ID']==3
    assert all((resolved[s]['strict_assignment'],resolved[s]['resolved_actor_ID'],resolved[s]['source_voice_class'])==(208,156,4) for s in [208,211,215,216])
    assert len(objects['style_records'])==85 and len(objects['choice_records'])==12 and objects['native_style_getter_cases']==96
    scoped=[];forms={}
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=REASONS[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B216_B252_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean/current Maria B216-B252 exchanges; exact scoped native name and role consumers only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=runtime['candidate'],candidate_sha256=runtime['candidate_sha256'],actor_ID=actor,original_consumers=row['current_consumers']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,new_credit=0)
        scoped.append(row)
    evidence.update({str(p):digest(p) for p in [comparison,terms_path]})
    for row in rows:
        text=row['proposed_English'];selector=row.get('source_selector');original_kind=row['kind']
        assert text.isascii() and text.strip()==text and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert all(text.count(t)==row['source_macros'].get(t,0) for t in ['FI','FA','FO','FU'])
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention')
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        if original_kind=='typed-menu-caption':kind,speaker='typed-choice-label','Player action in original conditional exchange'
        elif original_kind=='physical-style-alternative':
            assert selector in [208,211,215,216]
            kind,speaker='progressive',f'Dynamic selector{selector}; original voice slots{row["source_style_indices"]}; conditional assignment unvisited'
            obj=next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
            assert obj['source_selector']==selector
            row.update(native_object_kind='4100-style-alternative',source_object_hex=obj['source_object_hex'],
                source_choice_object_hex=obj['source_object_hex'],virtual_formatter_prefix_not_in_stored_body=True,
                current_record_index=row['current_reference']['physical_record_index'])
        elif selector==254:
            assert original_kind=='ordinary-speech' and row['source_complete_preamble_hex']=='0040ffff00fe'
            kind,speaker='system-FE','FE system message; no actor nameplate'
            row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
        else:
            assert original_kind=='ordinary-speech'
            if selector in resolved:
                kind,speaker='progressive',f'Dynamic selector{selector}; startup resolves {forms[resolved[selector]["resolved_actor_ID"]]}; conditional assignment unvisited'
            else:assert selector in forms;kind,speaker='progressive',forms[selector]
        row.update(english=text,logical_English=text,original_source_kind=original_kind,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},names_terms_consumers_andfresh_display_approval_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,scoped_prose_name_term_references=[str(NAMES),str(terms_path),str(rp)],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    assert Counter(r['kind'] for r in rows)=={'progressive':313,'system-FE':38,'typed-choice-label':12}
    save(NAMES,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=scoped,runtime=runtime,scoped_actors=29,individual_name_retentions=29,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,evidence=evidence,new_credit=0))
    evidence[str(NAMES)]=digest(NAMES)
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=packet['selected_blocks'],records=rows,
        source_objects=363,complete_exchanges=37,proposed_revisions=203,justified_retentions=160,runtime=runtime,
        current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,all363_paragraphs_read_in37_complete_exchanges=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,
        evidence=evidence,new_credit=0,full_goal_complete=False)
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed release gate')
    save(OUT,doc)
    save(proof_path,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=363,complete_exchanges=37,
        revisions=203,retentions=160,scoped_name_retentions=29,first_four_individual_gates_pass=True,all_fifth_gates_false=True,
        exact_macro_counts={t:sum(r['source_macros'].get(t,0) for r in rows) for t in ['FI','FA','FO','FU']},
        structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed363 four-gate prose reviews:203 revisions/160 retentions;29 scoped names; formatting/release remain.')


if __name__=='__main__':main()
