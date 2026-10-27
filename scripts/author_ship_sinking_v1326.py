"""Review sixteen sinking notices from clean Japanese; native gates stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/ship_sinking_editorial_manuscript_v1.json')
CONTEXT = Path('work/analysis/ship_sinking_context_v1325/source_and_consumer_binding.json')
REVIEWS = {
    2058:('Admiral, %s has sunk!','A polite urgent report to the admiral that the named ship has sunk.',
          'Retain the natural complete report;the perfect tense preserves the completed sinking without adding casualties.'),
    2059:('Admiral, %s is sinking...','A restrained report to the admiral that the named ship is going under,with a trailing pause.',
          'Retain the progressive and ellipsis;the source describes sinking in progress rather than replacing it with a completed result.'),
    2060:('Admiral, %s has sunk!','A youthful emphatic report to the admiral that the named ship has gone down.',
          'Retain the idiomatic alarm;the exclamation carries urgency without invented slang or childish dialect.'),
    2061:('Admiral, %s was sunk!','An emphatic report to the admiral that the named ship was sunk by enemy action.',
          'Retain the natural passive and exclamation;do not invent who fired the fatal shot or any death count.'),
    2062:('Admiral, %s was sunk!','A blunt urgent report to the admiral that the named ship was sunk.',
          'Retain the concise complete spoken report,including the passive meaning of gekichin sareta.'),
    2063:('Admiral, %s was sunk!','An older speaker reports emphatically to the admiral that the named ship was sunk.',
          'Retain natural English rather than inventing an archaic or comic accent for the Japanese ending.'),
    2064:('Admiral, %s sank!','A youthful distressed cry to the admiral that the named ship sank.',
          'Retain the short natural cry;the exclamation conveys the stretched Japanese alarm without decorative English letters.'),
    2065:('Admiral, %s has sunk!','A formal emphatic report to the admiral that the named ship has sunk.',
          'Retain the complete report and title;do not add a promise,crew fate or a ship class.'),
    2066:("We've sunk the enemy ship %s!",'A polite report that the named enemy ship has been sunk by our attack.',
          'Use a complete spoken report instead of a compressed status-label fragment;the source explicitly identifies the named enemy vessel.'),
    2067:('Enemy ship %s sunk!','A clipped urgent announcement that the named enemy ship has been sunk.',
          'Retain the conventional terse naval report because the Japanese is itself clipped;sentence fragments can be intentional dialogue.'),
    2068:("Admiral! We've sunk enemy ship %s!",'An excited youthful report to the admiral that we sank the named enemy ship.',
          'Retain the natural excited address and complete follow-up;enemy ship plus its name is idiomatic identification in this report.'),
    2069:("We've sunk the enemy ship %s!",'An emphatic spoken report that we sank the named enemy ship.',
          'Retain the natural complete sentence;do not manufacture gendered English from the Japanese ending.'),
    2070:("We did it! We've sunk the enemy ship %s!",'A rough triumphant cry followed by the announcement that the named enemy ship was sunk.',
          'Preserve both the celebration and specific sinking with natural spoken clauses;no extra victory over the fleet is claimed.'),
    2071:("We've sunk the enemy ship %s!",'An older speaker emphatically reports sinking the named enemy ship.',
          'Retain the idiomatic sentence and emphasis without a manufactured old-fashioned accent.'),
    2072:("We sank the enemy ship %s!",'A youthful emphatic report that we sank the named enemy ship.',
          'Use a natural complete spoken alarm rather than flattening the youthful report into a status label.'),
    2073:('We have sunk the enemy ship %s!','A formal emphatic report that we have sunk the named enemy ship.',
          'Use the complete uncontracted report for the formal voice;preserve the enemy ship name and avoid adding casualties or battle victory.')
}


def main():
    assert not OUT.exists()
    context = read(CONTEXT)
    assert len(context['voice_tables'])==2
    rom_path = Path(context['candidate'])
    assert sha(rom_path.read_bytes())==context['candidate_sha256']
    rom = NdsImage.open(rom_path)
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records = []
    for source in context['records']:
        row = deepcopy(source)
        number = row['message_id']
        english,meaning,note = REVIEWS[number]
        assert english.isascii() and english==' '.join(english.split()) and english.count('%s')==1
        assert english.replace('%s','').find('%')==-1 and not any(c in english for c in '{}\n\r\t')
        own = number<2066
        table = context['voice_tables'][0 if own else 1]
        row.update(id=f'COMMON_MESSAGE_{number}',source_family='fleet_ship_sinking_report' if own else 'enemy_ship_sinking_report',
            speaker='Original role1 First Mate through53D44' if own else 'Original firing-ship gun-position actor through55DC4 and53F0C',
            context=context['own_loss_context'] if own else context['enemy_loss_context'],
            consumer='original-portrait-speech-after-native-selection-and-printf-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[number].text.hex(),native_argument_count=1,
            native_argument_kind='original_virtual_ship_name_C_string',source_native_macros=[],
            original_native_entry=table['original_native_entry'],original_native_parent=table['original_native_parent'],
            source_table=table['table'],selector_stack_offset=table['selector_stack_offset'],
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-name-expansion-formatting-release-and-gameplay-pending')
        records.append(row)
    assert [r['message_id'] for r in records]==list(range(2058,2074))
    assert sum(r['editorial_decision']=='revise' for r in records)==4
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'ship-sinking-portrait-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'16-source-context-prose-reviewed;native-release-gameplay-pending',
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':str(rom_path),
        'current_ROM_sha256':sha(rom_path.read_bytes()),'current_COMMON_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'current_ARM9_sha256':sha(rom.read_file('/__arm9__.bin')),
        'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'source_arguments_and_all8_voice_selections_preserved':True,'no_authored_line_breaks_or_alignment':True,
        'records':records,'revised':4,'retained':12,
        'no_native_formatting_release_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Sixteen sinking notices source/context/prose reviewed:four revisions,twelve justified retentions. Native formatting and gameplay remain open.',flush=True)


if __name__=='__main__':
    main()
