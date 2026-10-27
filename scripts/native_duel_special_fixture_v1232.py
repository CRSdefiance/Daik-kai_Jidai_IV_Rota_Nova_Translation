"""V1224 ordinary-health pre-duel contact; all28 original fields preserved."""
import inspect
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_duel_contact_v1169 as previous

ROM = Path('out/all_routes_combined_v1224_candidate.nds')


def water(arm, points):
    return FunctionType(previous.previous.water.__code__, {**previous.previous.water.__globals__, 'ROM': ROM})(arm, points)


def apply_fixture(arm, raw, request):
    source = inspect.getsource(previous.apply_fixture)
    assert source.count('translations/duel_editorial_release_v1.json') == 2
    source = source.replace('translations/duel_editorial_release_v1.json', 'translations/duel_special_editorial_release_v1.json')
    old = 'from dk4tool.patch.duel_editorial import current_entries'
    assert source.count(old) == 1
    source = source.replace(old, 'from dk4tool.patch.duel_special_editorial import current_entries')
    env = {**previous.__dict__, 'ROM': ROM, 'water': water, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    after, receipt = env['apply_fixture'](arm, raw, request)
    receipt.update(special_fixture_adapter_sha256=sha(Path(__file__).read_bytes()),
        effective_adapter_sha256=sha(source.encode()), only_ROM_config_and_parser_binding_changed=True)
    return after, receipt
