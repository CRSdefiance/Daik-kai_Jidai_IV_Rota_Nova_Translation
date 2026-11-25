"""Restore only exact historical test inputs; never substitute current ROM bytes."""

from pathlib import Path
import json
import shutil

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta

ROOT = Path('work/patch_interaction_audit_20261027')


def main():
    inventory = json.loads((ROOT/'legacy_fixture_recovery_inventory.json').read_text())
    clean = Path('work/clean.nds')
    clean_hash = sha(clean.read_bytes())
    # Same original-source lock as scripts/prune_generated_roms.ps1. The
    # emulator harness's DEFAULT_ROM hash belongs to V189, not clean Japanese.
    assert clean_hash == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    stage = ROOT/'reconstructed_historical_inputs'
    stage.mkdir(exist_ok=False)
    results = []
    for row in inventory['inputs']:
        target = Path(row['ROM'])
        assert not target.exists(), target
        patch, manifest_path = target.with_suffix('.xdelta'), target.with_suffix('.manifest.json')
        if not patch.exists() or not manifest_path.exists():
            results.append(dict(ROM=str(target),status='no_adjacent_exact_patch_or_manifest'))
            continue
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        expected = manifest['candidate_sha256']
        restored = stage/target.name
        apply_xdelta(clean,patch,restored)
        actual = sha(restored.read_bytes())
        assert actual == expected, (target,actual,expected)
        assert target.resolve().parent == Path('out').resolve()
        assert not target.exists()
        shutil.copyfile(restored,target)
        assert sha(target.read_bytes()) == expected
        results.append(dict(ROM=str(target),status='restored_exact_historical_input',sha256=actual,
            patch=str(patch),patch_sha256=sha(patch.read_bytes()),
            manifest=str(manifest_path),manifest_sha256=sha(manifest_path.read_bytes()),
            decoded_copy=str(restored),research_only_not_current_playable_candidate=True))
        (ROOT/'legacy_fixture_recovery_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print('Restored exact fixture',target,flush=True)
    assert sha(clean.read_bytes()) == clean_hash
    (ROOT/'legacy_fixture_recovery_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print('Restored',sum(r['status']=='restored_exact_historical_input' for r in results),'of',len(results),'historical inputs.',flush=True)


if __name__ == '__main__':
    main()
