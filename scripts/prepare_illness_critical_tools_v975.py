"""Preflight registered release/startup successors and one optional condition4/5 stage."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/illness_critical_v975')


def main():
    items=[]
    items.append(rendered('scripts/prepare_physical_wounds_release_v969.py','scripts/prepare_illness_critical_release_v975.py',[
        ('Register the full V962 stack plus13 source-reviewed wound alternatives.','Register the full V969 stack plus26 source-reviewed illness/near-death alternatives.'),
        ("'scripts/physical_wounds_layout_v967.py','scripts/physical_wounds_layout_v968.py','scripts/physical_wounds_layout_v968b.py'","'scripts/illness_critical_layout_v973.py','scripts/illness_critical_layout_v974.py'"),
        ('physical_wounds','illness_critical'),('physical_fatigue_editorial as parent','physical_wounds_editorial as parent'),
        ('illness_critical_v969','illness_critical_v975'),('all_routes_combined_v962','all_routes_combined_v969'),
        ('all-routes-unified-v969','all-routes-unified-v975'),('all-routes-unified-v962','all-routes-unified-v969'),
        ('dk4tool/patch/physical_fatigue_editorial.py','dk4tool/patch/physical_wounds_editorial.py'),('translations/physical_fatigue_editorial_manuscript_v2.json','translations/physical_wounds_editorial_manuscript_v2.json'),
        ('probe_illness_critical_fonts_v968b','probe_illness_critical_fonts_v974'),('prepare_illness_critical_context_v965','prepare_illness_critical_context_v971'),
        ('prepare_illness_critical_prose_v966','prepare_illness_critical_prose_v972'),('prepare_illness_critical_native_v968','prepare_illness_critical_native_v974'),('audit_illness_critical_native_v969','audit_illness_critical_native_v975'),
        ('illness_critical_v965/','illness_critical_v971/'),('illness_critical_v966/source_context_and_terms.json','illness_critical_v972/source_context_and_names.json'),('illness_critical_v968b/','illness_critical_v974/'),
        ('dk4-physical-wounds-editorial-v1','dk4-illness-critical-editorial-v1'),
        ('Complete V962 stack plus13 reviewed wound comments1794-1806 for native conditions2/3.','Complete V969 stack plus26 reviewed illness/near-death comments1807-1832 for native conditions5/4.'),
        ('150 original wound selectors,25 healthy and25 fatigue controls,52 complete native fonts','150 original condition4/5 selectors,100 prior-status controls,52 complete native fonts'),
        ('V969 registered;13 wound messages','V975 registered;26 illness/near-death messages')]))
    items.append(rendered('scripts/verify_physical_wounds_release_v969.py','scripts/verify_illness_critical_release_v975.py',[
        ('only13 selected strings','only26 selected strings'),('physical_wounds','illness_critical'),('illness_critical_release_v969','illness_critical_release_v975'),
        ('from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries','from dk4tool.patch.physical_wounds_editorial import current_entries as previous_entries'),
        ('all_routes_combined_v969','all_routes_combined_v975'),('all-routes-unified-v969','all-routes-unified-v975'),('all-routes-unified-v962','all-routes-unified-v969'),
        ('len(changed_IDs)==11','len(changed_IDs)==22'),('V969_exact_patch','V975_exact_patch'),('changed_components_relative_to_V962','changed_components_relative_to_V969'),
        ('all3655_other_text_strings_exact','all3642_other_text_strings_exact'),('V969: full471/114 inheritance,bounded physical-wounds','V975: full471/114 inheritance,bounded illness-critical')]))
    items.append(rendered('scripts/run_physical_wounds_startup_v969.py','scripts/run_illness_critical_startup_v975.py',[
        ('physical_wounds_v969','illness_critical_v975'),('all_routes_combined_v969','all_routes_combined_v975')]))
    items.append(rendered('scripts/verify_physical_wounds_startup_v969.py','scripts/verify_illness_critical_startup_v975.py',[
        ('physical_wounds_v969','illness_critical_v975'),('all_routes_combined_v969','all_routes_combined_v975'),('physical_fatigue_v962','physical_wounds_v969'),('V962','V969')]))
    items.append(rendered('scripts/check_physical_wounds_title_v970.py','scripts/check_illness_critical_title_v976.py',[
        ("choices=('969',)","choices=('975',)"),('V962','V969'),
        ("('962',CAP/'physical_fatigue_v963_title_962'),('969',CAP/'physical_wounds_v970_title_969')","('969',CAP/'physical_wounds_v970_title_969'),('975',CAP/'illness_critical_v976_title_975')"),
        ("reports['962'][0][1100].tobytes()==reports['969'][0][1100].tobytes()","reports['969'][0][1100].tobytes()==reports['975'][0][1100].tobytes()"),
        ("assert args.run=='969'","assert args.run=='975'"),('all_routes_combined_v969_candidate','all_routes_combined_v975_candidate'),
        ("folder=CAP/'physical_wounds_v970_title_969'","folder=CAP/'illness_critical_v976_title_975'"),
        ("ROOT=Path('work/analysis/physical_wounds_v970')","ROOT=Path('work/analysis/illness_critical_v976')"),('title_969_run_plan','title_975_run_plan')]))
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes();anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('illness_critical_editorial')" not in before
    lo=before.index(b"    physical_wounds_editorial = profile_config.get('physical_wounds_editorial')");hi=before.index(anchor)
    block=before[lo:hi].replace(b'physical_wounds',b'illness_critical').replace(b'PHYSICAL_WOUNDS',b'ILLNESS_CRITICAL')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'builder_before.py').exists()
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block);provenance=[]
    for source,target,raw,text in items:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    assert builder.read_bytes()==before;builder.write_bytes(after)
    save(ROOT/'registered_tools_provenance.json',{'files':provenance,'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'builder_prior_bytes_restored_by_removing_exact_optional_block':builder.read_bytes().replace(block,b'',1)==before,
        'all_successor_replacements_syntax_and_stage_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Five historical tools unchanged;successors and one optional illness/near-death stage preflighted.',flush=True)


if __name__=='__main__':main()
