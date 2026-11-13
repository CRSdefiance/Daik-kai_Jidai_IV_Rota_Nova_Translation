"""V1000b corrects actor-object versus actor-ID fixture preflight.

Disposable source-bound proximity, First Mate and declaration-branch fixtures.

No message selection, renderer, captain identity or battle outcome is injected.
"""
import inspect
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_full_fleet_proximity_v653 as proximity
from scripts import native_village_contexts_v618 as terrain_source
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
ROM = Path('out/all_routes_combined_v997_candidate.nds')
CASES = {'KnownJanus': (4, 0, 1), 'UnknownEmilio': (14, 0, 0),
         'ReadyEmilio': (14, 2, 1)}


def assign(arm, raw, request):
    assert request in ('approach20', *CASES) and len(raw) == 0x400000
    config = read('translations/battle_declaration_editorial_release_v1.json')
    assert sha(arm) == config['target_arm9_sha256']
    rom = NdsImage.open(ROM)
    assert arm == rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x6EE90,0x6F0C8),(0x82478,0x825E4),(0x3CD2C,0x3CD78),
             (0x7DAF0,0x7DB14),(0x3CB30,0x3CB90),(0x367C8,0x36804))
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
    source_files = [Path(proximity.__file__), Path(terrain_source.__file__)]
    source_bytes = [p.read_bytes() for p in source_files]
    if request == 'approach20':
        body = inspect.getsource(terrain_source.terrain_queries)
        old = 'out/all_routes_combined_v604_candidate.nds'
        assert body.count(old) == 1
        body = body.replace(old, str(ROM).replace('\\','/'))
        scope = dict(terrain_source.terrain_queries.__globals__)
        exec(compile(body, '<V1000-current-terrain>', 'exec'), scope)
        effective = inspect.getsource(proximity.apply_fixture)
        env = {**proximity.apply_fixture.__globals__,
               'ARM': config['target_arm9_sha256'], 'REFERENCE': ROM,
               'terrain_queries': scope['terrain_queries']}
        exec(compile(effective, '<V1000-original-20-unit-proximity>', 'exec'), env)
        after, receipt = env['apply_fixture'](arm, raw, 'approach')
        assert len(receipt['owned_bytes']) == 8
        receipt.update(declaration_context=request, original_20_unit_candidates=True,
                       actual_battle_mode_not_assigned_by_fixture=True)
    else:
        cpu, get = get_machine(arm, raw)
        actor, relation, leader_flag = CASES[request]
        root, actors, companies = get(0xCB1A8), get(0xCB184), get(0xCB160)
        captain, active, player = get(0x7F244), get(0x2E58C), get(0x397D8, companies)
        assert (captain, active, player) == (1,1,2)
        own, enemy = root+4+0x84, root+4+5*0x84
        assert get(0x35320, own) == 2 and get(0x35320, enemy) == 5
        leader = get(0x3CD2C, companies+4+5*76)
        assert actors+4 <= leader < actors+4+208*32 and (leader-actors-4)%32 == 0
        leader_id = (leader-actors-4)//32
        assert leader_id != captain
        obj = actors+4+actor*32
        assert get(0x7E100,obj) == 0 and get(0x7E0B4,obj) in (1,2,3)
        controller = root+0x2090
        model = get(0x82E04,controller)
        occupants = [get(0x82BC4,controller,n) for n in range(31)]
        fields = {}
        for slot in range(31):
            if get(0x132C0,model,slot) == 6 or occupants[slot] == actor:
                fields[controller+6+slot] = b'\xD0'
        fields[model+0x1E+12] = b'\x06'
        fields[controller+6+12] = bytes([actor])
        # Exact original 3CB30 lower-company matrix and 7DB0C byte26 branch.
        relation_at = companies+4+2*76+0x1F+5
        flag_at = leader+26
        assert raw[relation_at-BASE] in (0,2) and raw[flag_at-BASE] in (0,1)
        fields[relation_at] = bytes([relation])
        fields[flag_at] = bytes([leader_flag])
        result, owned = bytearray(raw), set()
        for at, data in fields.items():
            assert BASE <= at < BASE+len(raw)
            result[at-BASE:at-BASE+len(data)] = data
            owned.update(range(at,at+len(data)))
        after = bytes(result)
        changes = [{'address':BASE+i,'before':a,'after':b}
                   for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a != b]
        assert all(c['address'] in owned for c in changes)
        verify_cpu, verify = get_machine(arm,after)
        assert verify(0x82478,controller,1) == actor
        assert verify(0x3CB30,companies+4+5*76,2) == relation
        assert verify(0x7DB0C,leader) == leader_flag
        assert verify(0x7F244) == captain and verify(0x2E58C) == active
        for at in (obj, actors+0x19E4):
            assert after[at-BASE:at-BASE+32] == raw[at-BASE:at-BASE+32]
        receipt = {'synthetic_declaration_context_fixture':True, 'declaration_context':request,
            'First_Mate_actor_ID':actor, 'original_role_selector_82478_returns':actor,
            'target_original_fleet_ID':5,'target_company_ID':5,'target_original_leader_ID':leader_id,'target_original_leader_object':leader,
            'relation_byte_address':relation_at,'original_relation_getter_result':relation,
            'leader_branch_byte26_address':flag_at,'original_7DB0C_result':leader_flag,
            'declared_owned_fields':{str(k):v.hex() for k,v in fields.items()},'changes':changes,
            'owned_bytes':sorted(owned),'all_other4MiB_RAM_exact':True,
            'captain_and_speaker_identity_records_unchanged':True,
            'no_battle_outcome_earned_progression_or_message_ID_injection':True,
            'source_note':'367C8 is the original fallback speech actor getter; it is not a guarantee of the story captain identity.',
            'before_RAM_sha256':sha(raw),'after_RAM_sha256':sha(after)}
    assert [p.read_bytes() for p in source_files] == source_bytes
    receipt.update(fixture_sha256=sha(Path(__file__).read_bytes()),
                   unchanged_source_helpers={str(p):sha(b) for p,b in zip(source_files,source_bytes)},
                   current_ROM_sha256=sha(ROM.read_bytes()),
                   source_bound_branch_guard_spans=[list(s) for s in spans])
    return after, receipt
