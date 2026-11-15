"""Preserve the V4348 failed count check and derive a hash-chained amended audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_amended_audit_tools_v4350')
if __name__=='__main__':
    assert not ROOT.exists()
    gate="""    amendment_root=Path('work/analysis/lil_B171_timing_count_amendment_v4349')
    amended=read(amendment_root/'amendment_receipt.json')
    assert sha(lp.read_bytes())==amended['ledger_sha256']
    assert receipt['ledger_sha256']==amended['prior_ledger_sha256']
    assert sha(gzip.decompress((amendment_root/'ledger.before.json.gz').read_bytes()))==receipt['ledger_sha256']
    chain={str(Path(r['path'])):r for r in read(amendment_root/'mutation_plan.json')}
    for r in chain.values():
        assert sha(Path(r['before_copy']).read_bytes())==r['before_sha256']
        assert sha(Path(r['path']).read_bytes())==r['planned_sha256']
    for path,digest in amended['updated_files'].items():assert sha(Path(path).read_bytes())==digest
    for path,digest in amended['preserved_release_files'].items():assert sha(Path(path).read_bytes())==digest
    assert ledger['lil_B171_command_timing_count_amendment_v4349']==amended['amendment']
    assert amended['amendment']['timing_command_census']=={'0000':1,'4000':17,'4621':1,'61FF':1,'6325':1,'C200':1}
"""
    oldloop="""    for kind in ['evidence','preserved_release_files','updated_files']:
        for path,digest in receipt[kind].items():assert sha(Path(path).read_bytes())==digest,(kind,path)
"""
    newloop="""    for kind in ['evidence','preserved_release_files','updated_files']:
        for path,digest in receipt[kind].items():
            if kind=='updated_files' and str(Path(path)) in chain:
                assert chain[str(Path(path))]['before_sha256']==digest,(kind,path)
            else:
                assert sha(Path(path).read_bytes())==digest,(kind,path)
"""
    tool=derive('scripts/verify_editorial_handoff_v4348.py','scripts/verify_editorial_handoff_v4350.py',{
        'Independent audit of B171 reference/gameplay checkpoint and preserved main build.':'Independent audit of B171 approval and hash-chained timing-count amendment.',
        'editorial_handoff_verification_v4348':'editorial_handoff_verification_v4350',
        "    assert sha(lp.read_bytes())==receipt['ledger_sha256']\n":gate,
        "'lil_B171_reference_reconciliation_v4347','latest_checkpoint'}":"'lil_B171_reference_reconciliation_v4347','latest_checkpoint','lil_B171_command_timing_count_amendment_v4349'}",
        oldloop:newloop,
        "sum(r['source']['word']==0x4000 for r in repeat['cross_language_command_timing_differences'])==16":"sum(r['source']['word']==0x4000 for r in repeat['cross_language_command_timing_differences'])==17",
        "startswith('# Current editorial handoff - V4347')":"startswith('# Current editorial handoff - V4349')",
        "dict(checkpoint='V4347'":"dict(checkpoint='V4349',timing_count_amendment_hash_chain_verified=True",
        'Independent V4348 audit passes':'Independent V4350 amended audit passes',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,failed_predecessor_preserved=True,no_ROM_prose_orcredit_change=True,full_goal_complete=False))
    print('Prepared V4350 audit of V4347 approval and V4349 exact17/5 timing-count amendment.')
