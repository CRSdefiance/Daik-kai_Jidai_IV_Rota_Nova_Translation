"""Source/voice-faithful American-English review of all15 special calls."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_special_layout_v1216 import IDS,PROFILE,compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_prose_v1216')
OUT=Path('translations/duel_special_editorial_manuscript_v1.json')
REVIEW={
1980:("I'll show you what two swords can do!",'Confidently offers to demonstrate a two-sword fighting technique.','Replace Behold my twin blades, which merely displays weapons and adds theatrical formality, with a natural promise to demonstrate two-sword skill. The original speaker is Samwell, not Maria.','revise'),
1981:('Playtime is over!','Declares that the fooling around ends here.','Retain the idiomatic, forceful taunt. Original actor3 selects this line; no gender or new character relationship is added.','retain'),
1982:('Just an afterimage!','Declares the visible image to be a lingering afterimage rather than the true body.','Express Cristina\'s counter/illusion taunt naturally. Just conveys the source declarative dismissal in the afterimage animation context.','revise'),
1983:('White Tree Sword Style: Twin Shadow Formation!','Announces the White Tree school of swordsmanship and its named Twin Shadow Formation technique.','Preserve both named components. Formation is the natural martial rendering of 陣; omit the unnecessary English article before the attack name. White Tree translates 白樹 semantically without inventing a pronunciation or equating its kanji with the separately verified katakana surname Shiraki. The established Yukihisa Shiraki name remains unchanged.','revise'),
1984:('Did you think such a predictable attack would work?','Scornfully asks whether the opponent expected such a monotonous/predictable attack to be effective.','Correct dull, which can mean merely boring, to predictable. Preserve Gerhard\'s rhetorical question and confidence instead of converting it to a generic statement.','revise'),
1985:("That swordplay is child's play compared to Gerhard's training!",'Dismisses the opponent\'s swordplay as childish tricks beside Gerhard\'s training.','Retain the natural idiom child\'s play and the explicit Gerhard comparison. Do not invent a family relationship or spell the established name differently. Original actor9 is Camille.','retain'),
1986:('Think brute-force swings will work on me? Take this!','Challenges the effectiveness of strength-only swordplay and follows with an attacking shout.','Retain the natural combat rhetoric, weapon-motion meaning and follow-up challenge. Original actor21 selects this line; no guaranteed result is asserted.','retain'),
1987:("Ha ha ha! It's showtime!",'Laughs and announces that the show is beginning.','Retain the playful showman voice. Normalize the inherited fullwidth I; do not author renderer workarounds into English. Original actor20 is Fernando; the Angelo/Fernando pairing is proven by the executed literal loads.','revise'),
1988:("Hey, hey! What's the matter? I'm not even trying yet!",'Taunts the opponent and boasts of not yet fighting seriously.','Retain the idiomatic teasing boast and normalize the old fullwidth I. Original actor15 is Angelo. The sentence is a character boast, not evidence about an actual combat calculation.','revise'),
1989:("I'll show you swordplay honed on the battlefield!",'Promises to demonstrate sword skill refined through battlefield experience.','Retain the natural battlefield-honed swordplay wording; normalize the inherited fullwidth I. Preserve the source boast without adding a rank, campaign or historical fact. Original actor17 is Al.','revise'),
1990:("You're done!",'Announces a finishing blow or intent to finish the opponent.','Retain the concise, idiomatic finisher taunt. It expresses Hodram\'s attack intent and does not force or certify the eventual duel result.','retain'),
1991:("Aaaah! You're going flying!",'A childlike shout followed by a playful declaration of throwing the opponent.','Retain the energetic, natural throw taunt. The original Emilio animation supports the throwing sense; no new weapon or supernatural power is added.','retain'),
1992:("Come on! You're wide open!",'Goads the opponent while pointing out that their guard is full of openings.','Use the standard natural combat idiom wide open and retain the goading address rather than the older detached So many openings fragment.','revise'),
1993:('Taoist arts! Hyaah!','Announces Taoist techniques and gives a martial exertion shout.','Retain the established clear terminology and shout. Do not invent a more specific named spell, deity or medical implication. Original actor25 is Yifa.','retain'),
2146:("I'll show you the power of booze!",'Boasts that the speaker will demonstrate alcohol-fueled power.','Retain the comic, natural boast and nonspecific alcohol reference. Normalize the old fullwidth I. Original actor6 is Julio; the earlier generic town-message description did not identify this special-move consumer.','revise'),
}


def main():
    assert not ROOT.exists() and not OUT.exists() and tuple(REVIEW)==IDS
    packet_path=Path('work/analysis/duel_special_context_v1215b/source_context_packet.json');packet=read(packet_path)
    records=[]
    for source in packet['records']:
        n=source['message_ID'];english,meaning,note,decision=REVIEW[n]
        row={'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':'special_move_numeric',
            'consumer':'original-D4D0-static-duel-side0-duration120','speaker':source['source_speaker_name'],
            'source_actor_ID':source['source_actor_ID'],'source_method':source['source_method'],
            'source_call_return':source['source_call_return'],'context':source['context'],
            'source_reference':source['source_reference'],'source_hex':source['source_hex'],'source_Japanese':source['source_Japanese'],
            'canonical_source_hex':source['canonical_source_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note+' Read aloud as an independent special-move call, not consecutive conversation. Prose stays one paragraph until original macro expansion. Native24x3 formatting, complete glyphs and representative original gameplay remain required.',
            'editorial_decision':decision,'native_argument_count':0,'native_argument_kind':'none','source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-and-prose-reviewed;native-numeric-format-and-actual-gameplay-pending'}
        row['compiled_hex']=compiled(row).hex();records.append(row)
    assert len(records)==15 and sum(r['editorial_decision']=='revise' for r in records)==9
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':PROFILE,'file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'source-prose-reviewed;not-release-approved','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'current_ROM':packet['current_ROM'],'current_ROM_sha256':packet['current_ROM_sha256'],
        'current_COMMON_sha256':packet['current_COMMON_sha256'],'current_ARM9_sha256':packet['current_ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'records':records,'full_goal_complete':False}
    ROOT.mkdir(parents=True);save(OUT,doc)
    save(ROOT/'source_prose_review.json',{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'source_and_prose_reviewed_IDs':list(IDS),'revised_drafts':9,'retained_drafts':6,
        'all_original_actor_message_bindings_and_faithful_glosses_reviewed':True,
        'newly_discovered2146_included':True,'formatting_gates_false_and_no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_with_source_and_prose_pass']==1283 and ledger['records_editorially_completed']==1245
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(IDS) and not set(IDS).intersection(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ledger['records_with_source_and_prose_pass']=1298
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],*IDS])
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==53
    ledger['source_prose_reviewed_counts_by_file']={'/COMMON/MESFILE.DK4':1297,'/data/SC2.DK4':1}
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=sorted([*drafts['native_message_IDs'],*IDS])
    drafts['manuscripts'].append(str(OUT));drafts['manuscript_record_subsets_pending'][str(OUT)]=list(IDS)
    drafts.update(status='older3-context;successful-shot;15-sighting-remaining-UI;15-special-native-format-and-gameplay-pending',
        note='53 reviewed incomplete COMMON entries are additional to the broader unreviewed shared/routes/raw-source inventory. Special set includes nonadjacent2146.')
    ledger['duel_special_prose_v1216']={'native_message_IDs':list(IDS),'manuscript':str(OUT),
        'source_context':str(packet_path),'source_prose_proof':str(ROOT/'source_prose_review.json'),
        'reviewed_entries':15,'native_format_and_actual_pending':True,'completed_entries':0}
    ledger['latest_checkpoint']='V1216 source/prose reviews all15 original special calls, including newly mapped2146.1298 source/prose reviewed;1245 complete unchanged;53 reviewed COMMON entries incomplete plus broader inventory. Source actor pairing and Japanese meanings verified;new numeric-consumer formatting and actual gameplay remain open.'
    save(ledger_path,ledger)
    print('15 source/English special calls reviewed:1298 prose-reviewed;1245 complete unchanged;format/gameplay pending.',flush=True)


if __name__=='__main__':main()
