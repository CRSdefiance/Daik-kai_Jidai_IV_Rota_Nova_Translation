"""Reproduce the integrated-builder object shape and independently validate all actual evidence after the exact inverse correction."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,require
from dk4tool.patch.hodram_outcomes_native_evidence_v3 import check_native_models
from dk4tool.patch.hodram_outcomes_actual_evidence_v1 import fixtures as previous_fixtures
from dk4tool.patch.hodram_outcomes_actual_evidence_v2 import check_actual
from scripts.Hodram_outcomes_release_paths_v8347 import DOC,PARENT,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_fixture_parent_inverse_validation_v8369')
if __name__=='__main__':
    assert not ROOT.exists();data={k:read(p) for k,p in proofs().items()};doc=read(DOC);parent=NdsImage.open(PARENT);canonical=Path('out/raphael_natural_v2_accepted_base.nds');aliased=NdsImage(canonical,deepcopy(parent.rom));clean=NdsImage.open('work/clean.nds');before=bytes(aliased.rom.save());original=aliased.rom
    assert aliased.source==canonical and canonical.read_bytes()!=PARENT.read_bytes() and before==PARENT.read_bytes()
    rebuilt=reconstruct_and_bind(aliased,clean,doc,data['relocation'],data['current'])
    try:previous_fixtures(data,doc['records'],aliased,clean,rebuilt,require)
    except ValueError as error:assert 'whole actual fixture parent ROM inverse' in str(error);reproduced=str(error)
    else:raise AssertionError('Expected original disk-path reader to reject exact integrated-builder object shape')
    native=check_native_models(data,doc['records'],aliased,read,require);result=check_actual(data,doc['records'],aliased,clean,rebuilt,native,read,require)
    assert result['complete_actual_holds']==100 and result['complete_actual_pages']==12 and aliased.rom is original and bytes(aliased.rom.save())==before
    ROOT.mkdir(parents=True);save(ROOT/'canonical_source_path_complete_V8300_memory_original_failure_reproduced_corrected100holds_pass.json',dict(original_failure_reproduced=reproduced,source_disk_path=str(canonical),source_disk_sha256=sha(canonical.read_bytes()),actual_inmemory_parent=str(PARENT),actual_inmemory_parent_sha256=sha(before),original_disk_path_differs_from_validated_current_contents=True,independent_corrected_actual_result=result,whole_four_fixture_inverses_equal_complete_validated_inmemory_parent=True,all_original_native_actual_scope_andglyph_guards_preserved=True,original_object_identity_allserialized_bytes_andfiles_unchanged=True,no_ROM_emulator_replay_registration_orcredit=True,new_credit=0,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in [Path(__file__),DOC,Path('dk4tool/patch/hodram_outcomes_actual_evidence_v1.py'),Path('dk4tool/patch/hodram_outcomes_actual_evidence_v2.py'),*proofs().values()]}))
    print('Reproduced original builder-path failure;corrected full in-memory inverse passes4fixtures/12pages/100holds withcanonical .source andexactV8300 .rom.No mutation/capture/credit.')
