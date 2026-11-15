"""Seal the four prose gates after scoped name,role and source-term reconciliation."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

OUT=Path('translations/maria_B51_B57_contextual_review_v1.json')
GATES=['source','context','localization','naturalness','formatting']
NAME_REASONS={
3:'Retain approved Maria Li and full Maria Huamei Li. Personal reflection,naval command and Grand General are contextual source roles,not extra components of her name. Keep FI/FA live.',
4:'Retain Janus Pasar from the clean personal-name components. His reassurance about official duties gives no new office or family connection.',
6:'Retain Julio Erneco. This scene explicitly calls Cristina his granddaughter,so her Grandpa address is supported here;that does not authorize Grandpa for unrelated older speakers.',
7:'Retain Cristina Erneco for this actor and her spoken Cristina forms. Her actual grandfather,unwanted arranged engagement and sword practice are explicit;do not change her identity to match the wrongly gendered older introduction. The wider Cristina/Christina consumer audit remains separate.',
10:'Retain Xien Yan. His counsel,suspicion,retirement joke and concern for Angelo do not establish kinship or a new title.',
11:'Retain Jam Ludwyan and full Jam Jack Ludwyan. Preserve his casual-to-formal joke as speech register,not This officer as a rank or name.',
12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki. His respectful 殿 and 拙者 forms do not justify Lord Angelo or This warrior in English.',
13:'Retain Cesare Tony from the source name components. His crowd nerves are his own reaction,not a reason to replace the speaker with a generic This one.',
14:'Retain Emilio Ferog,including the explicitly spoken surname. His bull throw and simple food-focused recruitment are the same actor;do not turn the act into the bull throwing him.',
15:'Retain Angelo Puccini. The Bianca-labeled dream and Maria\'s younger-sister question establish the sibling relationship;preserve his grief without inventing a death diagnosis or explaining the dream.',
16:'Retain source-reviewed Gerhard Adernkatz. His silent reaction is distinct from the spoken Herald in Julio\'s family discussion;the Japanese names ゲルハルト and ヘラルド differ.',
17:'Retain Al Shin and full Al Ferid Shin. His conditional protest,employment joke and chuckles remain separate from Jam\'s alternative occurrences.',
19:'Retain Carlo Sinat. His silent look and brief agreement concern official decorum,not a new rank.',
20:'Retain Fernando Dias. Rough shipboard banter and the troop reminder preserve his own voice;no extra role belongs in the nameplate.',
21:'Retain Ian Dukov. Respectful counsel and obedience to Maria preserve the existing identity;source military references stay contextual.',
22:'Retain Samwell Khan and full Samwell da Khan. Keep the native da component in its existing consumer;the formal-speech joke adds no new biography or global middle-field approval.',
23:'Retain Manuel Almeida. His courteous question is a named companion response,not a generic official.',
25:'Retain Yifa Sol. Her tentative key suggestion is speculation and does not change the source personal name.',
26:'Retain Julian Lopes for ユリアン/ロペス. His China question is not actor63 Julian Vermeer merely because they share a given name.',
74:'Retain Richard Townsend. His colonial-entitlement claims,subordinate devotion and barbaric-custom judgment remain his voice;Clifford-sama does not prove a Lord title.',
79:'Retain Mivor Genz in both native consumers for ミヴォール/ゲンツ. Reconcile spoken Gentz to the existing legible Genz;the engagement and extravagant affection establish no noble rank or reciprocal romance.',
82:'Retain Shopkeeper for the square shop owner speaking as a spectator. Neither Square Shopkeeper nor a new permanent Spectator label improves this source-bound identity.',
95:'Retain Patron for the tavern customer heard in the crowd. The source occupational/setting label supplies no personal name,rank or age.',
104:'Retain Trader for the trade-house speaker cheering in the crowd. 親父 is not proof of Father as a relationship label.',
113:'Retain Port Worker for the port-office speaker in town and the crowd. 兄貴 in this source label is familiar occupational address,not Brother as a family relationship.',
147:'Retain Guildmaster for the guild leader\'s crowd cheer. Attending the bullfight does not erase the established role or make the label a new noble title.',
}

def main():
    names_path=ROOT/'scoped26_name_editorial_review_v1.json';terms_path=ROOT/'scoped_terms_v1.json'
    proof_path=ROOT/'prose_gate_qualification_v1.json'
    assert not any(p.exists() for p in [OUT,names_path,terms_path,proof_path])
    proposals_path=ROOT/'all310_contextual_proposals_v1.json';bindings_path=ROOT/'scoped_names_macros_reference_v1.json'
    proposals,bindings=map(load,[proposals_path,bindings_path])
    assert proposals['runtime']==bindings['runtime'] and len(proposals['records'])==310
    assert {r['actor_ID'] for r in bindings['records']}==NAME_REASONS.keys()
    assert bindings['original_native_name_getters']==52 and len(bindings['default_macro_cases'])==4
    assert {r['token']:r['text'] for r in bindings['default_macro_cases']}==dict(FI='Maria',FA='Li',FO='Li Clan',FU='Maria Huamei Li')
    names=[];forms={}
    for original in bindings['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=NAME_REASONS[actor]
        public=next(c['text'] for c in row['current_consumers'] if c['consumer']=='progressive-nameplate')
        forms[actor]=public
        row.update(id=f'ACTOR{actor}_MARIA310_NAME',english=public,speaker=public,
            context='Source-bound speaker labels in Maria\'s complete B51–B57 exchanges. '+reason,
            source_meaning='Clean Japanese identity or occupational label: '+' / '.join(f['source']['text'] for f in row['source_andcurrent_fields']),
            decision='retention',finding=reason,retention_reason=reason,localization_note=reason,
            source_reference=dict(actor_ID=actor,fields=row['source_andcurrent_fields']),
            current_reference=dict(candidate=proposals['current_ROM'],candidate_sha256=proposals['current_ROM_sha256'],
                actor_ID=actor,original_consumers=row['current_consumers']),
            review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,
            final_font_complete_glyph_bounds_andrepresentative_display_checks_pending=True,
            no_global207_name_approval_ornew_dialogue_credit=True,new_credit=0)
        names.append(row)
    assert forms[79]=='Mivor Genz' and forms[14]=='Emilio Ferog' and forms[7]=='Cristina Erneco'
    save(names_path,dict(format='dk4-scoped-name-contextual-review-v2',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',records=names,review_gates=GATES,
        scoped_actors=26,justified_name_retentions=26,name_field_revisions=0,
        original_native_getters_bound=52,runtime=proposals['runtime'],
        all_four_name_prose_gates_pass=True,all_name_formatting_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [bindings_path,proposals_path,Path('docs/glossary.md'),Path(__file__)]}))
    source_rows={r['id']:r for r in proposals['records']}
    terms=[
        ('覇者の証','Proof of Conquest / Proofs of Conquest','Readable established terminology,also used in the source-bound Coerce help review. The ending explains collective recognition,not demonstrated magic or guaranteed universal peace.'),
        ('玉璽（ぎょくじ）','Imperial Seal','Preserve the Chinese imperial-cultural analogy. The reading aid does not name a second object;the dialogue questions whether relics are authentic.'),
        ('国防軍総覧','review of the national defense forces','Preserve the formal review and the wider force description;do not silently narrow it to a fleet-only event.'),
        ('将帥 / 将軍 / 大将軍','command / generals / Grand General','Use the military hierarchy only where explicitly supported in the ending. Source respect markers elsewhere do not create Lord or Lady ranks.'),
        ('ヘラルド','Herald','Retain the source-sound rendering in Julio\'s comment about his parenting. This is distinct from actor16 ゲルハルト/Gerhard;do not merge identities.'),
        ('ビアンカ','Bianca','Retain the explicitly labeled dream speaker and Angelo\'s sister;the story does not authorize a narrator diagnosis or new explanation of the vision.'),
        ('アマリリス','amaryllis','Keep Bianca\'s favorite flowers and the childhood promise to see all the world\'s flowers,not generic flowers without the memory\'s details.'),
        ('副闘牛士（ピカドール） / 闘牛士（マタドール）','picador / matador','The supporting performer wears down the bull before the star finishes it. Emilio throws the bull and Maria chooses him,not the star or Jam.'),
        ('善は急げ','No time like the present','Use a natural English proverb for Cristina\'s urge to act promptly,without adding a new promise or outcome.'),
        ('明朝 / 産業革命','Ming dynasty / Industrial Revolution','Preserve the source epilogue and its timeline as story narration,not a newly researched historical claim or an assertion Maria caused the revolution.'),
        ('じっちゃん / おじいさん / 我が孫娘','Grandpa / your grandfather / my granddaughter','Actual kinship is explicit for Julio and Cristina. Maria must say your grandfather;she is not his granddaughter.'),
    ]
    save(terms_path,dict(runtime=proposals['runtime'],contextual_terms=[dict(source=j,english=e,reason=n) for j,e,n in terms],
        exact_source_references={key:source_rows[key]['source_reference'] for key in [
            'DK4_MES_B53_R0109','DK4_MES_B54_R0231','DK4_MES_B54_R0481','DK4_MES_B54_R0511',
            'DK4_MES_B55_R0066','DK4_MES_B56_R0077','DK4_MES_B57_R0107','DK4_MES_B57_R0122','DK4_MES_B57_R0156']},
        name_reference=str(names_path),name_reference_sha256=digest(names_path),
        default_macros=bindings['default_macro_cases'],literal_native_macro_occurrences=9,
        no_global_UI_term_city_name_orfont_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [proposals_path,bindings_path,
            Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json'),Path(__file__)]}))
    rows=deepcopy(proposals['records']);amendments=[]
    for row in rows:
        english=row['proposed_English'];selector=row['source_selector']
        if row['id']=='DK4_MES_B57_R0079':
            assert 'Mivor Gentz' in english
            after=english.replace('Mivor Gentz','Mivor Genz')
            note='Reconcile the spoken surname to source-bound Mivor Genz in both current native consumers.'
            amendments.append(dict(id=row['id'],before=english,after=after,reason=note));english=after
            row['localization_note']+=' '+note;row['finding']=row['localization_note']
        assert not any(row['review'].values()) and english.isascii()
        assert dict(Counter(re.findall(r'F[A-Z]',english)))==row['source_macros']
        if row['decision']=='retention':assert english==row['current_comparison_paragraph'] and row['retention_reason']
        if selector==254:
            kind='system-FE'
            if row['block']==54:speaker='Epilogue narrator'
            elif row['block']==56:speaker='Arena crowd ambience'
            elif row['source_record_index']==208:speaker='Angelo, explicitly labeled off-portrait voice'
            else:
                assert row['block']==55 and english.startswith('Bianca:')
                speaker='Bianca, explicitly labeled dream voice'
        else:kind,speaker='progressive',forms[selector]
        row.update(english=english,logical_English=english,proposed_English=english,kind=kind,speaker=speaker,
            context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],
            source_presentation_kind='system-FE' if selector==254 else 'named-progressive',
            native_literal_token_counts=row['source_macros'],
            review={g:g!='formatting' for g in GATES},approved_names_terms_titles_andruntime_substitutions_pending=False,
            names_terms_consumers_andfresh_display_approval_pending=False,
            fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    assert Counter(r['decision'] for r in rows)=={'revision':184,'retention':126}
    assert Counter(r['kind'] for r in rows)=={'progressive':279,'system-FE':31}
    assert len(amendments)==1
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=list(range(51,58)),
        records=rows,source_objects=310,proposed_revisions=184,justified_retentions=126,
        current_ROM=proposals['current_ROM'],current_ROM_sha256=proposals['current_ROM_sha256'],runtime=proposals['runtime'],
        scoped_name_andterm_amendments=amendments,all_individual_four_prose_gates_pass=True,
        all_fifth_formatting_gates_pending=True,native_macro_tokens_still_require_formatter_marking=True,
        FE_distinct_consumer_fresh_formatting_andrepresentative_gameplay_pending=True,
        no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,
        evidence={str(p):digest(p) for p in [proposals_path,names_path,terms_path,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1'
    validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as e:
        assert 'v2 requires per-record' in str(e);blocked=str(e)
    else:raise AssertionError('Unformatted manuscript passed release gate')
    save(OUT,doc)
    save(proof_path,dict(records=310,complete_exchanges=7,proposed_revisions=184,justified_retentions=126,
        scoped_name_retentions=26,native_name_getters=52,default_macro_bindings=4,
        body_consumers=dict(progressive=279,system_FE=31),captions=0,
        logical_ASCII_paragraphs=True,all_four_prose_gates_pass=True,all_fifth_gates_false=True,
        structural_projection_pass=True,release_gate_correctly_rejected_unformatted_manuscript=blocked,
        native_display_gameplay_andregistration_pending=True,final_manuscript=str(OUT),final_manuscript_sha256=digest(OUT),
        new_credit=0,full_goal_complete=False))
    print('Sealed310 contextual prose reviews:184 revisions/126 retentions;26 scoped names;all formatting gates remain false.')
if __name__=='__main__':main()
