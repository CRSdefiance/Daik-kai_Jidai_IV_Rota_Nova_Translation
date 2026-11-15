"""Labeled playback fixture: current M28 through M20, no unlock/state edits."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

PARENT=Path('out/all_routes_combined_v484_candidate.nds')
ROOT=Path('work/analysis/m28_planes_v485')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    parent=NdsImage.open(PARENT)
    digest=sha(PARENT.read_bytes())
    assert digest=='f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c'
    m=json.loads(PARENT.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert m['candidate_sha256']==digest and m['profile']=='all-routes-unified-v484'
    before=files(parent)
    source=parent.read_file('/FLS/M28.fls')
    parent.replace_file('/FLS/M20.fls',source)
    out=ROOT/'research_only_m28_through_m20.nds'
    parent.save(out)
    saved=NdsImage.open(out)
    after=files(saved)
    assert before.keys()==after.keys() and [p for p in before if before[p]!=after[p]]==['/FLS/M20.fls']
    assert saved.read_file('/FLS/M20.fls')==source and sha(PARENT.read_bytes())==digest
    schedule=json.loads(Path('work/analysis/movie_gpu_fixture_v336/opening_inputs.json').read_text(encoding='utf-8'))
    assert all(x['start']<=2200 for x in schedule)
    (ROOT/'inputs.json').write_text(json.dumps(schedule,indent=2)+'\n',encoding='utf-8')
    manifest={'research_only':True,'not_a_playable_or_distribution_candidate':True,'parent':str(PARENT),
              'parent_sha256':digest,'research_ROM':str(out),'research_ROM_sha256':sha(out.read_bytes()),
              'only_changed_file':'/FLS/M20.fls','exact_substituted_source':'/FLS/M28.fls',
              'source_sha256':sha(source),'all_other_files_code_components_and_progression_exact':True,
              'no_save_unlock_flag_RAM_or_script_modification':True,
              'does_not_prove_normal_movie_caller_unlock_or_route_completion':True}
    (ROOT/'fixture_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Prepared labeled M28 renderer fixture; V484 unchanged.')


if __name__=='__main__':
    main()
