"""Seal349 individual contextual four-gate reviews; keep every formatting gate false."""
import inspect
from pathlib import Path
from scripts import finalize_maria363_prose_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B275_B285_clean_20261110')
OUT=Path('translations/maria_B275_B285_contextual_review_v1.json')
NAMES=Path('translations/maria_B275_B285_scoped_names_v1.json')
REASONS={
3:'Retain approved Maria Li and full Maria Huamei Li. Her humane care for the wounded man, political argument and command of the ruse identify the established captain. Praise of her skill is not fame, kinship or a new rank.',
10:'Retain Xien Yan. His pragmatic defense argument, theatrical support and praise of the mimic preserve his established thoughtful voice; no new official appointment or relationship is established.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. His exuberant shout and laughter are the existing actor, not a new guard title or biography.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. The martial cry belongs to the existing Japanese actor; nationality is explicit in the later ruse discussion, but no new office is granted.',
25:'Retain Yifa Sol, the established source-bound form of Ifa/Soru. Actor25 joins the joke about the fooled governor; do not silently substitute Emilio or infer a new nationality or surname from unrelated names.',
68:'Retain Jacob Portunto. The source explicitly names Jacob and identifies past work contact and present senior smuggling membership, not friendship, family, a nobility title or a new formal rank.',
88:'Retain Shopkeeper for the source plaza-shop role, even while answering the governor. Chinese-region metadata is not a surname; polite speech does not appoint this bystander a soldier.',
93:'Retain Barkeep for the Chinese-region tavern proprietor. Oyaji is familiar address, not fatherhood, and regional metadata supplies no proper name.',
101:'Retain Patron for the recurring source tavern customer, who acts as an informant here. Do not globally rename the archetype Informant from one scene or treat Korean-region metadata as a biography.',
102:'Retain Patron for the source Japanese-region tavern-customer archetype. This character reveals his smuggling past and joins Maria, but no personal name is supplied and one scene does not authorize globally renaming every reuse Smuggler.',
123:'Retain Guard, a natural role label for the source wei-bing. The acknowledgment addresses the staged official; region metadata adds no surname or new command rank.',
129:'Retain Magistrate as the source performance label. The reveal says a former actor is impersonating a county magistrate; preserving the displayed role does not certify an actual appointment, and replacing it globally with Actor would spoil or mislabel other uses.',
131:'Retain Governor. The clean exchange explicitly identifies the governor of Macao; no personal name is supplied, and the source European-region component is not a surname.',
139:'Retain Priest as the source displayed role of the disguised visitor. The conspiracy makes this delegation fraudulent, not every use of the priest archetype; do not globally change the label to Impostor or invent an ecclesiastical rank.',
151:'Retain Sailor in progressive nameplates and Retainer in the catalogue. Expedition alarm does not provide a proper name or a new military office; European metadata is not a surname.',
156:'Retain Sailor/Retainer for the two consumers. Selectors208/211/214/215/218 resolve to this fallback with voice4 only in the verified startup context; future treatment or injured-party assignments remain unvisited.',
201:'Retain the established Mihwa for clean kanji 美華 in this scoped exchange. The source gives no phonetic reading here; Hangzhou metadata is not a surname or proof of nationality. Do not replace it by an assumed Mandarin or Korean biography; the broader name-reading review remains open.',
203:'Retain Sakura. Osaka is location metadata, not her surname. Her nursing concern, temple visit and offer of partway guidance establish no romance, family relationship, age or formal medical post.',
205:'Retain Silvia, a natural established rendering of Shirubia. Veracruz is location metadata, not a surname. Her uncertain ruins tip supplies no romance, map ownership or new biography.',
}

source=inspect.getsource(previous.main)
old_save="""    save(comparison,dict(records=rows,records_count=363,complete_exchanges=37,blocks=packet['selected_blocks'],runtime=runtime,
        revised=203,retained=160,all_individual_findings_andretention_reasons_saved=True,all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,evidence=evidence,new_credit=0,full_goal_complete=False))"""
