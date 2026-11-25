"""Retain native stored checks for scopes with independently inventoried zero compound consumers."""
from scripts.check_editorial_stored_explicit_captain_v1 import source as previous,compound_storage
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "    styles_path=Path(rebuilt['styles']);assert sha(styles_path.read_bytes())==rebuilt['styles_sha256']\n    styles=load(styles_path);assert styles['runtime']==runtime and styles['manuscript_sha256']==rebuilt['manuscript_sha256']":
        """    assert rebuilt['style_physical_speech_count']==rebuilt['typed_choice_count']==rebuilt['compound_objects']==0
    assert all(not g.get('native_objects') and not any(c['word'] in [0x2100,0x2200,0x4100] for c in g['all_target_commands']) for g in rebuilt['groups'])
    styles={};menu={}  # No compound provider/getter approval is inferred.""",
    "style_proof=rebuilt['styles'],style_proof_sha256=rebuilt['styles_sha256'],":
        'exact_inventoried_zero_compound_scope=True,',
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
})
exec(compile(source,__file__+'::same-stored-native-guards-explicit-absence-of-compound-objects','exec'),globals())
