"""Seal individual contextual prose/name gates while leaving all display gates pending."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

GATES=['source','context','localization','naturalness','formatting']
OUT=Path('translations/maria_B137_B151_contextual_review_v1.json')
NAME_REASONS={
3:'Retain approved Maria Li and the full Maria Huamei Li consumer. No Sir or new royal title follows from her identity; the pirate princess address is a taunt only.',
6:'Retain Julio Erneco, directly matching フリオ/エルネコ and his spoken introduction. The age rivalry does not make him retired or related to Xien.',
10:'Retain Xien Yan and both exact consumers. Old-man rivalry and familiar address do not establish grandfather kinship.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan; the middle component belongs to the full-name consumer and is not added to every spoken address.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. Restore the explicitly spoken Yukihisa rather than the unsupported Yuki shortening.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort as established source-qualified forms; his teasing is not a rank or family label.',
20:'Retain Fernando Dias in both consumers, preserving the complete source given name and already-corrected native field.',
21:'Retain Ian Dukov, supported by イアン/ドゥーコフ. The vodka joke does not license added nationality or biography.',
23:'Retain Manuel Almeida. His prior sailing and carpentry do not justify adding Captain, Master or another title to his name.',
25:'Retain Yifa Sol, matching イファ/ソル and the installed spelling. Her familiar older-sister/brother addresses do not establish family.',
26:'Retain Julian Lopes. His actual grandfather relationship stays in the dialogue, while his courtship does not establish an accepted date or marriage.',
76:'Retain Mikhail Letzel and full Mikhail Volk Letzel. The scholar role does not require adding Doctor to either native name, and the womens old-man address is not grandparent kinship.',
81:'Retain Sanghyeon Kan, matching サンヒョン/カン and both consumers; reconcile provisional Sang Hyeon to the installed given name. He is a senior fellow student, not a biological brother.',
87:'Retain Shopkeeper as the natural generic equivalent of 広場の店主. The Southeast Asian field is regional metadata, not part of the spoken label or an invented personal name.',
153:'Retain the qualified progressive Sailor/full Retainer distinction for 配下 in this naval crew context. Do not substitute unused Arab metadata or assign a new employer or rank.',
165:'Retain Woman as the source-qualified generic participant. The original couple metadata does not make her Wife or establish age in the Mikhail exchange.',
166:'Retain Lady for 貴婦人 in both the Mikhail conversation and bread exchange. Do not append Europe1 or infer a husband for this speaker.',
167:'Retain Lady for 貴婦人. Her bread dialogue explicitly supports her own husband, but Wife would unnecessarily replace the recurring role label.',
168:'Retain Lady for 貴婦人 as the curious bread-baking learner. Neither Europe3 metadata nor the other womans husband establishes her identity or marriage.',
174:'Retain Owner for オーナー, the natural business-role label for the imperious food-trend speaker; no restaurant name, noble title or marriage is supplied.',
175:'Retain Cook for コック. The cooking instructions support this role without promoting the respondent to an unsupported chef rank or business owner.',
183:'Retain Angel as the source nickname エンジェル, not a supernatural identity or replacement Pirate rank.',
184:'Retain Snake as the source nickname スネーク, not a literal species or newly invented gang position.',
185:'Retain Dandy as the source nickname ダンディー. Its spoken chuckle does not justify adding a leader title.',
201:'Retain Mihwa for 美華 in the actual name consumers. Hangzhou metadata is not a surname or a reason to relabel her as Julians partner.',
202:'Retain Reika for 麗姫, preserving the installed proper name rather than reading a character in it as a Princess rank. Seoul remains location metadata.',
}
AMENDMENTS={
'DK4_MES_B138_R0097':("Assign officers with high Speech to the First Mate's Office and Chapel. They can ease discontent among the sailors.",
    'Use the exact active Speech skill and approved expanded First Mate room label, preserving both assignments and the morale effect.'),
'DK4_MES_B138_R0101':("The staff in the Galley and Nursery can reduce the fleet's consumption of water and food.",
    'Use the installed Nursery room label, preserving assigned personnel as the cause of reduced consumption.'),
'DK4_MES_B138_R0105':('A Surgeon assigned to the Sickbay can treat fatigue, disease and injuries among your companions and sailors.',
    'Match the installed Sickbay and reviewed Surgeon role while preserving all conditions and both groups of people.'),
'DK4_MES_B138_R0109':('Sick or injured navigators recover faster when assigned to a Private Cabin or the Recreation Room.',
    'Use the approved expanded Cabin/Lounge labels from exact installed Help pages; keep the navigator distinction and faster recovery.'),
'DK4_MES_B138_R0113':('A Shipwright like me can repair damage at sea in the Lumber Room. I can also help with refitting and repairs at shipyards.',
    'Match the reviewed Shipwright role and installed Lumber room term without changing the separate at-sea and shipyard benefits.'),
'DK4_MES_B144_R0017':('The Silla Gold Crown... Such radiant gold. Breathtakingly beautiful...',
    'The original proposed retention fails the item-name consistency check: the exact registered catalogue name is Silla Gold Crown. Retain the otherwise natural admiration.'),
}


def main():
    nameout=Path('translations/maria_B137_B151_scoped_names_v1.json');proofout=ROOT/'prose_gates_v1.json'
    assert not any(p.exists() for p in [OUT,nameout,proofout])
    paths=[ROOT/n for n in ['all335_contextual_proposals_v1.json','scoped_names_macros_reference_v1.json','scoped_terms_reference_v1.json','current_objects_v1/current_objects.json']]
    proposals,names,terms,objects=map(load,paths);runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,terms,objects])
    assert (proposals['records_count'],proposals['revised'],proposals['retained'])==(335,184,151)
    assert {r['actor_ID'] for r in names['records']}==set(NAME_REASONS) and len(names['records'])==26
    assert terms['active_Speech_skill']['current']['text']=='Speech'
    assert len(terms['room_labels'])==len(terms['exact_current_HELP_pages'])==8 and terms['items'][0]['current']['text']=='Silla Gold Crown'
    assert len(objects['style_records'])==0 and len(objects['choice_records'])==2
    forms={};scoped=[]
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=NAME_REASONS[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B137_B151_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean Maria B137–B151 exchanges and both exact native identity consumers; scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    rows=deepcopy(proposals['records']);changes=[]
    for row in rows:
        assert not any(row['review'].values())
        before=text=row['proposed_English'];notes=[]
        if 'Sang Hyeon' in text:
            text=text.replace('Sang Hyeon','Sanghyeon');notes.append('Reconcile the provisional given-name spacing to the exact Sanghyeon native consumers without changing the nonfamilial relationship.')
        if row['id'] in AMENDMENTS:
            text,note=AMENDMENTS[row['id']];notes.append(note)
        if notes:
            assert before!=text;changes.append(dict(id=row['id'],before=before,after=text,reason=' '.join(notes)))
            row['finding']+=' '+' '.join(notes);row['localization_note']=row['finding'];row.update(decision='revision',retention_reason='')
        assert text.isascii() and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert re.findall(r'\bF[IAOU]\b',text)==re.findall(r'F[IAOU]',row['source_Japanese']),row['id']
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention'),row['id']
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        if row['decision']=='retention':assert row['retention_reason']
        sourcekind=row['kind'];selector=row.get('source_selector')
        if sourcekind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response to Manuels offered room tutorial'
        else:
            assert sourcekind=='ordinary-speech' and (selector<207 or selector==254)
            if selector==254:
                kind='system-FE';speaker={139:'Native FE tutorial about Mikhail and item information',145:'Unidentified female pirate in a native FE panel; no actor nameplate',
                    149:'Native FE Seville banana-fashion forecast',150:'Native FE Genoa tomato-fashion forecast',151:'Native FE Amsterdam wheat-fashion forecast'}[row['block']]
                assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_hex'].startswith('fe')
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            else:kind,speaker='progressive',forms[selector]
        row.update(independent_English_draft=row['english'],english=text,logical_English=text,proposed_English=text,
            original_source_kind=sourcekind,kind=kind,speaker=speaker,context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],
            native_literal_token_counts=row['source_macros'],review={g:g!='formatting' for g in GATES},
            names_terms_consumers_andfresh_display_approval_pending=False,approved_names_terms_titles_andruntime_substitutions_pending=False,
            scoped_prose_name_term_references=[str(nameout),str(paths[2])],final_whole_exchange_readaloud_review_complete=True,
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts=Counter(r['decision'] for r in rows);kinds=Counter(r['kind'] for r in rows)
    assert counts=={'revision':185,'retention':150} and kinds=={'progressive':315,'system-FE':18,'typed-choice-label':2}
    assert len(changes)==12 and sum(sum(r['source_macros'].values()) for r in rows)==21
    assert not any(t in r['english'] for r in rows for t in ['Sang Hyeon','Golden Crown of Silla','Persuasion',"Adjutant's Room",'Livestock Room','Infirmary','Timber Room'])
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=GATES,file_path='/data/SC3.DK4',blocks=list(range(137,152)),records=rows,source_objects=335,complete_exchanges=15,
        proposed_revisions=185,justified_retentions=150,runtime=runtime,current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],
        scoped_name_term_andreadaloud_amendments=changes,all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        all335_paragraphs_read_in15_complete_exchanges=True,no_dynamic_roles_orstyle_objects_in_source_scope=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:
        assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed release gate')
    save(nameout,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',records=scoped,
        runtime=runtime,scoped_actors=26,individual_name_retentions=26,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]}))
    doc['evidence'][str(nameout)]=digest(nameout);save(OUT,doc)
    save(proofout,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=335,complete_exchanges=15,revisions=185,retentions=150,
        scoped_name_retentions=26,first_four_individual_gates_pass=True,all_fifth_gates_false=True,amendments=changes,
        structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed335 contextual prose reviews:185 revisions/150 retentions,26 scoped names;first four gates pass,fresh formatting/release remain pending.')


if __name__=='__main__':main()
