"""Check the reconstructed bytes with the original renderer and exact staged row origins."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load
from scripts.check_rafael_B166_staged_FE_v7 import actual_rows
from scripts import check_qualified_rafael_stored_with_fu_v1 as previous
from scripts.qualify_rafael_B166_B167_names_v1 import MACROS, PREVIOUS_NAMES
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "identity['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']":
        "identity['exact_unchanged_actor0_macro_dependencies']",
    "    ownpath=Path(identity['same_Rafael_default_macro_proof']);assert sha(ownpath.read_bytes())==identity['same_Rafael_default_macro_proof_sha256']":
        """    inherited=load(PREVIOUS_NAMES[0])
    ownpath=Path(inherited['same_Rafael_default_macro_proof'])
    assert sha(ownpath.read_bytes())==inherited['same_Rafael_default_macro_proof_sha256']""",
    "identity['macro_widths']['FU']==78":
        "load(MACROS)['macro_widths']['FU']==78 and identity['evidence'][str(MACROS)]==sha(MACROS.read_bytes())",
    "                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)":
        """                    if row.get('source_staged_FE'):
                        expected=[tuple(q) for q in old['planned_native_row_comparison']['planned_visible_rows']]
                        assert actual_rows(rendered['events'])==expected
                        rendered['planned_native_row_comparison']=dict(complete_glyph_row_membership_exact=True,
                            complete_visible_row_origins_exact=True,planned_visible_rows=expected)
                    else:
                        rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)""",
    'args.native,args.identity,macro_path,ownpath,Path(__file__)':
        'args.native,args.identity,macro_path,ownpath,MACROS,PREVIOUS_NAMES[0],Path(__file__)',
})
env={**vars(previous),'actual_rows':actual_rows,'MACROS':MACROS,'PREVIOUS_NAMES':PREVIOUS_NAMES,'__file__':__file__}
exec(compile(source,__file__+'::original-stored-guards-and-exact-staged-origins','exec'),env)
if __name__=='__main__':
    env['main']()
