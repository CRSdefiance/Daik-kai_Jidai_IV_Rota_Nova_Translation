"""Seal individually reconciled whole-exchange prose; display and release gates stay closed."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

GATES=['source','context','localization','naturalness','formatting']
OUT=Path('translations/maria_B96_B124_contextual_review_v1.json')
NAME_REASONS={
1:'Retain approved Hodram Bergstrom and full Hodram Joakim Bergstrom. He introduces himself as Bergstrom of the Swedish navy; add neither Royal nor a specific military rank.',
3:'Retain approved Maria Li and full Maria Huamei Li. Her pirate sobriquet is a separate contextual epithet, not a replacement personal name or royal title.',
6:'Retain Julio Erneco. Cristina is explicitly his granddaughter and a skilled swordswoman; this supports the local family relationship without extending it to other characters.',
7:'Retain Cristina Erneco and spoken Cristina. This is the exact established source-bound spelling in both getters, replacing Christina in this exchange; other older consumers remain individually auditable.',
10:'Retain Xien Yan. His trusted counsel and Maria opening up to him do not establish kinship or romance; he keeps a measured, caring voice.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. His rough speech is a voice distinction, not permission to invent rank or nationality.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His formal account and farewell call for dignified English without a new samurai title or third-person this one.',
19:'Retain established Carlo Sinat in both native consumers. His jade interpretation supplies no new scholarly title or biography; no speculative alternate romanization is introduced.',
21:'Retain Ian Dukov. He narrates a past incident and explains strict rewards and punishment; this does not make him a new officer rank or narrator of every conditional alternative.',
22:'Retain Samwell Khan and full Samwell da Khan. Da is an explicit existing component, not a title or inferred historical identity; his questions and bedtime exit retain youthful curiosity.',
25:'Retain established Yifa Sol for イファ/ソル. Her Taoist-arts attempt is explicit cultural characterization, not a reason to invent new national identity, religious office or an unapproved name.',
26:'Retain established Julian Lopes. His optional agreement and understanding of Clifford are personal responses; the source adds no title, relationship or a reason to change the surname spelling.',
38:'Retain Zamorin Nagarpur and full Zamorin Ahmad Nagarpur. All three identity components are explicit source fields. Reconcile spoken company/person Nagalpur to Nagarpur; do not add a royal biography or further title.',
74:'Retain Richard Townsend. English connections are his boast, not a new crown appointment or guaranteed military support; his pompous interruptions remain distinct.',
92:'Retain Barkeep for the tavernkeeper role. Master is a form of address, not a personal name or a noble rank, and can be omitted in natural English.',
113:'Retain Port Worker for the source port-office man. Familiar address does not make him a brother; the Guam request and taught Chinese phrase supply no personal name.',
116:'Retain Port Worker for the Southeast Asia port-office role. He stumbles into politeness because of fear; regional metadata is not a surname or an English dialogue suffix.',
121:'Retain Guard for 衛兵. Checking company affiliation and allowing passage establish his function, not a rank, name or a religious affiliation from regional metadata.',
132:'Retain Priest for the ceremonial religious role 祭主. The solemn grant supports this generic label without asserting a Christian denomination, Islamic office or hereditary position.',
135:'Retain Priest for 祭主. The stranded passenger is a ceremonial religious figure; the European worker only teaches him a Chinese thanks, not a new faith, name or fluency.',
144:'Retain Innkeeper for the source inn woman. She is explicitly Mao\'s mother in this scene, but a shared role label must not become Mother or gain an invented personal name.',
147:'Retain Guildmaster for the European guild leader. Reported map information gives neither an official archaeological qualification nor a new political rank.',
149:'Retain Guildmaster for the Chinese guild leader. He conveys unofficial Ming terms; he is not thereby a government minister, noble or Maria\'s relative.',
163:'Retain Boy for the shared 男の子 actor. Mao is his local scene name, but the same actor is used elsewhere; do not globally rename the label or make Maria his sister.',
179:'Retain Villager for 村民. The tribal affiliation and grateful knife/gift discussion are supported, but no chieftain rank, personal name or exoticized speech is warranted.',
198:'Retain Benazir. Gifts, useful information and admiration express warmth and solidarity without implying romance, family or a royal title.',
}

TERM_REPLACEMENTS={
    'Staff of Good Guidance':'Guiding Staff',
    'Tang Dynasty Bamboo Craft':'Tang Bamboo Craft',
    'Bamboo Assembly Diagram':'Bamboo Assembly Plan',
    'Unwithering Lotus Leaf':'Evergreen Lotus Leaf',
    'Jar of Milky Liquid':'Lotion Jar',
    'Mysterious Tablet Upper Half':'Upper Stone Tablet',
    'Mysterious Tablet Lower Half':'Lower Stone Tablet',
    'Crimson Pigment':'Red Dye',
    'Nagalpur':'Nagarpur',
}
REFINEMENTS={
    'DK4_MES_B102_R0114':('A guiding staff...?','Keep Maria\'s questioning echo natural after the exact registered Guiding Staff term; no guaranteed effect is added.'),
    'DK4_MES_B115_R0028':('This leaf looks completely dry. Can it really still be alive?','Replace the awkward truly be unwithered with Maria\'s natural doubt about the apparently dried leaf, preserving its uncertain state.'),
    'DK4_MES_B116_R0087':('The admiral was so fearsome then that I dared not speak to her... Yet her sorrow was almost unbearable to behold.','Preserve Yukihisa\'s formal personal inability to address her; the draft\'s none could approach overgeneralized to everyone.'),
    'DK4_MES_B117_R0007':('The Upper Stone Tablet and the Lower Stone Tablet. We must put them together.','Use both complete exact registered tablet labels with a natural connecting article.'),
    'DK4_MES_B122_R0049':("'To my worthy rival...'?",'Keep the salutation and questioning reaction with conventional quote/question punctuation and no orphaned separator space.'),
}

def main():
    names_out=Path('translations/maria_B96_B124_scoped_names_v1.json');proof_out=ROOT/'prose_gates_v1.json'
    assert not any(p.exists() for p in [OUT,names_out,proof_out])
    paths=[ROOT/n for n in ['all330_contextual_proposals_v1.json','scoped_names_macros_reference_v1.json',
        'scoped_item_stat_reference_v1.json','registered_story_terms_reference_v1.json','dynamic_roles_current_v1.json','current_objects_v1/current_objects.json']]
    proposals,names,items,terms,roles,objects=map(load,paths);runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,items,terms,roles,objects])
    assert proposals['records_count']==330 and (proposals['revised'],proposals['retained'])==(248,82)
    assert {r['actor_ID'] for r in names['records']}==set(NAME_REASONS)
    assert terms['full_Proof_term']['singular']=='Proof of Conquest' and terms['epithet']['english']=='Soaring Scarlet Orca'
    assert terms['current_anchor_native_lookups']==2 and roles['source_selectors']==[207,208,209,214,220]
    actual_items={r['current']['text'] for r in items['items']}
    assert set(TERM_REPLACEMENTS.values())-{'Nagarpur'}<=actual_items
    forms={};scoped=[]
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=NAME_REASONS[actor]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f'SC3_B96_B124_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context='Complete clean Maria B96–B124 exchanges and exact native short/full identity consumers; scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    save(names_out,dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',records=scoped,
        runtime=runtime,scoped_actors=26,individual_name_retentions=26,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,evidence={str(p):digest(p) for p in [*paths,Path(__file__)]}))
    rows=deepcopy(proposals['records']);amendments=[]
    for row in rows:
        # This field is the saved editorial selection. Independent drafts remain immutable evidence.
        before=text=row['proposed_English'];notes=[]
        for old,new in TERM_REPLACEMENTS.items():
            if old in text:
                text=text.replace(old,new)
                notes.append(f'Reconcile {old} to exact registered {new}; preserve source actions and natural surrounding prose.')
        if row['id'] in REFINEMENTS:
            text,note=REFINEMENTS[row['id']];notes.append(note)
        if text!=before:
            amendments.append(dict(id=row['id'],before=before,after=text,reason=' '.join(notes)))
            row['finding']+=' '+' '.join(notes);row['localization_note']=row['finding']
            row.update(decision='revision',retention_reason='')
        assert not any(row['review'].values())
        assert text.isascii() and text.strip()==text and not any(t in text for t in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert {t:text.count(t) for t in row['source_macros']}==row['source_macros']
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention'),row['id']
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        if row['decision']=='retention':assert row['retention_reason']
        source_kind=row['kind'];selector=row.get('source_selector')
        if source_kind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response to Xien in the source conversation'
        elif source_kind=='physical-style-alternative':
            assert selector in [208,209,214,220];kind='progressive'
            speaker=f'Dynamic style selector{selector}; original voice slots{row["source_style_indices"]}; conditional assignment unvisited'
            obj=next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
            row.update(native_object_kind='4100-style-alternative',source_object_hex=obj['source_object_hex'],source_choice_object_hex=obj['source_object_hex'],
                virtual_formatter_prefix_not_in_stored_body=True,current_record_index=row['current_reference']['physical_record_index'])
        else:
            assert source_kind=='ordinary-speech'
            if selector==254:
                kind='system-FE';speaker={100:'FE reward message',102:'FE stat-increase message',116:'FE account of a past battle',121:'FE unseen calm male voice',122:'FE Clifford letter'}[row['block']]
                assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_hex'].startswith('fe')
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            elif selector in [207,209]:
                kind='progressive';speaker='Maria (native captain selector207)' if selector==207 else 'Dynamic role selector209; conditional assignment unvisited'
            else:kind,speaker='progressive',forms[selector]
        row.update(english=text,logical_English=text,proposed_English=text,original_source_kind=source_kind,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},names_terms_consumers_andfresh_display_approval_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,scoped_prose_name_term_references=[str(names_out),*[str(p) for p in paths[2:5]]],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts=Counter(r['decision'] for r in rows);kinds=Counter(r['kind'] for r in rows)
    assert len(rows)==330 and counts=={'revision':249,'retention':81} and kinds=={'progressive':320,'system-FE':8,'typed-choice-label':2}
    assert len(amendments)==20,len(amendments)
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=GATES,file_path='/data/SC3.DK4',blocks=sorted({r['block'] for r in rows}),records=rows,source_objects=330,complete_exchanges=26,
        proposed_revisions=counts['revision'],justified_retentions=counts['retention'],runtime=runtime,current_ROM=runtime['candidate'],
        current_ROM_sha256=runtime['candidate_sha256'],scoped_name_term_andreadaloud_amendments=amendments,all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,all330_paragraphs_read_in26_complete_exchanges=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):digest(p) for p in [*paths,names_out,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:
        assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted prose passed release gate')
    save(OUT,doc);save(proof_out,dict(manuscript=str(OUT),manuscript_sha256=digest(OUT),records=330,complete_exchanges=26,
        revisions=counts['revision'],retentions=counts['retention'],scoped_name_retentions=26,first_four_individual_gates_pass=True,
        all_fifth_gates_false=True,amendments=amendments,structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,new_credit=0,full_goal_complete=False))
    print(dict(records=330,revisions=counts['revision'],retentions=counts['retention'],names=26,amendments=len(amendments),formatting_pending=True,new_credit=0))

if __name__=='__main__':main()
