"""Seal contextual prose and scoped names after native identity/term reconciliation."""
from copy import deepcopy
from pathlib import Path
import re
import struct
from collections import Counter
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=Path('translations/maria_B37_B50_contextual_review_v1.json')
GATES=['source','context','localization','naturalness','formatting']
NAME_REASONS={
 0:'Retain approved Rafael Castor. His modest shipping ideal, Portuguese homeland and reciprocal cooperation do not add a rank. Clau and Rafi are source-supported familiar spoken forms, not nameplate replacements.',
 1:'Retain approved Hodram, Bergstrom and full-name Joakim. His return to the North Sea and redirection of thanks add no permanent alliance or new title.',
 2:'Retain Lil Argot. Her apology, recognition of her limitations and decision to return do not make her a child or a relative of a companion.',
 3:'Retain approved Maria Li and full Maria Huamei Li. Her admiral address is contextual command, not an added noble title; FI/FA/FO remain live substitutions.',
 5:'Retain Claudio Manaus. Rafael’s Clau and Claudio’s Rafi are supported familiar dialogue forms. Rumor, panic and flattery add no relationship beyond the exchange.',
 9:'Retain approved Camille with Overijssel and full Marinus component. His gratitude and decision to accompany Lil add no kinship or new office.',
 10:'Retain Xien Yan. Counsel, suspicion about Richard’s drinking and the defection warning support his established voice, not Grandpa as a family label.',
 11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. Keep his private thought distinct from spoken gratitude; Jack is a native component, not a second actor.',
 12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His polite alternate crowd observation adds no noble rank or proof of simultaneous companion presence.',
 21:'Retain Ian Dukov for the polite alternative reassurance. Do not merge his line with Xien’s or infer a new relationship from concern for Maria.',
 25:'Retain Yifa Sol. The optional all-show taunt belongs to this actor and supplies no new biography or title.',
 26:'Retain Julian Lopes, actor26. His appalled cowardice judgment does not identify him as the distinct actor63 Julian Vermeer.',
 27:'Retain Aziza Nurennahar. Her optional reflection on pirates does not confer a new rank, origin or connection to Maldonado.',
 28:'Retain James Clifford. His colonial replacement argument and condescending flattery add no noble Lord title. The preceding unseen voice is not a separately named person.',
 31:'Retain Pedro Valdes and full Pedro de Valdes as the named reference in conditional intelligence. The spoken Admiral is source-supported, not a new nameplate rank.',
 33:'Retain Hardum Pasha and full Hardum Ahmet Pasha. Pasha is the registered source-bound name component; do not confuse this mentioned actor with Janus Pasar or invent a real-world identity.',
 34:'Retain Barbarossa Hayreddin and full Barbarossa Fazul Hayreddin. 一家 describes his pirate band here, not proven biological kinship. He is mentioned, not newly observed speaking.',
 36:'Retain Geronimo Espinosa and full Geronimo de Espinosa. Graus’s 様 does not establish Lord; capture and threatened punishment do not prove execution or its method.',
 37:'Retain Abraham Uddin and full Abraham Ibn Uddin. The source identifies him as with the Uddin Company; do not invent ownership, a new religious office or unsupported ethnicity from the name.',
 38:'Retain registered Zamorin Nagarpur and full Zamorin Ahmad Nagarpur. Reconcile Nagalpur in dialogue to Nagarpur. Preserve native components without independently expanding Zamorin into a new rank or historical biography.',
 40:'Retain Antony Kuhn and full Antony von Kuhn as the spoken reference after the rescue. Correct Kuen in dialogue; no noble title or family link to Camille is inferred here.',
 42:'Retain Vasquez Maldonado and full Vasquez de Maldonado. His Caribbean-pirate claims and self-interested bargain do not justify a liberator or governor title.',
 43:'Retain Diogo Escante and full Diogo de Escante as the antagonist reference. Keep the conditional betrayals distinct and do not invent a new formal title.',
 47:'Retain Gilberto Graus. His plantation-worker ownership claim and rough threats belong to the source antagonist, without adding an office or a completed death.',
 74:'Retain Richard Townsend. English workers and defection are explicit story facts; FE monologue context alone does not prove a static speaker/portrait binding or an already received governorship.',
 84:'Retain Shopkeeper for 広場の店主. Shopkeeper naturally identifies the role; Africa metadata is not a surname or nationality, and the source friend is not a family relationship.',
 114:'Retain Port Worker for 出港所の兄貴. The familiar workplace epithet is not proof that he is anyone’s brother. His actual father and family are explicit in his own speech and remain there.',
 141:'Retain Innkeeper for 宿屋のおばさん. The workplace and adult familiar address do not support Aunt, a specific age or a family relationship; Africa metadata stays out of the name.',
}

