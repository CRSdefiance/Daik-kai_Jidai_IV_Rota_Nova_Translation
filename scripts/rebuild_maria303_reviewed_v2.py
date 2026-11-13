"""Bind the exact historical source-alignment owner without changing frozen complete-block guards."""
from scripts.rebuild_maria303_reviewed_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block':
        'from dk4tool.script.maria303_source_alignment_v1 import rebuild_block',
    "Path('dk4tool/script/reviewed_scene_rebuild_v3.py')":
        "Path('dk4tool/script/reviewed_scene_rebuild_v3.py'),Path('dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py'),Path('dk4tool/script/maria303_source_alignment_v1.py')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-303-object-rebuild-with-one-exact-source-alignment-owner','exec'),globals())
