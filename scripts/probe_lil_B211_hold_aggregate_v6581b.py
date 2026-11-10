"""Probe a semantic evidence-count gap in memory only; no ROM or real evidence file is edited."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B211_editorial_v1 as owned
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_hold_aggregate_probe_v6581b');CONFIG=Path('work/analysis/lil_B211_atomic_v6581/positive_config.json')
if __name__=='__main__':
    assert not ROOT.exists();conf=read(CONFIG);doc=read(conf['manuscript']);path=Path(doc['actual_English_proof']);value=deepcopy(read(path));removed=value['actual_panels'][0]['complete_body_holds'].pop();assert value['complete_native_body_holds']==47 and sum(len(r['complete_body_holds']) for r in value['actual_panels'])==46;image=NdsImage.open('out/all_routes_combined_v6541_candidate.nds');baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');original_load=owned.load;calls=[];replace=image.replace_file
    def injected(p):
        v=deepcopy(value) if Path(p)==path else original_load(p)
        if Path(p)==CONFIG:v['dependencies']={}
        return v
    def tracked(*args,**kwargs):calls.append(args[0]);return replace(*args,**kwargs)
    owned.load=injected;image.replace_file=tracked
    try:
        try:owned.apply_release(image,baseline,CONFIG)
        except (ValueError,AssertionError) as error:accepted=False;reason=str(error)
        else:accepted=True;reason='One hold removed while aggregate47 retained;v1 checks digests andnonempty holds butnot independent aggregate/individual declared counts.'
    finally:owned.load=original_load
    assert accepted and calls==[owned.PATH];ROOT.mkdir(parents=True);save(ROOT/'semantic_hold_count_gap_in_memory_only.json',dict(compiler='dk4tool.patch.lil_B211_editorial_v1',compiler_sha256=sha(Path(owned.__file__).read_bytes()),semantic_gap_observed_with_dependency_digests_deliberately_bypassed=True,removed_hold=removed,declared_body_holds=47,actual_array_body_holds=46,real_evidence_file_sha256=sha(path.read_bytes()),in_memory_archive_write_calls=calls,no_ROM_saved_no_real_evidence_modified_no_credit=True,registered_config_and_candidate_not_created=True,followup_bind_aggregate_and_per_record_declared_holds_before_write=True,full_goal_complete=False));print('In-memory probe confirmsv1 aggregate-count gap when digests are bypassed. No ROM/evidence files edited;bind counts in immutable successor before registration.')
