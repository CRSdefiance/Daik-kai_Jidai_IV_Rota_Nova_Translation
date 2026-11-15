"""Natural, faithful American English for the eight original NPC war responses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

CONTEXT = Path('work/analysis/declaration_responses_context_v1531/source_and_original_actor_context.json')
OUT = Path('translations/declaration_responses_editorial_manuscript_v1.json')
REVIEW = {
    2201: ("What? They've declared war?! Very well. We'll take up their challenge!",
           'A surprised polite response to a declaration of war,then a resigned but willing acceptance of the challenge.',
           'Restore both surprise and acceptance in natural spoken English. The statement is a response to accepted hostilities,not a new choice for the player.'),
    2202: ("Hmm... They've declared war... All fleets, prepare to intercept!",
           'A restrained reaction to the declaration followed by an order for every fleet to prepare to intercept the enemy.',
           'Restore the interception order omitted by the current draft. The pauses convey the stern considered response without authored layout breaks.'),
    2203: ("They've declared war?! All right! We're not going to lose!",
           'An energetic surprised response and determination that the speakers will not lose either.',
           'Preserve youthful competitive resolve. Remove the unsupported crushing threat in the current version;the speaker promises not to lose,not an invented degree of destruction.'),
    2204: ("They've declared war?! Then we'll beat them back!",
           'A surprised confident feminine response promising to defeat the attacker in return.',
           'Beat them back naturally conveys the counter-defeat implicit in kaeriuchi without adding casualty or destruction claims. Keep the confident challenge rather than artificial gendered English.'),
    2205: ("What?! They've declared war on me?! Ha! Do they really think they can beat me?",
           'An angry surprised response that the enemy has dared declare war,followed by a dismissive laugh and a boast asking whether they thought they could defeat him.',
           'Restore the full personal boast and question missing from the abbreviated current line. The original company leader is the speaker;the observed James Clifford response confirms the self-confident context.'),
    2206: ("What?! You dare declare war on me?! You've got a death wish! I'll send you to the bottom!",
           'An enraged arrogant response to the enemy daring to declare war,a declaration that they are recklessly risking their lives,and a threat to send them to a watery grave.',
           'Use natural hostile American English for the explicit source threat. Death wish localizes inochishirazu;send you to the bottom preserves the nautical threat. Ordinary ASCII I requires the mapped post-macro formatter,not a fullwidth workaround.'),
    2207: ("What? What?! Please stop! Did I do something wrong?",
           'A frightened childish reaction asking the aggressor to stop and whether the speaker has done something wrong.',
           'Retain the fluent repeated panic,plea and question. Normalize the current fullwidth I only after the original consumer and literal-English macro behavior have been verified.'),
    2208: ("Hmph! You've declared war?! I'll make you regret that reckless decision!",
           'A gruff formal surprised response to the declaration and a promise to make the aggressor regret that reckless judgment.',
           'Restore the direct promise and specific reckless decision instead of the detached shortened assessment. Hmph conveys the initial gruff reaction without invented titles or relationships.'),
}

if __name__ == '__main__':
    assert not OUT.exists()
    context = read(CONTEXT)
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    rows = []
    for original in context['records_and_neighbors']:
        if not original['selected_war_response']:
            continue
        row = deepcopy(original)
        n = row['message_id']
        english, meaning, note = REVIEW[n]
        assert english.isascii() and english == ' '.join(english.split())
        assert not any(c in english for c in '%{}\n\r\t')
        assert b'%' not in bytes.fromhex(row['source_hex'])
        row.update(id=f'COMMON_MESSAGE_{n}', source_family='NPC-company-leader-declaration-response8',
            speaker='Original target company leader through3CD2C/53F0C;source voice' + str(n - 2201),
            context=context['source_context'], consumer='original-direct-actor-speech-after-selection-printf-and-macro-expansion',
            english=english, source_meaning=meaning, localization_note=note,
            editorial_decision='retain' if english == row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(), native_argument_count=0, source_native_macros=[],
            original_native_entry=context['original_entry'], original_native_parent=context['original_parent'],
            selector_stack_offset=context['selector_stack_offset'], source_table=context['source_table'],
            source_voice_classes=[n - 2201], authored_as_one_unwrapped_paragraph=True,
            review={'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            status='source-context-prose-reviewed;native-font-wrap-release-and-revised-original-event-pending')
        rows.append(row)
    assert [r['message_id'] for r in rows] == list(range(2201, 2209))
    assert all(r['editorial_decision'] == 'revise' for r in rows)
    save(OUT, {'format': 'dk4-native-common-editorial-v1', 'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-relocatable-v1', 'consumer_layout_profile': 'NPC-declaration-direct-actor-postmacro-v1',
        'file_path': '/COMMON/MESFILE.DK4', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'formatting_review_pending': True, 'status': 'eight-source-context-prose-reviewed;native-font-wrap-release-original-event-pending',
        'source_clean_ROM_sha256': context['clean_ROM_sha256'], 'current_ROM': context['candidate'],
        'current_ROM_sha256': context['candidate_sha256'], 'current_COMMON_sha256': context['COMMON_sha256'],
        'current_ARM9_sha256': context['ARM9_sha256'], 'source_context': str(CONTEXT), 'source_context_sha256': sha(CONTEXT.read_bytes()),
        'no_authored_line_breaks_or_alignment': True, 'no_runtime_substitution_or_source_macro_added': True,
        'records': rows, 'revised': 8, 'retained': 0, 'no_native_formatting_release_or_revised_gameplay_completion_approval': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Eight source/context/prose-reviewed war responses,all revised;native wrapping,fonts,release and revised gameplay pending.')
