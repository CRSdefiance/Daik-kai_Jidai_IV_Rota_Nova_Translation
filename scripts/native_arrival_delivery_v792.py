"""Exact existing test inputs admitted for the registered arrival-only ARM9."""

from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_letter_delivery_v791 as previous
from scripts import native_letter_eligibility_v790 as qualification
from scripts.verify_village_wrap_v608 import read


def set_condition(arm,raw,request):
    cfg=read('translations/arrival_notices_editorial_release_v1.json')
    assert sha(arm)==cfg['target_arm9_sha256']
    allowed=set(previous.ARMS)|{cfg['target_arm9_sha256']}
    qualify=FunctionType(qualification.set_condition.__code__,{**qualification.__dict__,'ARMS':allowed})
    fixture=FunctionType(previous.set_condition.__code__,{**previous.__dict__,'ARMS':allowed,'qualify':qualify})
    return fixture(arm,raw,request)
