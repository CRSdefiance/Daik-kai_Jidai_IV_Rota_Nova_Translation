"""Keep stored guards, bind the empty menu explicitly andcheck FE row membership."""
from scripts import check_editorial_stored_explicit_captain_v1 as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    "    if rebuilt.get('typed_choice_count'):":
        """    if not rebuilt.get('typed_choice_count'):
        menu_path=Path(rebuilt['menu']);assert sha(menu_path.read_bytes())==rebuilt['menu_sha256']
        menu=load(menu_path)
        assert menu['runtime']==runtime and menu['manuscript_sha256']==rebuilt['manuscript_sha256']
        assert not menu['menus'] and menu['source_has_no_typed_choice_objects']
        assert menu['offline_visual_approved'] and not menu['direct_view_pending']
    if rebuilt.get('typed_choice_count'):""",
    '                    rendered=painter(expanded)':
        "                    rendered=painter(expanded)\n                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
})
if __name__=='__main__':
    env={**vars(previous),**globals()}
    exec(compile(source,__file__+'::same-stored-parity-native-branches-andFE-rows-no-compound-objects','exec'),env)
