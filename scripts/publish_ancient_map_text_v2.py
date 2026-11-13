"""Publish the prepared Ancient Map release with its exact mutation-plan path."""

from scripts import register_ancient_map_text_v2 as prepared


def main():
    release = prepared.base.load(prepared.RELEASE)
    pipeline = prepared.base.load(prepared.MANIFEST)['ancient_map_text_registered_successor_pipeline']
    assert prepared.base.digest(prepared.__file__) == pipeline['driver_sha256']
    assert prepared.base.digest(prepared.MANIFEST) == release['manifest_sha256']
    prepared.MUTATION_PLAN = prepared.VERIFICATION / 'registration_mutation_plan.json'
    prepared.publish_prepared()


if __name__ == '__main__':
    main()
