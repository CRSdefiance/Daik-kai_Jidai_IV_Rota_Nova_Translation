"""Prepare honest measured-state and full-screen review for the observed B203 run."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    source=Path('scripts/review_lil_B202_actual_v5993.py').read_text(encoding='utf-8')
    oldreview=next(line for line in source.splitlines() if line.strip().startswith("review='Viewed all19"))
    review="            review='Viewed all22 complete English panels and both full-screen paired sheets. The uncertain specimen observation,Chinese medicinal context,unspoken-title book explanation,expensive-looking gift hesitation,teasing companion interest and embarrassed reading request retain the full source exchange. R67 keeps the teasing clause intact after the chuckle;R70 keeps the reading admission intact after the hesitant reaction. The1000/100 gold proposals remain distinct and prospective,and the FE/FI notice remains a separate Charm+1 display. Original Lil/Mikhail/Mysterious Old Man portraits,nameplates and Mikhail middle-name omission agree;Unknown nationality remains metadata. The existing book card and generated acquired notice are unchanged. No dropped glyph,clipping,overflow,unintended or blank page was found. Both versions complete B203 and continue to unchanged B43 teaching dialogue,then later town/port UI. Source item/Local Product wording stays an unresolved separate lead. Eighteen later differences are advance-prompt pixels. Native queried final-state and PRNG measurements are retained separately;no full causal or broad simulation-equivalence claim.',"
    proof=derive('scripts/review_lil_B202_actual_v5993.py','scripts/review_lil_B203_actual_v6045.py',{
        oldreview:review,'B202':'B203','actual_review_v5993':'actual_review_v6045','actual_v5992':'actual_v6044','nineteen_actual_panels':'twenty_two_actual_panels',
        "d['complete_matching_holds']==74 and d['actual_unique_speech_panels']==d['complete_matching_observations']==19":"d['complete_matching_holds']==86 and d['actual_unique_speech_panels']==d['complete_matching_observations']==22",
        '[7657,7655]':'[8374,8373]',"len(d['actual_timing_differences'])==22 and len(d['later_whole_RGB_differences'])==21":"len(d['actual_timing_differences'])==23 and len(d['later_whole_RGB_differences'])==18",
        '[13,20,51,55,65,72]':'[21,35,54,67,70,80]',
        "selected += [('following B43',7690),('following B43',10030),('later town',12970),('prompt sample',d['later_whole_RGB_differences'][0]['frame'])]":"selected += [('offer1000',next(r for r in d['actual_panels'] if r['id'].endswith('0074'))['holds'][-1]['frame']),('accept100',next(r for r in d['actual_panels'] if r['id'].endswith('0077'))['holds'][-1]['frame']),('generated acquisition',8350),('following B43',8410),('later town',12970),('prompt sample',d['later_whole_RGB_differences'][0]['frame'])]\n        assert next(r for r in d['all_sampled_frame_comparisons'] if r['frame']==8350)['whole_RGB_equal']",
        'complete_source_matched_native_holds=74':'complete_source_matched_native_holds=86',
        'terminal_reaped_English_session=39799':'terminal_reaped_English_session=26932',
        'event202_activation':'event203_activation',
        'viewed19_panels':'viewed22_panels',
        'actual_unique_speech_panels=19,complete_native_holds=74':'actual_unique_speech_panels=22,complete_native_holds=86',
        'all26_original_commands':'all31_original_commands','all74_complete_holds':'all86_complete_holds',
        'command_timing_differences=22,later_prompt_differences=21':'command_timing_differences=23,later_prompt_differences=18',
        'English_scene_and_source_returns_observed=True':'English_scene_and_source_returns_observed=True,generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350=True',
        'source_only_names_title_context_and_prior_artifacts_preserved=True':'source_only_names_title_context_and_prior_artifacts_preserved=True,generated_item_acquired_notice_same_frame_whole_RGB_equal_at8350=True',
        'Six actual/full-screen sheets viewed;19 panels/74 native holds':'Six actual/full-screen sheets viewed;22 panels/86 native holds',
    })
    root=Path('work/analysis/lil_B203_actual_review_tools_v6045');root.mkdir(parents=True);save(root/'derivation.json',proof)
