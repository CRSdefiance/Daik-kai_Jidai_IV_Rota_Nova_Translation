"""Seal359 individual four-gate decisions and18 scoped names; formatting stays pending."""
import inspect
from pathlib import Path
from scripts import finalize_maria363_prose_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B253_B274_clean_20261110')
OUT=Path('translations/maria_B253_B274_contextual_review_v1.json')
NAMES=Path('translations/maria_B253_B274_scoped_names_v1.json')
REASONS={
3:'Retain approved Maria Li and full Maria Huamei Li. Her poised command, personal offers and dry reply to a gourmet request support her established voice; the familiar guild address adds neither sisterhood nor a new title.',
4:'Retain Janus Pasar, the installed source-bound form of Jenasu/Pasa. Reconcile independent provisional Janas in contextual notes to Janus; his modest shipbuilding knowledge adds no engineering rank or qualification beyond this exchange.',
10:'Retain Xien Yan. His concern when rescuing Maria, age-marked Japanese voice and rebuke to Jam do not establish kinship, romance or a new office; his own name is explicit in Maria\'s thanks.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. His incredulous complaint sets up the source joke about his own recklessness; it does not justify a new identity or relationship label.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His measured caution belongs to this established actor, without adding Lord or a military office from polite Japanese.',
13:'Retain Cesare Tony as the established source-bound American-English name form for Chezaare/Toni. His eager shipbuilding remarks and admitted gunnery weakness do not make him a new professor or an expert in both fields.',
18:'Retain Charles Rochefort and full Charles Jean Rochefort. He supplies gunnery expertise. B271R223 is also explicitly source actor18 despite feminine Japanese phrasing; preserve that header rather than silently assigning Maria or altering his name.',
23:'Retain Manuel Almeida. His measured shipbuilding advice and armor placement identify the existing actor; no new rank, title or nationality is supplied merely by the name.',
95:'Retain Patron for the European tavern customer. Regional metadata is not a surname or proof that he is Turkish; his Istanbul referral does not supply a personal identity.',
110:'Retain Shipwright, a natural role label for the shipyard worker researching armor. Oyaji is familiar address, not fatherhood; Islamic-region metadata does not make him a religious official or require a new personal name.',
113:'Retain Port Worker. The familiar Japanese aniki does not establish brotherhood; European metadata is not a surname, and his London referral does not imply prior friendship.',
147:'Retain Guildmaster for the local guild role. Reuse across London and Malacca does not establish one traveling person; region metadata adds neither surname nor personal biography.',
148:'Retain Guildmaster for the source Islamic-region guild role. Guiding the expedition and requesting courier/armor help add no religious title, fatherhood or individual proper name.',
151:'Retain Sailor in progressive nameplates and Retainer in the catalogue. The subordinate in danger or pain is not assigned a nationality, friendship or new proper name from regional metadata.',
156:'Retain Sailor/Retainer for the two scoped consumers. Noncaptain dynamic selectors208/211/214/215/216 resolve here with voice4 only in the verified startup snapshot; future conditional roster assignments remain unvisited.',
192:'Retain Matilda, a natural established form of Machiruda. Genoa is location metadata, not her surname; the ruins recommendation supplies no romance or family relationship.',
197:'Retain Safia. Basra is location metadata, not a surname. Her gratitude for improved dancing does not establish a marriage, formal teaching relationship or a new biography.',
203:'Retain Sakura. Osaka is location metadata, not her surname, and the map reminder and farewell supply no age, kinship or mythological identity.',
}

