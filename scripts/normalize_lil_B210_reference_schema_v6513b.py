"""Expose the same twelve measured command maps to the registered census schema."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_relocation_reference_v6513b')
SOURCE=Path('work/analysis/lil_B210_relocation_research_v6513/ten_speech_relocation_complete_preambles_A000_end_and_full_inverse_RESEARCH.json')
if __name__=='__main__':
    assert not ROOT.exists();old=read(SOURCE);new=deepcopy(old);spec=new['blocks'][0];assert len(spec['mapped_native_commands'])==12 and not spec['relative_skip_fixups'] and not any(c['word'] in [256,512,768,1024] for c in spec['mapped_native_commands'])
    spec['command_map']=[dict(word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],old_extent=c['old_native_extent'],new_extent=c['new_native_extent']) for c in spec['mapped_native_commands']];spec['target_native_skip_cases']=[];new.update(previous_research_plan=str(SOURCE),previous_research_plan_sha256=sha(SOURCE.read_bytes()),same_exact_block_SC2_bytes_and_no_relative_sites_schema_only=True);ROOT.mkdir(parents=True);save(ROOT/'ten_speech_relocation_complete_preambles_A000_end_and_full_inverse_RESEARCH.json',new)
    restored=deepcopy(new);restored['blocks'][0].pop('command_map');restored['blocks'][0].pop('target_native_skip_cases')
    for k in ['previous_research_plan','previous_research_plan_sha256','same_exact_block_SC2_bytes_and_no_relative_sites_schema_only']:restored.pop(k)
    assert restored==old;print('B210 measured maps exposed in census schema;all original plan values and target bytes unchanged,no relative sites invented.')
