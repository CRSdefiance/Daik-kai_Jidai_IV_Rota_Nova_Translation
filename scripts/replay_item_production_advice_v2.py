"""Allow only the additional acquisition bit written by native Local Product transfer."""

import inspect
from struct import unpack_from

from scripts import replay_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


ITEMS = previous.ITEMS.with_name('items_advice_v2')
LOCAL_PRODUCT_BIT = previous.FLAG_OWNER + 7


def check_product_flag(parent_arm, current_arm):
    assert unpack_from('<I', current_arm, 0x4A0F0)[0] == previous.FLAG_OWNER
    assert parent_arm[0x49FB4:0x49FD4] == current_arm[0x49FB4:0x49FD4]
    assert current_arm[0x49FC4:0x49FC8] == bytes.fromhex('1d10a0e3')


def main():
    source = checked_text(inspect.getsource(previous.replay), {
        "    transfer_source = checked_text(inspect.getsource(inventory.transfer), {":
            """    check_product_flag(parent_arm, current_arm)
    transfer_source = checked_text(inspect.getsource(inventory.transfer), {
        'permitted = set(range(history, history + 28))': 'permitted = set(range(history, history + 28)) | {LOCAL_PRODUCT_BIT}',""",
        "vars(inventory) | {'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],)}":
            "vars(inventory) | {'SUPPORTED_ARM_SHA': (prepared['research_ARM9_sha256'],), 'LOCAL_PRODUCT_BIT': LOCAL_PRODUCT_BIT}",
        "        assert receipt['items'][0]['name'] == 'Baby Shark'":
            """        assert receipt['items'][0]['name'] == 'Baby Shark'
        offset = LOCAL_PRODUCT_BIT - inventory.BASE
        assert transferred[offset] == raw[offset] | 32
        assert not raw[offset] & 32
        receipt['native_local_product_acquisition_flag'] = dict(bit=29, address=LOCAL_PRODUCT_BIT)""",
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::checked-local-product-acquisition-bit', 'exec'), env)
    env['replay']()


if __name__ == '__main__':
    main()
