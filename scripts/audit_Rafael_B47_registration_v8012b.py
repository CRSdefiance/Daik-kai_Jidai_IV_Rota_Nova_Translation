"""Preserve the executed registration receipt and supersede only its stale diagnostic counts."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
REG=Path('work/analysis/Rafael_B47_registration_v8012')
OLD=REG/'registration_receipt.json'
OUT=REG/'registration_receipt_corrected.json'
VALIDATION=Path('work/analysis/Rafael_B47_atomic_challenges_v8011/atomic_validation_receipt.json')
if __name__=='__main__':
    assert not OUT.exists()
    before=OLD.read_bytes();old=read(OLD);v=read(VALIDATION)
    assert old['profile']=='all-routes-unified-v8013' and old['parent_profile']=='all-routes-unified-v7964'
    assert old['negative_count']==187 and old['expected_manifest_batches']==635
    assert v['negative_count']==len(read(v['negative_cases']))==202 and v['positive_records']==15
    parent_manifest=Path(old['parent_ROM']).with_suffix('.manifest.json')
    assert len(read(parent_manifest)['batches'])==635 and len(old['manuscripts'])==1
    assert sha(Path('translations/release_stack.json').read_bytes())==old['registry_after_sha256']
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==old['builder_after_sha256']
    fixed=deepcopy(old);fixed.update(negative_count=202,expected_manifest_batches=636,
        supersedes_receipt=str(OLD),supersedes_receipt_sha256=sha(before),
        correction_only_fields=['negative_count','expected_manifest_batches'],
        source_bound_atomic_validation=str(VALIDATION),source_bound_atomic_validation_sha256=sha(VALIDATION.read_bytes()),
        original_registration_assertions_checked202_andcomplete635_parent_manifest=True,
        original_stdout_stale_V7964_two_manifests26objects_superseded=True,
        correct_registration_description='Experimental V8013 after V7964;636 expected batches/114 accepted;one new manifest/15objects;202 independent guard rejections.',
        no_registration_replay_builder_registry_ROM_policy_orcredit_change=True,
        correction_producer_sha256=sha(Path(__file__).read_bytes()))
    probe=deepcopy(fixed);probe['negative_count']=187;probe['expected_manifest_batches']=635
    for key in fixed.keys()-old.keys():probe.pop(key)
    assert probe==old
    save(OUT,fixed);assert OLD.read_bytes()==before
    print('Corrected registration metadata:V8013,636 expected batches,one15-record manifest,202 guard rejections. Original receipt/producer/stdout preserved;no replay orregistry/ROM change.')
