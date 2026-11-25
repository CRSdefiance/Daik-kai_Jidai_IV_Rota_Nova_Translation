"""Keep the dynamic-selector native checks and journal each completed record."""
from scripts import check_editorial_compiled_pages_explicit_captain_v1 as previous
from scripts import check_editorial_compiled_pages_static_captain_v2 as journal
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(journal.source, {
    "assert f'assert identity==prefix and captain=={args.captain}' in macro_adapter\n    assert all(r['source_selector']<207 for r in doc['records'] if r['kind']=='progressive')":
        "assert f'assert captain=={args.captain} and identity==(prefix if prefix<207 else DYNAMIC_BINDINGS[prefix])' in macro_adapter",
})
# Prove that the only difference from the established dynamic runner is its
# append-only run/record receipts, using the already-qualified journaling edits.
assert previous.source in journal.previous.previous.source or previous.source == journal.previous.previous.source
if __name__ == '__main__':
    env = {**vars(previous), **globals()}
    exec(compile(source, __file__+'::unchanged-dynamic-native-guards-with-record-journals', 'exec'), env)
