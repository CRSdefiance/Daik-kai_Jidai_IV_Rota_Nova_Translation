"""Thirteen faithful natural hot-spring lines; native/scene gates stay pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

CONTEXT=Path('work/analysis/hot_spring_source_v1610/original_hot_spring13_source_context.json')
OUT=Path('translations/hot_spring_editorial_manuscript_v1.json')
REVIEW={
    2275:("It looks like the expedition has found a hot spring!",
        'A polite report says the expedition seems to have discovered a hot spring.',
        'The existing sentence is natural and faithful. Replace only the mixed-font full-width leading I in the new paragraph;native literal-I and post-expansion formatting must pass before integration.'),
    2276:("Admiral, it appears the expedition has found a hot spring!",
        'A formal report addresses the admiral and says the expedition appears to have found a hot spring.',
        'Keep the formal it appears and explicit admiral address. Present perfect naturally reports the fresh discovery without claiming direct observation or a guaranteed recovery outcome.'),
    2277:("Admiral! I hear the expedition found a hot spring!",
        'An excited informal speaker tells the admiral they heard the expedition found a hot spring.',
        'Restore the reported-information nuance of ndatte and the expedition subject in a fluent excited report. Do not turn hearsay into a personally witnessed event.'),
    2278:("I hear the expedition found a hot spring!",
        'An animated polite feminine voice reports hearing that the expedition found a hot spring.',
        'Use a natural English report for ndasutte without adding an admiral address absent from this alternative. Native literal-I safety and full first letter remain explicit formatting gates.'),
    2279:("Whoa! Sounds like the expedition found a hot spring!",
        'A rough informal speaker reacts enthusiastically and says it sounds like the expedition found a hot spring.',
        'Whoa and the conversational Sounds like preserve the excited informal reaction and rashii uncertainty. Avoid invented profanity or a direct witness claim.'),
    2280:("The expedition found a hot spring!",
        'An emphatic older voice announces that the expedition found a hot spring.',
        'Keep the direct confident announcement and restore its explicit expedition subject. Do not add hearsay or an admiral address to this alternative.'),
    2281:("They say the expedition found a hot spring!",
        'An excited youthful speaker repeats a report that the expedition found a hot spring.',
        'Move the awkward trailing they say to a natural opening while preserving the source reported speech. Do not invent an age,rank or relationship for the speaker.'),
    2282:("Admiral, this feels wonderful. Hot springs soothe weary travelers.",
        'A polite speaker tells the admiral that the bath feels good and hot springs help with travel fatigue.',
        'Retain this fluent two-sentence localization. Soothe weary travelers faithfully expresses relief from travel fatigue without inventing a numeric outcome or saying every fatigue point is gone.'),
    2283:("Admiral, hot springs do wonders for travel fatigue.",
        'A formal speaker addresses the admiral and observes that hot springs are effective for travel fatigue.',
        'Replace the overly clinical cure with the natural do wonders for. Preserve the admiral address and the journey-related fatigue without claiming a complete mechanical reset.'),
    2284:("Hot springs feel so good! I feel completely refreshed!",
        'An informal speaker enjoys the bath and exclaims that the weariness of the journey has flown away.',
        'Restore the omitted enjoyment and express the exaggerated relief as a personal feeling. This is character speech,not a guarantee that the underlying fatigue stat is zero.'),
    2285:("Admiral, hot springs feel wonderful, don't they? I feel like all the travel fatigue just melts away.",
        'A feminine speaker seeks the admiral agreement that hot springs feel good and says it feels as if the journey fatigue disappears.',
        'Preserve the explicit ki ga suru qualification with I feel like and the conversational agreement-seeking tone. Remove the old unconditional All fatigue is gone claim;do not omit the feeling to fit a line.'),
    2286:("Ahh... Admiral, this feels good. Nothing beats a hot spring when you're worn out from traveling.",
        'An older speaker sighs with pleasure,addresses the admiral and says hot springs are best for travel weariness.',
        'Keep the relaxed sigh and admiral address omitted in the old draft. Nothing beats conveys saikou naturally without a clinical cure claim or an invented event outcome.'),
    2287:("Hot springs don't taste very good, but they sure feel nice!",
        'A playful speaker says hot springs do not taste good but feel pleasant.',
        'Make the joke understandable as one natural spoken sentence. Preserve the odd taste-versus-bathing contrast;do not invent poisoning,a drinking accident or a new gameplay effect.'),
}

if __name__=='__main__':
    assert not OUT.exists()
    context=read(CONTEXT);canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    rows=[]
    for original in context['records_and_neighbors']:
        if not original['selected_hot_spring_dialogue']:continue
        row=deepcopy(original);n=row['message_id'];english,meaning,note=REVIEW[n]
        assert english.isascii() and english==' '.join(english.split()) and not any(c in english for c in '%{}\n\r\t')
        assert b'%' not in bytes.fromhex(row['source_hex'])
        table=next(t for t in context['voice_tables'] if n in t['signed_members'])
        voices=[i for i,v in enumerate(table['signed_members']) if v==n or (v<0 and table['signed_members'][0]==n)]
        row.update(id=f'COMMON_MESSAGE_{n}',source_family='expedition-hot-spring-discovery-and-relaxation13',
            speaker='Original logical role1 through82478/53D44;source voices '+','.join(map(str,voices)),
            context=context['source_context'],consumer='original-role1-speech-after-selection-printf-and-macro-expansion',
            english=english,source_meaning=meaning,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(),native_argument_count=0,source_native_macros=[],
            original_native_entry=0x02053D44,original_native_parent=0x02053DB8,selector_stack_offset=0x27C,
            source_table=table['table'],original_role=1,source_voice_classes=voices,
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-font-wrap-release-and-original-hot-spring-pending')
        rows.append(row)
    assert [r['message_id'] for r in rows]==list(range(2275,2288))
    assert sum(r['editorial_decision']=='revise' for r in rows)==12
    doc={'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'expedition-hot-spring-role1-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'source_clean_ROM_sha256':context['clean_ROM_sha256'],
        'current_ROM':context['candidate'],'current_ROM_sha256':context['candidate_sha256'],
        'current_COMMON_sha256':context['COMMON_sha256'],'current_ARM9_sha256':context['ARM9_sha256'],
        'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'records':rows,'revised':12,'retained':1,'no_authored_line_breaks_or_alignment':True,
        'no_runtime_substitution_relationship_or_source_macro_added':True,
        'no_native_formatting_release_or_original_gameplay_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    validate_natural_dialogue_batch(doc);save(OUT,doc)
    print('Hot-spring13 source/prose draft:12 revisions,1 justified retention. Full leading I,hearsay/feeling,voice and joke reviewed;native/release/actual gates pending.')
