"""Compare the complete older English only after clean glosses and actual source staging."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_contextual_findings_v6185')
SOURCE=Path('work/analysis/lil_B205_source_v6172/all17_clean_current_complete_context.json')
CONTROL=Path('work/analysis/lil_B205_dispatches_v6176/all17_source_current_dispatches_seven_FE_sounds_echoes_no_macros_and8_control_leaves.json')
VIEW=Path('work/analysis/lil_B205_source_view_v6184/complete_source_scenes_and_return_visual_review.json')
RETAIN={
5:'The lowercase sound caption flap, flap! naturally conveys the two opening wing beats. Its sound function is clear in the following startled reaction;no named narrator,extra call or invented action is needed.',
9:"Whoa! What's that?! naturally conveys Angelo's startled response to the unfamiliar creature. That is an ordinary spontaneous English reference,not a new location fact. The following bird echo repeats the question's exact words without Whoa;retain it.",
13:"WHAT'S THAT copies the complete question wording from Angelo without the initial startled interjection. The source echo has no punctuation;the flat all-capital repeat is a readable bird imitation. Retain the words and actorless presentation.",
17:'Mamma mia! You can talk?! naturally reacts to the bird having just spoken. You can talk expresses the startling human-speech ability revealed by that action;no separate fact about a specific language is needed. Mamma mia is explicit in the source,not an invented accent or nationality. Retain the direct address and surprised question.',
20:'YOU CAN TALK repeats exactly the words in Angelo\'s preceding reaction,excluding Mamma mia. The all-capital unpunctuated echo follows the Japanese katakana mimicry. It is not an independent narrator conclusion or another human speaker.',
24:'A parrot! is a natural exclamatory identification by Lil after Angelo asks what it is. The English fragment answers the question completely in context;there is no need to add a particular species,pet bond or item name.',
28:'A parrot, eh? naturally conveys Angelo taking in Lil\'s identification with curiosity. The following echo copies those words,so retain this recognizably spoken reaction without adding a new regional accent or a parrot lesson.',
32:'A PARROT, EH echoes the full preceding recognition phrase. Keep the same words and flat all-capital presentation,with no human nameplate. There is no new independent identification or speaker to invent.',
47:'Here goes! Hah! is an energetic natural announcement and effort cry as Angelo starts the catching attempt. The following scuffle caption supplies the action;this line does not need a new instruction to Lil or a claim of success.',
}
REVISE={
36:'Stop that! is understandable but unnecessarily vague beside explicit 真似するな. Restore the objection to being copied as a natural imperative;the bird must repeat the same localized objection next.',
40:'The echo must follow the revised explicit copying objection from36 with identical localized words. Keep it actorless and do not turn it into a different warning or an insult.',
44:'Oh, fun! Gonna catch you! sounds compressed and changes the amused observation into clipped fragments. Convey the shift to enthusiasm and prospective catch naturally in complete spoken clauses,without adding a trap,weapon,pet bond or completed capture.',
51:'The old compressed sound caption drops repeated wing beats and changes their order. Preserve two opening flaps,then a bang and crack,another flap,a thud and rustling. The sounds do not prove a gunshot,broken bone,injury,cage or ship damage.',
55:'Got you! omits やっと,which pays off the preceding extended scuffle. Restore finally and the capture announcement. Japanese omits the capturing agent and target;do not state that Lil captured Angelo or invent a joint capture mechanism.',
59:'Surrender now? changes the triumphant already-defeated taunt into a request for future surrender. Preserve the sigh,the Well?/Had enough? boast and laugh;the following bird echo repeats the taunt alone.',
63:'Replace SURRENDER NOW? with the same localized victory-taunt words as59,excluding the sigh and laugh. This exact echo is the setup for Lil\'s final joke,not a new offer to surrender.',
67:'He\'s caught risks attributing capture to Angelo or assigning the bird an unsupported sex. The immediate preceding voice is the mimicking bird;Lil laughs that the captured bird sounds as if it will not admit defeat. Restore the initial suppressed laugh/full laughter and sounds-like qualification naturally,with a clear bird referent. Remove the authored early line break and leading continuation space;do not force the old rows.',
}
if __name__=='__main__':
    assert not ROOT.exists();packet,control,view=map(read,[SOURCE,CONTROL,VIEW]);assert view['all17_Japanese_objects_five_FE_echoes_and_two_sound_captions_viewed']
    assert set(RETAIN).isdisjoint(REVISE) and set(RETAIN)|set(REVISE)=={r['source_record_index'] for r in packet['records']}
    dispatch={r['id']:r for r in control['speech_dispatch_cases'] if r['version']=='current-English'};rows=[]
    for original in packet['records']:
        r=deepcopy(original);case=dispatch[r['id']];raw=bytes.fromhex(r['current_hex']);body=raw[1:].decode('ascii')
        assert case['registered_catalog_match'] is None
        boundaries=[b for b in case['boundaries'] if 'text_hex' in b];assert len(boundaries)==1 and bytes.fromhex(boundaries[0]['text_hex'])==raw[1:]
        i=r['source_record_index'];r.update(older_English=body,older_effective_runtime_paragraph=' '.join(body.split()),registered_catalog_match=None,
            proposed_editorial_decision='retain-wording' if i in RETAIN else 'revise',whole_exchange_finding=(RETAIN if i in RETAIN else REVISE)[i],target_prose_not_authored=True,target_formatting_not_approved=True,no_completion_credit=True)
        rows.append(r)
    counts=Counter(r['proposed_editorial_decision'] for r in rows);assert counts=={'retain-wording':9,'revise':8}
    ROOT.mkdir(parents=True);save(ROOT/'seventeen_source_current_findings_nine_retentions_eight_revisions.json',dict(records=rows,counts=dict(counts),source_current_packet=str(SOURCE),source_current_packet_sha256=sha(SOURCE.read_bytes()),all17_effective_runtime_bodies_equal_raw_stored_bodies=True,no_registered_catalogue_override=True,
        clean_first_glosses_and_nine_actual_source_sheets_precede_older_English_comparison=True,all_five_echo_pairs_reviewed_together=True,two_sound_captions_not_human_speaker_labels=True,
        current_names_Lil_Argot_Angelo_Puccini_retained_with_source_name_field_and_voice_proofs=True,broader207_names_and_other_editorial_scope_open=True,
        no_target_prose_native_layout_integration_or_credit=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,VIEW,Path(__file__)]}))
    print('B20517 complete-context findings:9 justified word retentions/8 revisions;exact stored/effective source-current references;zero credit.')
