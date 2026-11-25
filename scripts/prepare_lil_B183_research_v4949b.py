"""Prepare B183 reference loading,census,unaligned end and both FE control contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive
import re
from dk4tool.patch.grand_race_menu_release import sha

def derive(a,b,changes):
    if not Path(b).exists():return original_derive(a,b,changes)
    text=Path(a).read_text(encoding='utf-8')
    for key in changes:assert key in text,key
    expected=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    assert Path(b).read_text(encoding='utf-8')==expected
    return dict(previous=a,previous_sha256=sha(Path(a).read_bytes()),successor=b,successor_sha256=sha(Path(b).read_bytes()),exact_prepared_tool_reused=True)

from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B183_research_tools_v4949')
PARENT=Path('out/all_routes_combined_v4914_candidate.nds')
ROM=Path('out/lil_B183_reference_v4950_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B183_relocation_v4947/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B181_reference_v4852.py','scripts/create_lil_B183_reference_v4950.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949',
        'research_v4852':'research_v4950','stored_v4847':'stored_v4948',
        'all10_final_stored_targets40':'all25_final_stored_targets100','all10_final_targets':'all25_final_targets',
        'editorial_handoff_verification_v4850':'editorial_handoff_verification_v4921',
        "stored['current_final_stored_macro_alignment_cases']==40":"stored['current_final_stored_macro_alignment_cases']==100",
        'current_final_stored_macro_alignment_cases=40':'current_final_stored_macro_alignment_cases=100','==[181]':'==[183]','V4821':'V4914'}))
    tools.append(derive('scripts/verify_lil_B181_loader_v4853.py','scripts/verify_lil_B183_loader_v4951.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949','loader_v4853':'loader_v4951','research_v4852':'research_v4950',
        'work/analysis/lil_B180_loader_v4802/whole_SC2_and_B180_initial_entry_proof.json':'work/analysis/lil_B182_loader_v4899/whole_SC2_and_B182_initial_entry_proof.json',
        'V4821':'V4914'}))
    tools.append(derive('scripts/verify_lil_B181_references_v4854.py','scripts/verify_lil_B183_references_v4952.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949','reference_census_v4854':'reference_census_v4952',
        'loader_v4853':'loader_v4951','[181]':'[183]','13-command/no-relative-site':'28-command/no-relative-site',
        "sum(len(r['mapped_commands'])for r in result)==13":"sum(len(r['mapped_commands'])for r in result)==28",
        'all13':'all28','native_commands_each=13':'native_commands_each=28'}))
    tools.append(derive('scripts/prove_lil_B181_ends_v4855.py','scripts/prove_lil_B183_ends_v4953.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949','ends_v4855':'ends_v4953','n==181':'n==183'}))
    tools.append(derive('scripts/prove_lil_B181_relocated_controls_v4856.py','scripts/prove_lil_B183_relocated_controls_v4954.py',{
        'B181':'B183','prepare_lil_B181_research_v4851':'prepare_lil_B183_research_v4949','relocated_controls_v4856':'relocated_controls_v4954',
        'editorial_manuscript_v3':'editorial_manuscript_v7','blocks[181]':'blocks[183]','block=181':'block=183',
        '00a0ffff014913a1':'00a0ffff013926a1','len(dispatches)==10':'len(dispatches)==25',
        "sum(d['resolved_actor_ID'] is None for d in dispatches)==1":"sum(r['resolved_actor_ID'] is None for r in dispatches)==2",
        '[(0xA000,8,8),(0xC200,390,374),(0,392,376)]':'[(0xA000,8,8),(0xC200,950,1048),(0,952,1050)]',
        "len(spec['command_map'])==13":"len(spec['command_map'])==28",'all10':'all25','all9_progressive_static_actors1_impersonal_null_actor_FE_and_no_FI_FA_FO_exact':'all23_progressive_static_actors2_impersonal_null_actor_FE_and_no_FI_FA_FO_exact',
        'ten relocated dispatches':'25 relocated dispatches','Ten relocated dispatches,nine progressive/one impersonal FE':'25 relocated dispatches,23 progressive/two impersonal FE'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),
        source_speeches=25,source_commands=28,progressive=23,FE=2,source_bytes956_stored1056_logical1054=True,
        source_C200950_target1048_source_end952_target1050=True,halfword_aligned_target_end_requires_guarded_native_decode=True,
        parent_whole_loader_reuse_requires_exact_V4914_hash_to_B182_reference=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared B183 research reference,exact-parent loader reuse,fresh target loading/census/end and25 relocated dispatches.')
