"""Record actually viewed source scenes and current speaker-label evidence."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_source_view_v6184')
PATHS=Path('work/analysis/lil_B205_source_paths_v6182/one_actual_source_path_and_complete_command_intervals.json')
RETURN=Path('work/analysis/lil_B205_source_return_v6183/complete_source_return_and_following_block.json')
CAT=Path('work/analysis/lil_B205_voices_v6173/current207_catalog_eight_voices_and_two_source_selectors.json')
if __name__=='__main__':
    assert not ROOT.exists();paths,ret,cat=map(read,[PATHS,RETURN,CAT])
    sheets=paths['review_sheets']+paths['transition_sheets']+[dict(path=ret['sheet'],sha256=ret['sheet_sha256'])]
    assert len(sheets)==9 and paths['stored_source_objects']==17 and paths['unvisited_source_indices']==[]
    for r in sheets:assert sha(Path(r['path']).read_bytes())==r['sha256']
    jp=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');p=struct.unpack_from('<I',jp,0x11E210+147*24)[0];raw=jp[p-0x02000000:].split(b'\0',1)[0];assert raw.decode('cp932')=='七色のオウム'
    rows={r['actor_ID']:r for r in cat['catalog']['rows']};assert rows[164]['current_catalog_name']=='Man' and rows[165]['current_catalog_name']=='Woman'
    assert paths['source_end616_return_frame']==7175 and ret['first_following_SC_command']['frame']==8382 and ret['final_following_observed_command']['frame']==11976
    ROOT.mkdir(parents=True);save(ROOT/'complete_source_scenes_and_return_visual_review.json',dict(
        viewed_sheets=sheets,all17_Japanese_objects_five_FE_echoes_and_two_sound_captions_viewed=True,
        actual_nameplates=['Angelo Puccini','Lil Argot'],source_owned_names_and_voice_proof='work/analysis/lil_B205_source_names_v6175/two_exact_source_name_fields_voices_and_distinct_name_consumers.json',
        all_seven_FE_objects_have_no_human_nameplate_or_portrait=True,
        actual_item_widget='Rainbow Parrot / Gift / dash; multicolored parrot image',
        item147_source=dict(record_offset=0x11E210+147*24,pointer=p,source_hex=raw.hex(),Japanese=raw.decode('cp932')),
        item_title_retention_reason='七色 means seven-colored or rainbow-colored in this item name. Rainbow Parrot naturally conveys the multicolored bird and matches the observed widget without inventing a specific species. No new item-name bytes or name-review credit.',
        source_sequence_notes='Wing flaps,Angelo surprise,five exact mimicry beats,Lil parrot identification,Angelo catch attempt,ordered impacts/flaps/rustling,Lil capture announcement,Angelo boast,parrot echo,Lil laughing payoff. Portraits identify Lil and Angelo;FE has the item widget but no human actor header. No visible capture animation identifies a special mechanism or supports Angelo being captured. The last FE is the bird echoing the victory taunt;Lil laughs at the captured bird sounding unwilling to admit defeat.',
        source55_omits_capture_agent_and_object=True,no_invented_cage_weapon_injury_pet_bond_or_Angelo_capture=True,
        actual_generated_notice_at7150='Rainbow Parrot acquired!',notice_not_eighteenth_stored_object_or_new_generic_notice_approval=True,
        complete25_source_plus9_initializer_commands_observed=True,scene_end7175=True,
        return_notes='7210 port UI;7630 Port Worker resupply prompt;8350 Sail/Auto Move/Deck View menu;B120 begins8382,8470 shows Lil with black upper background. Last B120 command is the complete end at11976,offset2312. Frame13001 shows sailing/Sea View after the conversation has completed. The earlier derived return script print says remains observed at13001;its exact command-frame data instead records the completed end at11976. This receipt disambiguates that wording without altering the frozen producer.',
        initialized_Amsterdam_content_fixture_not_original_location_or_natural_event205_activation=True,
        request_for_retrospective_speaker_localization_reaffirmed=True,
        current_screenshot_pair_names=[rows[164],rows[165]],
        screenshot_label_already_revised_in_V5891_and_preserved_in_current_V6160=True,
        all207_names_role_labels_aliases_and_other_consumers_review_remains_open=True,
        approved_names_preserved=['Rafael','Hodram','Joakim','Maria','Camille'],
        no_marriage_age_kinship_rank_or_biography_inferred_from_portraits_or_internal_labels=True,
        actual_source_run_only_not_English_display_or_full_route_hardware_proof=True,
        no_new_ROM_ledger_or_review_credit_change=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PATHS,RETURN,CAT,Path(__file__)]}))
    print('Nine source sheets reviewed:all17 objects,5 echoes,2 sound captions and completed return. Current Man/Woman pair confirmed;all207 review stays open;zero credit.')
