"""Preserve complete requests/courtesy phrases without changing words or native metrics."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B200_phrase_layout_v5846')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B200_layout_v1.py','dk4tool/dialogue/lil_B200_layout_v2.py',{
        '# No B199-only Samwell idiom rule is inherited into this source exchange.':
        "# Preserve the complete B200 reassurance transition,request and leave-taking idioms.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('still','you'),('take','care'),('care','of'),('please','accept'),('accept','it')})"})]
    tools.append(derive('scripts/plan_lil_B200_layout_v5844.py','scripts/plan_lil_B200_layout_v5847.py',{
        'layout_v5844':'layout_v5847','lil_B200_layout_v1':'lil_B200_layout_v2',
        "doc=deepcopy(read(INPUT));doc['actor172_Stranger_draft_not_applied_no_new_name_localization_completion_credit']=doc.pop('actor172_Strander_draft_not_applied_no_new_name_localization_completion_credit');image=":
        'doc=deepcopy(read(INPUT));image=',
        'manuscript_v1.json':'manuscript_v2.json','manuscript_v2.json':'manuscript_v3.json'}))
    tools.append(derive('scripts/verify_lil_B200_fonts_v5845.py','scripts/verify_lil_B200_fonts_v5848.py',{
        'fonts_v5845':'fonts_v5848','lil_B200_layout_v1':'lil_B200_layout_v2',
        'manuscript_v2.json':'manuscript_v3.json',"sum(c['kind']=='system-FE' for c in cases)==1":"sum(c['kind']=='system-FE' for c in cases)==2"}))
    before=read('translations/lil_B200_editorial_manuscript_v2.json')
    ROOT.mkdir(parents=True);save(ROOT/'complete_courtesy_requests_and_source_bound_formatter_successors.json',dict(tools=tools,
        manuscript_before='translations/lil_B200_editorial_manuscript_v2.json',manuscript_before_sha256=sha(Path('translations/lil_B200_editorial_manuscript_v2.json').read_bytes()),
        protected_pairs=[['still','you'],['take','care'],['care','of'],['please','accept'],['accept','it']],
        reasons={'40':'Keep Still with the subject of the following reassurance concern.',
            '44':'Keep Take care of yourself as a complete leave-taking sentence.',
            '62':'Keep Please accept it as a complete polite request.',
            '65':'Keep the acceptance verb and its object,and the complete take-care closing.'},
        all19_prose_wordings_controls_metrics_guards_phase_and_four_row_limits_unchanged=True,
        initial_font_test_expected_FE_count_one_corrected_to_source_owned_two_in_successor=True,
        earlier19_native_partial_planes_and_failed_producer_preserved=True,
        no_new_ROM_emulator_run_or_editorial_credit=True,full_goal_complete=False))
    print('B200 phrase-preserving successors prepared;all19 wordings/native limits unchanged. Native partial failure preserved;correct FE count is two.')
