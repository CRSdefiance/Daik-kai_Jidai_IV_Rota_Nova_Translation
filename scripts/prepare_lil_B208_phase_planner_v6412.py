"""Use proven exact pre-LF byte need;preserve native metrics,guards and all source words."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B208_phase_planner_tools_v6412')
PROOF=Path('work/analysis/lil_B208_phase_capacity_v6411/three_complete_native_planes12_alignment_cases_and_36_cell_rejection.json')
if __name__=='__main__':
    assert not ROOT.exists();p=read(PROOF);assert p['thirty_five_visible_continuation_characters_with_original_guard_fit_and_complete'] and p['first36_cell_preLF_auto_wrap_rejected'] and p['fresh_original_compiled_alignment_cases']==12
    helper='''PHASE_PROOF=Path(PROOF_PATH)
PHASE_PROOF_SHA256=PROOF_HASH
if sha(PHASE_PROOF.read_bytes())!=PHASE_PROOF_SHA256:raise ValueError('Exact original35-cell continuation proof changed')

def _phase_reserve(words,spaces,start,end,profile,cell):
    if not profile.pair_phase_safe_breaks or end+1==len(words):return 0
    if profile.name!='lil-B208-progressive-runtime-bound-v1':return cell
    # The unchanged codec starts at phase0. Each protected LF is preceded
    # by an odd phase,and its owned guard flips that phase back to0.
    # Restrict exact reservation to wholly printable ASCII/no-macro prose.
    # Every other token shape retains the original conservative reservation.
    if any(t.kind!='text' or any(not 32<=b<128 for b in t.raw) for word in words for t in word):return cell
    if any(any(c!=' ' for c in gap) for gap in spaces):return cell
    count=sum(len(t.raw) for word in words[start:end+1] for t in word)+sum(len(gap) for gap in spaces[start+1:end+1])
    return cell if count%2==0 else 0

'''.replace('PROOF_PATH',repr(str(PROOF))).replace('PROOF_HASH',repr(sha(PROOF.read_bytes())))
    reserve='''old='            reserve = cell if profile.pair_phase_safe_breaks and not final else 0'
new='            reserve = _phase_reserve(words,spaces,start,end,profile,cell)'
if source.count(old)!=1:raise ValueError('Original conditional phase reservation source differs')
source=source.replace(old,new)

'''
    rows=[derive('dk4tool/dialogue/lil_B208_layout_v2.py','dk4tool/dialogue/lil_B208_layout_v3.py',{
        'source=inspect.getsource(layout._balanced_wrap)':helper+'source=inspect.getsource(layout._balanced_wrap)',
        'namespace={**layout.__dict__,':reserve+"namespace={**layout.__dict__,'_phase_reserve':_phase_reserve,",
    })]
    rows.append(derive('scripts/plan_lil_B208_layout_v6410.py','scripts/plan_lil_B208_layout_v6413.py',{'lil_B208_layout_v2':'lil_B208_layout_v3','lil_B208_layout_v6410':'lil_B208_layout_v6413'}))
    rows.append(derive('scripts/verify_lil_B208_fonts_v6409.py','scripts/verify_lil_B208_fonts_v6414.py',{'lil_B208_layout_v2':'lil_B208_layout_v3','fonts_v6409':'fonts_v6414'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_conditional_reservation_tools.json',dict(tools=rows,phase_proof=str(PROOF),phase_proof_sha256=sha(PROOF.read_bytes()),same216px_sixpx_font_four_rows_guard_and_pair_phase_encoder=True,only_exact_emitted_preLF_byte_is_reserved_for_printable_ASCII_progressive_prose=True,all_unknown_token_shapes_and_FE_keep_conservative_budget=True,first36_cell_rejection_and_all_existing_linter_guards_preserved=True,no_words_authored_breaks_or_QA_waivers_added=True,earlier_failed_Then_and_preparation_attempts_preserved=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B208 source-bound phase planner prepared;exact odd/even byte need only,all metrics/guards/words unchanged.')