source=inspect.getsource(previous.main)
start=source.index("    clean=NdsImage.open('work/clean.nds')")
end=source.index("    assert {r['actor_ID'] for r in names['records']}")
source=checked_text(source,{source[start:end]:'''    item_path=ROOT/'scoped_item_terms_v1.json';item=load(item_path)
    assert item['runtime']==runtime and len(item['items'])==1
    assert item['items'][0]['source']['text']=='ライムの雫' and item['items'][0]['current']['text']=='Lime Drops'
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');arm=NdsImage.open(current['current_ROM']).read_file('/__arm9__.bin')
    cannon_path=Path('translations/shipyard_ui_arm9_v1.json')
    cannon=next(r for r in load(cannon_path)['records'] if r['id']=='DK4_CANNON_CARRONADE')
    at=cannon['offset'];raw=bytes.fromhex(cannon['source_hex']);target=arm[at:at+len(raw)]
    assert clean[at:at+len(raw)]==raw and cannon['english']=='Carronade '
    assert target.startswith(b'Carronade ') and target[len(b'Carronade '):].strip(b'\\0')==b''
    save(terms_path,dict(runtime=runtime,items=item['items'],UI=[dict(id=cannon['id'],offset=at,source_hex=raw.hex(),current_hex=target.hex(),registered_English=cannon['english'])],
        unnamed_alternative_food_armor_gift_ruins_andtreasures_remain_descriptive=True,no_unspoken_catalogue_item_titles_added=True,
        native_UI_label_bytes_only_not_new_UI_layout_orstat_effect_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [item_path,cannon_path,cp,Path(__file__)]}))
'''})
source=checked_text(source,{
    "assert not any(p.exists() for p in [OUT,NAMES,comparison,terms_path,proof_path])":"assert comparison.exists() and not any(p.exists() for p in [OUT,NAMES,terms_path,proof_path])",
    'scoped_names_macros_reference_v2.json':'scoped_names_macros_reference_v1.json',
    "['B216_B226','B227_B251','B252']":"['comparisons']",
    '==363':'==359',
    "{'revision':203,'retention':160}":"{'revision':219,'retention':140}",
    '''    save(comparison,dict(records=rows,records_count=363,complete_exchanges=37,blocks=packet['selected_blocks'],runtime=runtime,
        revised=203,retained=160,all_individual_findings_andretention_reasons_saved=True,all_five_gates_still_pending=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,evidence=evidence,new_credit=0,full_goal_complete=False))''':
    "    assert load(comparison)['records']==rows and load(comparison)['records_count']==359",
    "names['original_native_name_getters']==58":"names['original_native_name_getters']==36",
    "roles['source_selectors']==[207,208,211,215,216]":"roles['source_selectors']==[207,208,211,214,215,216]",
    'for s in [208,211,215,216]':'for s in [208,211,214,215,216]',
    "len(objects['style_records'])==85 and len(objects['choice_records'])==12 and objects['native_style_getter_cases']==96":"len(objects['style_records'])==131 and len(objects['choice_records'])==10 and objects['native_style_getter_cases']==144",
    'SC3_B216_B252_ACTOR_':'SC3_B253_B274_ACTOR_',
    'Maria B216-B252':'Maria B253-B274',
    'selector in [208,211,215,216]':'selector in [208,211,214,215,216]',
    "{'progressive':313,'system-FE':38,'typed-choice-label':12}":"{'progressive':332,'system-FE':17,'typed-choice-label':10}",
    'scoped_actors=29,individual_name_retentions=29':'scoped_actors=18,individual_name_retentions=18',
    'source_objects=363,complete_exchanges=37,proposed_revisions=203,justified_retentions=160':'source_objects=359,complete_exchanges=22,proposed_revisions=219,justified_retentions=140',
    'all363_paragraphs_read_in37_complete_exchanges=True':'all359_paragraphs_read_in22_complete_exchanges=True',
    'records=363,complete_exchanges=37':'records=359,complete_exchanges=22',
    'revisions=203,retentions=160,scoped_name_retentions=29':'revisions=219,retentions=140,scoped_name_retentions=18',
    'Sealed363 four-gate prose reviews:203 revisions/160 retentions;29 scoped names; formatting/release remain.':'Sealed359 four-gate prose reviews:219 revisions/140 retentions;18 scoped names; formatting/release remain.',
})

# Keep the independent plural draft as evidence; approve only the source's neutral
# singular coin reading, with an explicit contextual gloss correction.
source=checked_text(source,{
    "        row.update(english=text,logical_English=text,original_source_kind=original_kind,kind=kind,speaker=speaker,":
    """        if row['id']=='DK4_MES_B263_R0030':
            assert text=='It looks like a very old coin.'
            row['independent_source_gloss_preserved']=row['source_meaning']
            row['source_meaning']='The find appears to be a coin from a very old era; Japanese does not specify a count.'
            row['contextual_source_gloss_correction_reason']='Avoid treating the independent plural draft as source proof of multiple coins; retain its original gloss anddraft as evidence.'
        row.update(english=text,logical_English=text,original_source_kind=original_kind,kind=kind,speaker=speaker,""",
})

if __name__=='__main__':
    env={**previous.main.__globals__,**globals(),'__file__':__file__}
    exec(compile(source,__file__+'::same-individual-source-current-names-macros-andunformatted-release-rejection-guards','exec'),env)
    env['main']()
