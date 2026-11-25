"""One prose correction;preserve the entire existing runtime and selector bank."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
from dk4tool.patch.ship_sinking_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import ship_sinking_native_plan_v1330 as previous
from scripts.battle_aftermath_layout_v1250 import paragraph
from scripts.ship_sinking_runtime_v1328 import CONTRACTS,TABLE_BYTES,GATE,GATE_BYTES
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_precision_payload_v1356')
MANUSCRIPT = Path('translations/flagship_capture_precision_manuscript_v1.json')
IDS = (2015,)
PROFILE = 'flagship-capture-precision-portrait-postmacro-v1'
SOURCE_COMMON = '0917556051ef3df291dc5db75aa9a17ae432ce2a492e5176715a985f376187ee'
SOURCE_ARM = 'e3728b9c7358d4e482191516831bd3e521243a788ad0297105e683d386b12583'


def compiled(row):
    assert row['message_id']==2015
    return b' '+paragraph(row)


def unchanged_runtime(arm):
    assert sha(arm)==SOURCE_ARM
    return arm,{'patches':[],'entire_existing_runtime_selector_bank_gate_code_and_allocations_preserved':True}


def plan(common,arm,doc):
    env = {**previous.__dict__,'current_entries':current_entries,'IDS':IDS,'PROFILE':PROFILE,
        'SOURCE_COMMON':SOURCE_COMMON,'SOURCE_ARM':SOURCE_ARM,'compiled':compiled,
        'runtime':SimpleNamespace(apply=unchanged_runtime)}
    c,a,proof = FunctionType(previous.plan.__code__,env,argdefs=previous.plan.__defaults__)(common,arm,doc)
    for start,size in [(CONTRACTS,TABLE_BYTES),(GATE,GATE_BYTES)]:
        at = start-0x02000000
        assert a[at:at+size]==arm[at:at+size]
    proof.pop('all3652_unselected_texts_and_native_copy_spans_preserved')
    proof.pop('only_COMMON22_native_metadata_and_existing188_byte_table_changed')
    proof.update(all3667_unselected_texts_and_native_copy_spans_preserved=True,
        only_COMMON22_and_original_native_offset_directory_data_changed=True,
        entire188_byte_selector_and172_byte_gate_and_all_runtime_code_exact=True)
    return c,a,proof


def main():
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    rom = NdsImage.open(doc['current_ROM'])
    c,a,proof = plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    ROOT.mkdir(parents=True)
    cp,ap = ROOT/'COMMON_RESEARCH_ONLY.DK4',ROOT/'ARM9_PAYLOAD_RESEARCH_ONLY.bin'
    cp.write_bytes(c)
    ap.write_bytes(a)
    save(ROOT/'native_payload_plan.json',{**proof,'target_COMMON':str(cp),'target_ARM9':str(ap),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_ROM_registry_or_completion_change':True,'full_goal_complete':False})
    print('Only2015 repacked;all3667 other texts and every runtime/table/code/allocation byte preserved.',flush=True)


if __name__=='__main__':
    main()
