"""Join unchanged runs using the explicitly proven reference-only occurrence correction."""
import inspect
from scripts import combine_hodram_B311_B324_bounded_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "    fixtures, actual, menus, transitions = [], [], [], []":
        "    resolution_path=ROOT/'source_occurrence_resolution_v2.json'\n    resolution=load(resolution_path)\n    assert resolution['duplicate_command_source_key_regression_pass'] and resolution['original_fixtures_ROMs_terminals_captures_andpixel_receipts_unchanged']\n    for p,h in resolution['evidence'].items():assert digest(p)==h\n    fixtures, actual, menus, transitions = [], [], [], []",
    "        fixtures.append(f)":
        "        corrected=resolution['records'][index-1]\n        assert corrected['fixture_sha256']==digest(fpath)\n        f={**f,'copied_commands':corrected['corrected_copied_commands'],'selected_records':corrected['corrected_selected_records'],\n            'source_occurrence_resolution':str(resolution_path),'source_occurrence_resolution_sha256':digest(resolution_path)}\n        fixtures.append(f)",
    "    for p in [fixture_manifest, rebuilt_path, native_path, capacity, ROOT/'bounded_selection_v1.json', LIVE, MENU]:":
        "    for p in [fixture_manifest, rebuilt_path, native_path, capacity, ROOT/'bounded_selection_v1.json',resolution_path, LIVE, MENU]:",
})
env = {**vars(previous), '__file__':__file__}
exec(compile(source,__file__+'::same-byte-order-pixel-return-guards-explicit-provenance-correction','exec'),env)
if __name__ == '__main__':
    env['main']()
