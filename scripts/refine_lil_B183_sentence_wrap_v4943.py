"""Preserve a fitting first sentence before optimizing row slack in this exact batch."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B183_sentence_wrap_v4943')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    oldproof=Path('work/analysis/lil_B183_fonts_v4941/all25_progressive_FE_native_planes_and200_alignment_cases.json')
    partial=next(r for r in read(oldproof)['cases'] if r['id']=='DK4_MES_B183_R0035')
    save(ROOT/'preserved_v2_partial_question_finding.json',dict(native_proof=str(oldproof),native_proof_sha256=sha(oldproof.read_bytes()),
        record=partial,reason='Recognizing complete over there improves the wrap but slack scoring still splits a first question that fits one row.',
        not_approved_layout=True,first_comparison_producer='scripts/compare_lil_B183_wrap_v4941.py',
        first_comparison_producer_sha256=sha(Path('scripts/compare_lil_B183_wrap_v4941.py').read_bytes())))
    tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B183_layout_v2.py','dk4tool/dialogue/lil_B183_layout_v3.py',{
        'tiny final fragments,row count,andthen slack.':'tiny final fragments,row count,an intact fitting first sentence,andthen slack.',
        "namespace={**layout.__dict__":
        "# A complete first sentence that fits the unchanged guarded row wins over\n# filling two partial sentence fragments. Row count,weak boundaries and orphans\n# retain their higher priorities;all words and native guards remain unchanged.\nneedle='    count = len(words)'\nreplacement='''    count = len(words)\n    first_sentence_end = next((i for i,v in enumerate(labels) if _terminal_label(v)), None)\n    first_sentence_fits = False\n    if first_sentence_end is not None and first_sentence_end + 1 < count:\n        first_width = sum(widths[:first_sentence_end+1]) + sum(profile.glyph_width(c) for gap in spaces[1:first_sentence_end+1] for c in gap)\n        first_reserve = cell if profile.pair_phase_safe_breaks else 0\n        first_sentence_fits = first_width + first_reserve <= profile.window_width_px'''\nif source.count(needle)!=1:raise ValueError('Scoped first-sentence source differs')\nsource=source.replace(needle,replacement)\nneedle='return (0, 0, 0, 0), ()'\nif source.count(needle)!=1:raise ValueError('Scoped cost base differs')\nsource=source.replace(needle,'return (0, 0, 0, 0, 0), ()')\nneedle='tail_cost[3] + (0 if final else slack * slack),'\nreplacement='tail_cost[3] + int(first_sentence_fits and start == 0 and end < first_sentence_end),\\n                tail_cost[4] + (0 if final else slack * slack),'\nif source.count(needle)!=1:raise ValueError('Scoped slack cost differs')\nsource=source.replace(needle,replacement)\n\nnamespace={**layout.__dict__"
    }))
    tools.append(derive('scripts/plan_lil_B183_layout_v4940.py','scripts/plan_lil_B183_layout_v4944.py',{
        'lil_B183_layout_v2':'lil_B183_layout_v3','layout_v4940':'layout_v4944','lil_B183_editorial_manuscript_v4':'lil_B183_editorial_manuscript_v6'}))
    tools.append(derive('scripts/verify_lil_B183_fonts_v4941.py','scripts/verify_lil_B183_fonts_v4945.py',{
        'lil_B183_layout_v2':'lil_B183_layout_v3','fonts_v4941':'fonts_v4945','lil_B183_editorial_manuscript_v4':'lil_B183_editorial_manuscript_v6'}))
    tools.append(derive('scripts/compare_lil_B183_wrap_v4941.py','scripts/compare_lil_B183_wrap_v4945.py',{
        'lil_B183_layout_v2':'lil_B183_layout_v3','lil_B183_editorial_manuscript_v4':'lil_B183_editorial_manuscript_v6','fonts_v4941':'fonts_v4945'}))
    tools.append(derive('scripts/approve_lil_B183_native_v4942.py','scripts/approve_lil_B183_native_v4946.py',{
        'lil_B183_layout_v2':'lil_B183_layout_v3','native_approval_v4942':'native_approval_v4946','fonts_v4941':'fonts_v4945',
        'lil_B183_editorial_manuscript_v4':'lil_B183_editorial_manuscript_v6','lil_B183_editorial_manuscript_v5':'lil_B183_editorial_manuscript_v7'}))
    save(ROOT/'prepared_refinement.json',dict(tools=tools,
        intact_fitting_first_sentence_precedes_slack_only_after_weak_boundaries_orphans_and_row_count=True,
        no_changed_prose_source_command_metric_width_font_guard_or_manual_break=True,
        no_shared_or_historical_formatter_change=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('Prepared source-bound B183 v3 sentence-coherence successor;no wording,guard,width or historical-code change.')
