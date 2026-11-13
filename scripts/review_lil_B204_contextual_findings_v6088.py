"""Record individual whole-exchange findings and proposed retentions before target authoring."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_contextual_findings_v6088')
SOURCE=Path('work/analysis/shachihoko_current_context_v6078/four_complete_source_current_exchanges_and_raw_Orca_candidates.json')
RETAIN={
5:'The clipped Bored/Time for a walk rhythm suits restless Jam. The next question explicitly supplies the walk-to-relieve-boredom context. Retain the words;regenerate ordinary wrapping and padding.',
9:'Ma\'am is a natural respectful address to the innkeeper without inventing an aunt. The nearby-attraction question and casual Need a walk to kill time preserve his motive and voice. A spoken fragment works in this complete exchange.',
13:'The lord\'s castle is east of here is a natural concise answer that preserves the explicit direction and location. No named castle,king or emperor is introduced. The source suggestion does not require copying a filler into English.',
19:'Jam! Where have you been? naturally conveys Lil\'s exasperated demand after his absence. The initial exclamation carries the raised voice without requiring a literal punctuation transcription.',
22:'Sorry. This thing\'s heavy. is a natural casual apology and weight excuse in answer to Lil. One English apology carries the repeated Japanese apology\'s function without inventing an injury or provenance.',
36:'The conditional if you didn\'t steal it preserves Lil\'s suspicion without confirming a legitimate gift. We\'re leaving soon. Get ready. gives her brisk departure instruction and urgency naturally in context.',
40:'Got it. Just give me a minute. is idiomatic casual compliance and a request to wait briefly. It does not assert that departure or an inventory effect has finished.',
58:'At once! is a natural deferential response to the search order. It promises compliance rather than claiming the thief is already caught;no invented rank or relationship is added.'}
REVISE={
16:'The older repeated castle/country\'s castle sounds translated. Convey the Japanese-term/loanword recognition naturally,then Jam\'s cheerful decision to look,without inventing a second place or a language lesson.',
25:'Where from? is needlessly telegraphic for Lil here. Preserve both the object question and the origin question as natural spoken English.',
29:'Restore Jam\'s cocky Can\'t you tell? challenge and genuine made-in-Japan boast. Keep figurehead as his confident character claim;do not replace his mistaken explanation with narrator correction.',
33:'The source says the locals apparently do not know how to use figureheads. Preserve that apparent judgment,his claim to have taught them and his claim to a thank-you gift. The old flat had no idea and detached Showed them weaken the source nuance and spoken flow.',
45:'Restore the guard\'s panicked stammer and repeated call in a natural urgent/deferential line. Disaster alone loses the sense that something terrible has happened;do not invent a military rank or royal title.',
48:'At dawn narrows the source\'s morning complaint without support. Restore an irritated What is it? and morning racket complaint in the daimyo\'s authoritative voice.',
52:'Preserve the frightened stammer and the fact that the letter uses foreign writing. Foreign letter alone may imply foreign provenance instead of script. Keep shachihoko consistent with the cultural object without inventing a particular language.',
55:'Restore the startled response and explicit disaster. The source orders the thief found;Catch can add an arrest not stated here. Preserve the determined search and prospective order.',
62:'Dear lord of Japan can imply a sole ruler of Japan. Preserve a Japanese lord as the letter\'s addressee and the greeting,without inventing an emperor,king,named ruler or unspoken allegiance. Review the salutation as part of Jam\'s complete letter.',
66:'Restore the writer\'s confident explanation and tentative guess about knowledge being passed on incompletely. Someone got the story mixed up replaces that specific supposition. Preserve the ship/castle contrast and unreliable character viewpoint.',
69:'No reward needed/Took one spare changes the source\'s no-thanks-needed and announced taking in exchange for advice. Preserve the presumptuous spare claim,one per ship and patronizing reminder without inventing permission,payment or a completed legitimate gift.',
72:'Take care, Jam Jack Ludwyan can read as addressing Jam. Preserve a sign-off followed by the separately bound full signature. The native FE letter object and any justified real paragraph boundary must not become authored indentation or premature ordinary wraps.'}
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);group=next(g for g in packet['groups'] if g['file_path']=='/data/SC2.DK4' and g['block']==204);assert set(RETAIN)|set(REVISE)=={r['source_record_index'] for r in group['records']} and not set(RETAIN)&set(REVISE)
    rows=[]
    for old in group['records']:
        r=deepcopy(old);i=r['source_record_index'];retain=i in RETAIN
        r.update(proposed_editorial_decision='retain-wording' if retain else 'revise',whole_exchange_finding=RETAIN[i] if retain else REVISE[i],
            target_prose_not_authored=True,target_formatting_not_approved=True,no_completion_credit=True)
        rows.append(r)
    counts=Counter(r['proposed_editorial_decision'] for r in rows);assert counts=={'retain-wording':8,'revise':12}
    ROOT.mkdir(parents=True);save(ROOT/'twenty_source_current_findings_eight_proposed_retentions_twelve_revisions.json',dict(source_current_packet=str(SOURCE),source_current_packet_sha256=sha(SOURCE.read_bytes()),
        source_first_complete_exchange_and_independent_four_route_context_review_preserved=True,file_path='/data/SC2.DK4',block=204,records=rows,
        counts=dict(counts),proposed_retentions_have_individual_contextual_reasons=True,
        all_speaker_controls_four_FE_objects_six_other_leaves_and_runtime_macro_absence_to_remain_exact=True,
        source_actor_role_name_field_and_actual_nameplate_proofs='work/analysis/lil_B204_source_names_v6065/five_exact_source_name_fields_voices_and_distinct_name_consumers.json',
        shared_item_name_and_COMMON2931_description_coordination_pending=True,
        no_new_target_words_native_layout_approval_integration_or_credit=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]}))
    print('B20420 source/current findings:8 individually justified proposed word retentions/12 revisions. Target prose/native formatting/integration pending;zero credit.')
