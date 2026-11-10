"""Refresh four changed layouts with the unchanged native checks and exact parent rows."""
from scripts import check_rafael_B36_B41_compiled_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

MEASURED=previous.MEASURED
check_FE_rows=previous.check_FE_rows
validate_documented_layouts=previous.validate_documented_layouts
source=checked_text(previous.source,{
    "    assert doc['physical_speech_objects']==175 and not any(r['kind']!='progressive' for r in doc['records'])":
        """    assert doc['physical_speech_objects']==4 and not any(r['kind']!='progressive' for r in doc['records'])
    parent_path=Path(doc['subset_of']);assert sha(parent_path.read_bytes())==doc['subset_of_sha256']
    parent={r['id']:r for r in load(parent_path)['records']}
    assert len(parent)==175 and all(r==parent[r['id']] for r in doc['records'])
    assert {r['id'] for r in doc['records']}=={'DK4_MES_B36_R0046','DK4_MES_B37_R0254','DK4_MES_B37_R0267','DK4_MES_B41_R0131'}""",
})
exec(compile(source,__file__+'::same-native-pages-four-exact-parent-layouts','exec'),globals())
