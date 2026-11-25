"""Preserve the failed menu probe and inspect its exact VM label widths before changing ownership."""
import inspect,struct
from pathlib import Path
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_menu_diagnostic_v4070')
SOURCE=Path('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);doc=read('translations/lil_B166_choice_manuscript_v1.json');arm=NdsImage.open(v['current_ROM']).read_file('/__arm9__.bin');c=next(c for c in v['blocks'][0]['all_current_native_commands'] if c['word']==0x2100);chunks=[];offsets=[];cursor=0
    for r in sorted(doc['records'],key=lambda r:r['option_index']):
        value=r['english'].encode('ascii');offsets.append(cursor);chunk=value+b'\0';chunk+=b'\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    target=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks);source=inspect.getsource(prior.choice_vm)
    for a,b in [('pointer, 32','pointer, len(object_bytes)'),('96','VM_GUARD_BYTES')]:assert a in source;source=source.replace(a,b)
    env={**prior.__dict__,'VM_GUARD_BYTES':256};exec(compile(source,__file__+'::original-VM-widths','exec'),env);cases=[]
    for label,value in [('current',bytes.fromhex(c['whole_command_hex'])),('reviewed',target)]:
        vm=env['choice_vm'](arm,value);width=vm['minimum_width_units']*6
        cases.append(dict(version=label,object_hex=value.hex(),VM=vm,width_px=width,storage_stride_px=(width+3)//4*4,label_lengths=[len(x.encode('ascii')) for x in vm['labels']]))
    ROOT.mkdir(parents=True);save(ROOT/'original_VM_widths_and_preserved_failed_probe.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,failed_probe='scripts/prove_lil_B166_choices_v4069.py',failed_probe_sha256=sha(Path('scripts/prove_lil_B166_choices_v4069.py').read_bytes()),failure='Original painter complete-pixel equality assertion;no menu approval orcredit',source_owned_VM_adapter=source,no_wording_or_guard_change=True,full_goal_complete=False));print(cases)
