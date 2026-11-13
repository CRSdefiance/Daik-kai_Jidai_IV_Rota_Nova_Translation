"""Finish the exact prepared ceramics registration after an interrupted ledger write."""

from gzip import decompress
from inspect import getsource
from pathlib import Path

from scripts import register_lil_ceramics_wrap_20261111 as release_driver
from scripts.source_locked_derivation_v5118 import checked_text


def append_verified_prefix(path, target):
    prefix = path.read_bytes()
    assert prefix and len(prefix) < len(target) and target.startswith(prefix)
    with path.open('ab') as stream:
        for start in range(len(prefix), len(target), 1024 * 1024):
            stream.write(target[start:start+1024*1024])
    assert release_driver.base.digest(path) == release_driver.stage.sha(target)


def main():
    d = release_driver
    base = d.base
    assert not d.DOC.exists() and not (d.VERIFICATION / 'registration_mutation_plan.json').exists()
    old, _, live, _, _ = d.verify_inputs()
    release = base.load(d.RELEASE)
    sha = base.digest(d.ROM)
    assert sha == release['candidate_sha256'] == live['candidate_sha256']
    assert d.ROM.read_bytes() == d.replay.ROM.read_bytes()
    assert base.digest(d.PATCH) == release['patch_sha256']
    assert base.digest(d.MANIFEST) == release['manifest_sha256']
    assert base.load(d.MANIFEST)['lil_ceramics_registered_successor_pipeline']['driver_sha256'] == base.digest(d.__file__)
    assert d.MANIFEST.read_bytes() == decompress((d.PACKAGE / 'build_manifest.json.gz').read_bytes())
    registry_pending = base.REGISTRY.with_name('release_stack.lil_ceramics.pending.json')
    ledger_pending = base.LEDGER.with_name('editorial_review_current.lil_ceramics.pending.json')
    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    assert base.digest(base.REGISTRY) == old['registry_sha256']
    assert before_registry == (d.ROOT / 'release_stack_before_lil_ceramics.json').read_bytes()
    assert before_ledger == decompress((d.ROOT / 'editorial_ledger_before.json.gz').read_bytes())
    assert base.digest(registry_pending) == release['registry_sha256']
    assert registry_pending.read_bytes() == decompress((d.PACKAGE / 'build_release_stack.json.gz').read_bytes())
    ledger = base.load(base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['predecessor']['candidate_sha256']
    assert ledger['records_editorially_completed'] == 27697
    main_sha = base.digest(base.PROMOTED)
    source = getsource(d.main)
    tail = source[source.index("    ledger['current_integrated_candidate'].update"):]
    tail = checked_text('def finish():\n' + tail, {
        '    write_pending(ledger_pending, encode_ledger(ledger))':
            '    append_verified_prefix(ledger_pending, encode_ledger(ledger))',
    })
    scope = vars(d) | dict(ledger=ledger, release=release, sha=sha, main_sha=main_sha,
        before_registry=before_registry, before_ledger=before_ledger,
        registry_pending=registry_pending, ledger_pending=ledger_pending, append_verified_prefix=append_verified_prefix)
    exec(compile(tail, str(Path(__file__)) + '::exact-registration-tail', 'exec'), scope)
    scope['finish']()


if __name__ == '__main__':
    main()
