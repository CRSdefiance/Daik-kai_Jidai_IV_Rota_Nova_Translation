"""Faithful natural fear/awe reactions for original creature and ghost inspection."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

CONTEXT = Path('work/analysis/sea_responses_context_v1552/source_and_original_inspection_context.json')
OUT = Path('translations/sea_responses_editorial_manuscript_v1.json')
REVIEW = {
    2209: ("O-oh, no... Are we going to make it home alive?",
           'A panicked,polite speaker stammers and wonders whether the group can return alive.',
           'Use a natural frightened stammer and complete question. Remove the unsupported declaration of war;the original inspection target can be a creature or ghost ship,and the Japanese never mentions war.'),
    2210: ("Incredible... I can hardly fathom it!",
           'A restrained astonished speaker says the sight is beyond comprehension.',
           'Express hakarishirenu as inability to comprehend,not a claim about measurable physical size. The complete natural clause preserves the educated voice and astonishment.'),
    2211: ("Whoa... I've never seen anything like that before!",
           'An excited informal speaker says this is the first time they have seen anything like it.',
           'Restore the complete personal observation in natural American English while keeping the drawn-out initial amazement. Do not invent a creature species or an encounter outcome.'),
    2212: ("A-amazing... How can something like that be out at sea?",
           'A surprised feminine speaker stammers and expresses disbelief that such a thing is in the sea.',
           'A natural rhetorical question conveys the Japanese elliptical disbelief. Avoid lives in the sea,which would invent a biological habitat claim and is unsuitable for the source Ghost Ship alternative.'),
    2213: ("Wow... A monster!",
           'A rough informal speaker reacts with amazement and identifies the frightening sight as a monster.',
           'Retain the current natural shocked exclamation. The noun phrase is intentional spoken recognition matching bakemon,not a missing predicate or fit-only abbreviation.'),
    2214: ("Whoa! Can we beat that thing?",
           'An excited speaker asks whether the group can defeat such a thing.',
           'Retain the fluent complete question and initial exclamation. It expresses doubt about a possible fight,not a claim that combat has begun or that the group will win.'),
    2215: ("Aaaah! I'm scared!",
           'A frightened childish speaker cries out and says they are scared.',
           'Keep the drawn-out frightened cry and use the natural personal admission rather than the stiff translated So scary fragment. Preserve the vulnerable informal voice without inventing age,kinship or rank.'),
    2216: ("A true mystery of the sea...",
           'An older formal speaker marvels that the sight is indeed a mystery of the sea.',
           'Retain the natural contemplative exclamation and trailing sense of wonder. The deliberate elliptical observation suits the source voice;it need not be expanded into explanatory narration or a species claim.'),
}

if __name__ == '__main__':
    assert not OUT.exists()
    context = read(CONTEXT)
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    rows = []
    for original in context['records_and_neighbors']:
        if not original['selected_separate_fear_awe_response']:
            continue
        row = deepcopy(original)
        n = row['message_id']
        english, meaning, note = REVIEW[n]
        assert english.isascii() and english == ' '.join(english.split())
        assert not any(c in english for c in '%{}\n\r\t')
        assert b'%' not in bytes.fromhex(row['source_hex'])
        row.update(id=f'COMMON_MESSAGE_{n}', source_family='sea-creature-ghost-inspection-fear-awe8',
            speaker='Original logical role7 through82478/53D44;source voice' + str(n - 2209),
            context=context['source_context'], consumer='original-role7-speech-after-selection-printf-and-macro-expansion',
            english=english, source_meaning=meaning, localization_note=note,
            editorial_decision='retain' if english == row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(), native_argument_count=0, source_native_macros=[],
            original_native_entry=context['original_entry'], original_native_parent=context['original_parent'],
            selector_stack_offset=context['selector_stack_offset'], source_table=context['source_table'], original_role=7,
            source_voice_classes=[n - 2209], authored_as_one_unwrapped_paragraph=True,
            review={'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
            status='source-context-prose-reviewed;native-font-wrap-release-and-original-inspection-pending')
        rows.append(row)
    assert [r['message_id'] for r in rows] == list(range(2209, 2217))
    assert sum(r['editorial_decision'] == 'revise' for r in rows) == 5
    save(OUT, {'format': 'dk4-native-common-editorial-v1', 'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
        'encoder': 'dialogue-relocatable-v1', 'consumer_layout_profile': 'sea-inspection-role7-postmacro-v1',
        'file_path': '/COMMON/MESFILE.DK4', 'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'formatting_review_pending': True, 'status': 'eight-source-context-prose-reviewed;native-font-wrap-release-original-inspection-pending',
        'source_clean_ROM_sha256': context['clean_ROM_sha256'], 'current_ROM': context['candidate'],
        'current_ROM_sha256': context['candidate_sha256'], 'current_COMMON_sha256': context['COMMON_sha256'],
        'current_ARM9_sha256': context['ARM9_sha256'], 'source_context': str(CONTEXT), 'source_context_sha256': sha(CONTEXT.read_bytes()),
        'no_authored_line_breaks_or_alignment': True, 'no_runtime_substitution_species_or_source_macro_added': True,
        'records': rows, 'revised': 5, 'retained': 3, 'no_native_formatting_release_or_original_gameplay_completion_approval': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Sea inspection8 source/prose:5 revisions3 justified retentions. Unsupported war removed;native/release/original inspection gates remain pending.')
