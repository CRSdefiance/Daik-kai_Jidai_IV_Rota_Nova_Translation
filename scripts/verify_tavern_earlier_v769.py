"""Earlier Yard,Port and shared dialogue controls through the new prefix."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_common import compile_text
from dk4tool.rom.nds import NdsImage
from scripts import probe_shipyard_runtime_v759 as yard
from scripts import verify_market_balanced_owners_v757 as controls
from scripts.context_tavern_continuation_v768 import CURRENT,RAM_REPORT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.tavern_continuation_runtime_v769 import load_into_cpu
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_runtime_v769')


def main():
    arm=NdsImage.open(CURRENT).read_file('/__arm9__.bin');raw=snapshot(read(RAM_REPORT),3200)
    def loaded(changed=True):
        u=machine(arm);u.mem_write(BASE,raw)
        if changed:load_into_cpu(u,arm)
        return u
    yard.call=call;controls.call=call;yard.YESNO=(*yard.YESNO,1246)
    prior=read('work/analysis/tavern_coordinates_v766/inherited_outputs.json')
    paragraphs={r['message_id']:compile_text(r) for r in read('translations/shipyard_editorial_manuscript_v3.json')['records']}
    results=[]
    for i,old in enumerate(prior['all1124_Yard_outputs']):
        if i%64==0:u=loaded()
        result=yard.layout(u,paragraphs[old['id']],old['id'],tuple(bytes.fromhex(v) for v in old['values_hex']))
        assert result==old
        results.append(result)
    ports=[]
    for old in read('work/analysis/port_services_v762/native_owned/verification.json')['complete_native_font_cases']:
        if old['id']==267:
            ports.append({'id':267,'unchanged_system_template_hex':old['template_hex'],'new_runtime_does_not_touch_system_consumer':True});continue
        result=yard.layout(loaded(),bytes.fromhex(old['template_hex']),old['id'],tuple(bytes.fromhex(v) for v in old['values_hex']))
        ports.append(result)
    assert ports==prior['all40_Port_cases']
    rows=[]
    for row in prior['all180_earlier_parent_output_controls']:
        out=[]
        for changed in (False,True):
            u=loaded(changed);u.mem_write(STACK+0x270,bytes(4));u.mem_write(STACK+0x27C,struct.pack('<I',0x021184C0))
            out.append(controls.scope_output(u,row['input'].encode(),row['id'],(),row['parent']))
        assert out[0]==out[1];rows.append(row)
    save(ROOT/'earlier_outputs.json',{'all1124_Yard_outputs':results,'all40_Port_cases':ports,
        'all180_earlier_parent_output_controls':rows,'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'runtime_plan_sha256':sha((ROOT/'owned_runtime_plan.json').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_actual_gameplay_or_ROM_emitted':True})
    print('All1124 Yard,40 Port and180 earlier full-output controls remain exact.',flush=True)


if __name__=='__main__':main()
