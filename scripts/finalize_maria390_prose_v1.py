"""Seal individual contextual prose/name gates; all display gates remain pending."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')
GATES=['source','context','localization','naturalness','formatting']
PROPER={
3:'Retain approved Maria Li/Maria Huamei Li, without new family, royal or military details.',
6:'Retain Julio Erneco from the clean name components; his enthusiasm for a legendary drink does not establish its identity.',
10:'Retain Xien Yan and his distinguished formal voice; familiar address does not establish grandfather kinship.',
12:'Retain Yukihisa Shiraki/Genjo full form. His Namahage recognition and dream explanation remain personal accounts.',
15:'Retain Angelo Puccini from the exact clean first/surname fields; the startled object reaction supplies no new biography.',
18:'Retain Charles Rochefort/Charles Jean Rochefort and his rare-book enthusiasm, without inventing the book giver as a thief.',
19:'Retain Carlo Sinat; his help to a collapsed stranger does not make him a doctor.',
20:'Retain Fernando Dias in the bargaining alternatives; no guarantee of a successful lower price follows from his advice.',
21:'Retain Ian Dukov; the seller is not made his lover, and the celestial identity remains a hypothesis.',
25:'Retain Yifa Sol; the bargaining aside gives no invented family or romantic relationship.'}
ROLE_GROUPS=[
([82,85,86,87],'Retain Shopkeeper for the source town-square shop role. The square is a location, not a needed awkward name prefix; regional metadata is not a new personal name.'),
([92],'Retain Barkeep for the tavern proprietor. The familiar source address does not mean a biological father.'),
([96,103],'Retain Patron for a tavern customer without adding ethnicity, age, profession or kinship from regional metadata.'),
([104,105],'Retain Trader for the trading-post role; familiar address in the rope sale does not establish fatherhood.'),
([110],'Retain the established Shipwright role without inventing rank or biography from the art discussion.'),
([113,115,117,119],'Retain Port Worker for the harbor-office role; source familiar big-brother address does not establish kinship.'),
([130],'Retain Daimyo, the explicit Japanese title. This supports the subordinate my lord address without inventing a named ruler.'),
([132],'Retain Priest for the source ritual officiant, without assigning a denomination, named religious figure or additional rank from regional metadata.'),
([140],'Retain Innkeeper for the lodging proprietor; the source auntie-style designation is not a family relationship.'),
([147,148,150],'Retain Guildmaster for the explicit guild head. Collecting paintings or attending the daimyo does not change the profession.'),
([152,153,154,155,156,157,159],'Retain the already qualified distinct Sailor progressive/Retainer full consumers for the generic source follower model. Do not replace an actual display alias from unused regional metadata.'),
([164],'Retain Man in the recurring pair: their closeness is supported, but the tea and fur conversations do not explicitly establish marriage.'),
([165],'Retain Woman in the recurring pair without converting her into Wife or inventing age.'),
([166,167,168],'Retain Lady for the refined female social role; the gift wishes and cooking friendships do not create a spouse or specific noble title.'),
([169],'Retain Alluring Woman for the explicitly female source label and flirtatious book seller. Do not promote Ian\'s celestial-maiden guess into her name.'),
([172],'Retain the approved Stranger label; the source collapse is conveyed by the scene, without naming a disease or importing unused sailor metadata.'),
([173],'Retain the approved Shady Man label for the suspicious seller. Do not call him a thief or make the bargaining advice refer to a woman.'),
([174],'Retain Owner for the explicit owner role in the sweetness dispute, without inventing family ties to the cook.'),
([175],'Retain Cook for the explicit food-preparation role, preserving the resigned response to the owner without new rank.')]
AMENDMENTS={
'DK4_MES_B153_R0072':('Scents may soon be popular in Lisbon.','Use the original current category getter\'s Scents label, distinct from Spices; preserve the prospective forecast.'),
'DK4_MES_B155_R0061':('Gems may soon be popular in London.','Use the exact Gems category, distinct from Jewelry, without identifying an unspecified gemstone.'),
'DK4_MES_B156_R0094':('Artwork may soon be popular in Basra.','Match the installed Artwork merchandise label in the forecast; ordinary conversation may still say paintings.'),
'DK4_MES_B162_R0064':('China may soon be popular in Hamburg.','Match the installed China merchandise label in the forecast; retain ceramics in the connoisseurs\' conversation.'),
'DK4_MES_B174_R0078':('Carlo: Wits +1!','Correct singular Wit to the exact installed Wits attribute while retaining the concise functional notice.'),
'DK4_MES_B175_R0054':("Let's see. 'Glassmaking Guide'...",'Use the exact registered Glassmaking Guide title for the source glassmaking-methods dictionary.')}


def main():
    out=Path('translations/maria_B152_B175_contextual_review_v1.json')
    nameout=Path('translations/maria_B152_B175_scoped_names_v1.json')
    proofout=ROOT/'prose_gates_v1.json';termout=ROOT/'scoped_terms_reference_v2.json'
    assert not any(p.exists() for p in [out,nameout,proofout,termout])
    paths=[ROOT/p for p in ['all390_contextual_proposals_v1.json','scoped_names_macros_reference_v1.json',
        'scoped_terms_reference_v1.json','scoped_category_terms_v1.json','current_objects_v1/current_objects.json']]
    proposals,names,terms,categories,objects=map(load,paths);runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,terms,categories,objects])
    assert (proposals['records_count'],proposals['revised'],proposals['retained'])==(390,152,238)
    assert terms['exact_bound_terms']==34 and categories['scoped_native_category_calls']==4
    assert [r['English'] for r in categories['records']]==['Scents','Gems','Medicine','Dyes']
    assert len(objects['choice_records'])==17 and not objects['style_records']
    reasons=dict(PROPER)
    for actors,reason in ROLE_GROUPS:
        for actor in actors:assert actor not in reasons;reasons[actor]=reason
    assert set(reasons)=={r['actor_ID'] for r in names['records']} and len(reasons)==47
    scoped=[];forms={}
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=reasons[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B152_B175_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean Maria B152–B175 exchanges and both actual native identity consumers; scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    rows=deepcopy(proposals['records']);changes=[]
    for row in rows:
        assert not any(row['review'].values())
        before=text=row['proposed_English']
        if row['id'] in AMENDMENTS:
            text,note=AMENDMENTS[row['id']];assert text!=before
            changes.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],before=before,after=text,reason=note))
            row['finding']+=' '+note;row['localization_note']=row['finding'];row.update(decision='revision',retention_reason='')
        assert text.isascii() and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert re.findall(r'\bF[IAOU]\b',text)==re.findall(r'F[IAOU]',row['source_Japanese'])
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention')
        assert row['source_meaning'] and row['finding'] and row['whole_exchange_context']
        sourcekind=row['kind'];selector=row.get('source_selector')
        if sourcekind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response in the complete bargaining/book exchange'
        elif selector==254:
            assert row['source_complete_preamble_hex']=='0040ffff00fe'
            kind='system-FE';speaker='Unidentified Namahage-scene voice; no static actor assignment' if row['block']==171 else 'Native system notice or scene sound effect'
            row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
        else:
            assert sourcekind=='ordinary-speech' and selector<207;kind,speaker='progressive',forms[selector]
        row.update(independent_English_draft=row['english'],english=text,logical_English=text,proposed_English=text,
            original_source_kind=sourcekind,kind=kind,speaker=speaker,context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],
            native_literal_token_counts=row['source_macros'],review={g:g!='formatting' for g in GATES},
            names_terms_consumers_andfresh_display_approval_pending=False,approved_names_terms_titles_andruntime_substitutions_pending=False,
            scoped_prose_name_term_references=[str(nameout),str(termout)],final_whole_exchange_readaloud_review_complete=True,
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts=Counter(r['decision'] for r in rows);kinds=Counter(r['kind'] for r in rows)
    assert counts=={'revision':153,'retention':237} and kinds=={'progressive':341,'system-FE':32,'typed-choice-label':17}
    assert len(changes)==6 and sum(sum(r['source_macros'].values()) for r in rows)==5
    historical=next(r for r in rows if r['id']=='DK4_MES_B172_R0008')
    assert 'ロッコ＝アレムケル' in historical['source_Japanese'] and 'Rocco Alemkel' in historical['english']
    save(termout,dict(runtime=runtime,pointer_terms=terms['records'],category_terms=categories['records'],
        all_five_previous_term_leads_resolved=True,descriptive_Sweets=categories['descriptive_Sweets'],prose_alias_notes=terms['prose_alias_notes'],
        historical_Rocco_reference=dict(id=historical['id'],source_reference=historical['source_reference'],source_hex=historical['source_hex'],
            current_reference=historical['current_reference'],current_hex=historical['current_hex'],English='Rocco Alemkel',
            source_spoken_name_andindependent_transliteration_agree=True,not_in_actor_catalogue_no_fake_actor_ID=True),
        native_fonts_widgets_andnew_gameplay_not_approved=True,new_credit=0,evidence={str(p):digest(p) for p in [paths[2],paths[3],paths[0],Path(__file__)]}))
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=GATES,file_path='/data/SC3.DK4',blocks=list(range(152,176)),records=rows,source_objects=390,complete_exchanges=24,
        proposed_revisions=153,justified_retentions=237,runtime=runtime,current_ROM=proposals['runtime']['candidate'],current_ROM_sha256=runtime['candidate_sha256'],
        scoped_prose_name_term_amendments=changes,all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        all390_paragraphs_read_in24_complete_exchanges=True,no_dynamic_roles_orstyle_objects_in_source_scope=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):digest(p) for p in [*paths,termout,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed the release gate')
    save(nameout,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',records=scoped,
        runtime=runtime,scoped_actors=47,individual_name_retentions=47,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]}))
    doc['evidence'][str(nameout)]=digest(nameout);save(out,doc)
    save(proofout,dict(manuscript=str(out),manuscript_sha256=digest(out),records=390,complete_exchanges=24,revisions=153,retentions=237,
        scoped_name_retentions=47,first_four_individual_gates_pass=True,all_fifth_gates_false=True,amendments=changes,
        structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed390 contextual reviews:153 revisions/237 retentions and47 names;four individual prose gates pass;all display/release gates pending.')


if __name__=='__main__':main()
