"""Fresh source/actor/cultural review of15 special calls;one English metadata normalization."""
from pathlib import Path
from copy import deepcopy
import unicodedata
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_special_layout_v1216 import compiled,IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_editorial_v2533')
DOC=Path('translations/duel_special_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/duel_special_context_source_v2529/all15_clean_current_context_catalog.json')
CONTEXT=Path('work/analysis/duel_special_context_v2530/source_context_packet.json')
NOTES={
1980:('Samwell confidently promises to demonstrate his two-sword fighting skill.','I\'ll show you what two swords can do! naturally promises a demonstration of 二刀流の技 rather than merely displaying weapons. Two swords is explicit in the source style. Samwell is the source actor22;no other character,weapon name,rank or guaranteed result is added.'),
1981:('Maria declares that the fooling around ends here.','Playtime is over! is the natural forceful taunt for 遊びはここまでよ. It does not establish literal children\'s play,an age or a new relationship. Original actor3 remains Maria.'),
1982:('Cristina dismisses the visible image as an afterimage.','Just an afterimage! preserves the terse declarative dismissal in the source special-move context. It names no additional illusion spell,clone or supernatural ability beyond the stated 残像.'),
1983:('Yukihisa announces the White Tree school of swordsmanship and its Twin Shadow Formation technique.','White Tree Sword Style: Twin Shadow Formation! retains both named components of 流派白樹剣術・双影陣. Formation naturally renders 陣. White Tree translates the school kanji without guessing a pronunciation or equating it with the separately verified katakana surname Shiraki. The established character name remains unchanged.'),
1984:('Gerhard scornfully asks whether the opponent thought such a monotonous or predictable attack would work.','Did you think such a predictable attack would work? preserves the rhetorical question and combat sense of 単調. Predictable avoids the misleading physical or merely boring senses of dull. It does not establish invulnerability or an engine guarantee.'),
1985:('Camille dismisses the opponent\'s swordplay as childish tricks compared with Gerhard\'s training.','That swordplay is child\'s play compared to Gerhard\'s training! preserves the explicit comparison and natural idiom. Gerhard\'s training keeps the source genitive without inventing a course,rank,kinship or extra history. さん is naturally omitted in this established-name combat taunt.'),
1986:('Ian challenges strength-only swordplay and follows with an attacking shout.','Think brute-force swings will work on me? Take this! preserves the sword-motion context,rhetorical challenge and くらえ follow-up. It adds no specific sword type,other weapon or guaranteed counterattack result.'),
1987:('Fernando laughs and announces that the show is starting.','Ha ha ha! It\'s showtime! preserves the laugh and playful showman announcement naturally. Source actor20 and literal1987 are distinct from Angelo1988. The body wording stays unchanged;only the review speaker label\'s legacy full-width F is normalized to ordinary English Fernando.'),
1988:('Angelo repeatedly goads the opponent,asks what is wrong and boasts that he has not yet become serious.','Hey, hey! What\'s the matter? I\'m not even trying yet! retains the repeated English Hey,teasing pressure and idiomatic not-serious-yet boast. It makes no literal claim about an effort statistic or attack calculation. Original actor15 is Angelo;no accent caricature is added.'),
1989:('Al promises to demonstrate sword skill honed through battlefield experience.','I\'ll show you swordplay honed on the battlefield! naturally expresses the source sword-skill boast. It does not invent a rank,campaign or independently verified biography,and does not mistake trained swordplay for manufactured steel.'),
1990:('Hodram announces an intended finishing blow.','You\'re done! is a natural concise finisher taunt for とどめだ. It expresses attack intent rather than certifying death,victory or the eventual duel result. Original actor1 remains Hodram.'),
1991:('Emilio cries out and playfully declares that he will throw the opponent.','Aaaah! You\'re going flying! retains the extended cry and emphatic throwing taunt in natural English. The source ほうり投げる supplies the throw;no literal levitation,new weapon or age fact is added.'),
1992:('Xien goads the opponent and points out that their guard is full of openings.','Come on! You\'re wide open! preserves the familiar goading call and standard combat idiom for 隙だらけ. It adds no named weakness,kinship or older-person title.'),
1993:('Yifa announces Taoist techniques and gives a martial exertion shout.','Taoist arts! Hyaah! preserves the established culturally specific 道術 terminology and exertion cry. It invents no named spell,deity,medical effect or guaranteed success.'),
2146:('Julio boasts that he will demonstrate the power of alcohol.','I\'ll show you the power of booze! retains the comic personal boast and natural colloquial alcohol reference. It adds no rum brand,Drunken Fist school,health benefit or actual combat modifier. The original numeric special-move context is retained rather than generic town dialogue.'),
}
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists()
 packet,context=read(PACKET),read(CONTEXT);preflight=read('work/analysis/duel_special_context_v2530/next15_preflight.json')
 priorpath=Path(preflight['registered_manuscript']);prior={r['message_id']:r for r in read(priorpath)['records']}
 bindings={r['message_ID']:r for r in context['all15_original_message_call_bindings']}
 assert set(prior)==set(NOTES)==set(IDS)
 rows=[];corrections=[]
 for source in packet['records']:
  n=source['message_ID'];old=prior[n];binding=bindings[n]
  assert source['source_hex']==old['source_hex']and bytes.fromhex(source['current_hex'])==compiled(old)
  assert old['source_actor_ID']==binding['actor_ID']and binding['side']==0 and binding['duration']==120
  meaning,reason=NOTES[n];row=deepcopy(old);speaker=old['speaker']
  if n==1987:
   assert speaker=='Ｆernando'and binding['actor_ID']==20
   speaker=unicodedata.normalize('NFKC',speaker);assert speaker=='Fernando'
   corrections.append(dict(message_id=n,source_actor_ID=20,before=old['speaker'],after=speaker,
    reason='Normalize the legacy full-width initial F in English review metadata. NFKC preserves the same source actor/name;ROM body text,actor identity,shared names and graphics are unchanged.'))
  row.update(file_path='/COMMON/MESFILE.DK4',speaker=speaker,prior_speaker_metadata=old['speaker'],speaker_metadata_corrected=n==1987,
   context='Independent original actor-specific special-move call. Original101EC dispatch and method-specific literal reach D4D0 with side0/duration120. This numeric consumer is distinct from timed-reaction duration60 and table-based acceptance/threat side1. Original actor identity is preserved;CPU controller-pointer and pose/animation bridges are source tests,not actual animation claims. Read with attack intent and character voice,not as consecutive conversation. '+old['context'],
   source_Japanese=source['clean_Japanese'],source_reference=source['source_reference'],current_reference=source['current_reference'],current_hex=source['current_hex'],
   current_stored_English=source['current_stored_English'],source_meaning=meaning,localization_note=reason,fresh_retained_wording_justification=reason,
   editorial_decision='retain-wording',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  rows.append(row)
 assert len(corrections)==1
 ROOT.mkdir(parents=True);supplement=ROOT/'source_context_and_faithfulness_review.json'
 save(supplement,dict(records=[],all15_complete_clean_source_and_actor_specific_context_freshly_read=True,
  named_martial_style_keeps_school_and_technique_distinct_from_Shiraki_surname=True,Gerhard_comparison_keeps_no_invented_kinship_or_rank=True,
  Taoist_arts_cultural_context_preserved=True,comic_alcohol_boon_is_character_boast_not_real_effect=True,
  actor15_Angelo1988_actor20_Fernando1987_and_actor22_Samwell1980_preserved=True,speaker_metadata_corrections=corrections,
  zero_credit_pending_native_historical_registered_reconciliation=True,full_goal_complete=False))
 doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
  consumer_layout_profile='duel-special-numeric-postmacro24x3-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',
  source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
  source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof=str(CONTEXT),native_context_proof_sha256=sha(CONTEXT.read_bytes()),
  fresh_ordinary_supplement=str(supplement),fresh_ordinary_supplement_sha256=sha(supplement.read_bytes()),prior_manuscript=str(priorpath),prior_manuscript_sha256=sha(priorpath.read_bytes()),
  revised_IDs=[],retained_count=15,speaker_metadata_corrections=corrections,formatting_review_pending=True,current_native_and_actual_family_reconciliation_pending=True,records=rows,full_goal_complete=False)
 save(DOC,doc);save(ROOT/'fresh_source_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),individual_new_glosses_and_retention_reasons=15,
  English_body_revisions=0,review_metadata_normalizations=1,no_ROM_runtime_shared_name_or_graphics_change=True,completion_pending_native_historical_registered_reconciliation=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('15 fresh source/context retentions;Fernando review metadata normalized;all display and integration gates pending.')
