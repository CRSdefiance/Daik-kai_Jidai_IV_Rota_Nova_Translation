"""Bind the current catalog and confirm every changed speech keeps its original native extent."""

from pathlib import Path

from scripts import prove_lil_shrines_temples_controls_v3168c as catalog
from scripts import replay_historical_story_wraps_20261111 as replay
from scripts import stage_historical_story_wraps_20261111 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
HISTORICAL = Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')


def main():
    assert not PROOF.exists()
    draft, stored, fixture = map(base.load,(stage.REVIEW,stage.PROOF,replay.SETUP))
    assert base.digest(stage.REVIEW)==stored['review_sha256'] and base.digest(stage.PROOF)==fixture['proof_sha256']
    assert base.digest(stage.parent.ROM)==fixture['parent_sha256'] and base.digest(replay.ROM)==fixture['candidate_sha256']
    parent, target = map(base.NdsImage.open,(stage.parent.ROM,replay.ROM))
    arm = parent.read_file(stage.ARM)
    assert arm==target.read_file(stage.ARM)
    adapter = base.load(HISTORICAL)['source_owned_dispatch_adapters']['bind_current_catalog']
    adapter = checked_text(adapter,{
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':stage.sha(arm),
        "read(Path(image.path).with_suffix('.manifest.json')) if hasattr(image,'path') else read(Path(read(SOURCE)['current_ROM']).with_suffix('.manifest.json'))":
            'read(MANIFEST)',
        "read(SOURCE)['current_ROM'].replace('.nds','.manifest.json')": 'str(MANIFEST)',
    })
    contexts, matches = [], []
    inventory,_,_ = stage.scoped_inventory()
    for path in stored['archives']:
        route = int(path.split('SC')[1][0]); env=vars(catalog)|dict(MANIFEST=stage.parent.MANIFEST,route=route,route_mask=1<<route)
        exec(compile(adapter,__file__+'::current-route-catalogue', 'exec'),env)
        lookup, receipt=env['bind_current_catalog'](parent)
        del receipt['records']
        contexts.append(receipt)
        old,new=[stage.IlnkContainer.parse(image.read_file(path)).blocks for image in (parent,target)]
        for _,block in (key for key in stored['blocks'] if key[0]==path):
            commands,bodies=[stage.raw_speeches(arm,blocks[block],inventory) for blocks in (old,new)]
            old_cmd,old_rows=commands; new_cmd,new_rows=bodies
            assert len(old_rows)==len(new_rows) and len(old_cmd)==len(new_cmd)
            selected={r['current_reference']['offset']:r for r in draft['records'] if r['file_path']==path and r['block']==block}
            for a,b in zip(old_cmd,new_cmd,strict=True):
                assert all(a[field]==b[field] for field in ('offset','native_extent','word','ancestor_0100_offsets'))
                if a['offset']+5 not in selected:
                    # A composite command may contain nested speech. Only those already verified body ranges may differ.
                    old_command=bytearray.fromhex(a['whole_command_hex']); new_command=bytes.fromhex(b['whole_command_hex'])
                    for at,row in selected.items():
                        relative=at-a['offset']
                        replacement=bytes.fromhex(row['target_hex'])
                        if relative>=0 and relative+len(replacement)<=len(old_command):
                            old_command[relative:relative+len(replacement)]=replacement
                    assert bytes(old_command)==new_command
            for a,b in zip(old_rows,new_rows,strict=True):
                if a['offset'] not in selected:
                    assert a==b
                    continue
                row=selected[a['offset']]
                assert a['raw_hex']==row['current_hex'] and b['raw_hex']==row['target_hex']
                assert all(a[key]==b[key] for key in a if key!='raw_hex')
                assert all(bytes.fromhex(r['raw_hex'])[1:] not in lookup for r in (a,b))
                matches.append(dict(id=row['id'],file_path=path,block=block,same_extent=a['native_extent'],
                    selector=a['selector'],no_original_or_target_catalogue_override=True))
    assert len(matches)==12
    base.save(PROOF,dict(candidate_sha256=fixture['candidate_sha256'],parent_sha256=fixture['parent_sha256'],
        owned_records=matches,catalogue_routes=contexts,all_command_extents_offsets_branches_and_preambles_exact=True,
        original_catalogue_helper_route_masks_and_entries_verified=True,dependencies={str(p):base.digest(p)
            for p in (HISTORICAL,stage.REVIEW,stage.PROOF,stage.parent.MANIFEST,Path(__file__))}))
    print('12 unchanged native boundaries and before/after catalog misses on all four routes verified.')


if __name__=='__main__':
    main()
