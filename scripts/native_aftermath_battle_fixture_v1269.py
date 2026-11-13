"""Rebind the audited V1243 pre-duel prerequisites to registered V1266.

Only ROM/config/parser bindings change. Original contact, recovery, equipment,
attribute and random/result exclusions remain in the frozen source functions.
"""
import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_duel_contact_v1169 as contact
from scripts import native_duel_long_fixture_v1239 as low_fencing
from scripts import native_duel_long_fixture_v1242 as long_luck

ROM = Path('out/all_routes_combined_v1266_candidate.nds')
_fixture = None


def water(arm,points):
    return FunctionType(contact.previous.water.__code__,{**contact.previous.water.__globals__,'ROM':ROM})(arm,points)


def apply_fixture(arm,raw,request):
    global _fixture
    if _fixture is None:
        source = inspect.getsource(contact.apply_fixture)
        old = 'translations/duel_editorial_release_v1.json'
        assert source.count(old) == 2
        source = source.replace(old,'translations/battle_aftermath_editorial_release_v1.json')
        old = 'from dk4tool.patch.duel_editorial import current_entries'
        assert source.count(old) == 1
        source = source.replace(old,'from dk4tool.patch.battle_aftermath_editorial import current_entries')
        env = {**contact.__dict__,'__file__':__file__,'ROM':ROM,'water':water}
        exec(compile(source,__file__,'exec'),env)
        low = FunctionType(low_fencing.apply_fixture.__code__,
            {**low_fencing.__dict__,'__file__':__file__,'ROM':ROM,'prior':env['apply_fixture']})
        _fixture = FunctionType(long_luck.apply_fixture.__code__,
            {**long_luck.__dict__,'__file__':__file__,'ROM':ROM,'prior':low})
    result,receipt = _fixture(arm,raw,request)
    receipt.update(aftermath_fixture_adapter_sha256=sha(Path(__file__).read_bytes()),
        exact_original_contact_source_sha256=sha(Path(contact.__file__).read_bytes()),
        exact_original_equipment_source_sha256=sha(Path(low_fencing.__file__).read_bytes()),
        exact_original_luck_source_sha256=sha(Path(long_luck.__file__).read_bytes()),
        only_registered_ROM_config_parser_and_provenance_bindings_changed=True)
    return result,receipt
