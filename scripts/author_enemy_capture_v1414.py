"""Source-first editorial review of eight individual enemy ship capture reports."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/enemy_capture_editorial_manuscript_v1.json')
CONTEXT = Path('work/analysis/enemy_capture_context_v1413/source_and_original_capture_context.json')
REVIEWS = {
    2082:('Enemy ship %s captured!',
        'A polite emphatic report that the named enemy vessel has been captured.',
        'Retain the idiomatic brief naval report. The named vessel and enemy affiliation remain explicit;capture does not mean sinking or the death of its crew.'),
    2083:('Enemy ship %s captured!',
        'A clipped report announcing capture of the named enemy vessel.',
        'Restore enemy,which the older English omitted. Retain the source voice\'s clipped reporting style rather than imposing a complete conversational sentence.'),
    2084:('Enemy ship %s captured!',
        'A cheerful conversational announcement that the named enemy vessel has been captured.',
        'Retain the fluent short report and exclamation. The conversational Japanese ending does not require adding an unspoken boast or extra action.'),
    2085:('Enemy ship %s captured!',
        'A conversational emphatic announcement that the named enemy vessel has been captured,with a feminine sentence ending.',
        'Retain natural English naval reporting. No artificial gendered catchphrase is needed to express the feminine Japanese ending.'),
    2086:('We took the enemy ship %s!',
        'A rough confident speaker exclaims that we seized the named enemy vessel.',
        'Use an idiomatic complete spoken clause for the forceful ubatta ze. We took conveys seizure without adding sinking,casualties,rewards or an admiral address absent from the Japanese.'),
    2087:('Enemy ship %s captured!',
        'An older speaker emphatically reports capture of the named enemy vessel.',
        'Retain the natural naval announcement. The older Japanese ending does not justify inventing an archaic or pirate accent.'),
    2088:('We took over the enemy ship %s!',
        'A youthful informal speaker announces that we took control of the named enemy vessel.',
        'Restore the omitted enemy affiliation and express nottotta as took over. This is the named vessel only,not a report that the entire opposing fleet has been captured.'),
    2089:('Enemy ship %s captured!',
        'A polite emphatic announcement that the named enemy vessel has been captured.',
        'Retain the idiomatic concise report. The emphatic zo reinforces the announcement without requiring an invented fact or forced English speech tic.')
}

if __name__=='__main__':
    assert not OUT.exists()
    context = read(CONTEXT)
    assert context['raw8_voice_table']==list(REVIEWS)
    assert len(context['all206_existing_actor_choices'])==206
    assert sha(Path(context['candidate']).read_bytes())==context['candidate_sha256']
    assert sha(Path('scripts/research_enemy_capture_v1413.py').read_bytes())==context['producer_sha256']
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    records = []
    for source in context['records_and_immediate_neighbors']:
        if not source['selected_for_review']:
            continue
        row = deepcopy(source)
        n = row['message_id']
        english,meaning,note = REVIEWS[n]
        assert english.isascii() and english==' '.join(english.split())
        assert english.count('%s')==1 and '%' not in english.replace('%s','')
        assert not any(c in english for c in '{}\n\r\t')
        row.update(id=f'COMMON_MESSAGE_{n}',source_family='individual_enemy_ship_capture',
            speaker='Existing attacker-side officer selected by original55DC4(attacker,8),then direct53F0C voice selection',
            context=context['original_context'],consumer='original-direct-portrait-speech-after-selection-printf-and-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(),native_argument_count=1,source_native_macros=[],
            original_native_entry=context['original_entry'],original_native_parent=context['original_parent'],
            source_table=context['source_table'],source_voice=n-2082,selector_stack_offset=context['selector_stack_offset'],
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-formatting-release-and-gameplay-pending')
        records.append(row)
    assert [r['message_id'] for r in records]==list(range(2082,2090))
    assert [r['message_id'] for r in records if r['editorial_decision']=='revise']==[2083,2086,2088]
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'enemy-capture-direct-portrait-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'8-source-context-prose-reviewed;native-release-gameplay-pending',
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':context['candidate'],
        'current_ROM_sha256':context['candidate_sha256'],'current_COMMON_sha256':context['COMMON_sha256'],
        'current_ARM9_sha256':context['ARM9_sha256'],'source_context':str(CONTEXT),
        'source_context_sha256':sha(CONTEXT.read_bytes()),'source_arguments_and_all8_voice_selections_preserved':True,
        'one_original_target_ship_name_printf_argument':True,'no_authored_line_breaks_or_alignment':True,
        'records':records,'revised':3,'retained':5,'no_native_formatting_release_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight capture reports reviewed:3 proposed revisions,5 justified retentions;native/release/gameplay gates open.',flush=True)
