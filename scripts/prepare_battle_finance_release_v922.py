"""Register12 battle Finance comments after the complete V916 stack."""

from copy import deepcopy
from pathlib import Path
from dk4tool.patch import battle_finance_editorial as owned
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_finance_v922')
MANUSCRIPT=Path('translations/battle_finance_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v916_candidate.nds')


def main():
    assert not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('translations/release_stack.json');registry=read(path)
    assert 'all-routes-unified-v922' not in registry['profiles'];save(ROOT/'registry_before.json',registry)
    rom=NdsImage.open(OLD);doc=read(MANUSCRIPT);assert sha(OLD.read_bytes())==doc['current_ROM_sha256']
    c,a,proof=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    save(ROOT/'repack_plan.json',proof);(ROOT/'target_COMMON.bin').write_bytes(c);(ROOT/'target_ARM9.bin').write_bytes(a)
    rows=entries(c,a,proof['directory_sha256']);loader=Loader(a,c);cases=[]
    for mode in ('warm','cold'):
        for i,row in enumerate(rows):
            cases.append(loader.copy(row.message_id,row.text,mode))
            if (i+1)%1000==0:print(mode,i+1,'complete',flush=True)
    loader.reset();sequence=[]
    for block in list(range(41))+list(reversed(range(41)))+[0,18,0,18,40,0,40]:
        n=loader.directory[block][0]
        for _ in range(2):sequence.append(loader.copy(n,rows[n].text,'sequence'))
    assert all(r['reads']==0 for r in sequence[1::2])
    copies=ROOT/'native_copy_proof.json'
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'complete_native_copies':len(cases),'cases':cases,
        'sequenced_cache_cases':sequence,'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,
        'callee_saved_ABI_and_stack_pass':True,'existing_single_cache_policy_bytes_unchanged':True,
        'host_open_read_contract_only_not_actual_ROM_or_hardware':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    audit=ROOT/'native_audit/audit.json'
    dependencies=list(map(Path,(
        'dk4tool/patch/battle_finance_editorial.py','dk4tool/patch/battle_chapel_planning_editorial.py',
        'dk4tool/patch/common_single_cache_v861.py','scripts/battle_finance_layout_v920.py',
        'scripts/battle_chapel_planning_layout_v914.py','scripts/battle_cooking_livestock_layout_v908.py',
        'scripts/battle_repair_medical_layout_v902.py','scripts/battle_personal_layout_v892.py',
        'scripts/gunnery_deck_layout_v887.py','scripts/sails_boarding_layout_v881.py','scripts/sails_boarding_layout_v880.py',
        'scripts/survey_lookout_layout_v875.py','scripts/survey_lookout_layout_v874.py','scripts/bridge_duties_layout_v869.py',
        'scripts/planning_finance_layout_v860.py','scripts/livestock_prayer_layout_v854.py','scripts/work_comments_layout_v843.py',
        'scripts/probe_battle_finance_fonts_v920.py','scripts/probe_work_fonts_v843.py','scripts/probe_common_single_cache_v862.py',
        'scripts/audit_battle_finance_native_v922.py','scripts/prepare_battle_finance_context_v918.py',
        'scripts/prepare_battle_finance_prose_v919.py','scripts/prepare_battle_finance_native_v921.py',
        'work/analysis/battle_finance_v918/source_context_packet.json',
        'work/analysis/battle_finance_v919/ordinary_context_and_terms.json',
        'work/analysis/battle_finance_v920/native_font_proof.json','work/analysis/battle_finance_v920/visual_review.json',
        'translations/battle_finance_editorial_manuscript_v1.json','translations/crew_help_manuscript_v1.json',
        'translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json',str(audit),str(copies))))
    config={'format':'dk4-battle-finance-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_copy_proof':str(copies),
        'native_consumer_audit':str(audit),'dependencies':{str(p):sha(p.read_bytes()) for p in dependencies}}
    save(owned.CONFIG,config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert read(path)==read(ROOT/'registry_before.json')
    profile=deepcopy(registry['profiles']['all-routes-unified-v916'])
    profile.update(battle_finance_editorial=owned.CONFIG,status='experimental',
        description='Complete V916 stack plus12 reviewed battle Finance20 comments1669-1680.',
        note='75 original battle/main/ordinary control selections,all12 fonts,7336 full native copies and178 sequences pass. Existing single8KiB cache,216x36 crop and all allocations preserved. Actual scenes/startup/exact patch pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v922']=profile;save(path,registry)
    print('V922 registered;12 battle Finance comments,7336 full native copies and178 sequences pass. Actual scenes remain.',flush=True)


if __name__=='__main__':main()
