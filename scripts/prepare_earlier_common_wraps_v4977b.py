"""Bind the existing registered Investment-title literal without weakening code locks."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/earlier_common_wraps_tools_v4977b');assert not root.exists()
    tool=derive('scripts/review_earlier_common_wraps_v4977.py','scripts/review_earlier_common_wraps_v4977b.py',{
        'from scripts.verify_village_wrap_v608 import read,save':'from scripts.verify_village_wrap_v608 import read,save\nfrom dk4tool.patch.market_contract_editorial import INVESTMENT',
        '    for a,b in spans:assert ca[a:b]==arm[a:b]':
        "    differences=sorted({at for a,b in spans for at in range(a,b,4) if ca[at:at+4]!=arm[at:at+4]})\n    assert differences==[0xBCA3C] and struct.unpack_from('<I',arm,0xBCA3C)[0]==INVESTMENT\n    assert arm[INVESTMENT-BASE:INVESTMENT-BASE+11]==b'Investment\\0'\n    restored=bytearray(arm);restored[0xBCA3C:0xBCA40]=ca[0xBCA3C:0xBCA40]\n    for a,b in spans:assert bytes(restored[a:b])==ca[a:b]",
        "exact_original_spans=[dict(start=a,end=b,sha256=sha(ca[a:b])) for a,b in spans],":
        "exact_original_spans=[dict(start=a,end=b,clean_sha256=sha(ca[a:b]),current_sha256=sha(arm[a:b])) for a,b in spans],\n        sole_registered_title_literal=dict(address=0x020BCA3C,clean_hex=ca[0xBCA3C:0xBCA40].hex(),current_hex=arm[0xBCA3C:0xBCA40].hex(),target=INVESTMENT,title='Investment',owner='dk4tool.patch.market_contract_editorial.relocate_providers',every_other_selected_source_word_exact=True),",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,diagnostic_v4977_preserved=True,new_editorial_credit=0))
