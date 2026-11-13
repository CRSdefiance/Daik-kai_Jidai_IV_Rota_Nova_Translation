"""Source-first natural English for24 own-loss and surrender alternatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

OUT = Path('translations/ship_loss_surrender_editorial_manuscript_v1.json')
CONTEXT = Path('work/analysis/ship_loss_surrender_context_v1439/source_and_original_loss_surrender_context.json')
REVIEW = {
    2074:('Admiral, %s has been captured!','A polite urgent report to the admiral that the named ship has been captured.',
        'Use the natural present-perfect passive for fresh bad news. Preserve the named ship and capture;do not say it sank or that its crew died.'),
    2075:('Admiral, %s has fallen into enemy hands!','A formal report to the admiral that the named ship has fallen into the enemy\'s hands.',
        'Render the source idiom directly in idiomatic English. Replace the grammatically incomplete enemy took wording without adding a specific captor or casualties.'),
    2076:('Admiral, they captured %s!','A conversational emphatic report to the admiral that the named ship was captured.',
        'Use a natural direct spoken clause for the conversational yo ending. They refers to the opposing side;the source reports capture,not destruction.'),
    2077:('Admiral, %s has been captured!','A conversational report to the admiral that the named ship has been captured,with a feminine ending.',
        'Use normal spoken English and fresh-news present perfect. Do not invent a gendered catchphrase from wa.'),
    2078:("Admiral, they've taken over %s!",'A rough regretful speaker reports to the admiral that the named ship has been taken over.',
        'Taken over preserves the specific nottorare sense and the contraction suits the informal voice. Keep the unwanted loss without inventing a mutiny,traitor or dead crew.'),
    2079:('Admiral, %s has been captured!','An older speaker emphatically reports the named ship\'s capture to the admiral.',
        'Use a complete natural report. The older zoi ending does not warrant a fabricated archaic or pirate accent.'),
    2080:('Oh no! They captured %s, Admiral!','A youthful dismayed exclamation to the admiral that the named ship has been caught or captured.',
        'Oh no expresses the regretful chatta and stretched ending naturally;moving the address to the end preserves whom the speaker addresses. Do not invent a total defeat or casualties.'),
    2081:('Admiral, %s has been captured!','A polite emphatic report to the admiral that the named ship has been captured.',
        'Use a complete uncontracted fresh-news report for the formal emphatic voice. Preserve the named vessel rather than claiming capture of the whole fleet.'),
    2090:('Admiral, %s has surrendered!','A polite emphatic report to the admiral that the named ship has surrendered.',
        'Use present perfect for a newly reported surrender. Preserve the voluntary capitulation distinction from being sunk or forcibly captured.'),
    2091:('Admiral, it looks like %s has surrendered!','A polite report to the admiral that the named ship appears to have surrendered.',
        'Restore the explicit source uncertainty in you desu. The old English stated surrender as an unqualified fact.'),
    2092:('Admiral, %s has surrendered!','A conversational emphatic report to the admiral that the named ship has surrendered.',
        'Use a fluent complete spoken report for yo without adding an invented explanation or promise.'),
    2093:("Admiral, I'm afraid %s has surrendered!",'A feminine conversational report expressing regret that the named ship has surrendered.',
        'The conventional bad-news phrase I\'m afraid carries the unwanted-event nuance of chatta;it does not assert a new danger or kinship. Keep the surrender itself definite in this source voice.'),
    2094:('Admiral, %s has surrendered!','A rough conversational report of the unwelcome surrender of the named ship.',
        'Keep the direct urgent exclamation. The informal shimatta construction need not become an invented curse or an accusation of treachery.'),
    2095:("Admiral, I'm afraid %s has surrendered!",'An older speaker regretfully reports that the named ship has surrendered.',
        'Use a natural conventional bad-news phrase for shiteshimatta and keep the admiral address. Avoid a manufactured old-fashioned accent.'),
    2096:('Admiral, %s has surrendered!','A youthful conversational report of the unwanted surrender of the named ship.',
        'Use an immediate natural report and exclamation. The surrounding loss context carries the regret without inventing blame or crew deaths.'),
    2097:('Admiral, %s has surrendered!','A polite emphatic announcement to the admiral that the named ship has surrendered.',
        'Preserve the formal direct address and complete report;do not replace surrender with destruction or enemy capture.'),
    2098:('Admiral, the enemy ship %s has surrendered!','A polite report to the admiral that the named enemy ship has surrendered to our side.',
        'Restore the omitted admiral address and use a complete natural spoken clause. The named vessel alone has surrendered.'),
    2099:("Admiral, the enemy ship %s has raised a white flag! It looks like they're surrendering!",'A polite report to the admiral that the named enemy vessel has raised a white flag,followed by the inference that it appears to be surrendering.',
        'Preserve both the observed white flag and the separate apparent-surrender inference. Author natural ASCII It as part of one paragraph;the mapped literal-name/postmacro formatter owns safe display rather than a full-width letter or copied Japanese breaks.'),
    2100:('Admiral, the enemy ship %s has surrendered!','A conversational report to the admiral that the named enemy ship has surrendered.',
        'Retain the fluent complete current sentence. It already preserves the admiral,enemy vessel,name and completed surrender without adding facts.'),
    2101:('Admiral, the enemy ship %s has surrendered!','A conversational feminine report to the admiral that the named enemy vessel has surrendered.',
        'Restore the missing admiral address and use a natural complete report. No artificial feminine speech tic is required.'),
    2102:('Admiral, the enemy ship %s has surrendered!','A rough emphatic report to the admiral that the named enemy ship has surrendered.',
        'Restore the source address and retain the confident exclamation without inventing a boast or total enemy defeat.'),
    2103:('Admiral, it looks like the enemy ship %s has surrendered!','An older speaker tells the admiral that the named enemy vessel appears to have surrendered.',
        'Restore both the omitted admiral address and the explicit appearance qualifier in you jana. Do not turn an inference into certainty or invent an archaic voice.'),
    2104:("Admiral, the enemy ship %s says they're surrendering!",'A youthful informal speaker relays to the admiral the named enemy vessel\'s stated intention to surrender.',
        'Restore the admiral address and preserve the reportative tte sa as says. They refers naturally to the people aboard the named ship;do not make this the speaker\'s prediction that surrender will happen.'),
    2105:('Admiral, the enemy ship %s appears to have surrendered!','A formal emphatic report to the admiral that the named enemy ship appears to have surrendered.',
        'Restore the omitted address and the source you desu uncertainty. The formal appears to have suits this voice without adding casualties or surrender of every enemy vessel.')
}

if __name__=='__main__':
    assert not OUT.exists()
    context = read(CONTEXT)
    assert context['all24_native_IDs']==list(REVIEW)
    assert sha(Path(context['candidate']).read_bytes())==context['candidate_sha256']
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    families = {n:f for f in context['families'] for n in f['native_IDs']}
    records = []
    for source in context['records_and_immediate_neighbors']:
        if not source['selected_for_review']:
            continue
        row = deepcopy(source);n = row['message_id'];family = families[n]
        english,meaning,note = REVIEW[n]
        assert english.isascii() and english==' '.join(english.split()) and english.count('%s')==1
        assert '%' not in english.replace('%s','') and not any(c in english for c in '{}\n\r\t')
        row.update(id=f'COMMON_MESSAGE_{n}',source_family=family['family'],
            speaker='Original role1 First Mate through53D44 and82478 logical member selection',
            context=context['original_context'],consumer='original-role1-portrait-speech-after-selection-printf-and-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(),native_argument_count=1,source_native_macros=[],
            original_native_entry=family['original_entry'],original_native_parent=family['original_parent'],
            source_table=family['source_table'],source_voice=n-family['first_ID'],selector_stack_offset=family['selector_stack_offset'],
            original_role=1,authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-formatting-release-and-gameplay-pending')
        records.append(row)
    assert [r['message_id'] for r in records]==list(REVIEW)
    revised = sum(r['editorial_decision']=='revise' for r in records)
    assert revised==23 and [r['message_id'] for r in records if r['editorial_decision']=='retain']==[2100]
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'ship-loss-surrender-role1-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'24-source-context-prose-reviewed;native-release-gameplay-pending',
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':context['candidate'],
        'current_ROM_sha256':context['candidate_sha256'],'current_COMMON_sha256':context['COMMON_sha256'],
        'current_ARM9_sha256':context['ARM9_sha256'],'source_context':str(CONTEXT),
        'source_context_sha256':sha(CONTEXT.read_bytes()),'source_arguments_and_all24_voice_selections_preserved':True,
        'exact_one_original_affected_ship_name_printf_argument':True,'no_authored_line_breaks_or_alignment':True,
        'records':records,'revised':23,'retained':1,'no_native_formatting_release_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('24 loss/surrender reports source/prose reviewed:23 proposed revisions,one justified retention;native/release/gameplay pending.',flush=True)
