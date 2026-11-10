"""Close seven measured document-identity gaps; preserve every original positive/negative result."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_production_tools_v7714b')
if __name__=='__main__':
    assert not ROOT.exists();report=read('work/analysis/maria_B207_atomic_challenges_v7715/challenge_report.json')
    expected=['wrong-document-file','wrong-document-route','wrong-document-current-ROM','wrong-document-current-ROM-hash','wrong-document-ARM9-hash','wrong-document-COMMON-hash','wrong-document-clean-hash']
    assert report['planned_cases']==163 and report['guard_rejections']==156 and [r['case'] for r in report['gaps']]==expected and all(r['error_type']=='CommitAttempt' and r['not_counted_as_guard_rejection'] for r in report['gaps'])
    key="require(doc['translation_policy']=='natural-dialogue-v2'"
    added="""require(doc['file_path']==file and doc['route_identity']=='Maria','document file/route identity')
        require(Path(doc['current_ROM']).resolve()==Path(packet['current_ROM']).resolve()==Path(mapping['source_ROM']).resolve() and doc['current_ROM_sha256']==packet['current_ROM_sha256']==mapping['source_ROM_sha256'],'document current ROM identity')
        require(doc['current_ARM9_sha256']==packet['current_ARM9_sha256']==conf['required_runtime_arm9_sha256'] and doc['current_COMMON_sha256']==packet['current_COMMON_sha256']==conf['required_runtime_common_sha256'],'document runtime identity')
        require(Path(doc['source_ROM']).resolve()==Path(conf['clean_ROM']).resolve() and doc['source_ROM_sha256']==conf['clean_ROM_sha256']==mapping['clean_ROM_sha256'],'document clean source identity')
        """
    production=derive('dk4tool/patch/maria_B207_editorial_v1.py','dk4tool/patch/maria_B207_editorial_v2.py',{key:added+key})
    positive=derive('scripts/validate_Maria_B207_atomic_v7714.py','scripts/validate_Maria_B207_atomic_v7714b.py',{
        'maria_B207_editorial_v1':'maria_B207_editorial_v2',
        'maria_B207_atomic_v7714':'maria_B207_atomic_v7714b',
        "Path(owned.__file__),":"Path(owned.__file__),Path('work/analysis/maria_B207_guard_provenance_v7714/identical_shared_fields_AST_andmeasured_seed_rebinding.json'),Path('work/analysis/maria_B207_production_tools_v7714b/closed_measured_document_identity_gaps.json'),",
    })
    negative=derive('scripts/challenge_Maria_B207_atomic_v7715.py','scripts/challenge_Maria_B207_atomic_v7715b.py',{
        'maria_B207_editorial_v1':'maria_B207_editorial_v2',
        'maria_B207_atomic_v7714':'maria_B207_atomic_v7714b',
        'maria_B207_atomic_challenges_v7715':'maria_B207_atomic_challenges_v7715b',
    })
    ROOT.mkdir(parents=True);save(ROOT/'closed_measured_document_identity_gaps.json',dict(production=production,positive=positive,negative=negative,measured_original_report='work/analysis/maria_B207_atomic_challenges_v7715/challenge_report.json',seven_original_commit_traps_preserved_not_counted_as_rejections=True,all_original_physical_inputs_unchanged=True,no_native_high_constant_changes=True,new_credit=0,full_goal_complete=False))
