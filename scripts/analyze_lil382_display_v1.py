"""Keep complete pixel/order guards with scoped current-name consumer bindings."""
from scripts.analyze_reviewed_dynamic_fixture_v1 import source as previous, dynamic_headers
from scripts.source_locked_derivation_v5118 import checked_text

def lil_source(source):
    return checked_text(dynamic_headers(source), {
        "byactor = {r['actor_ID']: r['english'] for r in load(decisions_path)['records']}":
            "byactor = {r['actor_ID']: next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in load(decisions_path)['records']}",
        "r['frame'] >= 2800": "r['frame'] >= 0",
    })

source = checked_text(previous, {
    "exec(compile(dynamic_headers(source),__file__+'::same-pixels-with-qualified-dynamic-header-expectations','exec'),globals())":
        "exec(compile(lil_source(source),__file__+'::same-pixels-with-qualified-dynamic-header-expectations','exec'),globals())",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-body-header-andblank-guard-checks', 'exec'), globals())
