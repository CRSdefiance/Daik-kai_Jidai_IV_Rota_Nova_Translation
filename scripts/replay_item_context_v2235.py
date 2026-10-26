"""Current original76 callers, role/voice tables, macro guards and registered type labels."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/item_context_v2235')
OLD=Path('scripts/context_item_diplomacy_v784.py')
PROVIDER=Path('work/analysis/item_diplomacy_context_v786/nominal_provider_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    expected=[r['text']for r in read(PROVIDER)['native_getter_cases']if r['getter']==0x02093D5C and r['type']<6]
    source=OLD.read_text()
    changes={
        'work/analysis/item_diplomacy_editorial_v784':'work/analysis/item_context_v2235',
        'out/all_routes_combined_v783_candidate.nds':'out/all_routes_combined_v2171_candidate.nds',
        'shared_v783_private_live2/capture_report.json':'recruitment_actual_v2202_V2171/capture_report.json',
        "'Japanese': text(get(0x93D5C, (i,))).decode('cp932')":"'current_runtime_label': text(get(0x93D5C, (i,))).decode('ascii')",
        "assert [r['Japanese'] for r in types] == ['親善', '協定締結', '協定破約', '停戦', '宣戦布告', '威圧']":"assert [r['current_runtime_label'] for r in types] == "+repr(expected),
        "'current_letter_type_values_still_Japanese': True":"'current_letter_type_values_are_registered_English': True",
        "'English_letter_type_localization_and_production_formatting_pending': True":"'current_production_formatting_recheck_pending': True",
    }
    for old,new in changes.items():
        assert source.count(old)==1,old
        source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    jp=[]
    for i in range(6):
        p=struct.unpack_from('<I',clean,0x14C5E8+4*i)[0]-0x02000000
        jp.append(clean[p:p+128].split(bytes(1))[0].decode('cp932'))
    assert jp==['親善','協定締結','協定破約','停戦','宣戦布告','威圧']
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),source_clean_six_type_labels=jp,current_expected_native_type_labels=expected,registered_provider_proof=str(PROVIDER),registered_provider_proof_sha256=sha(PROVIDER.read_bytes()),source_type_meaning_order_and_all_original_callers_preserved=True,current_genuine_prefixture_free_snapshot=True,all_original_F_IC_macro_guard_bytes_verified=True,no_new_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
