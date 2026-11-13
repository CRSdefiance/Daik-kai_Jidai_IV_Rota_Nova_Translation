"""Fresh individual contextual review of seven unfinished Lookout reports."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reinforcement_sniping_layout_v1024 import compiled, PROFILE
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/admiral_shot_editorial_v2657')
PACKET = Path('work/analysis/admiral_shot_context_v2656c/all7_clean_current_context_catalog.json')
OUT = Path('translations/admiral_shot_contextual_editorial_manuscript_v1.json')
NOTES = {
1924: ('Admiral, we have successfully shot the enemy admiral! This is our victory!',
       "Admiral, we've shot the enemy admiral! Victory is ours! preserves the explicit address, completed successful shot and collective victory. The concise professional announcement fits the original polite report. Shot does not assert death, execution or a particular firearm. The compiler owns the leading presentation cell; it is not authored prose."),
1925: ('We did it! We shot the enemy admiral! We won, I tell you!',
       'Yes! We shot the enemy admiral! We won! carries the exuberant opening and familiar repeated excitement of やった and よ. We is the original collective success, with no added Admiral address. The report announces victory after the successful shot, not a promise, a reward or a statement that the enemy admiral died.'),
1926: ('We successfully shot the enemy admiral! Victory is ours!',
       'We shot the enemy admiral! Victory is ours! naturally expresses the successful action and 私たち collective victory. The assertive, composed delivery preserves this voice without imposing an artificial feminine English dialect, relationship or rank. The wording does not expand successful sniping into death or total fleet destruction.'),
1927: ('The shot at the enemy admiral succeeded! We won!',
       'A direct hit on the enemy admiral! We won! is an excited, clipped battlefield report matching the emphatic success and familiar ぜ. Direct hit expresses the successful targeted shot without naming a weapon, specifying a wound or declaring death. It keeps the source victory and adds no Admiral address.'),
1928: ('Admiral, the shot at the enemy admiral succeeded! Victory is ours!',
       "Admiral, we shot their admiral! We've won! preserves the explicit address, successful action and わしら collective victory. Their has the immediately established enemy as its referent. Contractions give the older familiar voice natural warmth without invented age, kinship or archaic English. No fatality or reward is added."),
1929: ('Our shot hit the enemy admiral! Hooray! We won!',
       'Our shot hit the enemy admiral! Hooray! We won! preserves the explicit hit, drawn-out celebration and おいらたち collective victory. Hooray carries the playful excitement without inventing a child age, dialect or relationship. General shot respects 弾 without specifying a cannonball, musket or wound severity.'),
1930: ('We have shot the enemy admiral! This is our victory!',
       "We've shot the enemy admiral! Victory is ours! preserves the successful shot and polite, emphatic collective victory. The confident full victory declaration carries ですな naturally without a forced old-fashioned tag, new rank or age claim. It does not assert death, capture or a particular weapon."),
}

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists()
    packet = read(PACKET)
    owner = packet['registered_prose_owner_binding']
    prior = {r['message_id']: r for r in read(owner['manuscript'])['records']}
    cp = Path(packet['source_context'])
    context = read(cp)
    assert sha(cp.read_bytes()) == packet['source_context_sha256']
    rows = []
    for s in packet['records']:
        n = s['message_ID']
        r = deepcopy(prior[n])
        assert r['source_hex'] == s['source_hex'] and compiled(r).hex() == s['current_hex']
        meaning, note = NOTES[n]
        r.update(file_path='/COMMON/MESFILE.DK4',
                 consumer='original-53D44-role7-admiral-shot-portrait',
                 registered_prose_owner=owner['stage'],
                 registered_manuscript=owner['manuscript'],
                 registered_compiler=owner['compiler'],
                 context=context['scope'], source_Japanese=s['clean_Japanese'],
                 source_reference=s['source_reference'], current_reference=s['current_reference'],
                 current_hex=s['current_hex'], current_stored_English=s['current_stored_English'],
                 source_meaning=meaning, localization_note=note,
                 fresh_retained_wording_justification=note,
                 editorial_decision='retain-wording', speaker_metadata_corrected=False,
                 review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
        rows.append(r)
    ROOT.mkdir(parents=True)
    ordinary = ROOT/'complete_event_context.json'
    save(ordinary, dict(storage_neighbors=packet['neighbors'],
        neighbors_are_not_sequential_replies=True,
        seven_alternative_reports_not_one_exchange=True,
        source_event='Original battle condition and physical Lookout metric/chance gate precede the report. A successful targeted shot is announced with victory; the original code then clears the enemy fleet state byte and chooses its existing battle outcome branch. No reply to the report is stored in this table.',
        context_only_no_extra_credit=True,
        distinct_risk='Existing support snapshot is not shot-eligible. Dispatch/font proof does not establish the distinct post-shot outcome transition or a naturally activated shot event. Focused source/transition reconciliation remains pending.',
        full_goal_complete=False))
    save(OUT, dict(format='dk4-natural-dialogue-manuscript-v2',
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', consumer_layout_profile=PROFILE,
        review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/COMMON/MESFILE.DK4', source_ROM_sha256=packet['source_ROM_sha256'],
        current_ROM=packet['current_ROM'], current_ROM_sha256=packet['current_ROM_sha256'],
        current_ARM9_sha256=packet['current_ARM9_sha256'], current_COMMON_sha256=packet['current_COMMON_sha256'],
        source_context_packet=str(PACKET), source_context_packet_sha256=sha(PACKET.read_bytes()),
        native_context_proof=str(cp), native_context_proof_sha256=sha(cp.read_bytes()),
        fresh_ordinary_supplement=str(ordinary), fresh_ordinary_supplement_sha256=sha(ordinary.read_bytes()),
        registered_prose_owner_bindings=[owner],
        prior_manuscripts=[dict(path=owner['manuscript'], sha256=owner['manuscript_sha256'])],
        revised_IDs=[], retained_count=7, speaker_metadata_corrections=[],
        formatting_review_pending=True, current_native_and_representative_transition_reconciliation_pending=True,
        completion_credit_added=0, records=rows, full_goal_complete=False))
    save(ROOT/'fresh7_review_receipt.json', dict(manuscript=str(OUT), manuscript_sha256=sha(OUT.read_bytes()),
        new_individual_glosses_and_retention_reasons=7, new_revisions=0,
        formatting_and_transition_reconciliation_pending=True,
        fresh_integrated_credit=0, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print('Seven original Lookout reports freshly reread; existing English retained with individual reasons. Native/transition completion pending; zero completion credit.')
