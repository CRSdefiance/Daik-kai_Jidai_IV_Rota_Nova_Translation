"""Review clean Inn prose with proven caller context; production gates stay open."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_context_v801')
MANUSCRIPT=Path('translations/inn_editorial_manuscript_v1.json')

PROSE={
1177:("That'll be 1 gold coin.", 'An overnight stay costs one gold coin.', 'State the fee conversationally at the original yes/no confirmation.'),
1178:('Sleep well!', 'The innkeeper wishes the guest a good night.', 'Retain the existing natural hospitality line.'),
1179:("It's 1 gold coin a night. How many nights would you like to stay?", 'Each night costs one gold coin; ask the desired number of nights.', 'Keep both the nightly price and the stay-length question in one logical paragraph.'),
1180:("You're staying for %s nights, then?", 'Confirm that the guest will stay the supplied number of nights.', 'The original choice is 3, 10 or 30 nights; preserve the original full-width numeric argument without adding padding.'),
1181:('Enjoy your stay.', 'A welcoming invitation to take it easy during the stay.', 'Use a natural inn hospitality phrase for goyukkuri.'),
1182:('Over in %s, the price of %s has plummeted, or so I hear.', 'The innkeeper has heard that the supplied commodity price has crashed in the supplied town.', 'Preserve town then goods argument order and the hearsay tone; this concerns one commodity, not all prices.'),
1183:('They say %s suffered a huge loss.', 'Rumor says the affected company suffered a large loss.', 'Retain the accurate natural existing line; the company argument is the same affected company as the market event.'),
1184:('I hear someone in %s bought up all the %s.', 'Apparently there was a buyout of the supplied commodity in the supplied town.', 'Render kaishime as buying up the supply; keep town then goods and do not invent the buyer.'),
1185:('They say %s was really upset about missing out.', 'The affected company that missed the chance to buy was reportedly very upset.', 'Replace the unrelated faction-opposition question. Missing out refers to the purchase in the preceding buyout report.'),
1186:("Admiral, I've gathered some information on %s.", 'The Strategist says they obtained information on the supplied company for the Admiral.', 'Neutral professional report; restore the address and first-person voice lost in the old fragment.'),
1187:("Admiral, I've obtained some information on %s.", 'The Strategist politely reports having obtained information on the supplied company.', 'Use obtained for the more formal itashimashita voice without inventing rank or relationship.'),
1188:('Admiral, I looked into %s for you.', 'The Strategist casually says they investigated the supplied company for the Admiral.', 'Keep the casual prepared-for-you tone.'),
1189:('Oh, by the way, I looked into %s.', 'The Strategist remembers to mention having investigated the supplied company.', 'Preserve the conversational souda opening and the softer casual voice without adding an Admiral address absent from this source.'),
1190:("Admiral, I've been checking up on %s.", 'The Strategist casually and assertively reports investigating the supplied company.', 'Use a confident informal report for the ze ending; do not invent a specific spying method.'),
1191:("Admiral, I've got some information on %s.", 'The Strategist assertively says they secured information on the supplied company.', 'Use a hearty, direct report for the zo voice.'),
1192:('I did some digging on %s!', 'The childlike casual speaker says they investigated the supplied company.', 'A lively informal report for oira; do not insert an Admiral address absent from this source.'),
1193:('Admiral, I have gathered some information concerning %s.', 'The elder formal voice reports obtaining information regarding the supplied company.', 'Keep deliberate formality without adding archaic language or a family relationship.'),
1194:("You don't have enough money.", 'The innkeeper says there is insufficient money to pay for the stay.', 'Address the guest naturally; preserve both the one-night and multi-night insufficient-funds consumers.'),
1195:("%s, I hear %s fought %s's fleet and won a brilliant victory!", 'At the supplied relative time, the town or company fought the other company fleet and won impressively.', 'Keep time, subject, opposing-fleet company in source order. The subject can be a town or a company; preserve the fleet and hearsay.'),
1196:("%s, %s took on %s's fleet and got beaten back, or so I hear.", 'At the supplied relative time, the town or company fought the other company fleet but was defeated instead.', 'Restore the opposing fleet and the reversal in kaeriuchi. Preserve time, subject, opposing company in that order.'),
1197:('%s, %s attacked %s. What a terrible thing to do!', 'At the supplied relative time, the attacking company raided the supplied town; the innkeeper condemns the action.', 'Preserve time, attacker and town plus the disapproving second sentence.'),
1198:('%s, %s attacked %s and failed miserably. Serves them right!', 'At the supplied relative time, the attacking company raid on the supplied town failed badly; the innkeeper approves of their comeuppance.', 'Retain the existing faithful natural line, with time, attacker and town in original order.'),
1199:('Oh, are you leaving already?', 'The innkeeper asks whether the guest is departing already.', 'Retain the existing natural question; the native consumer is the interrupt confirmation inside the multi-night loop, not a healing report.'),
}


def main():
    assert not MANUSCRIPT.exists(), 'Do not overwrite a pinned reviewed manuscript'
    packet=read('work/analysis/inn_editorial_v800/source_inventory.json')
    context=read(ROOT/'native_context.json');baseline=read(ROOT/'baseline_and_time_ownership.json')
    assert len(context['voice_cases'])==208 and len(context['month_prefix_native_cases'])==144
    assert len(context['stay_caller_fragments'])==10 and len(context['report_caller_fragments'])==3
    assert baseline['one_night_cost1_and_calendar48'] and baseline['three_night_cost3_and_calendar144']
    records=[]
    for source in packet['rows']:
        n=source['message_id'];english,meaning,note=PROSE[n]
        assert english.count('%s')==source['source_percent_s_count_inventory_only']
        assert '\n' not in english and english==english.strip()
        strategist=1186<=n<=1193
        if strategist:
            args=['company_name'];scene='Original5CC28-5CC44 calls queued53D44 with role2(参謀/Strategist),voice table021180E0 and the company name. Original53F4C selects this voice;all208 native actors are checked. Actual revised report activation remains pending.'
        elif n in (1182,1184):
            args=['town_name','goods_name'];scene='Original5CC70 market consumer: event type0 selects1182 then1183;type1 selects1184 then1185. Event byte6 supplies town,byte7 goods,byte4 affected company. Both original getter sequences and actual Inn speaker provider are proven;isolated event fields do not prove naturally occurring eligibility.'
        elif n in (1183,1185):
            args=['affected_company_name'];scene='Second message in original5CC70 market pair;the affected company comes from event byte4 and the original company name getter.1183 follows a crash;1185 follows a buyout.'
        elif 1195<=n<=1198:
            args=['relative_month','town_or_company_name','opposing_fleet_company_name'] if n<=1196 else ['relative_month','attacking_company_name','town_name']
            scene='Original history consumers5C5B0/5C8DC use1195-1196 for town-versus-fleet and company-versus-fleet;5C72C uses1197-1198 for company raids on towns.5CA8C supplies relative month,not a player name. Original selected-event fragments and all144 month pairs are proven;event eligibility and revised actual display remain pending.'
        else:
            args=['number_of_nights'] if n==1180 else []
            scene='Original one-night5D368 or multi-night5D1A8 stay branch;caller-fragment proof binds the Innkeeper and native wrappers. Choices3/10/30 useABF50 for1180.1177 is yes/no;1178 is the accepted one-night wish;1179 asks duration;1181 begins multi-night rest;1194 rejects insufficient funds;1199 is multi-night interruption yes/no. Baseline actual1177-1181 and1+3-night cost/calendar/normal return are verified;revised playback remains pending.'
        decision='retain' if n in (1178,1183,1198,1199) else 'revise'
        records.append(dict(id=f'COMMON_MESSAGE_{n}',message_id=n,
            interaction_group='Inn-stays-market-news-information-and-battle-rumors',
            source_hex=source['source_hex'],japanese=source['japanese'],source_reference=source['source_reference'],
            current_text_hex=source['current_hex'],current_English=source['current_English'],current_reference=source['current_reference'],
            source_meaning=meaning,english=english+'{PAD}',
            speaker='Original Strategist role2,voice variant'+str(n-1186) if strategist else 'Original Innkeeper,building role8(actor142 in Istanbul)',
            context=scene,localization_note=note,
            source_native_arguments=args,English_argument_source_indices=list(range(len(args))),decision=decision,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status='source-context-and-prose-reviewed;production-native-formatting-integration-and-revised-playback-pending'))
    doc=dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',
        target_locale='en-US',file_path='/COMMON/MESFILE.DK4',
        review_gates=['source','context','localization','naturalness','formatting'],
        source_pins=dict(clean_ROM_sha256='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
            current_ROM_sha256=packet['candidate_sha256'],source_ARM9_sha256=packet['source_ARM9_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256']),
        native_context_proof=str(ROOT/'native_context.json'),native_context_sha256=sha((ROOT/'native_context.json').read_bytes()),
        baseline_and_time_proof=str(ROOT/'baseline_and_time_ownership.json'),baseline_and_time_proof_sha256=sha((ROOT/'baseline_and_time_ownership.json').read_bytes()),
        records=records,production_approval=False,ROM_changed=False,full_goal_complete=False,
        remaining=['Compile reviewed paragraphs through COMMON runtime formatting;preserve existing selector/ABI contracts.',
                   'Install full owned time phrases with NULs and recheck144 native month cases.',
                   'Inspect every generated wrap and full native font plane,including long town/company/goods and full-width night counts.',
                   'Register combined release,verify exact patch reconstruction,and test revised real inn scenes plus isolated original market/report events.'],
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(MANUSCRIPT,doc)
    times=[]
    for number,(jp,en,gloss) in enumerate((('先月','Last month','The previous month,including year rollover.'),
         ('今月','This month','The same calendar month.'),('%sカ月前','%s months ago','The supplied elapsed number of months;the native helper uses this form only for2-11.'))):
        times.append(dict(id='INN_RELATIVE_MONTH_'+str(number),japanese=jp,english=en,source_meaning=gloss,
            speaker='Innkeeper relative-time argument',context='Original5CA8C produces the first argument of1195-1198.',
            localization_note='Expand UI abbreviation to natural prose. Share the two identical numeric format strings inside the original40-byte allocation;no next-allocation or palette/graphics change.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    save('translations/inn_time_phrases_manuscript_v1.json',dict(format='dk4-inn-time-prefix-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path='/__arm9__.bin',records=times,source_ownership_proof=str(ROOT/'baseline_and_time_ownership.json'),
        production_approval=False,ROM_changed=False,full_goal_complete=False))
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==527 and ledger['records_with_source_and_prose_pass']==530
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    ledger['records_with_source_and_prose_pass']=553;ledger['records_with_source_prose_drafts']=553
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']+=list(range(1177,1200));active['manuscripts'].append(str(MANUSCRIPT))
    active['status']='750-752-context-unmapped;Inn1177-1199-source-context-prose-reviewed-production-pending'
    active['note']='23 Inn source/context/prose reviewed(19 proposed revisions,4 retained);no new production formatting,integration or completion credit. Three older contexts750-752 remain unmapped.'
    ledger['next_Inn_source_packet'].update(dict(status='source-context-and-prose-reviewed;production-native-formatting-and-revised-gameplay-pending',
        manuscript=str(MANUSCRIPT),native_context=str(ROOT/'native_context.json'),baseline=str(ROOT/'baseline_and_time_ownership.json'),review_credit=23,completion_credit=0))
    for finding in ledger['findings']:
        if finding['id']=='COMMON1185-buyout-rumor-wrong-faction-question':
            finding.update(dict(status='source-consumer-context-proven;faithful-revision-drafted;integration-pending',proof=str(ROOT/'native_context.json'),
                detail='Original5CC70 type1 invokes1184 town/goods then1185 affected-company. Replace unrelated faction-opposition question with upset-over-missed-buyout report. No revised ROM shipped yet.'))
    ledger['findings'].append(dict(id='Inn-relative-month-prose-abbreviations',status='source-context-and-owned40-byte-plan-reviewed;native-installation-pending',
        proof=str(ROOT/'baseline_and_time_ownership.json'),detail='First rumor argument is relative calendar month. Last Mo/This Mo/%s Mo. Ago should become full prose. Four original pointer references only;sharing duplicate numeric format fits full English in40 owned bytes.'))
    ledger['latest_checkpoint']='V801 Inn source/context/prose pass:23 COMMON draft records(19 revisions/4 retained),208 native voice selections,144 relative-month cases,4 original market calls,6 selected battle/raid fragments,10 stay fragments and3 queued-report company arguments. Completed V799 baseline cold boot verifies five active Inn IDs,1+3-night fees/calendar and normal town return. Full month phrases have a source-owned40-byte plan. No new ROM,production formatting or completion credit:527 COMMON complete/553 source-prose reviewed. Full editorial goal and separate graphics audit remain unfinished.'
    ledger['coverage_units'][0]['next']='Integrate Inn1177-1199 with complete native formatting,full month phrases and revised gameplay/registered combined patch;then shared1200 onward,older750-752 contexts,all routes and other prose.'
    ledger['research_checkpoints'].append(dict(id='V801-Inn23-context-and-prose',documentation='docs/inn_editorial_v801_checkpoint.md',new_source_prose_reviewed=23,new_editorially_completed=0,new_ROM=False,full_goal_complete=False))
    save(ledger_path,ledger)
    print('Inn23 source/context/prose draft:19 revise/4 retain. Three full relative-month phrases reviewed.527 complete/553 source-prose;production formatting and integration open.',flush=True)


if __name__=='__main__':main()
