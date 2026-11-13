"""Same two-byte fixture contract on the exact V770 comparison ROM."""
from types import FunctionType
from scripts import native_town_condition_fixture_v774 as original
from dk4tool.patch.grand_race_menu_release import sha
from pathlib import Path

def set_condition(arm,raw,request):
    env=dict(original.__dict__)
    env['ARM_SHA']='4c8d986287a7b363283d8b3828b821aa044f1ea1661f6bbaa9b13f5f05ee87b3'
    return FunctionType(original.set_condition.__code__,env)(arm,raw,request)
