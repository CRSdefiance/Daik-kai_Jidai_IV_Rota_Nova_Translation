"""Correct a literal-pool address to its source-proven root getter;preserve failed probe."""
import ast
from collections import Counter
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_consumer_correction_v6081b')
if __name__=='__main__':
    source=Path('scripts/prove_shachihoko_item_consumers_v6081.py');target=source.with_name('prove_shachihoko_item_consumers_v6081b.py');assert not target.exists() and not ROOT.exists()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');current=NdsImage.open('out/all_routes_combined_v6050_candidate.nds').read_file('/__arm9__.bin')
    at=0xCB190;assert clean[at:at+12]==current[at:at+12] and current[at:at+8].hex()=='00009fe51eff2fe1'
    callers=[]
    for a,b in [(0x1C7CC,0x1C7EC),(0x1C91C,0x1C93C)]:
        assert clean[a:b]==current[a:b]
        dis=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(current[a:b],0x02000000+a)]
        assert any(i['mnemonic']=='bl' and i['operands']=='#0x20cb190' for i in dis);callers.append(dis)
    text=source.read_text('utf-8');assert text.count('root=get(0xCB198)')==1
    corrected=text.replace('root=get(0xCB198)','root=get(0xCB190)').replace("ROOT=Path('work/analysis/shachihoko_item_consumers_v6081')","ROOT=Path('work/analysis/shachihoko_item_consumers_v6081b')")
    compile(corrected,str(target),'exec');a,b=native_numbers(text),native_numbers(corrected)
    assert a-b==Counter({0xCB198:1}) and b-a==Counter({0xCB190:1})
    target.write_text(corrected,'utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'explicit_source_proven_native_root_correction.json',dict(failed_source=str(source),failed_source_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes()),
        correction='CB198 is the root getter\'s literal-pool pointer word;CB190 is its two-instruction LDR/BX function. Both real source virtual callers BL CB190. The failed offline probe executed the literal address and was stopped;no ROM mutation or credit occurred.',
        source_exact_getter_start=0x02000000+at,source_exact_getter12_hex=current[at:at+12].hex(),source_exact_real_virtual_callers=callers,
        only_native_integer_change_explicitly_verified=True,all_other_native_constants_preserved=True,no_game_code_or_ROM_change=True,full_goal_complete=False))
    print('Literal-pool/getter confusion corrected to source-native CB190;both original caller BL sites and exact12 bytes verified. Failed probe preserved.')
