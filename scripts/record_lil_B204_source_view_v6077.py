"""Record nine reviewed source/context sheets without adding English approval or credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_source_view_v6077')
PATHS=Path('work/analysis/lil_B204_source_paths_v6072/one_actual_source_path_and_complete_command_intervals.json')
RETURN=Path('work/analysis/lil_B204_source_return_v6076/complete_source_return_and_following_block.json')
if __name__=='__main__':
    assert not ROOT.exists();paths,ret=map(read,[PATHS,RETURN]);sheets=paths['review_sheets']+paths['transition_sheets']+[dict(path=ret['sheet'],sha256=ret['sheet_sha256'])]
    assert len(sheets)==9 and paths['stored_source_objects']==20 and paths['unvisited_source_indices']==[]
    for r in sheets:assert sha(Path(r['path']).read_bytes())==r['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'complete_source_scenes_and_return_visual_review.json',dict(viewed_sheets=sheets,all20_Japanese_objects_four_FE_letter_parts_and_full_signature_viewed=True,
        observed_nameplates=['Jam Ludwyan','Innkeeper','Lil Argot','Guard','Daimyo'],
        nameplate_decisions=[dict(label='Innkeeper',reason='宿屋のおばさん identifies the innkeeper role;English avoids an invented aunt or gratuitous age qualifier.'),dict(label='Guard',reason='衛兵 supports the guard role without an invented officer rank.'),dict(label='Daimyo',reason='大名 is a Japanese lord\'s established cultural title;retain it rather than invent royalty.'),dict(label='Jam Ludwyan',reason='The original progressive consumer omits the source middle name;the letter uses the separately bound full Jam Jack Ludwyan signature.'),dict(label='Lil Argot',reason='Established source-owned proper name,with distinct source voice preserved.')],
        actual_item_widget='Orca Figurehead / Figurehead / dash with upturned castle-ornament image',item_title_source_fidelity_risk_open=True,
        FE_panels_have_no_actor_portrait_or_nameplate=True,source43xx_picture47xx_A000_and_letter_sequence_observed_without_full_effect_claim=True,
        scene_end7894_followed_by_port_UI_then_B120_at9101=True,
        exact_observation_notes='Frame7930 shows port UI;8350 Port Worker resupply question;9070 port Sail/Auto Move/Deck View menu. Following SC2B120 is on a black upper background at9190 and13001,with Lil then Camille. Do not describe an idle-town final endpoint,a B43 tutorial or a generated item-acquisition notice not captured here.',
        initialized_Amsterdam_content_fixture_not_original_location_or_natural_event204_activation=True,
        all207_names_review_and_all_other_editorial_scope_remain_open=True,no_English_native_format_or_release_approval=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PATHS,RETURN,Path(__file__)]}))
    print('Nine source sheets reviewed:20objects/fourletterparts/roles/item risk/real port-to-B120 continuation. No English approval or credit.')
