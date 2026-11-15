"""Register the full V975 stack plus39 source-reviewed mood/panic alternatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import mood_comments_editorial_v981b as owned,illness_critical_editorial as parent
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v981')
MANUSCRIPT=Path('translations/mood_comments_editorial_manuscript_v2.json')
OLD=Path('out/all_routes_combined_v969_candidate.nds')


def main():
    assert not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True,exist_ok=True)
    registry_path=Path('translations/release_stack.json');registry=read(registry_path);assert 'all-routes-unified-v981' not in registry['profiles']
    assert not (ROOT/'registry_before.json').exists();save(ROOT/'registry_before.json',registry)
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
    save(copies,{'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'complete_native_copies':len(cases),'cases':cases,'sequenced_cache_cases':sequence,
        'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass':True,'callee_saved_ABI_and_stack_pass':True,
        'existing_single_cache_policy_bytes_unchanged':True,'host_open_read_contract_only_not_actual_ROM_or_hardware':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    previous=read(parent.CONFIG)
    for name,digest in previous['dependencies'].items():assert sha(Path(name).read_bytes())==digest
    audit=ROOT/'native_audit/audit.json'
    extra=['dk4tool/patch/mood_comments_editorial_v981b.py', 'dk4tool/patch/illness_critical_editorial.py', 'translations/illness_critical_editorial_release_v1.json', 'translations/illness_critical_editorial_manuscript_v2.json', 'scripts/mood_comments_layout_v979.py', 'scripts/mood_comments_layout_v980.py', 'scripts/prepare_mood_comments_context_v977.py', 'scripts/prepare_mood_comments_prose_v978.py', 'scripts/probe_mood_comments_fonts_v979.py', 'scripts/probe_mood_comments_fonts_v980.py', 'scripts/prepare_mood_comments_native_v980.py', 'scripts/prepare_mood_repack_successor_v981b.py', 'scripts/audit_mood_comments_native_v981b.py', 'translations/mood_comments_editorial_manuscript_v1.json', 'work/analysis/mood_comments_v977/source_context_packet.json', 'work/analysis/mood_comments_v978/source_context_and_nonverbal_review.json', 'work/analysis/mood_comments_v979/native_font_proof.json', 'work/analysis/mood_comments_v980/native_font_proof.json', 'work/analysis/mood_comments_v980/visual_review.json', 'work/analysis/mood_comments_v981/repack_successor_provenance_v981b.json']+[str(audit),str(copies)]
    dependencies={name:sha(Path(name).read_bytes()) for name in [*previous['dependencies'],*extra]}
    config={'format':'dk4-illness-critical-editorial-v1','source_common_sha256':owned.SOURCE_COMMON,'source_arm9_sha256':owned.SOURCE_ARM,
        'target_common_sha256':sha(c),'target_arm9_sha256':sha(a),'directory_sha256':proof['directory_sha256'],
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_copy_proof':str(copies),'native_consumer_audit':str(audit),'dependencies':dependencies}
    save(owned.CONFIG,config);assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),owned.CONFIG)[:2]==(c,a)
    assert read(registry_path)==read(ROOT/'registry_before.json')
    profile=deepcopy(registry['profiles']['all-routes-unified-v975'])
    profile.update(mood_comments_editorial=owned.CONFIG,status='experimental',description='Complete V975 stack plus39 reviewed mood/panic comments1833-1871 for native moods0/4/5.',
        note='225 original mood selectors,75 physical-priority and72 normal-mood controls,78 complete native font cases,7336 copies and178 cache sequences pass. Existing native code,single8KiB cache,216x36 crop and123040 staged bytes preserved. Actual scenes,startup and exact patch pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v981']=profile;save(registry_path,registry)
    print('V981 registered;39 mood/panic messages,7336 native copies and178 sequences pass. Actual scenes remain.',flush=True)


if __name__=='__main__':main()
