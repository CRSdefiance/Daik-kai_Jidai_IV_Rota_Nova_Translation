"""Seal the contextual prose/name pass; fresh formatting remains a release gate."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

GATES=['source','context','localization','naturalness','formatting']
OUT=Path('translations/maria_B125_B136_contextual_review_v1.json')
NAME_REASONS={
3:'Retain Maria Li in the short consumer and user-approved Maria Huamei Li in the full consumer. Her compassion and commanding questions do not add nobility, a marriage or a baptism story.',
7:'Retain Cristina Erneco. Her flamenco performance and drinking conversation establish neither romance with Maria nor a new profession or national biography.',
10:'Retain Xien Yan. The familiar older-man address is not grandfather kinship; his counsel and objections remain those of an experienced companion.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. The energetic food/gambling mishap adds no new rank, actual enslavement or family relationship.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. Formal rescuer speech and a samurai voice do not authorize adding a named rank or new office.',
13:'Retain established Cesare Tony in both current consumers and reconcile the spoken Tohni/Toni variants to Tony. The source name sounds and current registered identity support this familiar spelling; no speculative biographical identity is added.',
15:'Retain Angelo Puccini. Bianca is explicitly his sister and dead in the later confession; his reported fever encounter does not create a living replacement or a newly named ghost actor.',
17:'Retain Al Shin and full Al Ferid Shin with the native component order. He introduces himself only as Al here; do not expand that speech into an unspoken full name or invent national service.',
19:'Retain established Carlo Sinat in both consumers and reconcile the story introduction from Sinato/Cinato to Sinat. Merchant skills and grief do not supply a new scholarly title or warrant a speculative spelling.',
20:'Retain Fernando Dias in both consumers. Restore his spoken first name where the old story repeats Dias; confidence in luck does not add a commissioned rank or alter the coin-toss conditions.',
22:'Retain Samwell Khan and full Samwell da Khan. His childlike bargaining and elephants remark do not establish an elephant-related occupation or a different family name.',
43:'Retain Diogo Escante and full Diogo de Escante for the spoken-reference-only identity. The coup report supplies no basis for changing his name or inventing a new royal title.',
74:'Retain Richard Townsend. Keep the pompous objections and heat complaint without inserting an official rank, noble title or new relationship.',
105:'Retain Trader for the shared trade-house man. Adil is his spoken scene name, not a new global replacement for the reusable role label; the scene does not establish the innkeeper as his wife.',
116:'Retain Port Worker. The absent-party report gives no brother relationship, proper name or gender for the missing referent; regional metadata is not a surname.',
131:'Retain Governor for the explicitly administrative role. The Spain/Escante report does not establish a higher rank or a personal name.',
142:'Retain Innkeeper for the shared inn woman. Her concern and familiarity do not independently establish marriage to Adil or justify a Wife label.',
148:'Retain Guildmaster for the guild leader who fires Al. The role and rough speech do not imply a military command rank or family relationship.',
153:'Retain the already-qualified distinct Sailor and Retainer consumers. Reuse the exact prior scoped alias review rather than replacing the progressive source-qualified Sailor with unused metadata or inventing a named employer for the beating scene.',
164:'Retain Man for the shared male speaker. The complete quarrel establishes a dating couple and breakup, not marriage, fatherhood or a new age category.',
165:'Retain Woman for the shared female speaker. Review her with the paired Man; the breakup supports neither Wife nor a newly invented personal name.',
}

AMENDMENTS={
'DK4_MES_B125_R0007':("Apparently, Escante was planning a coup to break away from Spain. Thanks to you, we stopped it before it could happen.",
    'On the whole-exchange reread, preserve the governor reporting newly learned information with Apparently; the earlier retention was too categorical about the report.'),
'DK4_MES_B126_R0004':("By the way, FI, wouldn't the Ceremonial Knife fit perfectly in the Sun-Crest Sheath?",
    'Reconcile both complete item labels to the exact installed catalogue names, retaining Xien\'s fitting suggestion.'),
'DK4_MES_B130_R0271':("I'm Carlo Sinat. I'm glad to be joining you.",
    'Correct the spoken Sinato and provisional Cinato to registered Carlo Sinat; the earlier retention fails body/nameplate consistency.'),
'DK4_MES_B135_R0294':('Cesare Tony! Thank you very much indeed!',
    'Reconcile both the old Tohni and provisional Toni to the established Cesare Tony name in both native consumers.'),
'DK4_MES_B135_R0348':('Medium ships have either two or three masts. Three masts are faster, of course, but need more Sail Handlers.',
    'Use the exact registered Sail Handler job label while preserving mast counts, speed and additional staffing.'),
'DK4_MES_B135_R0351':("With refitting, you can have up to five Cargo holds. If you don't intend to fight for a while, you won't need Quarters for marines or Batteries for cannons.",
    'Use installed Cargo, Quarters and Battery terminology, explaining the latter two naturally; keep the maximum and noncombat condition.'),
'DK4_MES_B135_R0354':("If you want to open routes to distant towns, add more Supplies holds. You'll be able to sail much farther.",
    'Match the installed Supplies hold label while preserving the range advice and its conditional purpose.'),
'DK4_MES_B135_R0360':("At least your flagship should have Quarters and Batteries. You'll have a hard time winning naval battles without them.",
    'Keep the already-explained native room labels consistent in the combat recommendation.'),
'DK4_MES_B135_R0366':("You'll eventually replace them with large ships, but if you plan to form regional fleets, you may want to keep your old medium ships rather than sell them.",
    'Match regional fleet to the exact reviewed installed Help article; retain eventual replacement and optional reuse of old medium ships.'),
}

def main():
    names_out=Path('translations/maria_B125_B136_scoped_names_v1.json'); proof_out=ROOT/'prose_gates_v1.json'
    assert not any(p.exists() for p in [OUT,names_out,proof_out])
    paths=[ROOT/n for n in ['all337_contextual_proposals_v1.json','scoped_names_macros_reference_v1.json',
        'scoped_terms_reference_v1.json','current_objects_v1/current_objects.json']]
    proposals,names,terms,objects=map(load,paths); runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,terms,objects])
    assert (proposals['records_count'],proposals['revised'],proposals['retained'])==(337,222,115)
    assert {r['actor_ID'] for r in names['records']}==set(NAME_REASONS)
    assert terms['full_Proof_term']['singular']=='Proof of Conquest'
    assert {r['current']['text'] for r in terms['items']}=={'Ceremonial Knife','Sun-Crest Sheath'}
    assert len(objects['style_records'])==0 and len(objects['choice_records'])==2
    forms={}; scoped=[]
    for original in names['records']:
        row=deepcopy(original); actor=row['actor_ID']; reason=NAME_REASONS[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B125_B136_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean Maria B125–B136 exchanges and exact native short/full identity consumers; scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    rows=deepcopy(proposals['records']); changes=[]
    for row in rows:
        # Select the reviewed proposal, never silently revert to the independent draft.
        before=text=row['proposed_English']
        if row['id'] in AMENDMENTS:
            text,note=AMENDMENTS[row['id']]; assert before!=text
            changes.append(dict(id=row['id'],before=before,after=text,reason=note))
            row['finding']+=' '+note; row['localization_note']=row['finding']; row.update(decision='revision',retention_reason='')
        assert text.isascii() and not any(t in text for t in ['\n','\r','{LB','{ALIGN','{PAD'])
        assert sorted(re.findall(r'\bF[IAOU]\b',text))==sorted(re.findall(r'F[IAOU]',row['source_Japanese'])),row['id']
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention'),row['id']
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        if row['decision']=='retention':assert row['retention_reason']
        source_kind=row['kind']; selector=row.get('source_selector')
        if source_kind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response to Fernando in the source conversation'
        else:
            assert source_kind=='ordinary-speech' and (selector<207 or selector==254)
            if selector==254:
                kind='system-FE'; speaker={130:'FE recollection of Carlo\'s family loss; no actor nameplate',131:'FE patrons and applause; inline labels, no actor nameplate'}[row['block']]
                assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_hex'].startswith('fe')
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            else:kind,speaker='progressive',forms[selector]
        row.update(english=text,logical_English=text,proposed_English=text,original_source_kind=source_kind,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},names_terms_consumers_andfresh_display_approval_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,scoped_prose_name_term_references=[str(names_out),str(paths[2])],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts=Counter(r['decision'] for r in rows); kinds=Counter(r['kind'] for r in rows)
    assert len(rows)==337 and counts=={'revision':224,'retention':113} and kinds=={'progressive':329,'system-FE':6,'typed-choice-label':2}
    assert len(changes)==9
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=GATES,file_path='/data/SC3.DK4',blocks=sorted({r['block'] for r in rows}),records=rows,source_objects=337,complete_exchanges=12,
        proposed_revisions=counts['revision'],justified_retentions=counts['retention'],runtime=runtime,current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],
        scoped_name_term_andreadaloud_amendments=changes,all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        all337_paragraphs_read_in12_complete_exchanges=True,no_dynamic_roles_orstyle_objects_in_source_scope=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]})
    structural=deepcopy(doc); structural['translation_policy']='natural-dialogue-v1'; validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:
        assert 'v2 requires per-record' in str(exc); blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed release gate')
    # Save all three approved prose artifacts only after every assertion passes.
    save(names_out,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',records=scoped,
        runtime=runtime,scoped_actors=21,individual_name_retentions=21,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]}))
    doc['evidence'][str(names_out)]=digest(names_out); save(OUT,doc)
    save(proof_out,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=337,complete_exchanges=12,revisions=224,retentions=113,
        scoped_name_retentions=21,first_four_individual_gates_pass=True,all_fifth_gates_false=True,amendments=changes,
        structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print('Sealed337 prose reviews:224 revisions/113 retentions,21 scoped names;first four gates pass,fresh formatting/release remain pending.')

if __name__=='__main__':main()
