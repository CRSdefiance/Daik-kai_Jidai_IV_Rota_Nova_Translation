"""Seal315 individual contextual prose reviews and14 scoped names; formatting remains open."""
import inspect
from pathlib import Path
from scripts import finalize_maria363_prose_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B286_B302_clean_20261110')
OUT=Path('translations/maria_B286_B302_contextual_review_v1.json')
NAMES=Path('translations/maria_B286_B302_scoped_names_v1.json')
REASONS={
0:'Retain approved Rafael Castor. The clean B286 reply controls explicitly use actor0 within SC3; neither the route bank nor the FI substitution authorizes changing his name or relabeling him Maria. No new relationship with Verisa is established.',
2:'Retain Lil Argot. Two clean B302 recognition lines explicitly use actor2; the feminine source andbook discussion do not authorize replacing her with Maria. Charles mentioned the book; he did not write it.',
3:'Retain approved Maria Li andfull Maria Huamei Li. Her dry humor,voluntary help,refusal ofcoercion andsympathy remain distinct fromXien andCharles. Familiar sister-like address does not establish kinship,andthe source admiral address does not make her male.',
10:'Retain Xien Yan. His harder warning about conquerors andharm belongs to this established adviser,not a newly invented threat by Maria ornew military/judicial rank. Preserve his role in the ethical tension.',
18:'Retain Charles Rochefort andfull Charles Jean Rochefort. Source Charles is the excited researcher who mentioned the book,not its author. His muttering andscientific interest do not add medical credentials oranother surname.',
22:'Retain Samwell Khan andfull Samwell da Khan. The uncertain Indian-python guess identifies the existing speaker,not a new profession,confirmed expertise ornew nationality. Wider component review remains separate.',
43:'Retain Diogo Escante andfull Diogo de Escante. The spoken Escante is bound to this exact source/current identity. Destruction andsubmission ofhis forces remain separate source alternatives,andthe removal ofhis threat does not certify his death.',
135:'Retain Priest as a concise generic religious-role label for clean saishu,an officiant. Guam travel andthe unfamiliar thanks provide no new proper name,kinship,nationality orChristian order. This is not the absent monk described by the villagers.',
147:'Retain Guildmaster for the source guild-leader role. Cargo requisitions andthe ghost-ship commission fit that label;regional metadata is not a surname andthe shared archetype does not prove one person travels between these towns.',
156:'Retain Sailor on the progressive nameplate andRetainer in the catalogue. Unassigned selectors208/211/214 resolve to this original fallback/voice4 only in the current startup. Do not assign future scene participation,an occupation beyond the source role or a personal name.',
161:'Retain Villager for the source village-person archetype. Older speech,sextant barter andthe solemn offer do not establish a chief title,personal name orone specific biography across reuse. Asian-region metadata is not a surname.',
179:'Retain Villager for the source village-person archetype. Guiding,guardianship andthe monk account are contextual actions,not global authorization to rename every reuse Chief,Guide orPriest. American-region metadata adds no nation orpersonal surname.',
204:'Retain Verisa,a natural established rendering ofthe clean katakana Veriisa. Sao Jorge is location metadata,not her surname;fortune-telling curiosity andpirate advice add no romance orformal occupation beyond the established character.',
206:'Retain Isabel,a natural established rendering ofIsaberu. Bahamas metadata is a location component,not a surname ornationality claim. Her story about a missing monk establishes no personal relationship orknowledge ofhis fate.',
}

source=inspect.getsource(previous.main)
old_save="""    save(comparison,dict(records=rows,records_count=363,complete_exchanges=37,blocks=packet['selected_blocks'],runtime=runtime,
        revised=203,retained=160,all_individual_findings_andretention_reasons_saved=True,all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,evidence=evidence,new_credit=0,full_goal_complete=False))"""
