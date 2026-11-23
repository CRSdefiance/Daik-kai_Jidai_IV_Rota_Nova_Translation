"""Finish the verified release after the Windows ledger rename was interrupted."""

from gzip import decompress
from os import fsync
from pathlib import Path

from scripts import register_ruin_statue_and_ice_20261118 as release


base = release.base
LEDGER_PENDING = base.LEDGER.with_name('editorial_review_current.ruin_statue_and_ice.pending.json')


def update_ledger_in_place(ledger_before, ledger_after):
    with base.LEDGER.open('r+b') as stream:
        assert stream.read() == ledger_before
        try:
            stream.seek(0)
            assert stream.write(ledger_after) == len(ledger_after)
            stream.truncate()
            stream.flush()
            fsync(stream.fileno())
            stream.seek(0)
            assert stream.read() == ledger_after
        except (AssertionError, OSError):
            stream.seek(0)
            assert stream.write(ledger_before) == len(ledger_before)
            stream.truncate()
            stream.flush()
            fsync(stream.fileno())
            raise


def main():
    receipt = base.load(release.VERIFY / 'registration_mutation_plan.json')
    registered = base.load(release.RELEASE)
    assert base.digest(base.PROMOTED) == receipt['main_sha256']
    assert base.digest(base.REGISTRY) == receipt['registry_before']
    assert base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(LEDGER_PENDING) == receipt['ledger_after']
    assert base.digest(release.ROM) == registered['candidate_sha256']
    assert base.digest(release.PATCH) == registered['patch_sha256']
    assert base.digest(release.MANIFEST) == registered['manifest_sha256']
    manifest = base.load(release.MANIFEST)
    verified = base.load(release.REVIEW)
    checksums = base.load(release.PACKAGE / 'checksums.json')
    assert checksums == release.workflow.package_checksums(release.PACKAGE)
    assert base.digest(release.REVIEW) == manifest['ruin_statue_and_ice_pipeline']['registered_review_sha256']
    assert not release.DOC.exists()

    registry_before = base.REGISTRY.read_bytes()
    ledger_before = decompress((release.ROOT / 'editorial_ledger_before.json.gz').read_bytes())
    ledger_after = LEDGER_PENDING.read_bytes()
    registry_after = decompress((release.PACKAGE / 'build_release_stack.json.gz').read_bytes())
    assert release.native.digest(registry_before) == receipt['registry_before']
    assert release.native.digest(ledger_before) == receipt['ledger_before']
    assert release.native.digest(ledger_after) == receipt['ledger_after']
    assert release.native.digest(registry_after) == receipt['registry_after'] == registered['registry_sha256']
    pins_path = Path('translations/rom_retention_pins.json')
    pins = base.load(pins_path)
    for path in (release.ROM, release.stage.ROM, release.stage.prior.ROM):
        absolute = str(path.resolve())
        assert all(row['path'] != absolute for row in pins)
        pins.append(dict(path=absolute, reason=f'Preserve verified ruin statue and ice candidate {base.digest(path)}'))
    assert base.digest(base.LEDGER) == receipt['ledger_before']
    assert base.digest(base.REGISTRY) == receipt['registry_before']
    base.replace_checked(base.REGISTRY, registry_after)
    try:
        update_ledger_in_place(ledger_before, ledger_after)
    except (AssertionError, OSError):
        base.replace_checked(base.REGISTRY, registry_before)
        raise
    assert base.digest(base.REGISTRY) == receipt['registry_after']
    assert base.digest(base.LEDGER) == receipt['ledger_after']
    base.replace_checked(pins_path, (release.workflow.dumps(pins, ensure_ascii=False, indent=2) + '\n')
                         .replace('\n', '\r\n').encode())

    front = release.VERIFY / 'ice_front_live_1.png'
    left = release.VERIFY / 'ice_left_live_1.png'
    right = release.VERIFY / 'ice_right_live_1.png'
    with release.DOC.open('x', encoding='utf-8', newline='\n') as out:
        out.write(f'''# Ruin statue and floating-ice puzzle

Reviewed the compassionate statue, floating-ice riddle and nearby ruin replies across the four routes. The {registered["prose_revisions"]} prose revisions keep the protective voice unidentified, Fernando's fear of a curse tentative and each captain's response distinct. Eight inscriptions restore the brim-full vessel and pair the front stone with a rise, left with a fall and right with no change. The ledger records {registered["text_display_revisions"]} wrap-only revisions and {registered["justified_retentions"]} retentions. [Exact review ledger](../{release.REVIEW.as_posix()})

All {len([row for row in verified["records"] if row["decision"] == "revision"])} revised pages passed native checks and visual review. The final statue reflow received 16 fresh native checks. The eight inscriptions passed the original FE painter and null-actor checks. Initialized DeSmuME runs on Maria's scene covered both wrong answers, the opening wall and the figurehead reward. The final ROM retains the byte-identical puzzle scene, host and renderer. The other routes and unvisited voice branch received offline checks. Natural activation and physical hardware remain unverified. [Front](../{front.as_posix()}) [Left](../{left.as_posix()}) [Right](../{right.as_posix()})

The clean-input patch reconstructs the candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and {registered["repository_tests"]} targeted tests passed. Main retains its accepted build. [Test ROM and patch](../{release.PACKAGE.as_posix()}/README.md)

The 27,700 credited records and 276 pending shared keys carry forward. Next, review the 206 survey and guild-search records in SC0 B265–272, SC1 B248–250 and B256–260, SC2 B247–249 and B255–258, and SC3 B225–232. The paired source dumps are under work/guild_search_and_survey_source_20261118.
''')
    prefix = (f'# Current editorial checkpoint - 2026-11-18\n\n'
              f'The ruin statue and floating-ice puzzle are reviewed across all routes. '
              f'[Checkpoint]({release.DOC.name})\n\n').encode()
    for name in ('editorial_handoff_current.md', 'translation_progress.md', 'build_continuity_protocol.md'):
        path = Path('docs') / name
        base.replace_checked(path, prefix + path.read_bytes())
    assert base.digest(base.PROMOTED) == receipt['main_sha256']
    print(f'Registered {registered["candidate_sha256"]} with '
          f'{registered["registered_manifest_entries"]} entries, 114 accepted layers and '
          f'{registered["passing_release_checks"]} passing checks.')


if __name__ == '__main__':
    main()
