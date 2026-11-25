"""Apply and audit the clean-only lead while preserving all verified B169 completions."""
import os
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B170_clean_context_v4258 import ROOT as CHECKPOINT,SOURCE,PRIOR
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v4259')
if __name__=='__main__':
    assert not ROOT.exists()
    workspace=Path.cwd().resolve()
    receipt=read(CHECKPOINT/'staged_receipt.json')
    assert sha(SOURCE.read_bytes())==receipt['source_sha256'] and sha(PRIOR.read_bytes())==receipt['prior_sha256']
    for path,digest in receipt['preserved_release_files'].items():
        assert sha(Path(path).read_bytes())==digest,path
    plan=read(CHECKPOINT/'mutation_plan.json')
    for entry in plan:
        target,staged=Path(entry['target']),Path(entry['planned'])
        assert target.is_relative_to(workspace) and staged.is_relative_to(CHECKPOINT.resolve())
        assert sha(target.read_bytes())==entry['before_sha256'] and sha(staged.read_bytes())==entry['planned_sha256']
        assert staged.stat().st_size>=target.stat().st_size
    for entry in plan:
        with Path(entry['target']).open('r+b') as stream:
            stream.write(Path(entry['planned']).read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
    lp=Path('translations/editorial_review_current_v1.json')
    ledger,before=read(lp),read(CHECKPOINT/(lp.name+'.before'))
    allowed={'latest_checkpoint','lil_B170_clean_context_only_uncredited_v4257','unfinished_editorial_scope_v4258'}
    assert {k:v for k,v in before.items() if k not in allowed}=={k:v for k,v in ledger.items() if k not in allowed}
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(5692,5692,0)
    assert (ledger['records_with_source_and_prose_pass'],ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(5695,5692,3614,2078)
    source=read(SOURCE)
    assert source['all33_clean_source_read_and_individually_glossed_before_predecessor_English'] and source['no_predecessor_English_exposed']
    assert source['source_prose_or_completion_credit_added']==source['new_emulator_runs']==0
    block=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[170]
    lead=source['block']
    assert sha(block)==lead['clean_block_sha256'] and len(lead['records'])==33 and len(lead['complete_native_commands'])==45
    assert lead['source_selectors']==[2,25] and lead['source_macro_counts']=={'FI':1,'FA':0,'FO':1}
    for row in lead['records']:
        raw,at=bytes.fromhex(row['source_hex']),row['source_reference']['offset']
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert row['fresh_source_gloss'] and row['clean_source_complete_exchange_read_before_predecessor_English']
    assert sha(Path(source['source_transcript']).read_bytes())==source['source_transcript_sha256']
    candidate=ledger['current_integrated_candidate']
    prior=read(PRIOR)
    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']
    assert sha(Path(candidate['patch']).read_bytes())==candidate['patch_sha256']==prior['patch_sha256']
    assert ledger['completed_editorial_families']==before['completed_editorial_families']
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V4258')
    ROOT.mkdir(parents=True)
    result={**prior,'checkpoint':'V4258','ledger_sha256':sha(lp.read_bytes()),
        'prior_verified_checkpoint':str(PRIOR),'prior_verified_checkpoint_sha256':sha(PRIOR.read_bytes()),
        'B170_clean_context_only_uncredited_source':str(SOURCE),'B170_clean_context_sha256':sha(SOURCE.read_bytes()),
        'B170_clean_glosses':33,'B170_predecessor_English_unexposed':True,'B170_credit_added':0,
        'new_source_prose_reviews':0,'new_completed_records':0,'new_emulator_runs':0,'all_jobs_terminal':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'verified_handoff.json',result)
    save(CHECKPOINT/'checkpoint_receipt.json',{**receipt,'ledger_sha256':result['ledger_sha256'],
        'updated_files':{str(Path(e['target']).relative_to(workspace)):e['planned_sha256'] for e in plan}})
    print('V4258 independently verified:5692 completed,5695 source/prose,zero pending;B169 exact release unchanged,B17033 clean glosses uncredited. Full goal active.')
