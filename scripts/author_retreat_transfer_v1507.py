"""Faithful natural English for seven original replacement-ship retreat notices."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

CONTEXT=Path('work/analysis/retreat_transfer_context_v1506/source_and_original_transfer_context.json')
OUT=Path('translations/retreat_transfer_editorial_manuscript_v1.json')
REVIEW={
2683:("Our flagship's out of action! We're retreating to %s!",'A polite report that the flagship has been incapacitated and the speakers are withdrawing to the named replacement ship.','Retain the fluent complete current report. Retreating to names the other vessel in this source-proven transfer context;it does not claim a town destination or that the flagship sank.'),
2684:("Our flagship's out of action! Get aboard %s!",'An urgent report that the flagship has been incapacitated,followed by an order to take refuge on the named replacement ship.','Use get aboard to make the imperative explicitly refer to the surviving ship. Preserve the loss of flagship capability and single literal ship name;do not add a death,sinking or port.'),
2685:("Our flagship's out of action! Fall back to %s!",'An excited conversational report that the flagship is out of action and an urgent retreat to the named replacement ship.','Retain the natural current words and normalize its full-width Latin F. The native source macro and name-guard contract must be repaired before ordinary ASCII is approved.'),
2686:("Our flagship's out of action! We're falling back to %s!",'An assertive report that the flagship is incapacitated and the speakers are withdrawing to the named replacement ship.','Retain the natural military phrasing and collective action;do not invent an attacker,a town or total fleet destruction.'),
2687:("Our flagship's out of action! Get aboard %s!",'An older-sounding urgent declaration that the flagship is out of action and an order to withdraw onto the named replacement ship.','Use a clear urgent English transfer order without artificial archaic grammar. The short command can naturally match2684 despite Japanese register differences.'),
2688:("Our flagship's out of action! We're retreating to %s!",'An alarmed informal cry about the flagship being put out of action,followed by withdrawing to the named replacement ship.','Retain the fluent alarmed report. Exclamations convey the drawn-out Japanese reaction without inventing a speech tic or outcome.'),
2689:("Our flagship's out of action! Let's retreat to %s!",'A measured older formal report that the flagship is incapacitated and a suggestion to withdraw to the named replacement ship.','Retain the natural let us suggestion matching shimashou. The ship transfer is proven by the original virtual ship-name getter and observed fleet-slot swap.')}

if __name__=='__main__':
    assert not OUT.exists()
    context=read(CONTEXT);canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    rows=[]
    for original in context['records_and_immediate_neighbors']:
        if not original['selected_for_review']:continue
        row=deepcopy(original);n=row['message_id'];english,meaning,note=REVIEW[n]
        assert english.isascii() and english==' '.join(english.split()) and english.count('%s')==1
        assert '%' not in english.replace('%s','') and not any(c in english for c in '{}\n\r\t')
        row.update(id=f'COMMON_MESSAGE_{n}',source_family='flagship_replacement_ship_retreat',
            speaker='Original logical First Mate role1 through53D44/82478',context=context['original_context'],
            consumer='original-role1-portrait-speech-after-selection-printf-and-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(),native_argument_count=1,source_native_macros=[],
            original_native_entry=context['original_entry'],original_native_parent=context['original_parent'],
            selector_stack_offset=context['selector_stack_offset'],original_role=1,source_table=context['source_table'],
            source_voice_classes=[i for i,value in enumerate(context['source_signed_voice_members']) if value==n or value<0 and n==2683],
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-name-guard-format-release-and-current-gameplay-pending')
        rows.append(row)
    assert [r['message_id'] for r in rows]==list(range(2683,2690))
    assert sum(r['editorial_decision']=='revise' for r in rows)==3
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'flagship-transfer-role1-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'seven-source-context-prose-reviewed;native-name-repair-release-gameplay-pending',
        'source_clean_ROM_sha256':context['clean_ROM_sha256'],'current_ROM':context['candidate'],
        'current_ROM_sha256':context['candidate_sha256'],'current_COMMON_sha256':context['COMMON_sha256'],
        'current_ARM9_sha256':context['ARM9_sha256'],'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'source_replacement_ship_name_argument_and_voice3_fallback_preserved':True,
        'no_authored_line_breaks_or_alignment':True,'records':rows,'revised':3,'retained':4,
        'no_native_formatting_release_or_revised_gameplay_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Retreat7 source/prose:3 proposed revisions4 retentions. Original transfer context mapped;literal-name repair/native/release/revised-scene gates remain open.')
