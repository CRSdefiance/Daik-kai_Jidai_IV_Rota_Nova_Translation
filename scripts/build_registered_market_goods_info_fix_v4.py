"""Classify ARM9 as an NDS component while retaining exact all-file/component guards."""
from scripts.build_registered_market_goods_info_fix_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "assert [p for _,p,data in parent_image.iter_files() if proposed.read_file(p)!=data]==['/__arm9__.bin']":
        "assert [p for _,p,data in parent_image.iter_files() if proposed.read_file(p)!=data]==[]",
    "assert all(proposed.read_file(p)==data for p,data in parent_image.iter_components())":
        "assert [p for p,data in parent_image.iter_components() if proposed.read_file(p)!=data]==['/__arm9__.bin']",
    "changed_internal_files=['/__arm9__.bin'],changed_components=[]":
        "changed_internal_files=[],changed_components=['/__arm9__.bin']",
})
exec(compile(source,__file__+'::same-registered-guards-exact-NDS-component-classification','exec'),globals())
