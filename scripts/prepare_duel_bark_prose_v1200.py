"""Review16 source reactions as natural English; keep formatting gate incomplete."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_bark_layout_v1200 import IDS,PROFILE,compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_prose_v1200')
OUT=Path('translations/duel_bark_editorial_manuscript_v1.json')

# English is authored from the clean Japanese and original timing/voice context.
REVIEW={
1957:('Perfect!','An upbeat exclamation that the action went exactly right.','Retain the concise, idiomatic positive reaction.','retain'),
1958:('...I saw that coming!','A restrained, confident reaction: the speaker has read through or anticipated the move.','Use the natural combat idiom saw that coming for 見切った. Keep the source hesitation, normalize the old fullwidth I, and do not add a supernatural ability.','revise'),
1959:("That attack won't work on me!",'Dismisses the effectiveness of an attack against the speaker.','Retain the natural, confident second-person combat taunt.','retain'),
1960:('Too easy! Where are you looking?','A feminine, dismissive taunt: the opponent is naive/easy to read and is looking the wrong way.','甘い is dismissive of the effort rather than specifically its speed. Preserve the pointed question as a natural taunt.','revise'),
1961:('Come on! Are you even trying?','A rough, goading challenge asking whether the opponent has any will to fight.','Even makes the English question a taunt rather than a sincere inquiry; retain the rough direct voice without added insults.','revise'),
1962:('Take that! Right on target!','A confident old-fashioned exclamation boasting of a strike that surely hits its mark.','Use a natural shout and an accuracy boast. Do not introduce an elder/family address or ornate archaic grammar to mimic じゃ.','revise'),
1963:('Yay! I hit you!','Childlike delight at landing a hit.','Retain the cheerful simple wording; normalize the inherited fullwidth I as compiler-independent English text.','revise'),
1964:('Good! Right here!','A measured positive reaction identifying the right point or moment.','Retain the concise, grammatical spoken fragment; do not invent a named weakness or special technique.','retain'),
1965:('Whoa! I messed that up...','A startled exclamation followed by acknowledgment of a failed action.','失敗 is a failed attempt, not necessarily a literal missed blow. Express the self-directed admission naturally.','revise'),
1966:('Ugh... I let my guard down!','A frustrated reaction admitting carelessness or a lapse in vigilance.','Correct the old Slipped mistranslation of 油断. Use the established English combat idiom without inventing a physical stumble.','revise'),
1967:('Missed! Got too cocky...','Acknowledges missing and becoming overconfident or carried away.','Retain the natural clipped combat reaction and self-reproach. These deliberate spoken fragments preserve the source voice.','retain'),
1968:('Ugh! This is so frustrating!','An irritated, drawn-out complaint expressing frustration.','Complete the English complaint naturally without inventing an accusation about the opponent.','revise'),
1969:('Damn! I rushed that a bit!','A rough, annoyed reaction admitting a little haste or impatience.','Use a mild gruff exclamation and preserve the source hedge 少し with a bit. Normalize the old fullwidth I.','revise'),
1970:('Ugh... No matter. This fight is just getting started!','A pained but defiant older voice insists that the encounter is only beginning or that more is still to come.','Retain the natural, deliberately formal No matter and the idiomatic defiant continuation; do not add a promise of victory.','retain'),
1971:('Whoa! You dodged it!','A surprised, disappointed young voice reacts to the opponent evading the action.','Address the present dueling opponent directly in natural English; preserve the surprise and evasion rather than adding a new participant.','revise'),
1972:("Ugh... I'm not much of a fighter...",'A pained, self-effacing speaker admits being poor at fighting.','Replace the awkward No good at combat fragment with a natural complete admission while retaining both source hesitations and the lack of confidence.','revise'),
}


def main():
    assert not ROOT.exists() and not OUT.exists() and tuple(REVIEW)==IDS
    packet_path=Path('work/analysis/duel_bark_context_v1199/source_context_packet.json');packet=read(packet_path)
    records=[]
    for original in packet['records']:
        n=original['message_ID'];english,meaning,note,decision=REVIEW[n]
        row={'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':original['family'],
            'consumer':'original-duel-D458-side0-timed-action-feedback',
            'speaker':f"Original duel side0 speaker, voice class{original['voice_class']}",
            'context':original['context'],'source_table':0x02117560 if n<1965 else 0x021175C0,
            'source_voice_classes_including_native_fallback':[original['voice_class']],
            'source_reference':original['source_reference'],'source_hex':original['source_hex'],'source_Japanese':original['source_Japanese'],
            'canonical_source_hex':original['canonical_source_hex'],'current_reference':original['current_reference'],
            'current_text_hex':original['current_hex'],'current_English':original['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note+' Independent alternatives were read aloud as positive/negative timed-action reactions, not as consecutive dialogue. Prose has no authored line breaks, padding or alignment; post-macro24x3 formatting and original gameplay remain required.',
            'editorial_decision':decision,'native_argument_count':0,'native_argument_kind':'none','source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-and-prose-reviewed;new-table-native-format-and-original-gameplay-pending'}
        row['compiled_hex']=compiled(row).hex();records.append(row)
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':PROFILE,'file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'draft-source-prose-reviewed;not-release-approved','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'current_ROM':packet['current_ROM'],'current_ROM_sha256':packet['current_ROM_sha256'],
        'current_COMMON_sha256':packet['current_COMMON_sha256'],'current_ARM9_sha256':packet['current_ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'records':records,'full_goal_complete':False}
    ROOT.mkdir(parents=True);save(OUT,doc)
    save(ROOT/'source_prose_review.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'source_and_prose_reviewed_IDs':list(IDS),'revised_drafts':11,'retained_drafts':5,
        'all_clean_source_glosses_context_voice_and_naturalness_reviewed':True,
        'each_formatting_gate_false_no_new_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_with_source_and_prose_pass']==1267 and ledger['records_editorially_completed']==1229
    assert not set(IDS).intersection(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['records_with_source_and_prose_pass']=1283
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],*IDS])
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted([*drafts['native_message_IDs'],*IDS]);drafts['manuscripts'].append(str(OUT))
    drafts['manuscript_record_subsets_pending'][str(OUT)]=list(IDS)
    drafts['status']='older3-context;successful-shot;15-sighting-remaining-UI;16-duel-action-format-gameplay-pending'
    drafts['note']='54 reviewed incomplete COMMON entries are additional to the broader unreviewed shared/routes/raw-source inventory;14 additional special moves remain unreviewed.'
    ledger['duel_bark_prose_v1200']={'native_message_IDs':list(IDS),'manuscript':str(OUT),
        'source_context':str(packet_path),'source_prose_proof':str(ROOT/'source_prose_review.json'),
        'source_prose_reviewed':16,'formatting_and_actual_pending':True,'completed_entries':0}
    ledger['latest_checkpoint']='V1200 source/prose reviews16 timed duel reactions from clean Japanese and original caller/voice context.1283 prose-reviewed;1229 complete remains unchanged;54 reviewed COMMON entries incomplete plus broader inventory. New formatting/actual gates remain false;14 special moves unreviewed.'
    save(ledger_path,ledger)
    print('16 natural-English drafts reviewed:1283 source/prose reviewed;1229 complete unchanged;format/gameplay pending.',flush=True)


if __name__=='__main__':main()
