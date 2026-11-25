"""Create scoped235object tools without changing prior or global helpers."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Shrines_Temples_tools_v3175')
PROFILE = Path('dk4tool/dialogue/lil_shrines_temples_profile.py')
LAYOUT = Path('dk4tool/dialogue/lil_shrines_temples_layout_v1.py')
PARENT = Path('dk4tool/dialogue/lil_crew_items_layout_v2.py')
SOURCE = Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
CONTROL = Path('work/analysis/lil_Shrines_Temples_controls_v3168c/all235_source_current_dispatch_dynamic_styles_and_predicates.json')
TERMS = Path('work/analysis/lil_Shrines_Temples_terms_v3170/clean_current_items_cathedral_and_source_roles.json')
VOICES = Path('work/analysis/lil_Shrines_Temples_voices_v3167/current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json')

if __name__ == '__main__':
    assert not any(p.exists() for p in [ROOT, PROFILE, LAYOUT])
    source, control = read(SOURCE), read(CONTROL)
    hashes = sorted({b[k] for b in source['blocks'] for k in ['clean_block_sha256', 'current_block_sha256']})
    assert len(hashes) == 20
    selectors = [2, 9, 16, 20, 139, 151, 160, 177, 178, 191, 207, 208]
    assert len(control['speech_and_stored_alternative_dispatch_cases']) == 440
    assert len(control['whole_original4100_command_cases']) == 16
    binding = Path(control['registered_catalog_binding'])
    deps = {str(p): sha(p.read_bytes()) for p in [SOURCE, CONTROL, TERMS, VOICES, binding]}
    text = '''"""Exact ten-block speech/FE and virtual actor-style context."""
from pathlib import Path
from dataclasses import replace
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA = @ARM@
BLOCKS = frozenset(@HASHES@)
SELECTORS = frozenset(@SELECTORS@)
DEPENDENCIES = @DEPS@
CONTROL = Path(@CONTROL@)
VOICES = Path(@VOICES@)

def profile_for(arm, source_block, consumer='progressive'):
    if sha(arm) != ARM9_SHA or sha(source_block) not in BLOCKS:
        raise ValueError('Shrines/Temples requires exact ten reviewed clean/current blocks and runtime')
    for p, digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes()) != digest:
            raise ValueError('Shrines/Temples source contract changed:' + p)
    control = json.loads(CONTROL.read_text(encoding='utf8'))
    voices = json.loads(VOICES.read_text(encoding='utf8'))
    if (len(control['speech_and_stored_alternative_dispatch_cases']) != 440
        or len(control['whole_original4100_command_cases']) != 16
        or len(control['all207_actor_style_source_pointer_cases']['cases']) != 3312
        or len(control['current_original_predicate_cases']) != 21
        or control['original_event_queries']
        or not control['all30_FE_before_fallback208_use5473C_and24310_null_actor']
        or not control['source_current_effective_runtime_English_distinguished_from_storage']
        or not voices['dynamic_CF_is_original_role0_captain_and_D0_role1_with_original_fallback']
        or len(voices['catalog']['rows']) != 207):
        raise ValueError('Complete current speech, FE, dynamic actor-style and predicate contract required')
    base = get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer == 'progressive':
        return replace(base, name='lil-shrines-temples-progressive-runtime-bound-v1',
            leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source + '; exact10blocks/164preambles/56stored actor-style alternatives. CFcaptain/D0role1fallback source bound. VirtualD0prefix is formatter-only; typed4100 packing must remove it and preserve the source20byte header/eight alias slots. Current fonts and three-choice geometry still required.')
    if consumer == 'FE-paper':
        return replace(base, name='lil-shrines-temples-FE-runtime-bound-v1',
            leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source + '; exact30FE before fallback208; original24310 null actor then5473C. Inherited228x48logical/228x64physical mode1paper, conservative216px planning. English starts first line; source vertical staging breaks are not authored. Complete per-record glyph/pagination proof required.')
    raise ValueError('Unknown Shrines/Temples consumer')
'''
    replacements = {
        '@ARM@': repr(source['current_ARM9_sha256']),
        '@HASHES@': repr(hashes), '@SELECTORS@': repr(selectors), '@DEPS@': repr(deps),
        '@CONTROL@': repr(CONTROL.as_posix()), '@VOICES@': repr(VOICES.as_posix())}
    for old, new in replacements.items():
        assert old in text
        text = text.replace(old, new)
    planner = PARENT.read_text(encoding='utf8')
    old = "'lil-crew-items-progressive-runtime-bound-v1':frozenset({2,4,6,7,12,14,15,16,18,20,22,108,114,152,188})"
    new = "'lil-shrines-temples-progressive-runtime-bound-v1':frozenset({2,9,16,20,139,151,160,177,178,191,207,208})"
    assert planner.count(old) == 1
    planner = planner.replace(old, new).replace('lil-crew-items-FE-runtime-bound-v1', 'lil-shrines-temples-FE-runtime-bound-v1').replace('Crew/Items', 'Shrines/Temples')
    pairs = [('of', 'conquest'), ('map', 'keys'), ('holy', 'spirit'), ('santiago', 'cathedral'),
             ('ancient', 'megalithic'), ('civilization', 'research'), ('research', 'society'),
             ('new', 'star'), ('dead', 'end'), ('left', 'hand'), ('right', 'hand'), ('first', 'mate')]
    anchor = 'PROTECTED_BOUNDARIES=frozenset({'
    assert planner.count(anchor) == 1
    planner = planner.replace(anchor, anchor + ','.join(repr(v) for v in pairs) + ',')
    compile(text, str(PROFILE), 'exec')
    compile(planner, str(LAYOUT), 'exec')
    PROFILE.write_text(text, encoding='utf8')
    LAYOUT.write_text(planner, encoding='utf8')
    ROOT.mkdir(parents=True)
    save(ROOT / 'new_scoped_tools_provenance.json', dict(
        profile=str(PROFILE), profile_sha256=sha(PROFILE.read_bytes()),
        layout=str(LAYOUT), layout_sha256=sha(LAYOUT.read_bytes()),
        parent_layout=str(PARENT), parent_layout_sha256=sha(PARENT.read_bytes()),
        dependencies={**deps, str(Path(__file__)): sha(Path(__file__).read_bytes())},
        exact20_clean_current_block_hashes=hashes, ordinary_and_virtual_actor_selectors=selectors,
        FE_selector=254, virtual_D0_control_not_inserted_in_physical_alternative_body=True,
        three_option_native_geometry_not_approved_by_this_profile=True,
        no_global_or_previous_module_change=True, no_editorial_or_completion_credit=True,
        full_goal_complete=False))
    print('Exact20hash/12selector profile and local planner created;30FE separate. VirtualD0 packing and three-option VM/font checks required; prior helpers preserved.')
