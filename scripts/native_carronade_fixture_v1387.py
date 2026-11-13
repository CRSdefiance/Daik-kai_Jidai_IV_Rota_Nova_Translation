"""Successor prebattle loadout:original Carronade,unchanged45-byte ownership."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_ship_cannon_fixture_v1378 as previous
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read


def apply_fixture(arm,raw,request):
    prior_proof = read('work/analysis/ship_loadout_pilot_verified_v1381/actual_loadout_pilot_verification.json')
    assert sha(Path(previous.__file__).read_bytes())==prior_proof['sole_fixture']['fixture_sha256']
    after,parent = previous.apply_fixture(arm,raw,request)
    cpu,get = get_machine(arm,after)
    assert get(0xAB784,4)==get(0xAB784,5)==5
    assert get(0x48144,4)==160 and get(0x48144,5)==224
    item = parent['cannon_equipment'][0]
    assert item['slot']==0 and item['after']==4 and after[item['field']-0x02000000]==4
    result = bytearray(after)
    result[item['field']-0x02000000] = 5
    result = bytes(result)
    assert {0x02000000+i for i,(a,b) in enumerate(zip(after,result,strict=True)) if a!=b}=={item['field']}
    receipt = deepcopy(parent)
    receipt.update(context='five_ship_prebattle_location_Carronade_and_escort_NoGun',
        parent_equipment_fixture_sha256=sha(Path(previous.__file__).read_bytes()),
        intermediate_HeavyCannon_receipt_is_not_a_separate_live_application=True,
        original_HeavyCannon_range=160,original_Carronade_range=224,equal_original_strength=5,
        after_RAM_sha256=sha(result),fixture_sha256=sha(Path(__file__).read_bytes()))
    receipt['cannon_equipment'][0].update(after=5,equipment='original Carronade',native_range_after=224)
    receipt['changes'] = [{'address':0x02000000+i,'before':a,'after':b}
        for i,(a,b) in enumerate(zip(raw,result,strict=True)) if a!=b]
    assert len(receipt['owned_bytes'])==45 and all(c['address'] in receipt['owned_bytes'] for c in receipt['changes'])
    return result,receipt
