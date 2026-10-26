"""All3 original current modal consumers; current captured heap, no SDK widget claim."""
import inspect
from pathlib import Path
from scripts import verify_arrival_consumer_v792 as original
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/courier_context_v2238')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot']
    program=inspect.getsource(original.main)
    for old,new in(
        ("arm=(ROOT/'ARM9_RESEARCH_ONLY.bin').read_bytes()","arm=NdsImage.open(ROM).read_file('/__arm9__.bin')"),
        ("raw_path='E:/Rota Nova translations/Generated/work/emulation_v193/letter_delivery_v791_recovered/frame_017200_arm9_ram.bin'",'raw_path='+repr(snapshot['path'])),
        ('arrival_notices_editorial_manuscript_v2.json','arrival_notices_editorial_manuscript_v3.json'),
        ("        s=MainCodeFile(arm,BASE).sections[4];cpu.mem_write(s.ramAddress,bytes(s.data))\n",''),
    ):
        assert program.count(old)==1,old
        program=program.replace(old,new)
    env={**original.__dict__,'ROOT':ROOT,'ROM':ROM,'__file__':__file__}
    exec(compile(program,__file__,'exec'),env);env['main']()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x91598,0x93BAC),(0xCB240,0xCB3C8),(0x546B8,0x5479C))
    assert all(arm[a:b]==clean[a:b]for a,b in spans)
    old=Path('work/analysis/letter_delivery_v791/delivery_verification.json')
    save(ROOT/'current_replay_provenance.json',dict(original=str(Path(original.__file__)),original_sha256=sha(Path(original.__file__).read_bytes()),effective_source_sha256=sha(program.encode()),current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),current_ARM9_sha256=sha(arm),current_snapshot=snapshot,original_courier_lifecycle_and_modal_consumer_source_clean_exact=[dict(span=[a,b],sha256=sha(arm[a:b]))for a,b in spans],historical_lifecycle_proof=str(old),historical_lifecycle_proof_sha256=sha(old.read_bytes()),historical_recovered_v791_report_contains_superseded_formatting_defects_not_current_visual_approval=True,current3_consumer_expected_bytes_use_v3_registered_wording=True,source346_refuses_receipt_not_acceptance_of_a_pact=True,no_actual346_activation_or_current_lifecycle_outcome_claim=True,no_full_static_section_reload_over_live_heap=True,no_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
