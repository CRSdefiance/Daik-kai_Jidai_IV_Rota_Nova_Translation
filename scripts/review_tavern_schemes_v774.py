"""Source-led scheme editorial draft; presentation approval remains separate."""

import re
from pathlib import Path

from scripts.context_tavern_schemes_v774 import ROOT, TABLES
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT = Path('translations/tavern_schemes_editorial_manuscript_v1.json')
TEXTS = {
908: "Disrupting the enemy will cost about 1,000 coins. What kind of scheme do you have in mind?",
909: "With 1,000 gold coins, we can disrupt the enemy. What scheme shall we use?",
910: "1,000 gold coins should be enough. What scheme shall we use?",
911: "With 1,000 gold coins, we can throw the enemy off balance. What scheme do you want?",
912: "With 1,000 gold coins, we can certainly disrupt the enemy. Which scheme shall we choose?",
913: "With 1,000 gold coins, we can really surprise them! What should we do?",
914: "About 1,000 gold coins should let us disrupt the enemy. What scheme shall we try?",
915: "%s, correct? Please choose the faction we should target.",
916: "%s, then? Which faction should we target?",
917: "%s, right? Which faction are we targeting?",
918: "%s, then? Which faction should we target?",
919: "%s, right? So, which faction should we target?",
920: "Hmm, %s? Which faction shall we target?",
921: "Which town should I send them to?",
922: "Which town are we sending them to?",
923: "Which town do you want me to send them to?",
924: "Which town shall we send them to?",
925: "Which town should they go to?",
926: "Which town would you like us to send them to?",
927: "Which town should we spread the rumors in?",
928: "Which town should we spread the rumors in?",
929: "Which town do you want the rumors spread in?",
930: "Which town shall we spread the rumors in?",
931: "Where do you want us to spread the rumors?",
932: "Which town would you like us to spread the rumors in?",
933: "Which faction should we turn them against?",
934: "Who should we get them to pick a fight with?",
935: "Who should we turn them against?",
936: "Who do you want us to set them against?",
937: "Which faction shall we turn them against?",
938: "Who do you want them picking a fight with?",
939: "Which faction would you have us turn them against?",
940: "We're to lure a fleet from %s to %s, correct?",
941: "We're to lure a fleet from %s to %s. Is that correct?",
942: "We're drawing a fleet from %s out to %s, right?",
943: "You want us to draw a fleet from %s out to %s, right?",
944: "So, we're luring a fleet from %s to %s, right?",
945: "We're luring a fleet from %s to %s. Is that right?",
946: "We're getting a fleet from %s to come out to %s, right?",
947: "We're to lure a fleet from %s to %s. Is that your order?",
948: "We're to turn %s and %s against each other, correct?",
949: "Turn %s and %s against each other?",
950: "We're getting %s and %s to fight, right?",
951: "You want %s and %s to fight each other, right?",
952: "So, we're getting %s and %s to fight each other, right?",
953: "Pit %s against %s?",
954: "We're getting %s and %s to quarrel, right?",
955: "We're to set %s and %s against each other, correct?",
956: "We're to spread bad rumors in %s about %s, correct?",
957: "We're to spread bad rumors in %s about %s. Is that correct?",
958: "We're spreading bad rumors in %s about %s, right?",
959: "I'm to spread bad rumors in %s about %s, correct?",
960: "You want me to spread bad rumors in %s about %s?",
961: "We're spreading bad rumors in %s about %s, is that right?",
962: "So, we tell people in %s that %s is bad news, right?",
963: "Hmm, we're to spread bad rumors in %s about %s, correct?",
}
PRICE_GLOSSES = {
908: 'Disrupting the enemy costs about1000 gold coins; asks which scheme to use.',
909: 'With1000 gold coins, the enemy can be disrupted; asks which scheme to use.',
910: '1000 gold coins should be enough; casually asks which scheme to choose.',
911: 'With1000 gold coins, the enemy can be disrupted; bluntly asks which scheme to use.',
912: 'With as much as1000 gold coins, the enemy can be disrupted; older voice asks which scheme is best.',
913: 'With1000 gold coins, they can really be surprised; enthusiastically asks what to do.',
914: 'About1000 gold coins will enable disruption; formally asks which scheme to attempt.',
}


def normal(text):
    return ' '.join(text.replace('\uff29','I').split())


