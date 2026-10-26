"""Fresh clean-source review of16 timed duel reactions in their original action flow."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_bark_layout_v1200 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_reaction_editorial_v2524')
DOC=Path('translations/duel_reaction_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/duel_reaction_context_source_v2520/all16_clean_current_context_catalog.json')
CONTEXT=Path('work/analysis/duel_reaction_context_v2521/source_context_packet.json')
NOTES={
1957:('The duelist gives an upbeat exclamation that the action went just right.','Perfect! is a natural concise positive reaction to ばっちりだ. It adds no named move,damage amount or guaranteed future result.'),
1958:('The restrained duelist pauses,then confidently says they have read or anticipated the move.','...I saw that coming! preserves the pause and natural combat sense of 見切った. It adds no supernatural foresight or new ability. The complete literal I after the opening dots must remain visible.'),
1959:('The duelist dismisses the effectiveness of that kind of attack against them.','That attack won\'t work on me! preserves the confident personal taunt in familiar English. It does not identify a weapon or establish universal invulnerability as an engine rule.'),
1960:('The duelist dismisses the opponent\'s effort as naive or easy to read,then asks where they are looking.','Too easy! Where are you looking? preserves both the dismissive 甘い and pointed question. It avoids changing the taunt into a claim about attack speed or inventing a particular target.'),
1961:('The rough duelist goads the opponent and asks whether they have any intention of fighting.','Come on! Are you even trying? naturally combines the repeated goading call and taunting question. Even conveys the challenge to the opponent\'s effort without adding a named insult or another participant.'),
1962:('The older-voiced duelist gives an attacking shout and boasts that a single strike hits its mark.','Take that! Right on target! preserves the shout and 一撃必中 accuracy boast as natural combat speech. It invents no measured accuracy statistic,guaranteed future hit,rank or family address.'),
1963:('The simple duelist celebrates having landed a hit.','Yay! I hit you! retains the delighted cry and simple personal statement. You is the present dueling opponent. The speech is not independent verification of damage or a new target;the initial I must survive.'),
1964:('The measured duelist reacts positively and identifies the right point or moment.','Good! Right here! is a natural complete spoken reaction for よし、ここですな. It leaves the point or moment unspecified rather than inventing a named weakness or special technique.'),
1965:('The duelist reacts in surprise and admits having failed at the action.','Whoa! I messed that up... preserves the startled cry,self-directed admission and trailing disappointment. Failure need not mean a literal missed blow,and no particular mistake or cause is invented.'),
1966:('The duelist reacts with frustration and realizes they let their vigilance lapse.','Ugh... I let my guard down! preserves the pained reaction and retrospective self-realization in 油断したか. It is a natural realization rather than a genuine question to another person. It does not invent a physical slip or stumble.'),
1967:('The duelist admits missing and becoming too carried away or overconfident.','Missed! Got too cocky... preserves both the missed action and clipped self-reproach. The deliberate spoken fragments suit a brief combat reaction;they do not assign blame or invent a diagnosis.'),
1968:('The duelist gives an irritated drawn-out complaint of frustration.','Ugh! This is so frustrating! preserves irritation and the complete personal complaint naturally. It adds no accusation,insult or explanation for the frustration.'),
1969:('The rough duelist reacts in annoyance and admits being a little hasty.','Damn! I rushed that a bit! localizes the annoyed tongue-click as a mild gruff exclamation and preserves 少し with a bit. It adds no directed insult and keeps the haste self-directed.'),
1970:('The older-voiced duelist reacts in pain but defiantly insists that more of the fight is still to come.','Ugh... No matter. This fight is just getting started! preserves the pained opening,measured defiance and idiomatic continuation. It is the character\'s resolve,not an independently measured timer state,promise of victory or proof that combat will continue.'),
1971:('The simple duelist reacts with surprised disappointment because the opponent evaded the action.','Whoa! You dodged it! naturally addresses the present dueling opponent and preserves both surprise and evasion. It adds no new participant,weapon or explanation for the dodge.'),
1972:('The duelist reacts in pain and admits not being good at fighting.','Ugh... I\'m not much of a fighter... preserves both hesitations and the self-effacing admission as complete natural English. It adds no rank,diagnosis,permanent inability or accusation.'),
}

if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists()
 packet=read(PACKET);context=read(CONTEXT);preflight=read('work/analysis/duel_reaction_context_v2521/next16_preflight.json')
 priorpath=Path(preflight['registered_manuscript']);prior={r['message_id']:r for r in read(priorpath)['records']}
 assert set(prior)==set(NOTES)==set(range(1957,1973))and len(context['all416_unchanged_native_voice_selections'])==416
 rows=[]
 for source in packet['records']:
  n=source['message_ID'];old=prior[n]
  assert source['source_hex']==old['source_hex']and bytes.fromhex(source['current_hex'])==compiled(old)
  meaning,reason=NOTES[n];row=deepcopy(old)
  row.update(file_path='/COMMON/MESFILE.DK4',prior_speaker_metadata=old['speaker'],speaker_metadata_corrected=False,
   context='Independent timed-action voice alternative in the original duel flow. Both positive and negative1042C branches call D458 with nested-controller side0 and duration60. The positive branch returns caller result1;the negative branch returns0. These are timing/control-flow facts,not independent proof of HP damage from character boasts. Storage neighbors and other voice variants are not consecutive conversation. Keep genuine actor identity and the distinct24x3 static-duel consumer. '+old['context'],
   source_Japanese=source['clean_Japanese'],source_reference=source['source_reference'],current_reference=source['current_reference'],
   current_hex=source['current_hex'],current_stored_English=source['current_stored_English'],source_meaning=meaning,
   localization_note=reason,fresh_retained_wording_justification=reason,editorial_decision='retain-wording',
   review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  rows.append(row)
 ROOT.mkdir(parents=True);supplement=ROOT/'source_context_and_faithfulness_review.json'
 save(supplement,dict(records=[],all16_complete_clean_Japanese_and_timed_duel_context_freshly_read=True,
  independent_alternatives_not_sequential_turns=True,both_families_original_side0_duration60=True,
  anticipation_not_supernatural_sight=True,accuracy_and_hit_speech_not_measured_damage=True,
  carelessness_not_literal_stumble=True,haste_self_reproach_and_defiance_preserved=True,
  zero_credit_pending_native_historical_registered_reconciliation=True,full_goal_complete=False))
 doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
  consumer_layout_profile='duel-timed-reaction-postmacro24x3-v1',review_gates=['source','context','localization','naturalness','formatting'],
  file_path='/COMMON/MESFILE.DK4',source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
  current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),
  native_context_proof=str(CONTEXT),native_context_proof_sha256=sha(CONTEXT.read_bytes()),fresh_ordinary_supplement=str(supplement),fresh_ordinary_supplement_sha256=sha(supplement.read_bytes()),
  prior_manuscript=str(priorpath),prior_manuscript_sha256=sha(priorpath.read_bytes()),revised_IDs=[],retained_count=16,speaker_metadata_corrections=[],
  formatting_review_pending=True,current_native_and_actual_family_reconciliation_pending=True,records=rows,full_goal_complete=False)
 save(DOC,doc);save(ROOT/'fresh_source_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),individual_new_glosses_and_retention_reasons=16,
  no_English_speaker_ROM_or_runtime_change=True,completion_pending_native_historical_registered_reconciliation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('16 fresh clean-source glosses and individual timed-context retention reasons;formatting and reconciliation pending.')
