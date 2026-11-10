"""Keep typed captions outside a changed speech-page subset's exact membership."""
from scripts.prepare_changed_dialogue_native_subset_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "assert changed and {r['id'] for r in doc['records']}=={r['id'] for r in plan['records']}":
        "assert changed and {r['id'] for r in doc['records'] if r['kind'] in ['progressive','system-FE']}=={r['id'] for r in plan['records']}",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-exact-changed-membership-with-separate-typed-captions', 'exec'), globals())
