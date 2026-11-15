"""All3668 warm/cold original copies,then register the independent cooking stage."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.cooking_comments_editorial import CONFIG,compiled,plan
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.work_comments_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_remaining_common_layout as loader
from scripts.probe_common_copy_arm946_alignment import arm946_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/cooking_comments_v850')
MANUSCRIPT=Path('translations/cooking_comments_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v845_candidate.nds')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    assert not Path(CONFIG).exists()
    registry_path=Path('translations/release_stack.json')
    registry=read(registry_path);assert 'all-routes-unified-v850' not in registry['profiles']
    save(ROOT/'registry_before.json',registry)
    rom=NdsImage.open(OLD);common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    doc=read(MANUSCRIPT);assert sha(OLD.read_bytes())==doc['current_ROM_sha256']
    c,a,proof=plan(common,arm,doc)
    (ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    save(ROOT/'repack_plan.json',proof)
    print('Cooking repack:',proof['repacked_block_range'],'changed strings:',len(proof['changed_records']),flush=True)
    expected={e.message_id:e.text for e in current_entries(common,arm)}
    expected.update({r['message_id']:compiled(r) for r in doc['records']})
    before_factory=loader.machine_for;loader.machine_for=arm946_machine;cases=[]
    try:
        for number in range(3668):
            outputs=[loader.warm_copy(a,c,number,expected[number],cold_cache=cold) for cold in (False,True)]
            cases.append({'message_id':number,'text_sha256':sha(expected[number]),
                'warm_and_cold_complete_native_copy_and_guards_pass':True,
                'warm_copy_bytes':outputs[0]['copied_bytes'],'cold_host_file_contract_reads':outputs[1]['host_file_contract_reads']})
            if number%500==0:print('Native warm/cold:',number,'/3668',flush=True)
    finally:loader.machine_for=before_factory
    copies=ROOT/'native_copy_proof.json'
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'all3668_native_IDs_warm_and_cold7336_complete_copies':cases,
        'native_loader_cache_and_aligned_copy_execute':True,'host_ILNK_read_bridge_not_hardware_or_gameplay':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    dependencies=list(map(Path,('dk4tool/patch/cooking_comments_editorial.py','scripts/work_comments_layout_v843.py',
        'scripts/probe_cooking_fonts_v849.py','scripts/prepare_cooking_context_v847.py','scripts/prepare_cooking_prose_v848.py',
        'scripts/prepare_item_common_v788.py','scripts/prepare_recruitment_common_v772.py',
        'work/analysis/cooking_comments_v847/source_context_packet.json','work/analysis/cooking_comments_v849/native_font_proof.json',
        'work/analysis/cooking_comments_v849/visual_review.json','translations/cooking_comments_editorial_manuscript_v1.json')))
    dependencies.append(copies)
    config={'format':'dk4-cooking-comments-editorial-v1','source_common_sha256':sha(common),'source_arm9_sha256':sha(arm),
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_copy_proof':str(copies),
        'dependencies':{str(p):sha(p.read_bytes()) for p in dependencies}}
    save(CONFIG,config)
    assert read(registry_path)==read(ROOT/'registry_before.json')
    profile=deepcopy(registry['profiles']['all-routes-unified-v845'])
    profile.update(cooking_comments_editorial=CONFIG,status='experimental',
        description='Complete V845 stack plus13 reviewed Cook15 comments,including special Sera1422,in the unchanged216x36 paper window.',
        note='All earlier layers,native code,crop and fixed memory allocations retained. Native copy/font gates pass;actual revised cooking scenes remain pending. Human cold-boot acceptance required for canonical promotion.')
    registry['profiles']['all-routes-unified-v850']=profile;save(registry_path,registry)
    print('All7336 native copies pass;complete V850 profile registered. Build and actual revised cooking scenes remain.',flush=True)


if __name__=='__main__':main()
