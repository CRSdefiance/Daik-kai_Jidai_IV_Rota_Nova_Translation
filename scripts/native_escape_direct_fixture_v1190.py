"""Only rebind the proven pre-duel fixtures to the registered formatter successor."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_duel_injured_contact_v1176 as injured
from scripts import native_duel_unarmored_v1179 as unarmored

ROM=Path('out/all_routes_combined_v1189_candidate.nds')


def water(arm,points):
    return FunctionType(injured.previous.water.__code__,{**injured.previous.water.__globals__,'ROM':ROM})(arm,points)


def apply_fixture(arm,raw,request):
    source=inspect.getsource(injured.apply_fixture)
    assert source.count('translations/duel_editorial_release_v1.json')==2
    source=source.replace('translations/duel_editorial_release_v1.json','translations/escape_direct_formatting_release_v1.json')
    old='from dk4tool.patch.duel_editorial import current_entries'
    assert source.count(old)==1
    source=source.replace(old,'from dk4tool.patch.escape_direct_entries import current_entries')
    env={**injured.__dict__,'ROM':ROM,'water':water,'__file__':__file__}
    exec(compile(source,__file__,'exec'),env)
    fn=FunctionType(unarmored.apply_fixture.__code__,{**unarmored.apply_fixture.__globals__,'prior':env['apply_fixture']},
        argdefs=unarmored.apply_fixture.__defaults__)
    after,receipt=fn(arm,raw,request)
    receipt.update(formatter_successor_fixture_adapter_sha256=sha(Path(__file__).read_bytes()),
        effective_injured_adapter_sha256=sha(source.encode()),
        only_ROM_config_parser_binding_changed_all_fixture_field_and_outcome_guards_retained=True)
    return after,receipt