def main():
    names_path=ROOT/'scoped28_name_editorial_review_v1.json';terms_path=ROOT/'scoped_terms_v1.json'
    assert not any(p.exists() for p in [OUT,names_path,terms_path])
    proposals_path=ROOT/'all286_contextual_proposals_v1.json'
    bindings_path=ROOT/'scoped_names_macros_reference_v1.json'
    proposals,bindings=map(load,[proposals_path,bindings_path])
    assert proposals['runtime']==bindings['runtime'] and len(proposals['records'])==286
    ctx=RegisteredRuntime(proposals['runtime']['release_proof'],proposals['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==proposals['runtime']
    assert {r['actor_ID'] for r in bindings['records']}==NAME_REASONS.keys()
    names=[]
    for original in bindings['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=NAME_REASONS[actor]
        row.update(decision='retention',finding=reason,retention_reason=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=ctx.receipt()['candidate'],candidate_sha256=ctx.receipt()['candidate_sha256'],
                actor_ID=actor,original_consumers=row['current_consumers']),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            final_font_complete_glyph_bounds_andrepresentative_display_checks_pending=True,
            no_global207_name_approval_ornew_dialogue_credit=True,new_credit=0)
        names.append(row)
    save(names_path,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',records=names,review_gates=GATES,scoped_actors=28,justified_name_retentions=28,
        name_field_revisions=0,original_native_getters_bound=56,runtime=ctx.receipt(),
        all_four_name_prose_gates_pass=True,all_name_formatting_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [bindings_path,proposals_path,Path('docs/glossary.md'),Path(__file__)]}))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    wanted={'Sofala','Cape Town','Mogadishu','Hangzhou'};cities=[]
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in wanted:continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        value=ctx.arm[entry.offset:entry.offset+entry.slot_size];expected=entry.suggested_english.encode()
        assert value==expected+bytes(entry.slot_size-len(expected))
        cities.append(dict(profile_ID=entry.row_id,offset=entry.offset,source_hex=entry.expected_bytes.hex(),
            source_Japanese=entry.japanese,current_span_hex=value.hex(),current_term=entry.suggested_english))
    assert len(cities)==6 and {r['current_term'] for r in cities}==wanted
    route_path=Path('translations/route_forces_arm9_v1.json')
    tamsui=next(r for r in load(route_path)['records'] if r['id']=='DK4_ROUTE_CITY_TAMSUI')
    offset=tamsui['offset'];source=bytes.fromhex(tamsui['source_hex']);span=ctx.arm[offset:offset+len(source)]
    assert clean[offset:offset+len(source)]==source and source.split(b'\0')[0].decode('cp932')=='淡水'
    assert span==b'Tamsui\0\0'
    goods_path=Path('translations/commodity_name_manuscript_v343.json')
    wine=next(r for r in load(goods_path)['records'] if r['Japanese']=='ワイン')
    assert wine['English']=='Wine' and wine['pointer_field']==0x15F0B0
    field=wine['pointer_field'];sp,tp=[struct.unpack_from('<I',arm,field)[0] for arm in [clean,ctx.arm]]
    source_wine,current_wine=string(clean,sp),string(ctx.raw,tp)
    assert source_wine['text']=='ワイン' and current_wine['text']=='Wine'
    assert clean[field+4:field+12]==ctx.arm[field+4:field+12]==bytes.fromhex(wine['metadata_hex'])
    assert {r['token']:r['text'] for r in bindings['default_macro_cases']}==dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    save(terms_path,dict(runtime=ctx.receipt(),inline_city_aliases=cities,
        Tamsui=dict(registered_record=tamsui,source_span_hex=source.hex(),current_span_hex=span.hex()),
        Wine=dict(pointer_field=field,source=source_wine,current=current_wine,metadata_hex=wine['metadata_hex']),
        default_macros=bindings['default_macro_cases'],
        contextual_terms=[
            dict(source='マダガスカル',english='Madagascar',reason='Preserve the explicitly named island as the proposed East African hub, not an early name for the later Ming island.'),
            dict(source='鄭和',english='Zheng He',reason='Retain the established readable Chinese personal-name rendering in Maria’s Africa-arrival reflection; no historical research claim is made.'),
            dict(source='明',english='Ming',reason='Keep the named polity and mainland geography without substituting modern national borders.'),
            dict(source='イギリス',english='England',reason='Use the established period-story name, retaining explicit English workers and allegiance without introducing the modern United Kingdom.'),
            dict(source='倭寇',english='wokou pirates',reason='Explain the source maritime-pirate term while avoiding a claim that all pirates or all members of any nationality are equivalent.'),
            dict(source='船倉５つ分 / 倉庫５つ分',english='five holds of wine',reason='The paired request and confirmation establish the same five-load delivery. Preserve holds and quantity; do not invent five ships, barrels or generic five-unit crates.'),
            dict(source='権益 / 交易権 / シェア',english='trading rights',reason='Regional fleet interests and local market-share transfer concern the game’s trade control. Keep most/exclusive/local distinctions; do not imply corporate stock or military sovereignty.'),
            dict(source='覇者の証',english='Proof of Conqueror',reason='Use the registered terminology and preserve the distinction between the unnamed gift and the treasure Espinosa sought.'),
        ],no_global_city_alias_commodity_orfont_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [bindings_path,route_path,goods_path,Path(__file__)]}))
    forms={r['actor_ID']:next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in names}
    rows=deepcopy(proposals['records']);amendments=[]
    for row in rows:
        english=row['proposed_English']
        if row['id']=='DK4_MES_B39_R0008':
            assert 'Nagalpur' in english
            revised=english.replace('Nagalpur','Nagarpur')
            reason='Reconcile the spoken Nagalpur spelling to the current source-bound Nagarpur nameplate/catalogue.'
            amendments.append(dict(id=row['id'],before=english,after=revised,reason=reason));english=revised
            row['localization_note']+=' '+reason;row['finding']=row['localization_note']
        if row['id']=='DK4_MES_B48_R0216':
            revised='Spain and the Ottoman Turks hold most of the trading rights in the Mediterranean. Admirals Valdes and Pasha keep skirmishing with each other.'
            reason='Use natural established regional trade-control terminology for 権益, preserving most and the separate skirmish report.'
            amendments.append(dict(id=row['id'],before=english,after=revised,reason=reason));english=revised
            row['localization_note']+=' '+reason;row['finding']=row['localization_note']
        native_kind=row['kind'];selector=row.get('source_selector')
        if native_kind=='typed-menu-caption':speaker,kind='Player choice','typed-choice-label'
        elif selector==254:
            assert native_kind=='ordinary-speech' and row['source_presentation_kind']=='system-FE'
            kind='system-FE'
            speaker=('Unseen young man’s voice before Clifford’s named entrance' if row['block']==46 else
                'Location transition' if row['source_record_index']==24 else
                'System trade-share notice' if row['source_record_index']==76 else
                'Unnamed monologue; context linked to Richard, no static FE actor binding')
        else:
            assert native_kind=='ordinary-speech' and selector in forms
            kind,speaker='progressive',forms[selector]
        assert not any(row['review'].values())
        assert english.isascii() and not any(x in english for x in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert dict(Counter(re.findall(r'F[A-Z]',english)))==row['source_macros']
        if row['decision']=='retention':assert english==row['current_comparison_paragraph'] and row['retention_reason']
        context=row['whole_exchange_context'].replace('Nagalpur','Nagarpur').replace('Grau’s','Graus’s')
        row.update(english=english,logical_English=english,proposed_English=english,kind=kind,speaker=speaker,
            context=context,exchange_context=context,native_literal_token_counts=row['source_macros'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            source_meaning_pending=False,localized_draft_pending=False,current_English_comparison_pending=False,
            approved_names_terms_titles_andruntime_substitutions_pending=False,
            names_terms_consumers_andfresh_display_approval_pending=False,
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    assert Counter(r['kind'] for r in rows)=={'progressive':269,'system-FE':13,'typed-choice-label':4}
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=list(range(37,51)),
        records=rows,source_objects=286,proposed_revisions=170,justified_retentions=116,
        current_ROM=proposals['current_ROM'],current_ROM_sha256=proposals['current_ROM_sha256'],runtime=ctx.receipt(),
        scoped_name_andterm_amendments=amendments,all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,native_macro_tokens_still_require_formatter_marking=True,
        FE_distinct_consumer_fresh_formatting_andrepresentative_gameplay_pending=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,
        evidence={str(p):digest(p) for p in [proposals_path,names_path,terms_path,Path(__file__)]})
    projection=deepcopy(doc);projection['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(projection)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as e:
        assert 'v2 requires per-record' in str(e);blocked=str(e)
    else:raise AssertionError('Unformatted manuscript passed release gate')
    save(OUT,doc)
    save(ROOT/'prose_gate_qualification_v1.json',dict(records=286,complete_exchanges=14,proposed_revisions=170,
        justified_retentions=116,scoped_name_retentions=28,native_name_getters=56,default_macro_bindings=4,
        body_consumers=dict(progressive=269,system_FE=13),captions=4,logical_ASCII_paragraphs=True,
        all_four_prose_gates_pass=True,all_fifth_gates_false=True,structural_projection_pass=True,
        release_gate_correctly_rejected_unformatted_manuscript=blocked,native_display_gameplay_andregistration_pending=True,
        final_manuscript=str(OUT),final_manuscript_sha256=digest(OUT),new_credit=0,full_goal_complete=False))
    print('Sealed286 four-gate prose reviews:170 revisions/116 retentions;28 scoped names;formatting safely gated,zero credit.')

if __name__=='__main__':main()
