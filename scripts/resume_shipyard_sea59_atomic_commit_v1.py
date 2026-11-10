"""Resume only the verified pending59-record ledger replacement after a Windows rename refusal."""
import gzip,json,os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Sea22_Fleet66_release_verified_20261105')
DEST=Path('translations/editorial_review_current_v1.json')
PENDING=Path('translations/editorial_review_current.shipyard_sea59_completion.pending.json')
BEFORE='dfa1cadc43a5afa0b43376e2228ad1f28c6217b27f0d418b0bdec7e0bd15185a'
AFTER='2fdc1973fdd2cc32b0adc9ec6df8e5fe3aeec1ee704bd422736d52d51f9c1572'
FAMILY='shared_HELP_shipyard37_sea22_Command66_complete_contextual_release_20261105'

if __name__=='__main__':
    assert not (ROOT/'completion_checkpoint.json').exists()
    oldbytes=gzip.decompress((ROOT/'ledger_before_completion.json.gz').read_bytes())
    assert sha(oldbytes)==sha(DEST.read_bytes())==BEFORE and sha(PENDING.read_bytes())==AFTER
    old=json.loads(oldbytes);new=load(PENDING)
    assert (old['records_editorially_completed'],new['records_editorially_completed'])==(11359,11418)
    assert (new['records_revised_and_integrated'],new['retained_wordings_editorially_completed'])==(6645,4773)
    assert new['records_with_source_and_prose_pass']==new['records_with_source_prose_drafts']==11421
    assert new['current_integrated_candidate']['sha256']=='81511dde6bc4cd81dee799e8ce893ba06f1fa44d96bbd541ac86ca67ae2d9635'
    context='contextual_story_natural_dialogue_pass_v1871'
    for field in ['record_keys','integrated_record_keys','record_IDs','reconciled_families']:
        assert new[context][field][:len(old[context][field])]==old[context][field]
    allowed={'completed_editorial_families','coverage_units','records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','records_with_source_prose_drafts',context,'shared_HELP_T44_T80_contextual_20261104',
        'shared_HELP_T81_T102_contextual_20261104','shared_HELP66_Command_amendment_20261104','sea22_fleet66_registered_cumulative_20261105',
        'current_integrated_candidate','latest_checkpoint'}
    assert {k:v for k,v in old.items() if k not in allowed}=={k:v for k,v in new.items() if k not in allowed}
    assert len(new[context]['record_keys'])==len(new[context]['integrated_record_keys'])==11418
    assert len(new['completed_editorial_families'])==len(old['completed_editorial_families'])+1 and new['completed_editorial_families'][-1]['id']==FAMILY
    rp=ROOT/'registered_release_verification.json';release=load(rp)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==new['current_integrated_candidate']['sha256']
    assert not new['full_goal_complete']
    os.replace(PENDING,DEST)
    assert sha(DEST.read_bytes())==AFTER
    save(ROOT/'completion_checkpoint.json',dict(family=FAMILY,new_credit=59,counts=dict(completed=11418,revised=6645,retained=4773),
        ledger_before_sha256=BEFORE,ledger_after_sha256=AFTER,all_unrelated_keys_andearlier_record_prefixes_exact=True,
        source_prose_draft_historical_counts=11421,main_unchanged=True,full_goal_complete=False,guide_photos=False,
        exact_prepared_transaction_resumed_without_regenerating_or_double_crediting=True,
        original_Windows_rename_refusal_preserved_in_producer_history=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Committed exact pending59-record transaction once:11418 completed/6645 revisions/4773 retentions;all earlier prefixes preserved.')
