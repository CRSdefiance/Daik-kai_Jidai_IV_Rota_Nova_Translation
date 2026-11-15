"""Exercise actual changed semantic inputs with production digest layer alone bypassed;zero commits permitted."""
from copy import deepcopy
from pathlib import Path
import json
from dk4tool.rom.nds import NdsImage
from dk4tool.patch import hodram_B51_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B51_release_paths_v8595 import PARENT,ROM,DOC,NAMES,SEAL,CONFIG,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B51_atomic_challenges_v8605b')

def digest(value):return sha(json.dumps(value,sort_keys=True,ensure_ascii=False).encode('utf8'))
def setpath(value,path,new):
    for part in path[:-1]:value=value[part]
    value[path[-1]]=new

if __name__=='__main__':
    assert not ROOT.exists();conf=read(CONFIG);template=NdsImage.open(PARENT);baseline=NdsImage.open(owned.CANONICAL);paths=proofs()
    watched={Path(p) for p in conf['dependencies']}|{CONFIG,PARENT,ROM,DOC,NAMES,SEAL,Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json')}
    hashes={str(p):sha(p.read_bytes()) for p in watched};cases=[]
    specs=[
        ('config-format',CONFIG,['format'],'unapproved-release','exact complete source-qualified configuration'),
        ('config-parent',CONFIG,['parent_ROM_sha256'],'0'*64,'whole in-memory predecessor/reference identities'),
        ('config-prior-profile',CONFIG,['required_registered_stack_dependency','predecessor_profile'],'incomplete-route','explicit registered V8543/Adernkatz/B49/B50 dependency'),
        ('doc-context',DOC,['records',0,'context'],read(DOC)['records'][0]['context']+' Invented relationship.','Exact Hodram-B51 approved prose/source/context'),
        ('doc-English',DOC,['records',0,'english'],read(DOC)['records'][0]['english']+' Unapproved words.','Exact Hodram-B51 approved prose/source/context'),
        ('doc-source-bytes',DOC,['records',0,'source_hex'],'01'+read(DOC)['records'][0]['source_hex'][2:],'Exact Hodram-B51 approved prose/source/context'),
        ('doc-final-reference',DOC,['records',0,'final_reference','offset'],19,'Exact Hodram-B51 approved prose/source/context'),
        ('sealed-record-order',SEAL,['records'],list(reversed(read(SEAL)['records'])),'five sealed exact source/current/final references'),
        ('current-block-bytes',Path(paths['current']),['groups',0,'current_block_hex'],'00'+read(paths['current'])['groups'][0]['current_block_hex'][2:],'complete literal source/current blocks'),
        ('relocation-source-hash',Path(paths['relocation']),['groups',0,'source_block_sha256'],'0'*64,'complete source/current block'),
        ('wrong-query-value',Path(paths['stored']),['stored_queries',0,'native_result',1],1,'complete relocated query ABI/scratch/input/return records'),
        ('discarded-sixth-query-word',Path(paths['stored']),['stored_queries',1,'native_result',5],1,'complete relocated query ABI/scratch/input/return records'),
        ('wrong-normal-value-carry',Path(paths['stored']),['normal_seeded_ends',1,'native_result',1],0,'twenty-five complete normal result/value carries and all six return fields'),
        ('lost-complete-body-name-hold',Path(paths['actual']),['groups',0,'speeches',0,'complete_holds'],read(paths['actual'])['groups'][0]['speeches'][0]['complete_holds'][:-1],'every independently reconstructed actual trace/hold/header/return/following-command field'),
        ('false-Charles-visit',Path(paths['actual']),['groups',1,'unvisited_conditional_text_IDs'],[],'exact observed andexplicitly unvisited source memberships'),
        ('comparison-final-RNG',Path(paths['comparison']),['groups',0,'final_PRNG_seeds'],[0,0],'exact raw RNG/calendar scope'),
        ('sealed-scope',SEAL,['observed_scope','all_measured_timing_PRNG_RGB_andcalendar_limits_retained'],False,'all measured actual fixture/timing/RNG/component/calendar/RGB limits'),
    ]
    previous=Path('work/analysis/Hodram_B51_atomic_challenges_v8605')
    assert len(list(previous.glob('case*.json')))==10
    for index,(label,path,key,new,expected) in enumerate(specs[:10]):
        row=read(previous/f'case{index:02d}.json');prior=read(path);changed=deepcopy(prior);setpath(changed,key,new)
        assert row['case']==label and row['original_value_sha256']==digest(prior) and row['changed_value_sha256']==digest(changed)
        assert row['rejected'] and row['actual_changed_input'] and row['commit_calls']==0 and row['original_object_files_components_andserialized_bytes_unchanged']
        assert row['expected_guard']==expected and expected in row['error']
        cases.append(row)
    ROOT.mkdir(parents=True);original_load,dependencies,commit=owned.load,owned.check_dependencies,owned.commit_image
    try:
        for index,(label,path,key,new,expected) in enumerate(specs[10:],start=10):
            prior=read(path);changed=deepcopy(prior);setpath(changed,key,new);assert changed!=prior and digest(changed)!=digest(prior),label
            image=NdsImage(owned.CANONICAL,deepcopy(template.rom));original=image.rom;before=bytes(original.save());files=list(original.files);components={p:v for p,v in image.iter_components()};calls=[]
            def intercepted(requested):return deepcopy(changed) if Path(requested).resolve()==path.resolve() else original_load(requested)
            def forbidden(*args):calls.append('forbidden');raise AssertionError('Semantic rejection reached commit:'+label)
            owned.load=intercepted;owned.check_dependencies=lambda unused:None;owned.commit_image=forbidden
            try:owned.apply_release(image,baseline)
            except ValueError as exc:
                message=str(exc);assert expected in message,(label,expected,message)
                assert 'Native dependency changed' not in message and 'Frozen Hodram-B51 contract changed' not in message
            else:raise AssertionError('Changed semantic evidence accepted:'+label)
            finally:owned.load=original_load;owned.check_dependencies=dependencies;owned.commit_image=commit
            assert not calls and image.rom is original and bytes(original.save())==before and original.files==files and {p:v for p,v in image.iter_components()}==components
            result=dict(case=label,changed_evidence_path=str(path),original_value_sha256=digest(prior),changed_value_sha256=digest(changed),actual_changed_input=True,rejected=True,error=message,expected_guard=expected,commit_calls=0,original_object_files_components_andserialized_bytes_unchanged=True,only_production_dependency_digest_layer_bypassed_all_frozen_native_source_andsemantic_guards_active=True)
            save(ROOT/f'case{index:02d}.json',result);cases.append(result);print('PASS',index+1,label,flush=True)
        assert hashes=={str(p):sha(p.read_bytes()) for p in watched}
        save(ROOT/'semantic_rejections.json',dict(cases=cases,negative_count=len(cases),all_changed_inputs_distinct_andexpected_semantic_guards_match=True, prior_ten_cases_reused_after_exact_original_changed_input_andguard_revalidation=True, prior_case_root=str(previous),zero_commits_andwhole_input_unchanged_forall_failures=True,all_protected_files_ROMs_registry_ledger_pins_andmodules_hash_exact=True,no_frozen_native_orsemantic_guard_bypassed=True,only_production_digest_layer_bypassed_to_reach_semantics=True,no_emulator_replay_ROM_registration_promotion_orcredit=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    finally:owned.load=original_load;owned.check_dependencies=dependencies;owned.commit_image=commit
    print('All17 changing semantic precommit challenges rejected at expectedguards;zero commits/whole input exact.No emulator replay orcredit.')
