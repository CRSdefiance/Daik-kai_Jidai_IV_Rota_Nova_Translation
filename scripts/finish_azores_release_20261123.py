"""Resume the checked Azores registration after the prepared archive boundary."""

from os import link

from scripts import register_azores_wording_20261123 as release
from scripts.source_locked_derivation_v5118 import checked_text


def package_link(source, destination, expected):
    if destination == release.PACKAGE / "build_release_stack.json.gz":
        assert source == release.WORK / "release_stack_with_azores_wording.json.gz"
        assert source.resolve(strict=True).parent == release.WORK.resolve(strict=True)
        assert destination.parent.resolve(strict=True) == release.PACKAGE.resolve(strict=True)
        assert release.base.digest(source) == expected
        if not destination.exists():
            link(source, destination)
        assert source.samefile(destination) and release.base.digest(destination) == expected
    else:
        release.reuse_link(source, destination, expected)


def main():
    archive = release.scope["archive"]

    def reuse_verified_archive(source, destination):
        if not destination.exists():
            archive(source, destination)
        assert release.snapshot_digest(destination) == release.base.digest(source)

    release.scope.update(reuse_link=package_link, archive=reuse_verified_archive)
    source = checked_text(release.build, {
        'value(data, "supply_ratio_hint_20261123", 1) == entry': 'value(data, "azores_wording_20261123", 1) == entry',
    })
    exec(compile(source, __file__ + "::checked-resume", "exec"), release.scope)
    release.scope["main"]()


if __name__ == "__main__":
    main()
