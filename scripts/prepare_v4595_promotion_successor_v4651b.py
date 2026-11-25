"""Preserve failed staging and normalize the Windows manuscript path comparison."""
from pathlib import Path
import hashlib
import json

source = Path('scripts/promote_v4595_checkpoint_v4651.py')
target = Path('scripts/promote_v4595_checkpoint_v4651b.py')
assert not target.exists()
text = source.read_text(encoding='utf-8')
changes = {
    "AUDIT = ROOT / 'work/analysis/promotion_v4651'": "AUDIT = ROOT / 'work/analysis/promotion_v4651b'",
    "assert fresh['pending_contextual_families'][0]['manuscript'] == 'translations/lil_B177_editorial_manuscript_v6.json'":
        "assert Path(fresh['pending_contextual_families'][0]['manuscript']) == Path('translations/lil_B177_editorial_manuscript_v6.json')",
    "assert pins[:-1] == oldpins": "assert pins[:-2] == oldpins\n    assert Path(pins[-2]['path']).read_bytes() == ROM.read_bytes()",
    "assert Path.cwd() == ROOT and not AUDIT.exists() and not PACKAGE.exists()":
        """assert Path.cwd() == ROOT and not AUDIT.exists() and PACKAGE.exists()
    expected = {'build_manifest.json.gz','build_release_stack.json.gz','promotion.json',
        'release_manifest.json','translation.xdelta','verification/current_Lil_startup_and_town_review.png',
        'verification/promotion_reconstruction.json','verification/promotion_test_results.json',
        'verification/UNINTEGRATED_B177_status.json'} | {'verification/'+name for name in EVIDENCE}
    assert {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob('*') if p.is_file()} == expected
    partial_hashes = {name:sha((PACKAGE/name).read_bytes()) for name in expected}
    failed_reconstruction = ROOT/'work/analysis/promotion_v4651/promoted_patch_reconstruction_RESEARCH_ONLY.nds'
    assert failed_reconstruction.read_bytes() == ROM.read_bytes()
    assert sha((ROOT/'translations/editorial_review_current_v1.json').read_bytes()) == read(ROOT/'work/analysis/lil_B177_reference_checkpoint_v4641/checkpoint_receipt.json')['ledger_sha256']""",
    "verification.mkdir(parents=True)": "verification.mkdir(parents=True,exist_ok=True)",
    "pins = oldpins+[{'path':str(reconstruction.resolve())":
        "pins = oldpins+[{'path':str(failed_reconstruction.resolve()),'reason':'Preserve initial V4651 byte-exact reconstruction; metadata staging stopped at Windows path separator assertion before current metadata mutation. SHA-256 '+ROM_SHA}, {'path':str(reconstruction.resolve())",
    "print('Staged V4651 promotion;12 metadata files,byte-exact clean-input reconstruction,no editorial credit added.')":
        """assert all(sha((PACKAGE/name).read_bytes()) == digest for name,digest in partial_hashes.items())
    save(AUDIT/'source_derivation.json',{'predecessor':str(ROOT/'scripts/promote_v4595_checkpoint_v4651.py'),
        'predecessor_sha256':sha((ROOT/'scripts/promote_v4595_checkpoint_v4651.py').read_bytes()),
        'failure':'Windows manuscript path uses backslashes; raw string comparison rejected identical native path before any current metadata write.',
        'correction':'Compare pathlib.Path values; preserve failed producer/reconstruction and exact partial package. Pin both reconstructions.',
        'partial_package_preserved':partial_hashes})
    print('Staged V4651 promotion;12 metadata files,byte-exact clean-input reconstruction,no editorial credit added.')""",
}
for old,new in changes.items():
    assert text.count(old) == 1, old
    text = text.replace(old,new)
compile(text,str(target),'exec')
target.write_text(text,encoding='utf-8',newline='\n')
print(json.dumps({'successor':str(target),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'replacements':len(changes),'no_current_metadata_modified':True}))
