"""Pin researched recruitment prose, native evidence and unfinished coverage."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_tavern_recruitment_v771 import CURRENT,ROOT
from scripts.review_tavern_recruitment_v771 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save


def main():
    folder=ROOT/'native_layout_phrases_v2'
    doc=read(MANUSCRIPT);native=read(folder/'verification.json')
    contracts=read(ROOT/'typed_status_contracts.json');scope=read(ROOT/'dispatch_adapter.json')
    statuses=read(folder/'all_status_font_review.json')
    assert native['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert native['complete_native_layouts']==3423 and contracts['count']==140
    assert scope['paired_scope_and_register_contracts']==128644
    assert read(folder/'matrix.json')['findings_count']==0
    assert len(doc['records'])==25 and sum(r['decision']=='revise' for r in doc['records'])==16
    assert all(not r['review']['formatting'] for r in doc['records'])
    old=read(ROOT/'case_only_prototype_SUPERSEDED/native_layout/verification.json')
    known={(r['id'],r['sha256']) for r in old['independent_full_font_planes']}
    planes=native['independent_full_font_planes']
    changed=[r for r in planes if (r['id'],r['sha256']) not in known]
    assert len(planes)==91 and len(changed)==20
    for row in planes+statuses['all24_independent_native_status_planes']:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
    assert statuses['primary_font_proof_sha256']==sha((folder/'verification.json').read_bytes())
    visual=folder/'visual_review.json'
    save(visual,{'new_complete_planes_visually_inspected':[{'path':r['path'],'sha256':r['sha256']} for r in changed],
        'byte_identical_to_previously_inspected_planes':71,
        'prior_plane_reference':str(ROOT/'case_only_prototype_SUPERSEDED/native_layout/verification.json'),
        'all24_condition_planes_visually_inspected':statuses['two_full_status_sheets'],
        'ambiguous_contact_sheet_checked_at_native_resolution':['font_082_ID906.png','font_083_ID906.png','font_087_ID906.png'],
        'findings':[], 'native_font_research_only_not_gameplay_screenshots':True})
    protected={
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        str(CURRENT):'eb170a31525470658180db3bd9e0d0ae07a8cffadba5002975bf8cc97cfe0f1f',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv':'d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv':'d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'}
    for path,digest in protected.items():assert sha(Path(path).read_bytes())==digest,path
    proof={'source_prose_drafts':25,'draft_revisions':16,'retained_wordings':9,
        'source_message_IDs':list(range(883,908)),'paired_dispatch_ABI_cases':128644,
        'whole8MiB_typed_field_contracts':140,'native_layouts':3423,'independent_primary_font_planes':91,
        'newly_inspected_primary_planes':20,'unchanged_prior_inspected_planes':71,'additional_condition_planes':24,
        'protected_files_unchanged':protected,'current_integrated_candidate':read('out/editorial_review_latest.json'),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'native_proof_sha256':sha((folder/'verification.json').read_bytes()),
        'new_editorially_completed':0,'new_ROM':False,'full_goal_complete':False,
        'remaining':['Owned no-growth runtime code and phrase storage','Full native copies and inherited-output verification',
            'Registered combined release and exact clean patch','Targeted cold-boot recruitment and condition scenes/returns',
            'Remaining shared dialogue,all routes,other player-facing prose and separate graphics audit'],
        'producer_sha256':sha(Path(__file__).read_bytes())}
    proof['storage_investigation']={
        'unchanged_Japanese_census':str(ROOT/'unchanged_Japanese_allocations_NOT_FREE.json'),
        'unchanged_Japanese_census_sha256':sha((ROOT/'unchanged_Japanese_allocations_NOT_FREE.json').read_bytes()),
        'consolidation_design':str(ROOT/'dispatcher_consolidation_DESIGN_NOT_APPROVED.json'),
        'existing_private_dispatch_bytes_for_unproven_consolidation':564,
        'production_storage_approved':False}
    save(ROOT/'research_checkpoint.json',proof)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==230 and ledger['records_revised_and_integrated']==175
    assert ledger['retained_wordings_editorially_completed']==55
    ledger['records_with_source_and_prose_pass']=258;ledger['records_with_source_prose_drafts']=258
    ledger['active_source_prose_drafts']={
        'native_message_IDs':[750,751,752]+list(range(883,908)),
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'not-integrated-context-and-native-presentation-evidence-recorded-per-family',
        'note':'750-752 caller context remains unmapped.883-907 source/caller/prose and scoped native prototype pass;owned production placement,copies,registered patch and actual scenes remain.'}
    checkpoint={'id':'V771-recruitment-and-condition-phrase-native-research',
        'documentation':'docs/recruitment_editorial_v771_research.md','manuscript':str(MANUSCRIPT),
        'source_prose_records':25,'draft_revisions':16,'retained_wordings':9,'new_editorially_completed':0,
        'new_ROM':False,'complete_native_layouts':3423,'independent_complete_font_planes':91,
        'additional_condition_font_planes':24,'evidence':str(ROOT/'research_checkpoint.json')}
    ledger['research_checkpoints']=[r for r in ledger['research_checkpoints'] if r['id']!=checkpoint['id']]+[checkpoint]
    ledger['latest_checkpoint']='V771 research reviews25 recruitment/condition entries(16 proposed revisions/9 retained).128644 paired scope/ABI cases,140 whole8MiB contracts,3423 native layouts,91 primary and24 condition font planes pass.230 remain complete(175 revised/55 retained);258 source/prose with28 drafts. V770 remains latest;owned placement,copies,registered patch and actual scenes for883-907 remain. Broader goal and graphics audit remain open.'
    ledger['coverage_units'][0]['next']='Integrate883-907 after owned no-growth runtime/copy proofs and actual scenes;map750-752,then908 onward and broader shared/Lil/all routes/player-facing prose. Preserve graphics audit and older-record follow-up.'
    save(ledger_path,ledger)
    archive=Path('E:/Rota Nova translations/Editorial review/V771 Recruitment editorial research')
    files=[p for p in ROOT.rglob('*') if p.is_file() and 'case_only_prototype_SUPERSEDED' not in p.parts]
    for path in files:
        target=archive/'evidence'/path.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    extras=[MANUSCRIPT,ledger_path,Path('docs/recruitment_editorial_v771_research.md')]
    extras += [Path('docs')/n for n in ('translation_progress.md','known_issues.md','todo.md')]
    extras += [Path('scripts')/n for n in ('inventory_tavern_recruitment_v771.py','context_tavern_recruitment_v771.py',
        'review_tavern_recruitment_v771.py','recruitment_runtime_research_v771.py','verify_recruitment_runtime_v771.py',
        'probe_recruitment_layout_v771.py','review_status_previews_v771.py','checkpoint_recruitment_v771.py',
        'inventory_recruitment_storage_v771.py')]
    for path in extras:
        target=archive/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    manifest={str(p.relative_to(archive)):sha(p.read_bytes()) for p in archive.rglob('*') if p.is_file() and p.name!='archive_manifest.json'}
    save(archive/'archive_manifest.json',{'files':manifest,'new_ROM':False,'source_integrated_candidate':proof['current_integrated_candidate']})
    print(f'V771 research checkpoint:25 drafts,3423 layouts;230 completed unchanged. Archived {len(manifest)} files on E.',flush=True)


if __name__=='__main__':main()
