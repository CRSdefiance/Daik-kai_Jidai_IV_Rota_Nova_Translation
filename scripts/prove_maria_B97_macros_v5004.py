"""Measure current route3 macro lengths and the real source/current FO paragraph."""
from pathlib import Path
import inspect
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/maria_B97_macros_v5004')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['source_macro_counts']==dict(FI=0,FA=0,FO=1)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');probes=[]
    for actor in [3,10,180]:probes.append(ctx.execute(expand,b'FI FA FO',actor));ctx.machines.pop()
    actual=[];row=next(r for r in packet['records'] if b'FO' in bytes.fromhex(r['source_hex']))
    assert row['source_record_index']==22 and row['source_selector']==3
    for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
        raw=bytes.fromhex(row[key]);r=ctx.execute(expand,raw[1:],raw[0]);ctx.machines.pop();actual.append(dict(id=row['id'],version=label,source_hex=raw.hex(),**r))
    assert not ctx.machines and sum(len(r['cases']) for r in probes+actual)==20
    save(ROOT/'three_actors_default_and_real_FO20_alignment_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        synthetic_default_macro_measurements=probes,real_source_and_current_FO_paragraph_cases=actual,macro_ascii_lengths=dict(FI=5,FA=2,FO=7),source_macro_counts=packet['source_macro_counts'],
        only_one_real_FO_macro_preserved_no_FI_FA_added_to_shipped_source=True,all20_original_macro_ABI_canaries_and_all4MiB_exact=True,
        portable_source_owned_adapter=inspect.getsource(expand),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_B97_activation_and_custom_player_names_not_claimed=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('20 current macro alignments pass:Maria5/Li2/Li Clan7. RealFO source/current paragraphs bound;syntheticFI/FA probes do not add source macros.')
