"""Research only: determine whether existing COMMON wrapping preserves generated LF."""
from pathlib import Path
import inspect
from ndspy.code import MainCodeFile
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import machine,BASE
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/square_page_wrap_probe_v2127')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 plan=read('work/analysis/square_context_payload_v2124/native_payload_plan.json');arm=Path(plan['target_ARM9']).read_bytes();cpu=machine(arm);cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]))
 source=inspect.getsource(native_layout);assert source.count('assert len(lines) <= 4')==1;source=source.replace('assert len(lines) <= 4','assert len(lines) <= 6');env=dict(native_layout.__globals__);exec(compile(source,__file__,'exec'),env);formatter=env['native_layout'];cases=[]
 for prefix in(b' ',b'  '):
  text=prefix+b'See the fashions and decor\n  that will be the talk\n  of society!\n  Fancy yourself a lady\n  or gentleman?\n  Step right up!'
  output,lines=formatter(cpu,text,677,())
  cases.append(dict(input_hex=text.hex(),output_hex=output.hex(),native_wrapper_preserves_generated_layout_exactly=text==output,lines=lines))
 save(ROOT/'native_generated_LF_preservation.json',dict(ARM9_sha256=sha(arm),cases=cases,helper_line_count_assertion_only_relaxed_in_host_test=True,no_game_code_or_ROM_changed=True,full_goal_complete=False));print(cases)
