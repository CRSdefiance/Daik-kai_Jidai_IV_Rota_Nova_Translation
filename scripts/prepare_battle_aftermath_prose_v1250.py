"""Natural,faithful US-English review of75 connected aftermath alternatives."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_layout_v1250 import IDS,PROFILE,paragraph
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_aftermath_prose_v1250')
OUT=Path('translations/battle_aftermath_editorial_manuscript_v1.json')
# English is authored against the Japanese source/context,not inherited breaks.
# Each entry supplies its own source gloss and specific localization rationale.
REVIEW={
1994:('%s has surrendered!','Reports that the named town has surrendered.','Retain the clear,idiomatic completed-action report;the argument is the native town name.'),
1995:('Admiral! %s has surrendered!','Excitedly addresses the admiral and reports the named town surrender.','Retain both the excited address and the accurate report.'),
1996:('%s has given up!','Casually reports that the named town has surrendered.','Retain the natural informal given up in the established surrender context.'),
1997:('%s has surrendered!','An older-sounding speaker reports the named town surrender.','Retain the concise natural report;do not manufacture archaic English to mimic the Japanese ending.'),
1998:('They say %s wants to surrender!','Reports that the named town says it wishes to surrender.','Restore the reported desire rather than turn this alternative into a completed surrender.'),
1999:('%s has surrendered!','A courteous speaker announces the named town surrender.','Retain the clear report;the portrait and established voice provide characterization.'),
2000:('The enemy flagship has been destroyed!','Formally reports defeat/destruction of the enemy flagship.','Use a complete report and preserve flagship;do not reduce the subject to a generic lead ship.'),
2001:('Enemy flagship destroyed!','Briefly announces defeat/destruction of the enemy flagship.','A concise battle callout is natural here;retain flagship and avoid inventing a separate sinking statement.'),
2002:('Enemy flagship destroyed!','Briefly announces defeat/destruction of the enemy flagship.','Restore the exact flagship referent in a conventional battle callout.'),
2003:('Enemy flagship destroyed!','Briefly announces defeat/destruction of the enemy flagship.','Preserve the identical source report without manufacturing extra dialect or facts.'),
2004:('The enemy flagship sank!','An informal youthful voice reports that the enemy flagship has sunk.','Retain the natural wording;this source explicitly says sank.'),
2005:("We've destroyed the enemy flagship!",'A courteous speaker reports destruction of the enemy flagship.','Retain the complete,idiomatic battle report.'),
2006:("Admiral, our flagship's been hit! We can't stop the flooding!",'Warns the admiral that the flagship has been damaged and flooding cannot be stopped.','Retain the natural urgent report with both the damage and uncontrollable flooding.'),
2007:("Admiral, the flagship's been hit! We can't stop the water coming in!",'A rougher voice warns of flagship damage and unstoppable flooding.','Restore the inability to stop the water,which the older Taking water fragment omitted;keep spoken contractions.'),
2008:("Admiral, this flagship's finished! We can't stop the flooding!",'An older voice says the flagship is finished and the flooding cannot be stopped.','Use natural alarm rather than the clipped ship is done/taking water wording.'),
2009:("Admiral, we're done for! The water won't stop coming in!",'A frightened youthful voice says all is lost and the water will not stop.','Restore the panicked inability to stop the water without adding a weapon or injury.'),
2010:("Admiral, this flagship won't hold out much longer! We can't stop the flooding!",'A courteous speaker warns that the flagship cannot last and the flooding is unstoppable.','Keep both source warnings in fluent English rather than a shortened flooding fragment.'),
2011:("We've defeated the enemy flagship's entire crew and captured the ship!",'Reports that the entire enemy flagship crew has been defeated and the ship captured.','Restore entire crew and flagship in one complete report;defeated does not invent deaths.'),
2012:("Admiral! We beat the enemy flagship's whole crew and took their ship!",'Excitedly reports to the admiral that all flagship crew were beaten and the vessel captured.','Keep the excited address and every important result in natural spoken English.'),
2013:("We beat the enemy flagship's whole crew! The ship's ours!",'Boasts that the whole enemy flagship crew was defeated and the ship captured.','The ship is ours naturally conveys capture;do not substitute an unspecified lead ship.'),
2014:("We beat their flagship's whole crew and took the ship!",'A youthful speaker reports beating all the enemy flagship crew and capturing the vessel.','Restore the complete crew and flagship facts in simple energetic language.'),
2015:("We've defeated the entire enemy crew and captured their flagship!",'A courteous voice reports all enemy flagship crew defeated and the vessel captured.','Use a complete report while preserving all and the precise flagship referent.'),
2016:('The entire crew has been killed! Get to another ship!','Reports that all sailors have died in battle and urges transfer to another vessel.','Preserve the explicit deaths and the destination of the evacuation,without inventing named-character deaths.'),
2017:('The entire crew is dead! Admiral, get to another ship at once!','Urgently warns the admiral that all sailors are dead and orders immediate evacuation to another ship.','Restore urgency and another ship;avoid the old clipped Crew dead fragment.'),
2018:('The entire crew is down! Admiral, hurry and get to another ship!','Warns that all sailors are beaten/down and urges the admiral to flee quickly to another ship.','Do not narrow the ambiguous down/defeated source into explicit deaths;restore hurry.'),
2019:("We're losing the crew! Admiral, get to another ship!",'Warns of mounting crew casualties and urges the admiral to abandon the ship for another.','Express continuing losses naturally and retain the required transfer to another vessel.'),
2020:('The sailors are dying one after another! Admiral, you must abandon ship!','An older voice reports sailors dying in succession and urges the admiral to abandon ship.','Restore the continuing deaths and forceful advice without invented family address or dialect.'),
2021:("The whole crew's down! Admiral, you've got to get to another ship!",'A youthful voice warns all sailors are down and tells the admiral to flee to another ship.','Preserve the source ambiguity about defeat versus death and use natural urgent speech.'),
2022:('Further fighting is pointless. Please surrender.','Politely states that further battle is futile and asks for compliant surrender.','A measured,polite English surrender demand conveys the requested compliance without unnecessary jargon.'),
2023:('Resistance is useless. Surrender.','Sternly declares further resistance futile and commands surrender.','Retain the natural terse demand.'),
2024:("There's no point fighting! Just surrender!",'A direct youthful voice says more fighting is futile and urges surrender.','Retain the idiomatic spoken demand as one paragraph.'),
2025:('Resistance is useless! Surrender!','Forcefully declares resistance futile and demands surrender.','Retain the clear emphatic demand;no invented title or insult is needed.'),
2026:("You can't win! Surrender already!",'Roughly tells the opponent there is no chance of victory and to surrender quickly.','Retain the natural impatience of already.'),
2027:('Resistance is useless! Surrender!','An older speaker declares continued resistance futile and commands compliant surrender.','Retain the natural demand;the source age-marked ending does not require fabricated archaic dialogue.'),
2028:("There's no point fighting anymore! Just surrender!",'A casual youthful speaker says more fighting is pointless and urges surrender.','Replace the old clipped opening with natural complete spoken phrasing.'),
2029:('You cannot win! Surrender immediately!','A courteous speaker says victory is impossible and recommends prompt surrender.','Retain the composed urgent wording appropriate to this voice.'),
2030:("I can't let any more of our people die for nothing... We're surrendering this ship.",'The captain refuses further pointless deaths among companions and announces this ship surrender.','Restore the personal decision and specify this ship rather than imply the whole fleet.'),
2031:("I won't let so many of our comrades die for nothing. We have no choice... We surrender.",'A stern captain refuses to let many comrades die pointlessly and reluctantly orders surrender.','Retain the faithful military wording while normalizing the inherited fullwidth I;the formatter must preserve the complete initial pronoun.'),
2032:("It's hopeless... Admiral, we're surrendering this ship...",'A resigned voice tells the admiral the situation is hopeless and this ship is surrendering.','Use human agency naturally and preserve the individual ship decision;normalize the inherited fullwidth I.'),
2033:("We can't fight anymore... Admiral, we're surrendering this ship.",'A speaker says further fighting is impossible and informs the admiral this ship will surrender.','Keep the weary pause within one prose paragraph and identify the ship rather than the entire fleet.'),
2034:("We're not going to win this... Admiral, we're surrendering this ship.",'A rougher voice sees no prospect of victory and tells the admiral this ship will surrender.','Preserve the defeated assessment and specific ship decision in fluent speech.'),
2035:("We can't let any more of our people die for nothing... We surrender.",'An older voice refuses to waste more companions lives and announces surrender.','Restore the complete moral concern rather than an abbreviated wasted lives fragment.'),
2036:("It's hopeless... They're going to get us all! I'm sorry... We're surrendering this ship.",'A frightened youthful captain says everyone will be beaten,apologizes,and surrenders.','Restore the apology and fear;get us all preserves the source ambiguity rather than automatically claiming everyone will die.'),
2037:("It's important to know when to stand down. Admiral, we're surrendering this ship.",'A courteous captain says knowing when to stop is important and announces this ship surrender.','Keep the pragmatic reasoning and explicit surrender;do not replace surrender with a generic wise retreat.'),
2038:("If you intend to attack this city, we'll drive you back!",'A city defender warns the would-be attackers that an attack will be repelled.','Correct the older third-person they/them to the actual addressed attackers,as proven by the original defender caller.'),
2039:("You intend to attack this city?! I won't allow it!",'A stern defender angrily challenges the intention to attack and refuses to permit it.','Restore the direct challenge and city referent in natural authoritative speech.'),
2040:("If you're planning to attack this city, I won't let you!",'A youthful defender says the plan to attack the city will not be allowed.','Preserve the intended attack and personal refusal rather than a flattened generic statement.'),
2041:("You want to attack this town?! I won't let you!",'A defender indignantly challenges the group intention to attack and refuses it.','Retain the natural challenge while restoring the ordinary ASCII I;do not author a renderer workaround.'),
2042:("You mean to attack this city?! Then don't expect any mercy!",'A rough defender challenges the intended attack and promises no leniency.','Preserve the intended attack and source threat without adding a new insult or past attack.'),
2043:("So you're the ones planning to attack this city?! I'll teach you a lesson!",'An older defender identifies the attackers and threatens to make them regret it.','Restore the rhetorical group address and idiomatic teach you a lesson threat without invented kinship.'),
2044:("You think you can attack this city? Not so fast!",'A youthful defender insists the city will not be overcome so easily.','Use an idiomatic blocking challenge;do not invent a conquest,sacking,or civilian injury.'),
2045:("You've got some nerve attacking this town! We'll beat you back!",'A forceful courteous defender calls the attack brazen and vows to repel it.','Retain the natural,faithful threat.'),
2046:("The enemy flagship fled! We've won!",'Formally reports the enemy flagship has fled and victory is ours.','Retain the complete natural report already seen in original aftermath playback.'),
2047:('The enemy flagship fled! Victory is ours!','Briefly reports the enemy flagship escape and victory.','Restore a complete English report and retain the terse victorious tone.'),
2048:("The enemy flagship fled! Admiral, we've won!",'An excited voice reports the flagship escape and directly announces victory to the admiral.','Restore the source address to the admiral.'),
2049:("The enemy flagship has fled! We've won, Admiral!",'An older voice reports the flagship escape and confirms victory to the admiral.','Restore the source address and use a natural confident confirmation.'),
2050:("The enemy admiral's ship ran away! That means we won!",'A youthful voice reports that the ship carrying the enemy admiral escaped and realizes this means victory.','Restore the actual ship referent and cheerful realization rather than only saying the admiral fled.'),
2051:('The enemy flagship has fled! Admiral, victory is ours!','A courteous speaker reports the flagship escape and announces victory to the admiral.','Restore the explicit address and a composed complete victory report.'),
2114:("Admiral, we're withdrawing!",'Politely informs the admiral that we are leaving the battle.','Retain the natural concise report.'),
2115:("Admiral, we're disengaging!",'Briefly informs the admiral of withdrawal from combat.','Retain the conventional naval phrasing.'),
2116:("Admiral, we're pulling out!",'A casual youthful voice tells the admiral we are withdrawing.','Retain the idiomatic spoken report.'),
2117:("Admiral, we're leaving the battle!",'A speaker tells the admiral we are leaving combat.','Retain the clear natural report.'),
2118:("Admiral, we're pulling out!",'A rougher voice informs the admiral of withdrawal.','Replace the truncated withdrawing label with a complete spoken report.'),
2119:("Admiral, we're withdrawing!",'An older speaker informs the admiral of withdrawal.','Restore natural complete speech without inventing archaic diction.'),
2120:("Admiral, we're leaving the fight!",'A youthful voice reports moving away from the battle.','Use simple natural speech instead of a clipped interface label.'),
2121:("Admiral, we're withdrawing from the battle!",'A courteous speaker informs the admiral that we are withdrawing from combat.','Restore the full report in the established composed voice.'),
2138:("Our flagship is down. We've lost!",'Reports that our flagship has been defeated and we have lost.','Use a natural defeat report that covers both crew defeat and flooding without automatically claiming the ship sank.'),
2139:("Our flagship's been taken out! We've lost!",'A terse voice reports flagship defeat and our loss.','Taken out preserves defeat across both source loss branches without inventing a physical sinking.'),
2140:('They got our flagship! We lost!','A youthful voice reports the flagship was beaten and we lost.','Use natural disappointed speech with the complete flagship and loss facts.'),
2141:("Our flagship's gone... We've lost!",'A speaker laments that the flagship has been beaten and recognizes defeat.','Convey the resigned realization naturally;gone means lost from the fight,not a claim about the hull animation.'),
2142:("They've taken out our flagship! We lost!",'A rougher speaker reports the flagship defeat and our loss.','Preserve the frustrated force without inventing a curse or narrowing the loss to sinking.'),
2143:("It looks like our flagship's been taken out... We've lost!",'An older speaker observes that the flagship seems to have been defeated and admits loss.','Preserve the reflective seems/looks like phrasing and the definite loss announcement.'),
2144:('They got our flagship! We lost!','A childlike speaker cries that the flagship was beaten and we lost.','Use simple distressed language without invented baby talk.'),
2145:("Our flagship's been put out of action. We've lost!",'A courteous speaker reports flagship defeat and our loss.','Use a composed natural report broad enough for crew defeat as well as flooding.'),
2192:('We have no choice... Raise the white flag.','A town representative concedes there is no alternative and orders the white flag raised.','Restore the natural complete first sentence in the original town surrender exchange;keep the white flag explicitly.'),
}


def main():
    assert not ROOT.exists() and not OUT.exists() and tuple(REVIEW)==IDS
    context_path=Path('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
    binding_path=Path('work/analysis/battle_aftermath_bindings_v1249/source_context_complete.json')
    packet,binding=read(context_path),read(binding_path)
    assert binding['all75_source_consumers_speakers_substitutions_and_linked_contexts_mapped']
    assert binding['source_context_sha256']==sha(context_path.read_bytes())
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    canonical_entries=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records=[]
    for source in packet['records']:
        n=source['message_ID'];english,meaning,note=REVIEW[n]
        family=source['source_family']
        if family=='enemy_surrender_report':family='town_surrender_report'
        if family=='town_white_flag_reply':
            speaker='Original town representative selected by B2B60'
            context='Numeric2192 reply between the duty-selected surrender demand2022-2029 and town-name report1994-1999. Original71968 executes the exchange when lookup82428 finds a type6 member;otherwise it emits only the fallback report.'
        elif family in ('town_surrender_report','surrender_demand'):
            speaker='Original duty-selected member;voice alternative from the source table'
            context='Town surrender exchange in original71968. The optional demand is followed by town representative2192 and the town-name report. The %s argument in1994-1999 is the original CTown virtual name;this is not a vessel or fleet name.'
        elif family=='city_defense_challenge':
            speaker='Original defending fleet captain selected by3697C'
            context='Original6ED34 city-attack confirmation and eligibility branch calls53F0C at6EE2C using the defending fleet captain and table178C0. The defender directly addresses the would-be attackers.'
        elif family=='own_ship_surrender_reply':
            speaker='Original flagship captain or native ship-model spokesperson'
            context='Original7251C ship-status processing selects table17840 at72B10 or72B50. A nonflagship uses the original AB158/A4B70 model speaker;the flagship uses3697C. This ship announces its own surrender before its status changes;alternatives are not sequential dialogue.'
        elif family in ('own_crew_lost_abandon_ship','own_flagship_flooding','own_flagship_defeat','battle_withdrawal'):
            speaker='Original member selected by53D44 with selector1 and its native fallback'
            context='Original717F8/71D54 loss or withdrawal branches. Crew defeat2016-2021 or flooding2006-2010 is followed by defeat report2138-2145. Withdrawal2114-2121 is a separate branch. Do not infer sinking for every defeat alternative.'
        else:
            speaker='Original member selected by53D44 with selector1 and its native fallback'
            context='Original72368 result selector:mode0 emits boarding capture2011-2015,mode1 enemy flagship defeat2000-2005,other mode emits fled/victory2046-2051. These are independent event alternatives;the original battle outcome is not changed by translation.'
        old=' '.join(source['current_English'].split())
        decision='retain' if old==english else 'revise'
        row={'id':f'COMMON_MESSAGE_{n}','message_id':n,'source_family':family,
            'consumer':'original-portrait-speech-after-native-printf-and-macro-expansion',
            'speaker':speaker,'context':context,'source_meaning':meaning,'english':english,
            'localization_note':note+' Reviewed as an event voice alternative or its explicitly mapped neighbor,not an arbitrary adjacent-record conversation. Prose remains one paragraph;native margin,word-boundary,glyph,bounds,page and transition checks remain open.',
            'editorial_decision':decision,'source_reference':source['source_reference'],
            'source_hex':source['source_hex'],'source_Japanese':source['source_Japanese'],
            'canonical_source_hex':canonical_entries[n].text.hex(),
            'current_reference':source['current_reference'],'current_text_hex':source['current_hex'],
            'current_English':source['current_English'],'native_argument_count':source['native_argument_count'],
            'native_argument_kind':source['native_argument_kind'],'source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            'status':'source-and-prose-reviewed;native-format-integration-and-gameplay-pending'}
        if 'source_voice_table' in source:row['source_table']=source['source_voice_table']
        else:row['source_numeric_call']=source['source_numeric_call']
        raw=paragraph(row);row['unwrapped_paragraph_hex']=raw.hex()
        assert raw.count(b'%s')==source['source_hex'].count('2573')
        records.append(row)
    assert len(records)==75
    revised=sum(r['editorial_decision']=='revise' for r in records)
    assert revised==55 and len(records)-revised==20
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':PROFILE,'file_path':'/COMMON/MESFILE.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'source-and-prose-reviewed;runtime-layout-integration-and-original-gameplay-open',
        'source_clean_ROM_sha256':packet['source_ROM_sha256'],'current_ROM':packet['current_ROM'],
        'current_ROM_sha256':packet['current_ROM_sha256'],'current_COMMON_sha256':packet['current_COMMON_sha256'],
        'current_ARM9_sha256':packet['current_ARM9_sha256'],'native_context_proof':str(context_path),
        'native_context_proof_sha256':sha(context_path.read_bytes()),'complete_source_binding':str(binding_path),
        'complete_source_binding_sha256':sha(binding_path.read_bytes()),
        'no_compiled_release_payload_or_layout_approval_yet':True,'records':records,'full_goal_complete':False}
    ROOT.mkdir(parents=True);save(OUT,doc)
    proof=ROOT/'source_prose_review.json'
    save(proof,{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),
        'records':75,'revised_drafts':55,'retained_wording_drafts':20,
        'all_per_record_source_context_meaning_voice_and_naturalness_pass':True,
        'original_six_town_name_substitutions_preserved':True,
        'no_authored_padding_alignment_breaks_or_renderer_workarounds':True,
        'new_formatting_approval_ROM_and_completed_editorial_credit':False,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1260 and ledger['records_with_source_and_prose_pass']==1298
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not done.intersection(IDS) and not set(ledger['reviewed_but_incomplete_COMMON_IDs']).intersection(IDS)
    ledger['records_with_source_and_prose_pass']=1373
    ledger['source_prose_reviewed_counts_by_file']={'/COMMON/MESFILE.DK4':1372,'/data/SC2.DK4':1}
    ledger['reviewed_but_incomplete_COMMON_IDs']=sorted([*ledger['reviewed_but_incomplete_COMMON_IDs'],*IDS])
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==113
    drafts=ledger['active_source_prose_drafts']
    assert not drafts['native_message_IDs'] and not drafts['manuscripts'] and not drafts['manuscript_record_subsets_pending']
    drafts.update(native_message_IDs=list(IDS),manuscripts=[str(OUT)],
        manuscript_record_subsets_pending={str(OUT):list(IDS)},
        status='75-aftermath-source-prose-drafts;native-layout-integration-gameplay-open',
        note='75 new drafts plus38 older reviewed incomplete COMMON entries;broader unreviewed shared/routes/raw inventory remains.')
    ledger['battle_aftermath_prose_v1250']={'native_message_IDs':list(IDS),'manuscript':str(OUT),
        'source_context':str(context_path),'source_binding':str(binding_path),'source_prose_proof':str(proof),
        'reviewed_entries':75,'revised_drafts':55,'retained_drafts':20,'native_format_and_actual_pending':True,
        'completed_entries':0}
    ledger['latest_checkpoint']='V1250 source/prose reviews75 connected aftermath/town-surrender/city-defense lines:55 revisions,20 retained. Source/prose1373;1260 complete unchanged.113 reviewed COMMON entries incomplete. Source substitutions and three wrapper frames mapped;native layout,full fonts,registered integration and original gameplay remain open.'
    save(ledger_path,ledger)
    print('75 source/prose reviews:55 revised20 retained;1373 source/prose,1260 complete unchanged;native layout/integration/gameplay open.',flush=True)


if __name__=='__main__':main()
