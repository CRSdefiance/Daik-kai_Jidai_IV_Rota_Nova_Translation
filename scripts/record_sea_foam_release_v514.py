"""Record verified V514 evidence while retaining the full graphics audit."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    out=Path('work/analysis/sea_foam_family_v514')
    proof_path=out/'release_proof.json'
    proof=read(proof_path)
    parent_path=Path('work/analysis/tavern_family_v508/preservation_proof.json')
    preservation=read(parent_path)
    before=NdsImage.open('out/all_routes_combined_v508_candidate.nds')
    after=NdsImage.open(proof['candidate'])
    assert len(preservation['entries'])==921
    assert all(before.read_file(path)==after.read_file(path) for path in {r['path'] for r in preservation['entries']})
    preservation.update({'candidate':proof['candidate'],'candidate_sha256':proof['candidate_sha256'],
                         'exact_container_parent':'out/all_routes_combined_v508_candidate.nds',
                         'exact_container_parent_sha256':sha(Path('out/all_routes_combined_v508_candidate.nds').read_bytes()),
                         'parent_preservation_proof':str(parent_path),'parent_preservation_proof_sha256':sha(parent_path.read_bytes())})
    preservation_path=out/'preservation_proof.json'
    preservation_path.write_text(json.dumps(preservation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    record={'candidate':proof['candidate'],'candidate_sha256':proof['candidate_sha256'],
            'proof':str(proof_path),'proof_sha256':sha(proof_path.read_bytes()),
            'checkpoint':'docs/sea_foam_v514_checkpoint.md',
            'status':'experimental-actual-cold-boot-verified-awaiting-human-acceptance'}
    for name in ['graphics_completion_requirements_v313.json','graphics_completion_campaign_v1.json','graphics_visual_audit_v150.json']:
        path=Path('translations')/name;data=read(path)
        data['verified_sea_foam_family_v514']={**record,'all24_source_entries_reviewed':True,
            'actual_five_pages_complete_and_aligned':True,'all56_fresh_frames_exact':True,
            'all675_PXL_FLS_files_byte_exact':True,'all22_original_requirements_retained':True,
            'all18_plaques_incomplete':True,'full_goal_complete':False}
        if name=='graphics_completion_requirements_v313.json':
            assert len(data['historical_pending_items_retained'])==22
            data['candidate']=proof['candidate'];data['candidate_sha256']=proof['candidate_sha256']
            data['source_preservation_proof']=str(preservation_path)
            data['preservation_proof_sha256']=sha(preservation_path.read_bytes())
            for item in data['historical_pending_items_retained']:
                if item['historical_item'] in (6,7,21):item['additional_verified_sea_foam_family_v514']=str(proof_path)
        else:
            data['current_verified_release_candidate']=record
            data['current_verified_release_candidate_sha256']=proof['candidate_sha256']
        for key,value in list(data.items()):
            if isinstance(value,str) and value.replace('\\','/')==str(parent_path).replace('\\','/'):
                data[key]=str(preservation_path)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    heading='## V514 complete sea-foam dialogue and actual caller repair'
    for name in ('translation_progress.md','known_issues.md','todo.md'):
        path=Path('docs')/name;text=path.read_text(encoding='utf-8')
        if heading not in text:
            text+='\n\n'+heading+'\n\nComplete COMMON457–480 restores the source rumors and ship-swallowing danger.\n'
            text+='Actual crew and captain callers use shared paragraph wrapping; all five replay\npages have complete glyphs, whole words and equal x22 margins. All24 native\nvariants,52 neighbor copies and56 exact fresh regression captures pass.\n'
            text+='All470 batches,114 accepted layers,675 PXL/FLS files and921 preservation\nentries remain. Exact clean patch reconstruction passes. V514 experimental;\ncanonical unchanged. All22 requirements and18 incomplete plaques retained.\nSee [checkpoint](sea_foam_v514_checkpoint.md).\n'
            path.write_text(text,encoding='utf-8')
    notes=Path('E:/Rota Nova translations/BUILD_NOTES_V514.md')
    notes.write_text(Path('docs/sea_foam_v514_checkpoint.md').read_text(encoding='utf-8')+'\nPatch SHA-256: `'+proof['patch_sha256']+'`.\n',encoding='utf-8')
    print('V514 release, all921 preservation entries and full graphics scope recorded.')


if __name__=='__main__':main()
