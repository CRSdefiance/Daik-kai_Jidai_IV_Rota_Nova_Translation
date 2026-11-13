"""Prepare a guarded full-width planner with one exact retained CP932 silence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_layout_tools_v7586')
PAIRS={('your','own'),('own','business'),('back','to'),('old','self'),('back','in'),('in','action'),('at','last'),('their','ship'),('lost','in'),('in','thought'),('my','great-grandfather'),('kind','of'),('papal','states'),('direct','rule'),('almost','to'),('to','venice'),('those','lands'),('papal','power'),('its','height'),('back','then'),('the','lords'),('the','pope'),('how','much'),('to','give'),('moving','goods'),('goods','around'),('these','days'),('the','church'),('hard','work'),('come','to'),('think','of'),('of','it'),('linked','to'),('turn','up'),('he','once'),('once','ruled'),('they','say'),('said','to'),('to','have'),('have','been'),('been','used'),('used','by'),('a','pope'),('carry','a'),('a','blessing'),("god's",'favor'),('he','may'),('a','point'),('we','found'),('pope','treasured'),('quite','a'),('a','discovery'),('vacant','look'),('your','face'),('on','business'),('draw','customers'),('it','was'),('trade','in'),('power','was'),('flourished','in'),('make','fortunes'),('made','fortunes')}
if __name__=='__main__':
    assert not ROOT.exists();src=Path('scripts/plan_lil_B233_layout_v7538c.py').read_text('utf8')
    oldpairs=src[src.index('PAIRS={'):src.index('\ndef display')]
    ordinary="{'DK4_MES_B233_R0012':{('scrap','of'),('library','in')},'DK4_MES_B233_R0020':{('of','ancient')},'DK4_MES_B233_R0039':{('they','deserve'),('look','for')}}"
    changes={oldpairs:'PAIRS='+repr(PAIRS)+'\n',ordinary:'{}','B233':'B234','layout_v7538c':'layout_v7586','eleven_whole_paragraph_plans':'eighteen_whole_paragraph_plans','all11':'all18',
      "def display(text):return text.replace('{MACRO:FA}','Argot')":"def display(text):return text.replace('{MACRO:FA}','Argot').replace('…','XX')",
      "row['source_selector'] in [2,23]":"row['source_selector'] in [19,104]",
      "all(32<=ord(c)<127 for c in body)":"all(32<=ord(c)<127 or c=='…' and row['id']=='DK4_MES_B234_R0005' and body=='………' and bytes.fromhex(row['source_hex'])==bytes.fromhex('68816381638163') for c in body)",
      'leading_speaker_bytes=frozenset([2,23])':'leading_speaker_bytes=frozenset([19,104])',
      'native_complete_pages_and_source_specific_controls_pending=True':'native_complete_pages_and_source_specific_controls_pending=True,only_exact_source_R5_three_CP932_ellipses_allowed_no_global_non_ASCII_exception=True,source_bound_printable68_selector_not_generic_ASCII_prefix=True',
    }
    checked_text(src,changes);row=derive('scripts/plan_lil_B233_layout_v7538c.py','scripts/plan_lil_B234_layout_v7586.py',changes);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_full_width_layout.json',dict(tool=row,complete_prose_unchanged=True,source_R5_exact_three_CP932_ellipsis_glyphs_only=True,no_general_CP932_orprintable_selector_relaxation=True,native_geometry_guards_pair_phase_literal_I_andall_native_constants_preserved=True,all_individual_native_formatting_gates_pending=True,new_credit=0,full_goal_complete=False))
