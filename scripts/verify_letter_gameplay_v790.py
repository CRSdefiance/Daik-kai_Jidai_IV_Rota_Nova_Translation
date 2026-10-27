"""Original six-type dialogs,complete English type arguments and cancellation."""

import inspect,struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_item_transactions_v789 as prior
from scripts.native_call_abi_v764 import call
from scripts.native_letter_eligibility_v790 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/letter_eligibility_v790')
SELECTED={6000:1097,6400:1117,8000:1098,8800:1113,10000:1098,10800:1103,11600:1108,
    13600:1098,14400:1113,16800:1098,17600:1113,20400:1098,21200:1139,22000:1098,22800:1113}
KINDS={8000:2,8800:2,10000:1,13600:3,14400:3,16800:4,17600:4,20400:5,22000:0,22800:0}
PHRASES=('goodwill letter','pact proposal','pact termination notice','truce proposal','declaration of war','demand for submission')
PHASES=[]


def control(frame,diff,image):
    if diff.getbbox() is None:return
    assert frame in (11200,14000,17200,20800),(frame,diff.getbbox())
    path=prior.CAP/'letter_eligibility_v790_phase_control/capture_report.json'
    report=read(path);old=read(prior.CAP/'letter_eligibility_v790_baseline/capture_report.json')
    assert report['ROM_sha256']==old['ROM_sha256'] and report['scripted_input_schedule']==old['scripted_input_schedule']
    observer=report['letter_phase_observer']
    assert observer['original_controller_schedule_and_game_logic_unchanged']
    assert observer['adapter_sha256']==sha(Path('scripts/run_letter_phase_v790.py').read_bytes())
    assert observer['fixture_sha256']==sha(Path('scripts/native_letter_eligibility_v790.py').read_bytes())
    frames={r['frame']:r for r in report['frames_captured']};originals={r['frame']:r for r in old['frames_captured']}
    for f in (3200,6000,6400,8000,8800,10000,10800,11600,13600,14400,16800,17600,20400,21200,22000,22800,24000):
        assert Image.open(frames[f]['path']).convert('RGB').tobytes()==Image.open(originals[f]['path']).convert('RGB').tobytes()
    matches=[]
    for f,row in frames.items():
        if frame-100<=f<=frame:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
            if Image.open(row['path']).convert('RGB').tobytes()==image.tobytes():matches.append(f)
    assert matches,(frame,'no complete original full-frame phase matches')
    PHASES.append({'frame':frame,'complete_original_whole_frame_matches':matches,'capture_report':str(path),
        'capture_report_sha256':sha(path.read_bytes()),'no_rectangular_pixel_exclusion':True})


def fixture(report,rom,ram):
    fixtures=report['synthetic_condition_fixtures']
    assert len(fixtures)==1 and fixtures[0]['frame']==3200
    arm=rom.read_file('/__arm9__.bin')
    _,proof=set_condition(arm,ram[3200],{'mode':'Istanbul-letter-eligibility'})
    assert fixtures[0]=={**proof,'frame':3200}
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_condition_fixtures')
    adapter=report['letter_eligibility_adapter']
    assert adapter['single_import_replacement'] and adapter['no_dialogue_menu_or_outcome_logic_replacement']
    for key,path in (('adapter_sha256','scripts/run_letter_eligibility_v790.py'),
                     ('fixture_sha256','scripts/native_letter_eligibility_v790.py'),
                     ('original_harness_sha256','scripts/headless_desmume_v193.py')):
        assert adapter[key]==sha(Path(path).read_bytes())


def nominal(arm,kind):
    cpu=machine(arm);call(cpu,0x93D5C,(kind,))
    return bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0),128)).split(b'\0')[0]


def arguments(frame,n,old,new,oa,arm):
    if frame in KINDS:
        kind=KINDS[frame]
        assert old[-1]==nominal(oa,kind)
        assert new[-1]==nominal(arm,kind)==PHRASES[kind].encode()
        assert old[:-1]==new[:-1]
        if n==1113: assert new[0]==(b'Albuquerque' if kind==3 else b'Castor Co.')
    else:
        assert old==new
        if n==1108: assert new==(b'Castor Co.',b'Albuquerque')
        if n==1139: assert new==(b'Castor Co.',)


