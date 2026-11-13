"""Use measured FE text capacity;preserve the failed wider host plan and all prose."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B204_capacity_tools_v6126');PROOF=Path('work/analysis/lil_FE_row_capacity_v6125/original228px_descriptor_native36_ASCII_row_capacity.json')
if __name__=='__main__':
    assert not ROOT.exists();p=read(PROOF);assert p['thirty_seventh_ASCII_glyph_wraps_to_y12_at_x0'] and len(p['cases'])==8
    extra=repr(str(PROOF))+':'+repr(sha(PROOF.read_bytes()))+','
    tools=[derive('dk4tool/dialogue/lil_B204_profile.py','dk4tool/dialogue/lil_B204_profile_v2.py',{
        'DEPENDENCIES={':'DEPENDENCIES={'+extra,
        'window_width_px=228':'window_width_px=216',
        'Host planning uses the actual228px width;no native viewport,font,clip,guard,pair-phase or four-row change.':'Eight original native capacity probes establish36 printable ASCII glyphs per row despite the228px bitmap descriptor. Host planning uses measured216px text capacity;no native viewport,font,clip,guard,pair-phase or four-row change.',
    })]
    tools.append(derive('dk4tool/dialogue/lil_B204_layout_v1.py','dk4tool/dialogue/lil_B204_layout_v2.py',{"profile.window_width_px!={'lil-B204-progressive-runtime-bound-v1':216,'lil-B204-FE-runtime-bound-v1':228}[profile.name]":'profile.window_width_px!=216'}))
    tools.append(derive('scripts/plan_lil_B204_layout_v6123.py','scripts/plan_lil_B204_layout_v6126.py',{
        'layout_v6123':'layout_v6126','lil_B204_layout_v1':'lil_B204_layout_v2','dk4tool.dialogue.lil_B204_profile':'dk4tool.dialogue.lil_B204_profile_v2',
        'dk4tool/dialogue/lil_B204_profile.py':'dk4tool/dialogue/lil_B204_profile_v2.py',
        "INPUT=Path('translations/lil_B204_editorial_manuscript_v1.json')":"INPUT=Path('translations/lil_B204_editorial_manuscript_v2.json')", "OUTPUT=Path('translations/lil_B204_editorial_manuscript_v2.json')":"OUTPUT=Path('translations/lil_B204_editorial_manuscript_v3.json')",
    }))
    tools.append(derive('scripts/verify_lil_B204_fonts_v6124.py','scripts/verify_lil_B204_fonts_v6127.py',{
        'fonts_v6124':'fonts_v6127','lil_B204_layout_v1':'lil_B204_layout_v2','dk4tool.dialogue.lil_B204_profile':'dk4tool.dialogue.lil_B204_profile_v2','dk4tool/dialogue/lil_B204_profile.py':'dk4tool/dialogue/lil_B204_profile_v2.py','manuscript_v2':'manuscript_v3',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_capacity_correction.json',dict(tools=tools,source_native_capacity_proof=str(PROOF),source_native_capacity_proof_sha256=sha(PROOF.read_bytes()),failed228_host_profile_plans_previews_and_producers_preserved=True,all20_English_words_and_source_commands_exact=True,native_addresses_viewport_metrics_clip_guards_pair_phase_and_four_rows_unchanged=True,corrected_current_native_planes_and_actual_English_still_required=True,full_goal_complete=False));print('Measured216px FE capacity bound;failed228px plan retained. All prose and native behavior unchanged;new complete checks required.')