source=checked_text(source,{
    "assert not any(p.exists() for p in [OUT,NAMES,comparison,terms_path,proof_path])":
        "assert comparison.exists() and not any(p.exists() for p in [OUT,NAMES,terms_path,proof_path])",
    'scoped_names_macros_reference_v2.json':'scoped_names_macros_reference_v1.json',
    "['B216_B226','B227_B251','B252']":"['comparisons']",
    '==363':'==349',
    "{'revision':203,'retention':160}":"{'revision':184,'retention':165}",
    old_save:"    assert load(comparison)['records']==rows and load(comparison)['records_count']==349",
    "    clean=NdsImage.open('work/clean.nds')":"    compatibility_path=ROOT/'retained_UI_label_compatibility_v1.json';assert not compatibility_path.exists()\n    clean=NdsImage.open('work/clean.nds')",
    '    save(terms_path,dict(runtime=runtime,UI=terms,':'    save(compatibility_path,dict(runtime=runtime,UI=terms,',
    "    assert {r['actor_ID'] for r in names['records']}":"""    city_path=ROOT/'scoped_city_andProof_reference_v1.json';city=load(city_path)
    proof_path_reference=ROOT/'narrative_Proof_convention_v1.json';proof_convention=load(proof_path_reference)
    assert city['runtime']==runtime and len(city['terms'])==1
    assert city['terms'][0]['source']['text']=='マカオ' and city['terms'][0]['current']['text']=='Macao'
    assert proof_convention['source_term']=='証' and proof_convention['retained_narrative_English']=='Proof'
    assert digest(proof_convention['prior_approved_manuscript'])==proof_convention['prior_approved_manuscript_sha256']
    assert all(all(r['review'].values()) for r in proof_convention['records'])
    save(terms_path,dict(runtime=runtime,city=city['terms'],narrative_Proof=proof_convention,
        historical_fixed_UI_compatibility_only=str(compatibility_path),historical_fixed_UI_compatibility_sha256=digest(compatibility_path),
        Jesuit_Society_of_Jesus_andSon_of_Heaven_are_explicit_source_terms_not_new_game_UI_labels=True,
        no_new_item_UI_name_layout_orstat_effect_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [city_path,proof_path_reference,cp,compatibility_path,Path(__file__)]}))
    assert {r['actor_ID'] for r in names['records']}""",
    "names['original_native_name_getters']==58":"names['original_native_name_getters']==38",
    "roles['source_selectors']==[207,208,211,215,216]":"roles['source_selectors']==[208,211,214,215,218]",
    'for s in [208,211,215,216]':'for s in [208,211,214,215,218]',
    "len(objects['style_records'])==85 and len(objects['choice_records'])==12 and objects['native_style_getter_cases']==96":
        "len(objects['style_records'])==162 and len(objects['choice_records'])==8 and objects['native_style_getter_cases']==216",
    'SC3_B216_B252_ACTOR_':'SC3_B275_B285_ACTOR_',
    'Maria B216-B252':'Maria B275-B285',
    'selector in [208,211,215,216]':'selector in [208,211,214,215,218]',
    "{'progressive':313,'system-FE':38,'typed-choice-label':12}":"{'progressive':334,'system-FE':7,'typed-choice-label':8}",
    'scoped_actors=29,individual_name_retentions=29':'scoped_actors=19,individual_name_retentions=19',
    'source_objects=363,complete_exchanges=37,proposed_revisions=203,justified_retentions=160':
        'source_objects=349,complete_exchanges=11,proposed_revisions=184,justified_retentions=165',
    'all363_paragraphs_read_in37_complete_exchanges=True':'all349_paragraphs_read_in11_complete_exchanges=True',
    'records=363,complete_exchanges=37':'records=349,complete_exchanges=11',
    'revisions=203,retentions=160,scoped_name_retentions=29':'revisions=184,retentions=165,scoped_name_retentions=19',
    'Sealed363 four-gate prose reviews:203 revisions/160 retentions;29 scoped names; formatting/release remain.':
        'Sealed349 four-gate prose reviews:184 revisions/165 retentions;19 scoped names;formatting/release remain.',
})

if __name__=='__main__':
    env={**previous.main.__globals__,**globals(),'__file__':__file__}
    exec(compile(source,__file__+'::same-individual-source-current-native-name-role-macro-andunformatted-rejection-contract','exec'),env)
    env['main']()
