"""Localize the whole clean Noritsune exchange; retain four working paragraphs with reasons."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_prose_v7045')
SOURCE=Path('work/analysis/lil_B222_source_v7037/sixteen_clean_current_sunset_Noritsune_exchange_source_references.json')
CONSUMER=Path('work/analysis/lil_B222_consumers_v7038/sixteen_effective_bodies32_dispatches_two_actors_four_name_consumers.json')
ACTUAL=Path('work/analysis/lil_B222_source_actual_v7044/all16_Japanese_speeches27_commands_complete_masks_headers_and_normal_return.json')
VIEW=Path('work/analysis/lil_B222_source_view_v7044b/all16_source_speeches_four_source_sheets_and_six_name_planes_viewed.json')
NAMES=Path('translations/lil_B222_speaker_name_review_v2.json')
OUT=Path('translations/lil_B222_editorial_manuscript_v1.json')
PROSE={
5:('revise','...',
    'Preserve the initial silent beat with the conventional American dialogue ellipsis. The two original Japanese ellipsis glyphs do not encode an audible word or a fixed pause duration;do not invent a sigh,gesture or emotion. This punctuation decision is not driven by allocation.'),
9:('retain-wording',"Gerhard? Watching the sunset? What's wrong?",
    'The three short questions sound like Lil noticing an unusual quiet moment and prompting her reserved companion. The given name agrees with the original current name consumers and cleanゲルハルト;the casual fragments and concern are natural in this full exchange. No relationship,title or new cause for his mood is supplied.'),
13:('revise','Admiral... I heard a story here in Japan about a certain man, and it moved me deeply. Quite unlike me...',
    'Restore his personal report that he heard about a certain man and his unusual emotion,using active,spoken English instead of A story heard here. Admiral retains the explicit提督 fleet-leader address already present;it does not add a new commission or promotion. The trailing understatement preserves his formal,self-conscious voice and prepares Lil\'s later teasing.'),
17:('revise',"Hmm. Is he someone I'd know?",
    'Restore Lil\'s singularあたし rather than the predecessor\'s we. The question concerns recognition without inventing a personal acquaintance;the next answer can reveal that the man lived centuries ago.'),
20:('revise','He was a military commander who lived hundreds of years ago. His name was Noritsune.',
    'Give the source武将 its military-leader meaning in complete natural sentences. Preserve the nonspecific hundreds of years andノリツネ. Do not introduce a surname,clan name,dated battle,formal rank or outside biography.'),
23:('revise','What made him so great?',
    'Make the object of Lil\'s question explicit:the man just introduced. This is an interested prompt for the story,not a sarcastic dismissal or a question about the historical era.'),
27:('retain-wording','His clan had once known great glory. But defeat after defeat at the hands of their rivals drove them toward extinction.',
    'This already forms a fluent formal historical account matchingかつて栄華 and the repeated defeats that drove the unnamed clan toward滅亡. His clan establishes membership without making him its ruler;their rivals remain unnamed. Toward preserves the source\'s unfolding decline rather than certifying every member\'s death.'),
30:('revise','As his weak clansmen were cut down one by one, he alone fought back bravely...',
    'Restore the one-after-another progression and keep the same-clan membership and brave resistance. Weak is Gerhard\'s unflattering source judgment,not narrator fact. Do not intensify軟弱 into cowardice,treachery or a particular mental state.'),
33:('revise','They say he leaped across seven ships during the final naval battle, trying to reach the ship carrying the enemy commander.',
    'Restore the final naval battle and the reported-traditionそうです. Preserve exactly seven vessels and the enemy commander aboard the destination ship. Trying to reach preserves the goal without inventing a successful arrival,a kill,a flagship title or a measured distance.'),
37:('revise','But his strength finally failed. They say he sank to the bottom of the strait with an enemy soldier under each arm, gleaming armor and all...',
    'Preserve exhaustion,the two enemy soldiers(one under each arm),the strait\'s depths and the gleaming armor. They say carriesとか rather than presenting an independently verified narrator fact. Do not add a deliberate-suicide motive,a named strait,the armor\'s material or an acquisition. This wording supplies the phrase Lil later echoes.'),
40:('retain-wording','Such courage in this small eastern nation! What a glimpse of the spirit of the East.',
    'The short,admiring exclamations naturally convey his uncharacteristic enthusiasm and the source\'s small-eastern-country comparison. The spirit of the East is an idiomatic cultural metonym for his own dated東洋人の真髄 viewpoint;retain that characterization without adding a slur,biological assertion or narrator endorsement. Lil\'s following reply broadens the thought to heroes everywhere.'),
44:('retain-wording','Every land has exceptional heroes, huh?',
    'This fluent observation preservesどこの国にも and人並みはずれた英雄. Land is an ordinary geographical idiom and huh keeps Lil\'s conversationalね. It responds to Gerhard\'s generalization without adding a new national claim or a corrective lecture.'),
47:('revise',"Yes. Even an island nation shouldn't be underestimated.",
    'Restore the actual principle島国といえどもあなどれません. The earlier island can breed heroes replaces that warning with a different image. Keep the respectful agreement and the source\'s even without adding contempt,an assertion of military strength or an innate national trait.'),
50:('revise',"Hehe. So you've got a soft spot for stories like that, Gerhard. (He looks scary, but he's got such a pure heart.)",
    'Soft spot conveysこういう話に弱い without implying gullibility or irritation. Keep the familiar given-name address and gentle laugh. Only the parenthesized assessment is explicitly private;the complete English subject makes the thought natural while preserving frightening appearance versus a pure heart. No romance,kinship,childishness or new personality diagnosis is invented.'),
54:('revise','...Into the strait... gleaming armor and all... Hmm.',
    'Restore the gleaming description and the quiet echo of Gerhard\'s armor/strait details. This is suggestive reflection,not an explicit recovery plan,guaranteed treasure location,value,coordinate or item effect. Preserve the pauses through punctuation rather than authored line breaks or a new private-thought wrapper.'),
57:('revise','How unlike me to ramble on like that. I should get back to work.',
    'Restore his personal self-consciousness in私としたことが and natural return to reserve. Choosing I should avoids inventing an order to the fleet leader or an assigned job. It does not add an explicit apology,a promise or an outcome beyond the proposed return to work.')}
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists();source,consumers,actual,view,names=map(read,[SOURCE,CONSUMER,ACTUAL,VIEW,NAMES])
    assert source['all16_clean_speeches_glossed_together_before_old_English'] and source['total_editorial_objects']==16
    assert actual['actual_unique_source_speeches']==16 and actual['all27_stored_commands_executed'] and not view['visual_review_pending']
    assert names['all_two_contextual_name_retentions_five_gates_true_no_asset_change']
    effective={r['id']:r for r in consumers['effective_current_records']};speakers={2:'Lil Argot',16:'Gerhard Ardelknatts'};rows=[]
    assert set(PROSE)=={r['source_record_index'] for r in source['records']}
    for item in source['records']:
        row=deepcopy(item);previous=effective[row['id']];decision,body,note=PROSE[row['source_record_index']]
        assert '\n' not in body and '\r' not in body and body==body.strip() and '  ' not in body and all(x not in body for x in ['{LB','{PAD','{ALIGN'])
        if decision=='retain-wording':assert body==previous['effective_predecessor_paragraph']
        row.update(english=f'{{SPEAKER:{row["source_selector"]:02X}}}'+body,speaker=speakers[row['source_selector']],context=row['whole_exchange_context'],
            source_meaning=row['fresh_source_gloss'],localization_note=note,editorial_decision=decision,editorial_finding=note,
            fresh_retained_wording_justification=note if decision=='retain-wording' else None,retention_reason=note if decision=='retain-wording' else None,
            current_raw_storage_English=bytes.fromhex(row['current_hex'])[1:].decode('cp932'),current_effective_paragraph=previous['effective_predecessor_paragraph'],
            current_effective_runtime_template_hex=previous['current_effective_runtime_template_hex'],current_expanded_runtime_hex=previous['current_expanded_runtime_hex'],
            current_registered_catalogue_match=previous['registered_catalogue_match'],source_voice_class=previous['source_voice_class'],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            full_exchange_read_aloud_review='Read with all previous/next speeches:quiet opening,unexpected emotion,recognition question,entire heroic report,dated admiration,universal reply,teasing/private thought,armor echo and return to duty. Both character voices and all source uncertainty remain.',
            no_manual_line_break_padding_or_alignment_authored=True,current_complete_native_display_pending=True,registered_integration_pending=True,
            formatting_reason='Whole-paragraph formatting,pair phase,complete glyphs,bounds,pagination,relocation,actual English and registered release remain pending. No source facts or wording were shortened to satisfy an allocation.',source_prose_or_completion_credit_added=0)
        rows.append(row)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':4}
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONSUMER,ACTUAL,VIEW,NAMES,Path(__file__)]}
    doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        file_path='/data/SC2.DK4',records=rows,revised=12,retained=4,review_gates=['source','context','localization','naturalness','formatting'],formatting_review_pending=True,
        source_ROM=source['source_ROM'],source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=source['current_COMMON_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        current_strict_native_input=source['current_strict_native_input'],current_consumer_proof=str(CONSUMER),current_consumer_proof_sha256=sha(CONSUMER.read_bytes()),
        actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),source_visual_review=str(VIEW),source_visual_review_sha256=sha(VIEW.read_bytes()),
        speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),whole_exchange_context=read(source['whole_exchange_context_notes'])['whole_exchange_context'],
        all16_four_prose_gates_true_formatting_false=True,no_original_or_invented_FI_FA_FO=True,source_seven_vessels_two_soldiers_hearsay_private_thoughts_and_armor_subtext_preserved=True,
        all_historical_and_cultural_generalizations_remain_character_viewpoints=True,no_clan_name_strait_name_date_new_rank_relationship_or_guaranteed_find_invented=True,
        event222_requires89_initialized_Amsterdam_fixture_not_natural_Japan_activation=True,no_name_asset_or_duplicate_name_credit=True,
        source_prose_or_completion_credit_added=0,evidence=evidence,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUT,doc);save(ROOT/'whole_exchange_twelve_revisions_four_justified_retentions.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),
        revised=12,retained=4,all16_four_prose_gates_true_formatting_false=True,new_review_credit=0,full_goal_complete=False))
    print('B222 whole-exchange manuscript:12 revisions/4 justified retentions. Two names retained;format/native English/registered release pending.No completion credit.',flush=True)
