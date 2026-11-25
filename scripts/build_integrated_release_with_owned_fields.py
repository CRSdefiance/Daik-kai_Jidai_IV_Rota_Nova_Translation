"""Run the immutable cumulative pipelines, then registered exclusive fixed-slot fields."""
import argparse
import runpy
import sys
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.registered_owned_name_fields_v2 import plan_release
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--profile',required=True)
    for arg in ['out','work']:parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists() and not args.out.with_suffix('.manifest.json').exists()
    registry=Path('translations/release_stack.json');before=registry.read_bytes();stack=load(registry)
    config_path=Path(stack['profiles'][args.profile]['owned_name_fields']);config=load(config_path)
    args.work.mkdir(parents=True,exist_ok=True);stage=args.work/'post_Emilio_RESEARCH_ONLY.nds';assert not stage.exists()
    sys.argv=['scripts/build_integrated_release_with_owned_names.py','--profile',args.profile,'--out',str(stage),'--work',str(args.work/'owned_names')]
    namespace=runpy.run_path('scripts/build_integrated_release_with_owned_names.py',run_name='immutable_registered_owned_names');namespace['main']()
    assert registry.read_bytes()==before
    source=NdsImage.open(stage);manifest=load(stage.with_suffix('.manifest.json'))
    assert sha(stage.read_bytes())==config['parent_ROM_sha256']==manifest['candidate_sha256']
    assert manifest['release_stack_sha256']==sha(before) and all(manifest['checks'].values())
    arm,proof=plan_release(source,config_path);target=deepcopy(source);target.replace_file('/__arm9__.bin',arm)
    assert all(target.read_file(p)==v for _,p,v in source.iter_files())
    assert [p for p,v in source.iter_components() if target.read_file(p)!=v]==['/__arm9__.bin']
    inverse=deepcopy(target);inverse.replace_file('/__arm9__.bin',source.read_file('/__arm9__.bin'));assert bytes(inverse.rom.save())==stage.read_bytes()
    payload=bytes(target.rom.save());assert sha(payload)==config['target_ROM_sha256']
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(payload)
    assert NdsImage.open(args.out).read_file('/__arm9__.bin')==arm
    result=deepcopy(manifest);result.update(candidate_rom=str(args.out),candidate_sha256=sha(payload))
    result['batches'].append(str(config_path));result['changed_records'].setdefault('/__arm9__.bin',[]).extend(proof['changed_records'])
    result['relocations'].setdefault('/__arm9__.bin',{})['owned_name_fields']=dict(release_config=str(config_path),release_config_sha256=sha(config_path.read_bytes()),proof=proof)
    result['checks']['registered_owned_name_fields_and_complete_parent_target_inverse']=True
    result['owned_fields_production_pipeline']=dict(driver=__file__,driver_sha256=sha(Path(__file__).read_bytes()),
        post_Emilio_stage=str(stage),post_Emilio_stage_sha256=sha(stage.read_bytes()),post_Emilio_manifest=str(stage.with_suffix('.manifest.json')),
        post_Emilio_manifest_sha256=sha(stage.with_suffix('.manifest.json').read_bytes()),all_prior_drivers_unchanged=True,only_final_exclusive_fixed_slot_name_fields_changed=True)
    assert registry.read_bytes()==before;save(args.out.with_suffix('.manifest.json'),result)
    print('Registered cumulative field-corrected candidate:',args.out,sha(payload),flush=True)

if __name__=='__main__':main()
