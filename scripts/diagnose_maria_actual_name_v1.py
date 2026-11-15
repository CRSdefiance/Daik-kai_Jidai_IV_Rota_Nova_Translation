"""Print the exact failing captured header while preserving the original assertion."""
from scripts import analyze_maria301_display_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def diagnostic_source(source):
    source = previous.maria_source(source)
    return checked_text(source, {
        "            origin = match(image, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])":
        """            try:
                origin = match(image, mask(plane['native_plane'], plane['native_plane_sha256'], 216), (98, 97, 98), [16], [276])
            except AssertionError:
                print(dict(failing_ID=page['id'],frame=cap['frame'],selector=actor,expected_actor=expected_actor,expected_name=text,capture=cap['path'],native_name_plane=plane['native_plane']),flush=True)
                raise""",
    })


if __name__ == '__main__':
    exec(compile(previous.source, __file__+'::same-header-match-with-failure-context-only', 'exec'),
        {**vars(previous), '__file__':__file__, '__name__':'__main__', 'maria_source':diagnostic_source})
