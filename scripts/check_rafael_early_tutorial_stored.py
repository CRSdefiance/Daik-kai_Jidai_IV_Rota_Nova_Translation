"""Check complete stored tutorial pages, parity tails and fresh macro alignment cases."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand

source = checked_text(Path('scripts/check_editorial_stored_batch.py').read_text(encoding='utf-8'), {
    'from scripts.registered_editorial_runtime import RegisteredRuntime':
        'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    "ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'])":
        "ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)",
    "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'", "b'Bergstrom Fleet'": "b'Castor Co.'",
    '    compiled={r[\'id\']:r for r in native[\'records\']}':
        """    macro_path=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')
    macros=load(macro_path);assert macros['runtime']==runtime
    progressive_env=dict(progressive_expand.__globals__)
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::same-actor0-macro-ABI','exec'),progressive_env)
    fe_env=dict(FE_expand.__globals__)
    exec(compile(macros['source_owned_FE_adapter'],__file__+'::same-null-actor-ABI','exec'),fe_env)
    compiled={r['id']:r for r in native['records']}""",
    "            if text['parity_space_added']:":
        """            alignment=row['native_alignment']
            if text['parity_space_added']:
                alignment=ctx.execute(fe_env['expand'] if is_FE else progressive_env['expand'],raw[1:],*(() if is_FE else (raw[0],)))
                assert len(alignment['cases'])==4 and all(c['output_hex']==expanded.hex() for c in alignment['cases'])""",
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
    '                complete_stored_native_display=rendered,':
        '                complete_stored_native_display=rendered,native_alignment=alignment,',
})
exec(compile(source, __file__ + '::same-complete-stored-consumers-captain0-plus-parity-macros', 'exec'), globals())
