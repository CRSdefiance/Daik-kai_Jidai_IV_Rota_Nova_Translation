"""Finish the prepared Gallery registration after its interrupted ledger write."""

from gzip import decompress
from hashlib import sha256

from scripts import register_visible_gallery_captions_v1 as gallery
from scripts.editorial_ledger_storage_v1 import encode_ledger


def main():
    base = gallery.base
    assert not gallery.MUTATION_PLAN.exists() and not gallery.DOC.exists()
    assert gallery.LEDGER_PENDING.stat().st_size == 0
    release = base.load(gallery.RELEASE)
    predecessor = release['predecessor']
    assert release['profile'] == gallery.PROFILE
    assert base.digest(base.REGISTRY) == predecessor['registry_sha256']
    assert base.REGISTRY.read_bytes() == (gallery.TEST / 'release_stack_before_visible_gallery_captions.json').read_bytes()
    assert gallery.REGISTRY_PENDING.read_bytes() == decompress((gallery.PACKAGE / 'build_release_stack.json.gz').read_bytes())
    assert gallery.MANIFEST.read_bytes() == decompress((gallery.PACKAGE / 'build_manifest.json.gz').read_bytes())
    for path, field in ((gallery.ROM, 'candidate_sha256'), (gallery.MANIFEST, 'manifest_sha256'),
                        (gallery.PATCH, 'patch_sha256'), (gallery.REGISTRY_PENDING, 'registry_sha256')):
        assert base.digest(path) == release[field]

    before = base.LEDGER.read_bytes()
    assert before == decompress((gallery.TEST / 'editorial_ledger_before.json.gz').read_bytes())
    ledger = base.load(base.LEDGER)
    assert ledger['records_editorially_completed'] == 27696
    assert ledger['current_integrated_candidate']['sha256'] == predecessor['candidate_sha256']
    assert base.digest(predecessor['candidate']) == predecessor['candidate_sha256']
    parent = base.NdsImage.open(predecessor['candidate'])
    target = base.NdsImage.open(gallery.ROM)
    assert sha256(target.read_file(gallery.ARM)).hexdigest() == release['target_ARM9_sha256']
    assert parent.read_file(gallery.COMMON) == target.read_file(gallery.COMMON)

    prepared_review = base.digest(gallery.STAT_REVIEW)
    gallery.seal_stat(ledger, release, release['actual_verification_scope'], parent.read_file(gallery.ARM),
                      target.read_file(gallery.ARM), target.read_file(gallery.COMMON))
    assert base.digest(gallery.STAT_REVIEW) == prepared_review
    ledger_bytes = encode_ledger(ledger)
    with gallery.LEDGER_PENDING.open('wb') as pending:
        for offset in range(0, len(ledger_bytes), 1024 * 1024):
            pending.write(ledger_bytes[offset:offset + 1024 * 1024])
    ledger_after = base.digest(gallery.LEDGER_PENDING)
    assert ledger_after == sha256(ledger_bytes).hexdigest()
    base.save(gallery.MUTATION_PLAN, dict(registry_before=predecessor['registry_sha256'],
        registry_after=release['registry_sha256'], ledger_before=sha256(before).hexdigest(),
        ledger_after=ledger_after, main=base.digest(base.PROMOTED)))
    print('Recovered the prepared Gallery registration plan.')


if __name__ == '__main__':
    main()
