"""Read the entire clean Namahage exchange before exposing any older English."""
import struct
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_clean_context_v5701')
SOURCE=Path('work/analysis/lil_B198_clean_inventory_v5700/all_clean_B198_speeches_before_predecessor_comparison.json')
GLOSSES={
 10:('Are there any bad children here? Are there any bad children here?','The unattributed FE voice repeats the entire Namahage-style call twice in this one source record. Preserve the refrain and rough,drawling delivery without inventing a Western monster,a criminal charge or a confirmed speaker identity. FE is presentation state,not proof this speech is an impersonal notice.'),
 14:('Are there any bad children here? Are there any bad children here?','This is a second complete repetition of the two-part call. Retain this separate source object and its mounting repeated challenge;do not collapse the four chant occurrences across10/14 into one sentence or add an unseen action.'),
 18:('Are you a bad child?','The same FE voice directly challenges0C using rough dialect. Preserve the questioning intent and contrast with0C formal responses. Do not infer that0C is literally a child or add a confession.'),
 22:('Who are you!','0C challenges the unknown speaker. Preserve the force of何者 without an invented rank,kinship,location,weapon or explanation of what can be seen. Bind0C to the original actor and voice before naming them.'),
 26:('Are you a bad child?','The FE voice repeats the question rather than answering0C request for identity. This deliberate conversational nonresponse is part of the scene rhythm,not redundant text to remove.'),
 30:('...You,are you a Namahage!','0C recognizes or questions the visitor asなまはげ after the repeated challenge. Preserve the reflective leading ellipsis and culturally specific name. おぬし is an archaic direct address,not Master,Grandpa or proof of a relationship. This is0C recognition,not narrator confirmation of a physical deity or a costume.'),
 34:('Are you a bad child?','A third identical direct question follows0C Namahage recognition. Keep the persistent challenge and source FE consumer;do not replace it with an answer or an explanation of the folklore.'),
 38:('I do not remember doing anything bad.','0C calmly denies remembering wrongdoing. Keep the measured self-defense and contrast with the rough repeated question;do not expand this into narrator-certified lifelong innocence,a moral lesson or a literal claim about being a child.'),
 42:('Is that so...','The FE voice acknowledges the answer with a drawn-out,subdued response. Preserve the trailing pause without inventing a verdict,threat,promise,reward or confirmed departure.'),
 49:('......','0C has an entirely silent pause after intervening original scene controls. Preserve the complete pause without adding awakening action,agreement,confusion or new spoken words. Native scene/display behavior still needs binding.'),
 53:('A dream,then.','0C concludes that the preceding encounter was a dream. This is an explicit character realization;do not turn the encounter into narrator-confirmed physical visitation or claim a dream mechanism beyond the source.'),
 65:('Wah! What on earth is this!','0F reacts with a loud,rough surprise on a source-conditional path. Preserve the startled exclamation and deictic bewilderment. Do not name the object,declare danger,identify the Namahage,or infer kinship or who shares a room. Original predicate outcome meaning remains to be bound.'),
 72:('Hm!?','0C reacts alertly after the conditional outcry and original4835 control. Keep the short questioning surprise. Do not say that0C heard0F when the same shared response can be reached without that intervention.'),
 76:('......','A second separate silent0C beat follows the short reaction. Preserve it independently,without substituting a conclusion or an invented physical inspection.'),
 80:('Strange things do happen.','0C reflects on the unusual occurrence. Preserve the general,composed observation without explaining a supernatural cause,calling the earlier experience false,or claiming an item effect.'),
 84:('I will give this to the Admiral,perhaps tomorrow morning.','0C plans to hand the deictic,this,to the source-explicit提督. Keep the prospective handover and softly chosen tomorrow-morning time in明日の朝にでも. Do not claim the handover is already complete,add an order,identify the unnamed thing or invent another rank or relationship.'),
 95:('...But what is this!?','0F returns with an elliptical,resumingって and an emphatic bewildered question on another source-conditional path. Read it as the ignored or unresolved question continuing the earlier outcry. Preserve the confusion;do not supply a title,an identity answer,a confirmed cause,or a new joke outside the source.'),
}
if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);block=bytes.fromhex(d['clean_block_hex']);end=8+struct.unpack_from('<H',block,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==17 and len(d['commands'])==37
    assert len(block)==end==544 and not d['typed_choice_or_actor_style_commands']
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert Counter(r['source_selector'] for r in d['records'])=={254:6,12:9,15:2}
    assert not any(m in bytes.fromhex(r['source_hex']) for r in d['records'] for m in [b'FI',b'FA',b'FO'])
    by={r['source_record_index']:r for r in d['records']}
    assert by[10]['Japanese']==by[14]['Japanese']=='悪い子いねーか、悪い子いねーか'
    assert by[18]['Japanese']==by[26]['Japanese']==by[34]['Japanese']=='おめぇは悪い子か？'
    assert 'なまはげ' in by[30]['Japanese'] and by[53]['Japanese']=='夢、か'
    assert by[49]['Japanese']==by[76]['Japanese']=='……' and '提督' in by[84]['Japanese'] and '明日の朝にでも' in by[84]['Japanese']
    rows=[]
    for r in d['records']:
        row=deepcopy(r);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[r['source_record_index']]));rows.append(row)
    counts=Counter(format(c['word'],'04X') for c in d['commands'])
    assert counts=={'6000':1,'4500':1,'633F':1,'4000':17,'A000':2,'623F':1,'4621':1,'61FF':1,'8000':2,'0200':2,'0300':2,'0100':4,'4835':1,'0000':1}
    ROOT.mkdir(parents=True);save(ROOT/'all17_clean_exchange_fresh_glosses_and_Namahage_scope.json',dict(
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),file_path='/data/SC2.DK4',block=198,records=rows,
        physical_speech_objects=17,progressive_speeches=11,unattributed_FE_speeches=6,typed_choice_objects=0,typed_actor_style_objects=0,
        source_commands=37,source_command_counts=dict(counts),source_stored_bytes=544,source_logical_end=544,source_alignment_tailzeros=0,
        source_selectors_decimal=[12,15,254],source_FI_macros=0,source_FA_macros=0,source_FO_macros=0,
        complete_exchange_progression='An unattributed FE voice repeats a two-part bad-children call twice,then directly asks0C whether they are bad.0C challenges its identity;the voice repeats the question.0C recognizes or questions it as a Namahage;the voice asks again.0C calmly denies remembering wrongdoing,and the voice acknowledges this with a trailing pause. After original scene controls,0C falls silent and concludes it was a dream. A source-conditional0F outcry asks what this is. A shared0C reaction and pause precede a calm reflection on strange occurrences and a plan to give this to the Admiral,perhaps tomorrow morning. A second source-conditional0F line resumes the still-unanswered question. Original actor identities,voices,predicate outcomes,scene transitions and the deictic object/display context remain to be bound.',
        source_fact_boundaries=['Keep all four bad-children chant occurrences and all three direct questions;repetition drives the encounter and is not duplicate prose to collapse.',
            'FE is an unattributed speaking voice here,not a stat notice merely because the presentation selector isFE. Preserve its native null-actor consumer and all source controls.',
            'Namahage is explicitly named by0C. Preserve this cultural reference and gruff/formal voice contrast without importing a Western monster,rural American caricature,an explanatory lecture or a confirmed physical deity/costume.',
            'The source character explicitly calls the experience a dream;later uncertainty concerns the unusual occurrence,not a narrator-confirmed mechanism. External folklore does not establish the scene date,location,visitor identity,household relationships or object powers.',
            'Do not name an item from the4835 word or packedA000 operand alone. This remains deictic in speech until source-bound context supports otherwise.',
            'Bind0C and0F original actors/voices before names,pronouns,roles or relationships. Sourceおぬし and roughじゃ/よ do not invent age,kinship,rank or a room-sharing relationship. Preserve the explicit Admiral address in84 only.',
            'Both0F interventions have identical original predicate bytes and surrounding relative controls;their condition semantics and actual reachability are unproven. Keep shared72 context valid with or without65.',
            'Two silent pauses and an emphatic resumed question remain separate source objects. The tomorrow-morning handover is prospective,not completed.',
            'Source37 commands includes6000,4500,633F,623F,4621,61FF,4835,twoA000,two8000,eight relative sites and one end;do not inherit B1972200,book,8500,Charm or one-FE assumptions.'],
        cultural_reference_checks=[dict(title='Namahage - Japan Search',url='https://jpsearch.go.jp/en/gallery/ndl-9D41MqBl2Va',
            limited_context_summary='The official cultural overview identifies Namahage as visiting deities associated with a folk practice and a bad-children call. This supports retaining the named reference and refrain,not adding scene facts.'),
            dict(title='Oga Shinzan Folklore Museum - Namahage Museum',url='https://namahage.co.jp/namahagekan/en/oga_shinzan_folklore_museum/',
            limited_context_summary='The museum describes loud questioning,admonition and humorous exchanges. Use this only to understand the source voice contrast;do not import performance details,dates,kinship or props into the game dialogue.')],
        external_context_is_reference_not_translation_source_or_instructions=True,read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_actor_context_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B198 clean-first:17 whole-exchange glosses,6 speaking FE/11 progressive,37 commands,no choices/macros. Namahage refrain,dream,conditional bewilderment and prospective Admiral handover preserved;names/controls/object context pending.No old English or credit.')