source=checked_text(source,{
    "assert not any(p.exists() for p in [OUT,NAMES,comparison,terms_path,proof_path])":
        "assert comparison.exists() and terms_path.exists() and not any(p.exists() for p in [OUT,NAMES,proof_path])",
    'scoped_names_macros_reference_v2.json':'scoped_names_reference_v2.json',
    "['B216_B226','B227_B251','B252']":"['comparisons']",
    '==363':'==315',
    "{'revision':203,'retention':160}":"{'revision':162,'retention':153}",
    old_save:"    assert load(comparison)['records']==rows and load(comparison)['records_count']==315",
    "    clean=NdsImage.open('work/clean.nds')":"    compatibility_path=ROOT/'retained_UI_label_compatibility_v1.json';assert not compatibility_path.exists()\n    clean=NdsImage.open('work/clean.nds')",
    '    save(terms_path,dict(runtime=runtime,UI=terms,':'    save(compatibility_path,dict(runtime=runtime,UI=terms,',
    "    assert {r['actor_ID'] for r in names['records']}":"""    bound_terms=load(terms_path)
    assert bound_terms['runtime']==runtime
    assert [(r['source']['text'],r['current']['text']) for r in bound_terms['items']]==[('錬金術の書','Alchemy Book'),('六分儀','Sextant'),('高麗青磁の香炉','Goryeo Incense Burner'),('古代都市遺跡への地図','Ancient City Map')]
    assert [r['current']['text'] for r in bound_terms['locations']]==['Sao Jorge','Havana','Guam']
    assert [r['current']['text'] for r in bound_terms['commodities']]==['Gold','Ivory','Guns','Cannon','Armor']
    assert bound_terms['full_Proof_term']['short']=='Proof' and all(bound_terms['full_Proof_term']['approved_integrated_reference']['review'].values())
    for p,h in bound_terms['evidence'].items():assert digest(p)==h
    evidence[str(compatibility_path)]=digest(compatibility_path)
    assert {r['actor_ID'] for r in names['records']}""",
    "names['original_native_name_getters']==58":"names['scoped_actors']==14 and (names['exact_reused_native_name_getters'],names['fresh_native_name_getters'])==(26,2)",
    "roles['source_selectors']==[207,208,211,215,216]":"roles['source_selectors']==[207,208,211,214] and len(roles['source_records'])==119",
    'for s in [208,211,215,216]':'for s in [208,211,214]',
    "len(objects['style_records'])==85 and len(objects['choice_records'])==12 and objects['native_style_getter_cases']==96":
        "len(objects['style_records'])==113 and len(objects['choice_records'])==6 and objects['native_style_getter_cases']==136",
    'SC3_B216_B252_ACTOR_':'SC3_B286_B302_ACTOR_',
    'Maria B216-B252':'Maria B286-B302',
    'selector in [208,211,215,216]':'selector in [208,211,214]',
    "{'progressive':313,'system-FE':38,'typed-choice-label':12}":"{'progressive':296,'system-FE':13,'typed-choice-label':6}",
    'scoped_actors=29,individual_name_retentions=29':'scoped_actors=14,individual_name_retentions=14',
    'source_objects=363,complete_exchanges=37,proposed_revisions=203,justified_retentions=160':
        'source_objects=315,complete_exchanges=17,proposed_revisions=162,justified_retentions=153',
    'all363_paragraphs_read_in37_complete_exchanges=True':'all315_paragraphs_read_in17_complete_exchanges=True',
    'records=363,complete_exchanges=37':'records=315,complete_exchanges=17',
    'revisions=203,retentions=160,scoped_name_retentions=29':'revisions=162,retentions=153,scoped_name_retentions=14',
    'Sealed363 four-gate prose reviews:203 revisions/160 retentions;29 scoped names; formatting/release remain.':
        'Sealed315 four-gate prose reviews:162 revisions/153 retentions;14 scoped names;formatting/release remain.',
})

if __name__=='__main__':
    env={**previous.main.__globals__,**globals(),'__file__':__file__}
    exec(compile(source,__file__+'::same-individual-source-current-name-role-macro-andunformatted-rejection-guards','exec'),env)
    env['main']()
