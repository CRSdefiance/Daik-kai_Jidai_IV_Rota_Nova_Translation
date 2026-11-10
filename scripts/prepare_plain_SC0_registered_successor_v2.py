"""Preflight every dependency and reuse complete reference images from a pre-registration failure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL = Path('scripts/prepare_plain_SC0_registered_successor_v1.py')
source = ORIGINAL.read_text(encoding='utf-8')
start = source.index('    targets = []\n')
end = source.index('    final_research = Path', start)
old_generation = source[start:end]
start = source.index('    stage_proofs = []\n')
end = source.index('    profile = deepcopy(oldprofile)', start)
old_stage_collection = source[start:end]
source = checked_text(source, {
    "    parser.add_argument('--out',type=Path,required=True)":
        "    parser.add_argument('--out',type=Path,required=True)\n    parser.add_argument('--reference-reuse',type=Path,required=True)",
    "    spec = load(args.spec)":
        """    spec = load(args.spec)
    assert all(Path(p).is_file() for p in [*spec['dependencies'],*spec['evidence'].values()])
    reuse = load(args.reference_reuse)
    assert reuse['producer_sha256'] == sha(ORIGINAL.read_bytes())
    assert reuse['source_reference_generation_andall_eight_inverses_completed_before_failure']
    assert reuse['no_registry_orstage_config_orcompletion_credit_mutation']""",
    old_generation:
        """    assert reuse['registry_sha256'] == sha(before) and reuse['target_archive_sha256'] == rebuilt['target_archive_sha256']
    assert len(reuse['references']) == 8
    targets=[]
    for i,reference in enumerate(reuse['references']):
        path=Path(reference['path'])
        assert sha(path.read_bytes()) == reference['sha256']
        assert Path(reference['predecessor_path']) == oldstates[i]
        assert sha(oldstates[i].read_bytes()) == reference['predecessor_sha256']
        targets.append(path)
    save(args.out/'exact_reference_reuse.json',dict(original_failure=str(args.reference_reuse),original_failure_sha256=sha(args.reference_reuse.read_bytes()),
        all_eight_original_reference_bytes_andpredecessor_bytes_exact=True,
        reference_generation_andfull_inverse_proofs_reused_not_reexecuted=True,new_credit=0))
""",
    "{args.spec,Path(__file__),modulepath}": "{args.spec,args.reference_reuse,ORIGINAL,Path(__file__),modulepath}",
    old_stage_collection:
        """    stage_proofs=[]
    for i,(old,new) in enumerate(zip(oldstates,targets,strict=True)):
        a,b=NdsImage.open(old),NdsImage.open(new)
        assert all(b.read_file(p)==v for p,v in a.iter_components())
        for unchanged in ['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/COMMON/HELP.DK4']:
            assert a.read_file(unchanged)==b.read_file(unchanged)
        assert b.read_file(doc['file_path'])==resource
        stage_proofs.append(dict(stage=i,old_state=identity(old),new_state=identity(new),
            ARM9_COMMON_font_andall_final_stage_inputs_except_owned_SC0_exact=True,
            prior_full_unowned_file_andserialized_inverse_proof_qualified_by_exact_whole_ROM_identity=True,
            exact_reference_reuse_receipt=str(args.out/'exact_reference_reuse.json')))
        del a,b
        gc.collect()
""",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-prepublication-planner-reuse-completed-eight-inverses-preflight-dependencies', 'exec'), globals())
