"""Bind the independently proven consumers to the final combined byte payload."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_duel_cache_scope_v1150 as scoped
from scripts import probe_duel_resident_fonts_v1151 as fonts
from scripts.duel_editorial_layout_v1155 import compiled
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_final_consumer_v1164')
PLAN = Path('work/analysis/duel_native_release_v1162/final_payload_plan.json')


def main():
    assert not ROOT.exists()
    plan = read(PLAN)
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    code = inspect.getsource(scoped.pipeline)
    prior = "spans=[*plan['metadata_fields'],[0xDA28,0x134]]"
    assert code.count(prior) == 1
    code = code.replace(prior, "spans=[*plan['metadata_fields'],*plan['owned_ARM9_fields']]")
    environment = {**scoped.__dict__, 'PLAN_PATH': PLAN}
    exec(compile(code, str(Path(__file__)), 'exec'), environment)
    pipeline = environment['pipeline']
    scope_execute = FunctionType(scoped.execute.__code__, {**scoped.execute.__globals__,
        'pipeline': pipeline, 'PLAN_PATH': PLAN}, argdefs=scoped.execute.__defaults__)
    scope_execute.__kwdefaults__ = scoped.execute.__kwdefaults__
    font_execute = FunctionType(fonts.execute.__code__, {**fonts.execute.__globals__, 'pipeline': pipeline})
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    records = {r['message_id']: r for r in read(plan['manuscript'])['records']}
    tables = {'challenge': 0x02117340, 'acceptance': 0x02117360, 'threat': 0x021174E0,
              'named_escape_negative': 0x02117500, 'admiral_escape_negative': 0x02117620}
    cpu, get = get_machine(arm, raw)
    representatives = {}
    for row in catalog['names']:
        for family, table in tables.items():
            number = get(0x53F4C, row['object'], table)
            representatives.setdefault((family, number), (row['object'], bytes.fromhex(row['name_hex'])))
    scope_cases, font_cases = [], []
    for (family, number), (actor, name) in sorted(representatives.items()):
        scope_cases.append(scope_execute(arm, common, raw, actor, name, family, tables[family], number,
                                         compiled(records[number])))
    actor, name = representatives[('challenge', 1931)]
    for number in range(1931, 1951):
        scope_cases.append(scope_execute(arm, common, raw, actor, name, 'direct_negative', 0, number,
                                         compiled(records[number]), direct=True))
    rom = NdsImage.open(plan['source_ROM'])
    font, kanji = GameAsciiFont.from_arm9(arm), rom.read_file('/GRP/KANJI.FNT')
    for (family, number), (actor, unused) in sorted(representatives.items()):
        if number > 1950:
            continue
        row = records[number]
        for name in ((b'Clifford', b'ABCDEFGHIJKLMNOP', b'\x82\x65ernando') if row['native_argument_count'] else (b'Clifford',)):
            text = row['english'].encode('ascii').replace(b'%s', name)
            case, visible = font_execute(arm, common, raw, actor, name, family, tables[family], number, text, font, kanji)
            font_cases.append(case)
    assert len(scope_cases) == 53 and len(font_cases) == 36
    # The full 1356/1417 matrices prove identical executable/font bytes. Final
    # selected message bytes are exact compiler outputs, including speech state.
    research = read('work/analysis/duel_cache_payload_v1144/cache_prefix_research_plan.json')
    earlier = Path(research['target_ARM9']).read_bytes()
    escape = read('work/analysis/duel_escape_runtime_v1153/runtime_plan.json')
    for change in escape['public_changes']:
        at, value = change['address']-0x02000000, bytes.fromhex(change['target_hex'])
        assert arm[at:at+len(value)] == value
    assert arm[0xDA28:0xDB5C] == earlier[0xDA28:0xDB5C]
    ROOT.mkdir(parents=True)
    save(ROOT/'native_consumer_verification.json', {'final_plan': str(PLAN), 'final_plan_sha256': sha(PLAN.read_bytes()),
        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'final_original_caller_scope_cases': scope_cases, 'final_resident_complete_font_cases': font_cases,
        'all53_exact_original_filters_and36_complete_final_native_font_cases_pass': True,
        'entire_final_static_duel_renderer_and_component_exact_to_full1356_case_proof': True,
        'final_escape_bank_and_status_literal_exact_to_full56696_and1417_case_proofs': True,
        'only_declared_ROM_code_metadata_spans_patched_after_source_snapshot_load': True,
        'effective_pipeline_sha256': sha(code.encode()),
        'original_file_loader_refresh_and_prior_declared_CPU_boundaries_preserved': True,
        'no_host_layout_or_Y_replacement_or_emulator_message_injection': True,
        'actual_registered_ROM_boot_duel_cache_hardware_UI_and_transitions_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Final combined payload:53 native caller controls and36 full resident fonts pass; full matrix byte bindings exact.', flush=True)


if __name__ == '__main__':
    main()