def outcomes(arm,ram,states):
    assert len(states)==53
    cash={r['frame']:r['cash'] for r in states}
    assert set(cash.values())=={8371}
    assert prior.models(arm,ram[3600])==prior.models(arm,ram[24000])
    assert prior.persistent_objects(arm,ram[3600])==prior.persistent_objects(arm,ram[24000])
    assert prior.tasks(arm,ram[3600])==prior.tasks(arm,ram[24000])
    cpu=machine(arm);cpu.mem_write(0x02000000,ram[3600]);call(cpu,0xCB1B4,())
    clock=cpu.reg_read(UC_ARM_REG_R0)+8
    initial=struct.unpack_from('<I',ram[3600],clock-0x02000000)[0]
    assert all(struct.unpack_from('<I',raw,clock-0x02000000)[0]==initial for f,raw in ram.items() if f>=3200)
    save(ROOT/'cancellation_outcomes.json',{'cash8371_preserved_all53_native_snapshots':True,
        'calendar_ticks_unchanged':initial,'all_covered_postfixture_models_objects_and_tasks_return_exact':True,
        'no_courier_registration_or1000_coin_charge_on_cancellation':True,'normal_town_return_frame':24000,
        'successful_delivery_and_CScheme_object_menu_not_claimed':True})


def main():
    source=inspect.getsource(prior.load)
    replacements={"report['frames'] == 15600":"report['frames'] == 24000",
        "'942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f'":"'d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'",
        "    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))\n":"",
        "    return path, report, rom, frames, ram":"    fixture(report,rom,ram)\n    return path, report, rom, frames, ram"}
    for before,after in replacements.items():
        assert source.count(before)==1,before
        source=source.replace(before,after)
    body=inspect.getsource(prior.main)
    a=body.index("    cash = {r['frame']:r['cash'] for r in states}")
    b=body.index("    save(ROOT/'ordinary_transactions_gameplay.json'",a)
    body=body[:a]+'    outcomes(arm,new_ram,states)\n'+body[b:]
    replacements={"'item_transactions_v789_baseline'":"'letter_eligibility_v790_baseline'",
        "'item_transactions_v789_live'":"'letter_eligibility_v790_live'",
        'assert old_match and old_match.groups() == args':'assert old_match\n        arguments(f,n,old_match.groups(),args,oa,arm)',
        "assert diff.getbbox() is None, (f, 'unselected full screen', diff.getbbox())":"control(f,diff,b)",
        "ROOT/'ordinary_transactions_gameplay.json'":"ROOT/'actual_letter_dialogs.json'",
        "'purchase_7700_sale_6160_original_outcomes_preserved':True,'both_declines_preserve_cash':True,":"'all_cancelled_letter_flows_preserve_cash_calendar_and_courier_records':True,",
        "'fleet_ships_and_persistent_objects_return_to_original_state':True,":"'postfixture_fleet_ships_and_persistent_objects_return_exact':True,",
        "'company_cash_change_is_expected_transaction_result_not_a_preservation_failure':True,":"'original_target_filters_and_all_six_nominal_argument_getters':True,",
        "'normal_town_return_frame':15600,'no_fixtures_or_savestates':True,":"'normal_town_return_frame':24000,'eight_disclosed_qualification_bytes_no_savestates':True,",
        '7700 purchase,6160 sale,both declines and town return pass.':'all six letter questions,confirmations and cancellation/return pass.'}
    for before,after in replacements.items():
        assert body.count(before)==1,before
        body=body.replace(before,after)
    program=source+'\n\n'+body
    path=ROOT/'effective_actual_letter_verifier.py';path.write_text(program,encoding='utf-8')
    env={**prior.__dict__,'ROOT':ROOT,'SELECTED':SELECTED,'fixture':fixture,'arguments':arguments,
        'outcomes':outcomes,'control':control,'__file__':str(Path(__file__).resolve())}
    exec(compile(program,str(path),'exec'),env);env['main']()
    result=read(ROOT/'actual_letter_dialogs.json')
    result['strict_whole_screen_controls']=[f for f in result['strict_whole_screen_controls'] if f not in {r['frame'] for r in PHASES}]
    result['original_whole_frame_faction_highlight_controls']=PHASES
    font=GameAsciiFont.from_arm9(prior.NdsImage.open('out/all_routes_combined_v788_candidate.nds').read_file('/__arm9__.bin'))
    image_path=prior.CAP/'letter_eligibility_v790_live/frame_006800_navigation.png'
    image=Image.open(image_path).convert('RGB')
    labels=[dark_text(font,text,image,(90,226+i*20,175,248+i*20)) for i,text in enumerate(
        ('Goodwill','Sign Pact','Break Pact','Truce','Declare War','Threaten'))]
    result.update({'effective_program_sha256':sha(program.encode()),'frozen_base_verifier_sha256':sha(Path(prior.__file__).read_bytes()),
        'all_six_actual_command_labels_complete_native_ink_and_blank_cells':labels,
        'menu_capture':str(image_path),'menu_capture_sha256':sha(image_path.read_bytes()),
        'all_six_complete_nominal_phrases_used_by_real_questions':list(PHRASES),
        'source_eligibility_proof':str(ROOT/'native_eligibility_verification.json'),
        'not_a_CScheme_virtual_name_menu':True,'full49_entry_family_still_open':True})
    save(ROOT/'actual_letter_dialogs.json',result)


if __name__=='__main__':main()