def main():
    packet = read(ROOT/'source_and_neighbors.json')
    context = read(ROOT/'native_context.json')
    assert context['candidate_sha256'] == packet['pins'][2]['ROM_sha256']
    assert len(context['all320_actual_actor_voice_selections']) == 320
    sources = {r['id']:r for r in packet['rows']}
    records = []
    for table, ids in TABLES.items():
        for voice,n in enumerate(ids):
            if n == -1: continue
            s = sources[n]
            args = ['scheme_label'] if 915<=n<=920 else ['faction','town'] if 940<=n<=947 else ['first_faction','second_faction'] if 948<=n<=955 else ['town','faction'] if 956<=n<=963 else []
            expected = len(args)
            assert TEXTS[n].count('%s') == s['Japanese'].count('%s') == expected
            assert TEXTS[n].isascii() and not re.search(r'\s{2,}',TEXTS[n])
            if n <= 914:
                meaning = PRICE_GLOSSES[n]
                note = 'Keep source amount,approximation where stated,and individual formality. Disruption is a scheme effect,not a mental confusion status. Retain the enthusiastic surprise wording for913.'
                scene = 'Original57334-57348 role2 introduction before choosing a scheme.'
            elif n <= 920:
                meaning = 'Confirm the selected scheme and ask which opposing faction to target.'
                note = 'The argument is an exact scheme menu label such as Forge Papers,not a sum or the name of an opposing faction. Neutral label confirmation works with all four labels. Correct the old question about which faction opposes the scheme.'
                scene = 'Original56F30-56F44 role2 narration; original93D5C supplies action6/7/8/9 label before first faction menu.'
            elif n <= 926:
                meaning = 'Ask which town the selected opposing fleet should be sent to.'
                note = 'The Lure Fleet branch supplies the referent; retain conversational pronouns and voice without inventing our own fleet or agents.'
                scene = 'Original57104 action6 branch to57130-57138; destination town selector follows.'
            elif n <= 932:
                meaning = 'Ask which town to spread the hostile rumors in.'
                note = 'Use a natural location question for the town selector. Singular/plural rumor is a number-neutral scheme description; do not invent a reputation outcome.'
                scene = 'Original57104 action8 branch to57140-57148; town selector follows. Bribe action9 uses a different table outside this batch.'
            elif n <= 939:
                meaning = 'Ask which second faction to set at odds with the already selected first faction.'
                note = 'Restore the existing first-faction referent so the question clearly selects its rival. Faction is a collective; do not invent genders,war declarations or successful outcomes.'
                scene = 'Original51B64 mode4 branch to51B84-51B8C; earlier51ABC-51B34 excludes first faction and filters candidates for forged-paper discord.'
            elif n <= 947:
                meaning = 'Confirm luring a fleet belonging to the selected faction to the selected town.'
                note = 'Original faction and town getters supply arguments in this order. A fleet from avoids a redundant Fleet\'s fleet for the real Bergstrom Fleet name,without changing glossary names. Preserve each voice\'s question and informality.'
                scene = 'Original56CB0-56CF4 uses faction virtual+8 then destination-town virtual+8; role2 yes/no wrapper53CB0.'
            elif n <= 955:
                meaning = 'Confirm instigating conflict or discord between the two selected factions.'
                note = 'Keep both faction arguments and the confirmation. Fight/quarrel/turn against reflect source voice; do not promise a formal war or success. Existing natural948/949/953 wording can be retained after layout normalization.'
                scene = 'Original56E30-56E64 gets first and second faction names by virtual+8; role2 yes/no wrapper53CB0.'
            else:
                meaning = 'Confirm spreading bad rumors in the first argument town about the second argument faction.'
                if n == 962: meaning += ' The colloquial voice specifically calls the target outrageous or bad news.'
                note = 'Preserve TOWN then FACTION,unlike the lure confirmation. State bad/hostile rumors,which old956/957 omitted. Bad news in962 preserves the insult and works for a company or named person; terrible person falsely assumes the target is an individual.'
                scene = 'Original56B60-56BA0 gets town virtual+8 FIRST then faction virtual+8 SECOND; role2 yes/no wrapper53CB0.'
            records.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,
                'interaction_group':f'Tavern-scheme-table-{table:08X}',
                'source_hex':s['source_hex'],'japanese':s['Japanese'],
                'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_hex'],
                'current_text_hex':s['current_hex'],'current_English':s['current_English'],
                'current_reference':s['current_reference'],'english':TEXTS[n]+'{PAD}',
                'source_meaning':meaning,'speaker':f'Original role2 Strategist,voice slot{voice}',
                'context':scene,'localization_note':note,'source_voice_table':table,'source_voice_slot':voice,
                'source_native_arguments':args,'English_argument_source_indices':list(range(expected)),
                'decision':'retain' if normal(s['current_English']) == TEXTS[n] else 'revise',
                'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
                'status':'source-context-prose-reviewed-native-layout-and-integration-pending'})
    records.sort(key=lambda r:r['message_id'])
    assert [r['message_id'] for r in records] == list(range(908,964))
    save(MANUSCRIPT,{'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2',
        'encoder':'dialogue-fixed-v1','target_locale':'en-US',
        'review_gates':['source','context','localization','naturalness','formatting'],
        'status':'source-context-prose-reviewed-NOT-playable',
        'file_path':'/COMMON/MESFILE.DK4','source_pins':packet['pins'],
        'native_context_proof':str(ROOT/'native_context.json'),
        'source_context_scope':'Original consumer fragments and real providers,not gameplay activation or successful scheme outcomes.',
        'records':records,'producer_sha256':__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest()})
    print('56 source/context/prose drafts;',sum(r['decision']=='revise' for r in records),'revised wordings;',sum(r['decision']=='retain' for r in records),'retained. Formatting and integration unapproved.',flush=True)


if __name__ == '__main__': main()
