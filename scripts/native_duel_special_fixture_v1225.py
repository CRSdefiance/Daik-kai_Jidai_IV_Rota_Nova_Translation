"""Isolated pre-duel contact with extended positive HP for natural specials.

Only the existing28-byte field ownership is used. Both still-living captains
receive at least2000 HP through the original positive-health setter before
combat. No actor IDs, stats, equipment, RNG, special flags or results change.
"""
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
    replacements = {
        'translations/duel_editorial_release_v1.json': 'translations/duel_special_editorial_release_v1.json',
        'from dk4tool.patch.duel_editorial import current_entries': 'from dk4tool.patch.duel_special_editorial import current_entries',
        'max(value, 100)': 'max(value, 2000)',
        'max(v, 100)': 'max(v, 2000)',
    }
    for old, new in replacements.items():
        assert source.count(old) == (2 if old.endswith('release_v1.json') else 1)
        source = source.replace(old, new)
    env = {**previous.__dict__, 'ROM': ROM, 'water': water, '__file__': __file__}
    exec(compile(source, __file__, 'exec'), env)
    after, receipt = env['apply_fixture'](arm, raw, request)
    receipt.update(special_fixture_adapter_sha256=sha(Path(__file__).read_bytes()),
        effective_adapter_sha256=sha(source.encode()),
        isolated_extended_positive_health_for_original_special_observation=True,
        positive_HP_floor_before_duel_only=2000,
        no_actor_stats_equipment_RNG_special_flags_or_result_edits=True)
    return after, receipt
