"""Bind all nine subordinate roles and nine complete clean context samples; no global rename."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retainer_name_triage_v7744')
CENSUS=Path('work/analysis/retainer_speaker_uses_v7740/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json')
NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
SAMPLES={
('/data/SC0.DK4',13):"Three-speech hostile encounter:an unnamed follower cheers andthe named leader threatens FO withsinking. No personal name ornew rank isgiven.",
('/data/SC0.DK4',53):"Three-speech player aide exchange:the subordinate reports a Portuguese regular-army summons andthe admiral decides togo tothe palace. The source role isnot anarmy rank andbrother-style speech isnot kinship.",
('/data/SC3.DK4',263):"Three-speech discovery exchange:Maria asks what anobject is;the subordinate offers todig;Maria tentatively callsit anold coin. Digging alone establishes no specific naval occupation.",
('/data/SC0.DK4',203):"Thirteen-speech dye discussion withashopkeeper:the subordinate urges buying before other shops buythe dye,manages the merchant's hesitation andpromises profit. This sales-assistant context doesnot independently establish Sailor. No family inference from親父さん.",
('/data/SC0.DK4',270):"Thirteen-speech pirate-boss/follower exchange:underlings giveaway Jakob's name andflee,leaving him toRafael. 兄貴/親分 aregroup address,not proof ofblood kinship. A universal loyal-crewmate label wouldmiss their different allegiance.",
('/data/SC0.DK4',199):"Sixteen-speech illness/almond-remedy rumor between a subordinate andshopkeeper:one coughs,asks whether analmond medicine works anddecides tolook forit. No ship,naval occupation,diagnosis orverified cure isestablished.",
('/data/SC0.DK4',202):"Seventeen-speech rumor aboutahousehold master's supposedly cured unexplained illness andover-the-counter medicine;the two men decide tobuy some. This doesnot establish the speaking subordinate asamedic,household retainer ornoble officer.",
('/data/SC0.DK4',214):"Nineteen-speech unsolicited book handoff andpursuit:the unnamed subordinate thrusts abook onRafael andleaves whileanother man chases him;the companion laterrecognizes aglassmaking dictionary. No job title,rank orownership entitlement isproved.",
('/data/SC0.DK4',87):"Forty-two-speech Japan encounter:Kurushima's subordinate stages aninjury claim andjoins athreatening group;Shiraki intervenes andlaterrequests totravel withRafael. This henchman context differs fromthe player's aide. Keep samurai,cultural perspectives andgroup address withoutinventing family ties ornew ranks.",
}
if __name__=='__main__':
    assert not ROOT.exists();census,prior=map(read,[CENSUS,NAMES]);chosen=list(range(151,160))
    assert census['source_blocks_scanned']==1307 and len(census['selected_native_blocks'])==147
    assert sum(len(b['direct_retainer_speech_records']) for b in census['selected_native_blocks'])==484
    sample=[]
    for key,reason in SAMPLES.items():
        b=next(b for b in census['selected_native_blocks'] if (b['file_path'],b['block'])==key)
        sample.append(dict(file_path=b['file_path'],block=b['block'],source_block_sha256=b['source_block_sha256'],
            full_clean_exchange_records=deepcopy(b['all_speech_records']),complete_exchange_name_context_finding=reason,
            clean_only_no_current_English_dialogue_exposure=True,no_new_translation_orcompletion_credit=True))
    assert sum(len(b['full_clean_exchange_records']) for b in sample)==129
    assert {r['source_selector'] for b in sample for r in b['full_clean_exchange_records'] if r['source_selector'] in chosen}==set(chosen)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');fields=[]
    for ident in chosen:
        columns=[]
        for col,kind in [(0,'given-name-or-role'),(4,'regional-metadata-not-surname'),(8,'middle-name')]:
            at=0x120B80+32*ident+col;columns.append(dict(kind=kind,table_field=at,**string(clean,struct.unpack_from('<I',clean,at)[0])))
        fields.append(dict(actor_ID=ident,clean_fields=columns))
    adapter=checked_text(prior['source_owned_name_adapter'],{'all_sixteen_original_consumers':'all_eighteen_original_consumers'})
    ns={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(adapter,__file__+'::nine-static-roles-eighteen-getters','exec'),ns)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(ns['names']);ctx.machines.pop()
    assert len(native['rows'])==18 and not ctx.machines
    save(ROOT/'nine_roles18_getters147_source_blocks484_uses_nine_context_samples.json',dict(
        source_census=str(CENSUS),source_census_sha256=sha(CENSUS.read_bytes()),source_blocks_scanned=1307,selected_source_blocks=147,direct_source_role_speeches=484,
        complete_speeches_in_census=3150,all3150_not_claimed_editorially_reviewed=True,complete_sample_exchanges=sample,clean_sample_speeches_read_forname_triage=129,
        original_clean_nine_name_fields=fields,current_original_eighteen_name_consumers=native,source_owned_name_adapter=adapter,
        source_role_is_subordinate_follower_without_universal_nautical_job_ornew_rank=True,
        exact_scene_context_can_be_player_aide_company_employee_outsider_oropposing_henchman=True,
        no_universal_replacement_selected_from_these_samples=True,all147_contexts_indirect_roles_typed_uses_andother_UI_consumers_still_open=True,
        direct4000_census_not_exhaustive_dynamic_role_orother_UI_coverage=True,
        no_name_asset_ROM_registry_ledger_orcredit_changes=True,full207_names_roles_aliases_goal_active=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [CENSUS,NAMES,INPUT,Path(__file__)]},new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('Nine shared roles:18native name getters;147clean blocks/484direct uses;9complete name-context samples/129speeches. All3150not claimed reviewed.No replacement orcredit.')
