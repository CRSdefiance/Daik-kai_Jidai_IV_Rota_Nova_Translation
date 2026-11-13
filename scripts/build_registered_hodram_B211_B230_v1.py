"""Stage and register the reviewed SC1 successor over the complete Rafael5186 stack."""
from copy import deepcopy
import os
from pathlib import Path
import sys
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha as digest_bytes
from dk4tool.patch.hodram_b211_b230_release_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta,make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety_relocated_v1 import bind_registered_story_percent_guard
from scripts import build_registered_rafael4903_v1 as template
from scripts import build_registered_rafael5186_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finalize_hodram_B211_B230_research_v1 import FINAL,STORED
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B211_B230_registered_v1 import ARCHIVE,ARM,CLEAN,CONFIG,PARENT,QUALIFICATION,REGISTRY
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import REQUIRED_MENU_TEXT,REQUIRED_OPTIONS_TEXT

OUT=Path('work/hodram_B211_B230_release_v1')
PROFILE='all-routes-hodram-b211-b230-dialogue-v1-20261107'
CANDIDATE=OUT/'all_routes_hodram_B211_B230_candidate.nds'
MANIFEST=CANDIDATE.with_suffix('.manifest.json');PATCH=CANDIDATE.with_suffix('.xdelta')
INVERSE_PATCH=OUT/'clean_input_reconstruction_RESEARCH_ONLY.nds'
STAGED=OUT/'staged_successor.json';RELEASE=OUT/'registered_release_verification.json'
STARTUP=OUT/'own_registered_startup_verification.json';GETTERS=OUT/'own_registered_name_getters_v1.json'
PARENT_REGISTRY=OUT/'release_stack_before_Hodram_B211_B230.json'
CHECK_SC1='registered_Hodram_B211_B230_dialogue_and_complete_parent_target_inverse'
NEGATIVES=Path('work/Hodram_B211_B230_resume_20261106/registered_semantic_checks_v1/qualification.json')

stage_source=checked_text(template.stage_source,{
    '    assert not OUT.exists()':"    assert not OUT.exists()\n    assert load(NEGATIVES)['all8_production_scope_mutations_rejected']\n    assert load(NEGATIVES)['config_sha256']==digest(CONFIG)",
    "assert qualification['only_SC0_changes']":"assert qualification['only_SC1_changes']",
    "    assert Path(old_manifest['batches'][-1]) == previous.FINAL\n    assert old_manifest['checks'][previous.CHECK_SC0]":
        "    assert [Path(p) for p in old_manifest['batches'][-2:]]==[previous.FINAL,previous.NAME_CONFIG]\n    assert old_manifest['checks'][previous.CHECK_SC0] and old_manifest['checks'][previous.CHECK_NAMES]\n    assert release['owned_Rafael_residual_middle_fields_verified']",
    "len(old_manifest['batches']) == 697 and len(old_manifest['checks']) == 32":
        "len(old_manifest['batches']) == 700 and len(old_manifest['checks']) == 35",
    "len(dialogue_proof['changed_records']) == 556":"len(dialogue_proof['changed_records']) == 277",
    'target_SC0_sha256':'target_SC1_sha256','only_owned_SC0_blocks_changed':'only_owned_SC1_blocks_changed',
    '# The final four-archive guard runs fresh because SC0 changed. Earlier':'# The final four-archive guard runs fresh because SC1 changed. Earlier',
    'Staged Rafael4903.':'Staged Hodram B211-B230.',
})
register_source=checked_text(template.register_source,{
    "getters['both_name_getters_exact_for_actors_35_65_68_70_186_203']":"getters['both_name_getters_exact_for_all9_protected_actors']",
    'verified_Rafael4347_output_reused=True':'verified_Rafael5186_output_reused=True',
    'target_SC0_sha256':'target_SC1_sha256',
    "r['id']) for r in bindings}) == 556":"r['id']) for r in bindings}) == 277",
    'verified_rafael4347_predecessor':'verified_rafael5186_predecessor',
    'rafael_B321_B342_late_dialogue':'hodram_B211_B230_late_dialogue',
    'Rafael B321–B342 dialogue.':'Hodram B211–B230 dialogue.',
    'release_stack.Rafael4903.pending.json':'release_stack.Hodram_B211_B230.pending.json',
    "result['checks'][CHECK_SC0] = True":"result['checks'][CHECK_SC1] = True",
    'late_editorial:rafael-b321-b342':'late_editorial:hodram-b211-b230',
    'Rafael4903_registered_successor_pipeline':'Hodram_B211_B230_registered_successor_pipeline',
    "result['batches'][:697] == old_manifest['batches'] and len(result['batches']) == 698":
        "result['batches'][:700] == old_manifest['batches'] and len(result['batches']) == 701",
    "len(result['checks']) == 33":"len(result['checks']) == 36",
    "'complete_stack_entries': 698, 'registered_manifest_entries': 698, 'passing_release_checks': 33":
        "'complete_stack_entries': 701, 'registered_manifest_entries': 701, 'passing_release_checks': 36",
    "'changed_components': [], 'new_contextual_records': 556, 'prose_revisions': 364":
        "'changed_components': [], 'owned_Rafael_residual_middle_fields_verified': True, 'new_contextual_records': 277, 'prose_revisions': 170",
    "'justified_retentions': 192":"'justified_retentions': 107",
    'Registered Rafael4903 with 698 entries and 33 release checks.':'Registered Hodram B211-B230 with 701 entries and 36 release checks.',
})
exec(compile(stage_source+'\n'+register_source,__file__+'::qualified-cumulative-SC1-successor','exec'),globals())
if __name__=='__main__':
    if sys.argv[1:]==['--register']:register()
    else:
        assert not sys.argv[1:]
        stage()
