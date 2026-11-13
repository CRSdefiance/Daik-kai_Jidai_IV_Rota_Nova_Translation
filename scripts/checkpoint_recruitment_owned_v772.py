"""Archive proved runtime/copies without granting integration completion credit."""

import shutil
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.probe_button_prompt_native import BASE,machine
from scripts.review_tavern_recruitment_v771 import MANUSCRIPT
from scripts.verify_recruitment_owned_v772 import ROOT
from scripts.verify_village_wrap_v608 import read,save


def main():
    plan=read(ROOT/'prospective_common_repack.json');owned=read(ROOT/'owned_runtime_plan.json')
    contracts=read(ROOT/'typed_status_contracts.json');closure=read(ROOT/'quantity_caller_closure.json')
    assert contracts['count']==140 and len(closure['exact_seven_ARM_BLs'])==7
    assert not read(ROOT/'storage_reference_census.json')['unexpected_references']
    assert read(ROOT/'dispatch_adapter.json')['paired_scope_and_register_contracts']==128644
    assert read(ROOT/'quantity_equivalence.json')['count']==84
    assert read(ROOT/'native_layout/identical_to_reviewed_v771.json')['all3423_complete_case_records_exact']
    assert read(ROOT/'Thumb_ISA_audit.json')['only16bit_Thumb1_and_ARMv5_BL_BLX']
    count=0
    for block in range(41):
        proof=read(ROOT/f'native_copies/native_copies_block_{block:02d}.json')
        assert proof['COMMON_sha256']==plan['target_COMMON_sha256'] and proof['ARM9_sha256']==plan['target_ARM9_sha256']
        for row in proof['cases']:assert row['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact']
        count+=len(proof['cases'])
    assert count==7336
    common=(ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes();arm=(ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    entries=local_entries(plan['directory_sha256'])(common,arm,clean=False)
    prior=read('work/analysis/dialogue_formatting_user_recheck_v767/COMMON676_677.json');u=machine(arm)
    u.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));rows=[]
    for old in prior['entries']:
        n=old['id'];assert entries[n].text==old['template'].encode()
        formatted,lines=native_layout(u,entries[n].text,n,())
        assert formatted.hex()==old['native_formatted_hex'] and lines==old['lines']
        rows.append({'id':n,'lines':lines,'native_formatted_hex':formatted.hex()})
    save(ROOT/'user676_677_preserved.json',{'cases':rows,'scope':'New research bytes and native formatter only;earlier V747 actual scene remains the gameplay reference.'})
    protected=read('work/analysis/tavern_recruitment_editorial_v771/research_checkpoint.json')['protected_files_unchanged']
    for name,digest in protected.items():assert sha(Path(name).read_bytes())==digest
    latest=read('out/editorial_review_latest.json');assert latest['profile']=='all-routes-unified-v770'
    save(ROOT/'research_checkpoint.json',{'source_ROM':latest,'protected_files_unchanged':protected,
        'owned_plan_sha256':sha((ROOT/'owned_runtime_plan.json').read_bytes()),
        'native_cold_warm_copies':7336,'scoped_cases':128644,'whole8MiB_status_cases':140,'quantity_cases':84,
        'complete_layouts':3423,'new_completed_records':0,'source_prose_records':258,'completed_records':230,
        'production_parser_registry_ROM_patch_and_gameplay_pending':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    p=Path('translations/editorial_review_current_v1.json');ledger=read(p)
    assert ledger['records_editorially_completed']==230 and ledger['records_with_source_and_prose_pass']==258
    record={'id':'V772-owned-recruitment-runtime-and-native-copies','documentation':'docs/recruitment_runtime_v772_research.md',
        'manuscript':str(MANUSCRIPT),'new_editorially_completed':0,'new_ROM':False,'paired_scope_cases':128644,
        'native_layouts':3423,'whole_native_copies':7336,'evidence':str(ROOT/'research_checkpoint.json')}
    ledger['research_checkpoints']=[r for r in ledger['research_checkpoints'] if r['id']!=record['id']]+[record]
    ledger['latest_checkpoint']='V772 proves owned no-growth recruitment runtime,exact seven-caller currency/day compaction,128644 scope cases,140 whole8MiB cases,3423 identical layouts and7336 full native copies.25 drafts await registered integration/patch and actual consumers/scenes. V770 remains latest;230 complete/258 source-prose. Wider editorial and graphics work stay open.'
    ledger['formatting_watchlist']['latest_research_reference_proof']=str(ROOT/'user676_677_preserved.json')
    save(p,ledger)
    text='''\n\n## V772 research: owned recruitment runtime and complete copies\n\nA consolidated private dispatcher and104-byte currency/day helper preserve exact source memberships and all seven real quantity callers.14 owned private allocations/four documented tails,128644 paired cases,84 quantity cases,140 whole8MiB contracts,3423 identical layouts/91 fonts and7336 complete native cold/warm copies pass. Existing blocks2-23 fit all25 paragraphs;3643 other strings and repaired676/677 stay exact. No pool/section/cache growth,new playable ROM or completion credit. Registered integration/exact patch,legitimate null-NPC consumers and actual scenes remain next. V770 stays latest;230 complete/258 source-prose. Wider shared/routes/prose and graphics audit remain open. See [V772 research](recruitment_runtime_v772_research.md).\n'''
    for name in('translation_progress.md','known_issues.md','todo.md'):
        q=Path('docs')/name;old=q.read_text(encoding='utf-8')
        if '## V772 research: owned recruitment runtime and complete copies' not in old:q.write_text(old.rstrip()+text,encoding='utf-8')
    archive=Path('E:/Rota Nova translations/Editorial review/V772 Owned recruitment runtime research')
    for source in ROOT.rglob('*'):
        if source.is_file():
            target=archive/'evidence'/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    extras=[p,MANUSCRIPT]+[Path('docs')/n for n in('translation_progress.md','known_issues.md','todo.md','recruitment_runtime_v772_research.md')]
    extras += sorted(Path('scripts').glob('*v772.py'))
    for source in extras:
        target=archive/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    files={str(q.relative_to(archive)):sha(q.read_bytes()) for q in archive.rglob('*') if q.is_file() and q.name!='archive_manifest.json'}
    save(archive/'archive_manifest.json',{'files':files,'new_ROM':False,'current_ROM':latest})
    assert all(sha((archive/name).read_bytes())==digest for name,digest in files.items())
    print(f'V772 owned-runtime checkpoint and{len(files)} exact archived files.230 completed unchanged;no new ROM.',flush=True)


if __name__=='__main__':main()
