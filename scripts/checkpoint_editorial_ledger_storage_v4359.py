"""Preserve every ledger value while reducing indentation below the existing size gate."""
import gzip
import json
import os
from pathlib import Path
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/editorial_ledger_storage_v4359')
AUDIT=Path('work/analysis/editorial_handoff_verification_v4358c/verified_handoff.json')
LP=Path('translations/editorial_review_current_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    before=LP.read_bytes();ledger=json.loads(before);audit=read(AUDIT)
    assert sha(before)==audit['ledger_sha256'] and audit['checkpoint']=='V4357'
    assert (audit['integrated'],audit['pending'],audit['source_prose'])==(5762,0,5765)
    assert len(before)>100*1024*1024
    assert 'current_ledger_storage_v4359' not in ledger
    stable_paths=[Path('translations/release_stack.json'),Path('translations/promoted_build.json'),Path('scripts/build_integrated_release.py'),
        Path('out/all_routes_combined_v4353_candidate.nds'),Path('out/all_routes_combined_v4353_candidate.xdelta'),
        Path('out/raphael_natural_v2_accepted_base.nds'),Path('work/clean.nds'),Path('translations/lil_B171_contextual_final_review_v1.json')]
    stable={str(p):sha(p.read_bytes()) for p in stable_paths}
    record=dict(format='one-space-indent-crlf-v1',encoder='scripts/editorial_ledger_storage_v1.py',
        encoder_sha256=sha(Path('scripts/editorial_ledger_storage_v1.py').read_bytes()),
        before_bytes=len(before),before_sha256=sha(before),before_exact_copy=str(ROOT/'ledger.before.json.gz'),
        before_copy_encoding='gzip; decompress to recover every original byte',
        prior_verified_handoff=str(AUDIT),prior_verified_handoff_sha256=sha(AUDIT.read_bytes()),
        reason='Current complete ledger exceeded the existing100MiB promotion handoff size gate. Reduce indentation only; preserve all prior fields,records,translations,references,provenance and counts.',
        all_prior_JSON_values_preserved=True,no_source_prose_or_completion_credit_added=True,no_ROM_or_translation_wording_change=True,
        full_goal_complete=False)
    ledger['current_ledger_storage_v4359']=record
    after=encode_ledger(ledger)
    assert len(after)<100*1024*1024 and len(after)<len(before)
    assert {k:v for k,v in json.loads(after).items() if k!='current_ledger_storage_v4359'}==json.loads(before)
    ROOT.mkdir(parents=True)
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    note=('V4359 preserves every existing ledger value and the exact pre-formatting bytes while changing current-ledger JSON from two-space to one-space indentation,with CRLF preserved. The complete105030011-byte ledger had exceeded the existing100MiB promotion handoff gate;no historical field,translation,reference,proof,retention or coverage record is removed. Use scripts/editorial_ledger_storage_v1.py encode_ledger for future current-ledger writes. Original bytes remain in work/analysis/editorial_ledger_storage_v4359/ledger.before.json.gz.\n\n'
        'B171 remains independently complete in experimental V4353:37 reviews,24 revisions/13 justified retentions,547 manuscript batches/114 accepted layers,exact clean-input patch and fresh startup checks. Coverage stays5762 completed,5765 source/prose andzero pending. Promoted main V4303,all source/canonical inputs and every ROM/translation/proof remain preserved. No new emulator run or editorial/completion credit. The failed audit preparer and the first audit\'s stale predecessor block literal remain preserved;the corrected V4358c audit passes all171 references.\n\n'
        'Next: Continue clean-first whole-exchange review through B172-B180 (161 physical speeches,zero typed-choice leads) and every wider storyline,shared town/shop exchange,random scene,Help and other player-facing prose family. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell middle-field lead and B157 provenance amendment. Graphics/all18 plaques and the later older-record technical re-audit/queued0D gap remain separate and open. Full editorial goal active.')
    planned={LP:after}
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;first,rest=path.read_text(encoding='utf-8').split('\n',1)
        if name=='editorial_handoff_current.md':first='# Current editorial handoff - V4359'
        planned[path]=(first+'\n\n## V4359: Complete ledger retained with reduced indentation\n\n'+note+'\n\n'+rest).encode('utf-8')
    protocol=Path('docs/build_continuity_protocol.md')
    planned[protocol]=(protocol.read_text(encoding='utf-8')+'\n\n## Current editorial ledger storage after V4359\n\nWrite `translations/editorial_review_current_v1.json` with `scripts.editorial_ledger_storage_v1.encode_ledger`: one-space JSON indentation, UTF-8 and CRLF. This preserves the complete JSON object and all prior translation/provenance values while staying below the existing promotion file-size gate. Keep historical producers and byte-locked receipts unchanged; retain exact prior-byte snapshots. New current-ledger checkpoints and completions must use this encoder instead of restoring two-space indentation. Stage and validate before/planned hashes for every target before writing, and independently verify that prior records and counters are preserved. Other JSON formats retain their existing serialization.\n').encode('utf-8')
    stage=ROOT/'staged';stage.mkdir();mutations=[]
    for i,(path,data) in enumerate(planned.items()):
        original=path.read_bytes();backup=ROOT/f'{i}.before';backup.write_bytes(original)
        target=stage/f'{i}.planned';target.write_bytes(data)
        mutations.append(dict(path=str(path),before_copy=str(backup),before_sha256=sha(original),planned=str(target),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',mutations)
    for row in mutations:
        assert Path(row['path']).resolve().is_relative_to(Path.cwd().resolve())
        assert sha(Path(row['path']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
    for row in mutations:
        data=Path(row['planned']).read_bytes()
        with Path(row['path']).open('r+b') as f:
            f.write(data)
            f.truncate(len(data));f.flush();os.fsync(f.fileno())
        assert sha(Path(row['path']).read_bytes())==row['planned_sha256']
    assert all(sha(Path(p).read_bytes())==digest for p,digest in stable.items())
    save(ROOT/'storage_receipt.json',dict(checkpoint='V4359',ledger_sha256=sha(after),before_ledger_sha256=sha(before),
        before_bytes=len(before),after_bytes=len(after),bytes_saved=len(before)-len(after),all_prior_JSON_values_preserved=True,
        prior_verified_handoff=str(AUDIT),prior_verified_handoff_sha256=sha(AUDIT.read_bytes()),
        updated_files={r['path']:r['planned_sha256'] for r in mutations},preserved_files=stable,
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,full_goal_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(before_bytes=len(before),after_bytes=len(after),all_prior_JSON_values_preserved=True,completed=5762,pending=0,main='V4303'))
