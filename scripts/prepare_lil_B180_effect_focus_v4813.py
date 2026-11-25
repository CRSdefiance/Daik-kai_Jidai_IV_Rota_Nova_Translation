"""Read-only effect-boundary exports resolve the measured persistent-state risk."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_effect_focus_tools_v4813')
if __name__=='__main__':
    assert not ROOT.exists()
    needle='                self.rows.append(row)'
    extra='''                selected_source=row.get('source',{})
                if selected_source.get('block')==22 and selected_source.get('instruction_offset',0)>=56 and selected_source.get('first_word') in [0x8000,0xA000,0xC200,0]:
                    path=self.folder/('boundary_'+str(len(self.rows)).zfill(4)+'_'+row['kind']+'.bin')
                    path.write_bytes(raw)
                    row['targeted_readonly_RAM']=dict(path=str(path),sha256=sha(raw),bytes=len(raw),read_only_export=True)
'''
    tools=[derive('scripts/observe_lil_B180_v4810.py','scripts/observe_lil_B180_v4813.py',{needle:extra+needle})]
    tools.append(derive('scripts/run_lil_B180_display_fixture_v4810.py','scripts/run_lil_B180_effect_focus_v4813.py',{
        'observe_lil_B180_v4810':'observe_lil_B180_v4813','display_run_v4810':'effect_focus_run_v4813',
        'display_v4810':'effect_focus_v4813',"'--frames','9001'":"'--frames','6001'",
        "'requested_frames':9001":"'requested_frames':6001",
        'range(2350,9001,60)':'range(5230,6001,60)'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_focus.json',dict(tools=tools,
        concrete_risk='First paired cold boots select different original effects and final town-state hashes differ; export original command boundaries to identify exact owned changes.',
        two_focused_cold_boots_6001_frames_each=True,no_emulator_seed_or_outcome_forcing=True,
        raw_exports_readonly_not_savestates=True,full_goal_complete=False))
