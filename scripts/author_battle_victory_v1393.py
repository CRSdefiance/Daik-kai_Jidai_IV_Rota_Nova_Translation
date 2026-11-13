"""Review eight victory reports from clean Japanese;native gates remain open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/battle_victory_editorial_manuscript_v1.json')
CONTEXT = Path('work/analysis/battle_victory_context_v1392b/source_and_original_victory_context.json')
REVIEWS = {
    2130:('Admiral, we won!','A polite emphatic report to the admiral that our side has won.',
        'Retain the fluent direct report. The title and exclamation carry the address and announcement without adding casualties or total destruction.'),
    2131:('Admiral, victory is ours!','A formal emphatic report to the admiral that victory belongs to our side.',
        'Retain the natural naval announcement and slightly formal voice. Original Gerhard gameplay confirms the result-report context after a flagship capture.'),
    2132:("Admiral, we've won!",'An energetic youthful report to the admiral that we,as a group,have won.',
        'Retain natural collective we. Source IC is a genuine first-person pronoun command and tachi makes it plural;it is not a name. As with the earlier IC-ra/our ship localization1561,English grammatical we expresses that meaning without a singular I or a fabricated personal name.'),
    2133:('Admiral, we won!','A warm emphatic report to the admiral that we have won,with a conversational feminine ending.',
        'Retain natural spoken English and the delighted exclamation. Do not invent a gendered English speech tic from the Japanese ending.'),
    2134:('Admiral, we won!','A blunt confident report to the admiral that our group has won.',
        'Retain the short energetic announcement. Japanese ore-tachi gives a rough masculine first person;English we preserves the group without unnecessary slang.'),
    2135:('Admiral, we won!','An older speaker emphatically announces our victory to the admiral.',
        'Retain the complete natural spoken report. The older Japanese ending does not justify a manufactured archaic or pirate accent.'),
    2136:('We won! We did it, Admiral!','A jubilant youthful cheer that we won,followed by another emphatic announcement to the admiral that our group is victorious.',
        'Use two excited natural English clauses for the stretched winning cheer and repeated victory announcement. We did it restates the same victory in context;it does not invent a separate feat,reward or destruction of every enemy ship.'),
    2137:('Admiral, we have won!','A formal emphatic announcement to the admiral that our side has won.',
        'Use the natural uncontracted report for the formal emphatic voice. Replace the stiff victory belongs to us phrasing without adding a promise,enemy casualties or a different outcome.')
}


if __name__=='__main__':
    assert not OUT.exists()
    context = read(CONTEXT)
    assert context['raw8_voice_table']==list(REVIEWS)
    assert len(context['all206_existing_actor_choices'])==206
    rom = NdsImage.open(context['candidate'])
    assert sha(Path(context['candidate']).read_bytes())==context['candidate_sha256']
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records = []
    for source in context['records_and_immediate_neighbors']:
        if not source['selected_for_review']:
            continue
        row = deepcopy(source)
        number = row['message_id']
        english,meaning,note = REVIEWS[number]
        assert english.isascii() and english==' '.join(english.split())
        assert not any(c in english for c in '{}\n\r\t%')
        row.update(id=f'COMMON_MESSAGE_{number}',source_family='battle_victory_report',
            speaker='Original role1 First Mate through53D44 and automatic82478 logical member selection',
            context=context['original_context'],consumer='original-portrait-speech-after-native-selection-and-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[number].text.hex(),native_argument_count=0,
            source_native_macros=['IC first-person plus plural tachi localized grammatically as we'] if number==2132 else [],
            original_native_entry=context['original_entry'],original_native_parent=context['original_parent'],
            source_table=context['source_table'],source_voice=number-2130,selector_stack_offset=context['selector_stack_offset'],
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-formatting-release-and-gameplay-pending')
        records.append(row)
    assert [r['message_id'] for r in records]==list(range(2130,2138))
    assert sum(r['editorial_decision']=='revise' for r in records)==2
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'battle-victory-portrait-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'8-source-context-prose-reviewed;native-release-gameplay-pending',
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':context['candidate'],
        'current_ROM_sha256':context['candidate_sha256'],'current_COMMON_sha256':context['COMMON_sha256'],
        'current_ARM9_sha256':context['ARM9_sha256'],'source_context':str(CONTEXT),
        'source_context_sha256':sha(CONTEXT.read_bytes()),'source_arguments_and_all8_voice_selections_preserved':True,
        'source2132_collective_pronoun_explicitly_reviewed':True,'no_authored_line_breaks_or_alignment':True,
        'records':records,'revised':2,'retained':6,'no_native_formatting_release_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight victory paragraphs source/prose reviewed:two proposed revisions,six justified retentions;native/release/gameplay gates open.',flush=True)
