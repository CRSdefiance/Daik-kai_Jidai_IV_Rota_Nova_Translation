"""Retain stopped preparation; preserve the builder's existing mixed newline bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_builder_tools_v8694b');assert not root.exists()
    receipt=derive('scripts/prepare_Hodram_B52_builder_support_v8694.py','scripts/prepare_Hodram_B52_builder_support_v8694b.py',{
        'work/analysis/Hodram_B52_builder_support_v8694':'work/analysis/Hodram_B52_builder_support_v8694b',
        "source=BUILDER.read_text(encoding='utf-8');assert source.encode()==current":"source=current.decode('utf-8');assert source.encode()==current",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=receipt,
         failure='Original preparer correctly stopped before writes because universal-newline reading normalized existing builder bytes. Decode the original bytes directly and retain every original newline in the whole inverse.',
         stopped_preparer_preserved_no_live_builder_module_orconfiguration_written=True))
