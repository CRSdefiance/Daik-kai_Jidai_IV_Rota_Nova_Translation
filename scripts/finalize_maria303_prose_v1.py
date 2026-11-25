"""Seal whole-exchange editorial decisions; keep all native formatting/release gates closed."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')
OUT=Path('translations/maria_B58_B70_contextual_review_v1.json')
GATES=['source','context','localization','naturalness','formatting']
NAME_REASONS={
3:'Retain approved Maria. Maria Li and Maria Huamei Li are distinct short/full native forms of the same source components; Li Clan is the live FO faction, not a new personal surname or invented rank.',
4:'Retain Janus Pasar in both consumers and the recruitment introduction. Source パサー and current native Pasar do not support the old spoken Pasha variant or a new title.',
7:'Retain Cristina Erneco in both consumers and Cristina in the rescue. Familiar older-sister address by the boy is not evidence that she is his sister.',
10:'Retain Xien Yan, matching both original getters and the established spelling. Correct Shien in dialogue; the protective formal voice does not create a new title.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki, preserving the native middle component and distinct consumer forms. His Japanese identity and formal speech are explicit, not a license to invent a samurai rank.',
14:'Retain Emilio Ferog and Emilio in the two comic food exchanges; do not add a family relationship or occupation to the name.',
15:'Retain Angelo Puccini and Angelo. The source Mamma mia belongs to his voice and does not change his name or establish new biography.',
16:'Retain Gerhard Adernkatz and Gerhard. Admiral Adernkatz is expressly used by the boy; ordinary respectful addresses elsewhere do not make him Master. The old sword is personal, not a hereditary title or heirloom.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort. Restore the full spoken introduction; Dr. Charles is his self-introduction, not independent proof of medical training. Uncle is not kinship here.',
20:'Retain Fernando Dias and Fernando, including explicitly named separate stat-result panels. Pronoun His loses source identity in those system messages.',
26:'Retain Julian Lopes in both consumers. Correct provisional Lopez in draft speaker metadata; his flirting and promise to Mihwa do not prove an established romantic relationship.',
74:'Retain Richard Townsend as the source-bound named speaker in the rescue exchange; do not infer an extra rank or relationship from his presence.',
79:'Retain Mivor Genz, matching both native fields and the rescue introduction. His unwanted pursuit and matched fear comparisons remain characterization, not a newly invented relationship.',
82:'Retain Shopkeeper for the source square-shop owner. The natural functional header suffices; internal European-male metadata is not a player-facing surname or a reason to lengthen it.',
108:'Retain Trader for the trade-house seller who offers the tomato seedling. This identifies his commercial role without claiming that he grows the tomatoes; internal ethnicity metadata is not his name.',
109:'Retain Shipwright for the shipyard craftsman in the hiring exchange. The native functional header is natural; European metadata is not a family name or a new nationality claim in the prose.',
152:'Retain Sailor in the progressive header for the speaker who explicitly says he can no longer go to sea; retain the separate generic Retainer catalogue form for source 配下. These aliases do not establish that he serves Maria. Internal regional metadata remains outside this scoped header review.',
162:'Retain Boy for the expressly labeled child in the rescue and navigator-search exchanges. The generic role does not invent his personal name or kinship with Cristina.',
167:'Retain Lady for 貴婦人 as a generic descriptive header, not Lady plus a name or a peerage rank. Her relationship to the rescued boy is explicit in the dialogue; internal European 2 is not a personal identity.',
201:'Retain established Mihwa for 美華 in the exact native short/full consumers and body references, following the prior individual review. Provisional Meihua is superseded; this person is distinct from Maria Huamei/華梅, and Hangzhou metadata alone does not establish another reading or nationality.',
}

def main():
    names_out=ROOT/'scoped20_names_editorial_review_v1.json';proof_out=ROOT/'contextual_prose_qualification_v1.json'
    assert not any(p.exists() for p in [OUT,names_out,proof_out])
    parts=[ROOT/n for n in ['B58_contextual_proposals_v1.json','B59_B61_contextual_proposals_v1.json','B62_B70_contextual_proposals_v1.json']]
    docs=[load(p) for p in parts];runtime=docs[0]['runtime'];assert all(d['runtime']==runtime for d in docs)
    rows=deepcopy([r for d in docs for r in d['records']]);assert len(rows)==len({r['id'] for r in rows})==303
    assert Counter(r['decision'] for r in rows)=={'revision':180,'retention':123}
    name_path=ROOT/'scoped_names_macros_reference_v1.json';term_path=ROOT/'scoped_terms_reference_v1.json'
    names,terms=map(load,[name_path,term_path]);assert names['runtime']==terms['runtime']==runtime
    bindings=deepcopy(names['records']);bindings.append(deepcopy(terms['spoken_Mihwa']))
    assert {r['actor_ID'] for r in bindings}==set(NAME_REASONS)
    scoped=[];forms={}
    for r in bindings:
        actor=r['actor_ID'];consumers=r['current_consumers']
        assert {c['consumer'] for c in consumers}=={'progressive-nameplate','full-catalogue'}
        approved={c['consumer']:c['text'] for c in consumers};forms[actor]=approved['progressive-nameplate']
        assert all(t.isascii() for t in approved.values())
        reason=NAME_REASONS[actor]
        r.update(id=f'SC3_B58_B70_ACTOR_{actor}_SCOPED_NAME',approved_forms=approved,
            english=approved['progressive-nameplate'],speaker=approved['progressive-nameplate'],
            context='Complete Maria B58-B70 exchanges and exact native source/current name consumers; scoped forms only.',
            source_meaning=' / '.join(f['source']['text'] for f in r['source_andcurrent_fields'] if f['source']['text']),
            decision='retention',finding=reason,localization_note=reason,retention_reason=reason,
            review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            unused_metadata_not_globally_approved=True,no_global207_name_approval=True,new_credit=0)
        scoped.append(r)
    save(names_out,dict(format='dk4-scoped-name-editorial-review-v2',records=scoped,scoped_actors=20,
        runtime=runtime,individual_name_retentions=20,first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [name_path,term_path,Path(__file__)]}))
    amendments=[]
    for r in rows:
        text=r['proposed_English'];before=text;note=''
        if r['id'] in ['DK4_MES_B62_R0050','DK4_MES_B62_R0089']:
            assert 'Meihua' in text;text=text.replace('Meihua','Mihwa')
            note='Reconcile the provisional Meihua to established, source-bound Mihwa in both current native consumers and earlier individual naming reviews.'
        elif r['id']=='DK4_MES_B60_R0164':
            assert text=="Take the ship from the dock, then use 'Modify' to name it."
            text="Once you've taken the ship from the dock, choose Remodel to name it."
            note='Correct the instruction to exact native 改造/Remodel at ARM9 field0x118eb0, rather than the old Modify or provisional Refit. Preserve the dock-then-menu order.'
            assert r['decision']=='retention';r['decision']='revision';r['retention_reason']=''
        if text!=before:
            amendments.append(dict(id=r['id'],before=before,after=text,reason=note))
            r['finding']+=' '+note;r['localization_note']=r['finding']
        assert not any(r['review'].values())
        assert r['source_meaning'] and r['whole_exchange_context'] and r['finding']
        assert text.isascii() and text.strip()==text and not any(t in text for t in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert dict(Counter(re.findall(r'F[A-Z]',text)))==r['source_macros'],r['id']
        assert (text==r['current_comparison_paragraph'])==(r['decision']=='retention'),r['id']
        if r['decision']=='retention':assert r['retention_reason']
        kind=r['kind'];selector=r.get('source_selector')
        if kind=='typed-choice-label':speaker='Player choice (Maria)'
        elif selector==254:
            kind='system-FE';speaker=r['speaker']
            assert r['source_complete_preamble_hex'].startswith('fe')
        else:
            assert kind=='progressive' and selector in forms;speaker=forms[selector]
        r.update(english=text,logical_English=text,proposed_English=text,speaker=speaker,kind=kind,
            context=r['whole_exchange_context'],exchange_context=r['whole_exchange_context'],
            native_literal_token_counts=r['source_macros'],review={g:g!='formatting' for g in GATES},
            current_English_not_consulted=False,current_English_now_exposed=True,
            names_terms_consumers_andfresh_display_approval_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,
            scoped_prose_name_term_references=[str(names_out),str(term_path)],
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    counts=Counter(r['decision'] for r in rows);kinds=Counter(r['kind'] for r in rows)
    assert counts=={'revision':181,'retention':122}
    assert kinds=={'progressive':287,'system-FE':12,'typed-choice-label':4}
    assert len(amendments)==3
    assert sum(r['source_macros'].get('FI',0) for r in rows)==11
    assert sum(r['source_macros'].get('FA',0) for r in rows)==1
    assert sum(r['source_macros'].get('FO',0) for r in rows)==4
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',
        blocks=sorted({r['block'] for r in rows}),records=rows,source_objects=303,complete_exchanges=10,
        proposed_revisions=counts['revision'],justified_retentions=counts['retention'],runtime=runtime,
        current_ROM=runtime.get('candidate'),current_ROM_sha256=runtime.get('candidate_sha256'),
        scoped_name_andterm_amendments=amendments,all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,native_macro_tokens_still_require_formatter_marking=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*parts,name_path,term_path,names_out,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as e:
        assert 'v2 requires per-record' in str(e);blocked=str(e)
    else:raise AssertionError('Unformatted prose passed release gate')
    save(OUT,doc)
    save(proof_out,dict(source_objects=303,complete_exchanges=10,revisions=181,retentions=122,
        scoped_name_retentions=20,physical_speeches=299,FE_panels=12,choice_captions=4,
        first_four_individual_gates_pass=True,all_fifth_gates_false=True,logical_ASCII_paragraphs=True,
        exact_macro_counts=dict(FI=11,FA=1,FO=4,FU=0),structural_projection_pass=True,
        unformatted_manuscript_rejected_by_release_gate=blocked,
        native_formatting_every_new_page_visual_review_storage_gameplay_registration_pending=True,
        manuscript=str(OUT),manuscript_sha256=digest(OUT),new_credit=0,full_goal_complete=False))
    print('Sealed303 contextual prose decisions:181 revisions/122 retentions;20 scoped names;all formatting/release gates remain closed.')

if __name__=='__main__':main()
