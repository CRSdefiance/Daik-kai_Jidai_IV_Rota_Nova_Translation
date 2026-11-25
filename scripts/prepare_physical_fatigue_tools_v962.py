"""Preflight successors and one optional builder stage without editing historical tools."""
from pathlib import Path
from scripts.prepare_physical_fatigue_native_v961 import rendered
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/physical_fatigue_v962')


def main():
    sources=[]
    sources.append(rendered('scripts/prepare_battle_gunnery_deck_release_v954.py','scripts/prepare_physical_fatigue_release_v962.py',[
        ('Register24 battle Gunnery/DeckCleaning comments after the complete V947 stack.','Register13 physical fatigue comments after the complete V954 stack.'),
        ('battle_gunnery_deck','physical_fatigue'),('physical_fatigue_v954','physical_fatigue_v962'),
        ('all-routes-unified-v954','all-routes-unified-v962'),('all-routes-unified-v947','all-routes-unified-v954'),('all_routes_combined_v947','all_routes_combined_v954'),
        ('physical_fatigue_layout_v952','physical_fatigue_layout_v960'),('probe_physical_fatigue_fonts_v952','probe_physical_fatigue_fonts_v960'),
        ('audit_physical_fatigue_native_v954','audit_physical_fatigue_native_v962'),('prepare_physical_fatigue_context_v950','prepare_physical_fatigue_context_v957'),
        ('prepare_physical_fatigue_prose_v951','prepare_physical_fatigue_prose_v959'),('prepare_physical_fatigue_native_v953','prepare_physical_fatigue_native_v961'),
        ('scripts/probe_battle_boarding_pronoun_v943.py','scripts/probe_physical_fatigue_pronoun_v958.py'),
        ('work/analysis/battle_sails_boarding_v943/source_pronoun_proof.json','work/analysis/physical_fatigue_v958/source_pronoun_proof.json'),
        ('work/analysis/physical_fatigue_v950/','work/analysis/physical_fatigue_v957/'),
        ('work/analysis/physical_fatigue_v951/ordinary_context_and_terms.json','work/analysis/physical_fatigue_v959/source_context_and_terms.json'),
        ('work/analysis/physical_fatigue_v952/','work/analysis/physical_fatigue_v960/'),
        ("'dk4tool/patch/physical_fatigue_editorial.py',","'dk4tool/patch/physical_fatigue_editorial.py','dk4tool/patch/battle_gunnery_deck_editorial.py','scripts/battle_gunnery_deck_layout_v952.py',"),
        ('dk4-battle-gunnery-deck-editorial-v1','dk4-physical-fatigue-editorial-v1'),
        ('Complete V947 stack plus24 reviewed battle Gunnery8/DeckCleaning2 comments1757-1780.','Complete V954 stack plus13 reviewed physical-condition1 fatigue comments1781-1793.'),
        ('150 original battle/main/ordinary control selections,source-bound Aim/Gun Batteries help,all24 fonts,7336 full native copies and178 sequences pass.','75 original direct/main battle/ordinary condition1 selections,25 healthy controls,50 first-person expansions,all13 fonts in26 controls,7336 full native copies and178 sequences pass.'),
        ('V954 registered;24 battle Gunnery/DeckCleaning comments','V962 registered;13 physical fatigue comments')]))
    sources.append(rendered('scripts/verify_battle_gunnery_deck_release_v954.py','scripts/verify_physical_fatigue_release_v962.py',[
        ('only24 selected strings','only13 selected strings'),('battle_gunnery_deck','physical_fatigue'),
        ('from dk4tool.patch.battle_sails_boarding_editorial import current_entries as previous_entries','from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries'),
        ('physical_fatigue_release_v954','physical_fatigue_release_v962'),('all_routes_combined_v954','all_routes_combined_v962'),
        ('all-routes-unified-v954','all-routes-unified-v962'),('all-routes-unified-v947','all-routes-unified-v954'),
        ('len(changed_IDs)==17','len(changed_IDs)==10'),('V954_exact_patch','V962_exact_patch'),
        ('changed_components_relative_to_V947','changed_components_relative_to_V954'),('all3644_other_text_strings_exact','all3655_other_text_strings_exact'),
        ('V954: full471/114 inheritance,bounded battle-gunnery-deck','V962: full471/114 inheritance,bounded physical-fatigue')]))
    sources.append(rendered('scripts/run_battle_gunnery_deck_startup_v954.py','scripts/run_physical_fatigue_startup_v962.py',[
        ('battle_gunnery_deck_v954','physical_fatigue_v962'),('all_routes_combined_v954','all_routes_combined_v962')]))
    sources.append(rendered('scripts/verify_battle_gunnery_deck_startup_v954.py','scripts/verify_physical_fatigue_startup_v962.py',[
        ('battle_gunnery_deck_v954','physical_fatigue_v962'),('all_routes_combined_v954','all_routes_combined_v962'),
        ('battle_sails_boarding_v947','battle_gunnery_deck_v954'),('V947','V954')]))
    sources.append(rendered('scripts/check_battle_gunnery_deck_title_v955.py','scripts/check_physical_fatigue_title_v963.py',[
        ("choices=('954',)","choices=('962',)"),('V947','V954'),
        ("('947',CAP/'battle_sails_boarding_v948_title_947'),('954',CAP/'battle_gunnery_deck_v955_title_954')","('954',CAP/'battle_gunnery_deck_v955_title_954'),('962',CAP/'physical_fatigue_v963_title_962')"),
        ("reports['947'][0][1100].tobytes()==reports['954'][0][1100].tobytes()","reports['954'][0][1100].tobytes()==reports['962'][0][1100].tobytes()"),
        ("assert args.run=='954'","assert args.run=='962'"),('all_routes_combined_v954_candidate','all_routes_combined_v962_candidate'),
        ("folder=CAP/'battle_gunnery_deck_v955_title_954'","folder=CAP/'physical_fatigue_v963_title_962'"),
        ("ROOT=Path('work/analysis/battle_gunnery_deck_v955')","ROOT=Path('work/analysis/physical_fatigue_v963')"),('title_954_run_plan','title_962_run_plan')]))
    builder=Path('scripts/build_integrated_release.py');before=builder.read_bytes()
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('physical_fatigue_editorial')" not in before
    lo=before.index(b"    battle_gunnery_deck_editorial = profile_config.get('battle_gunnery_deck_editorial')")
    hi=before.index(anchor);block=before[lo:hi].replace(b'battle_gunnery_deck',b'physical_fatigue').replace(b'BATTLE_GUNNERY_DECK',b'PHYSICAL_FATIGUE')
    after=before[:hi]+block+before[hi:];assert after.replace(block,b'',1)==before;compile(after,str(builder),'exec')
    assert not (ROOT/'builder_before.py').exists()
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    provenance=[]
    for source,target,raw,text in sources:
        with target.open('x',encoding='utf-8') as f:f.write(text)
        assert source.read_bytes()==raw
        provenance.append({'source':str(source),'source_before_sha256':sha(raw),'source_after_sha256':sha(source.read_bytes()),'source_unchanged':True,
            'successor':str(target),'successor_sha256':sha(target.read_bytes())})
    assert builder.read_bytes()==before;builder.write_bytes(after)
    save(ROOT/'registered_tools_provenance.json',{'files':provenance,'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),
        'builder_prior_bytes_restored_by_removing_exact_optional_block':builder.read_bytes().replace(block,b'',1)==before,
        'all_replacements_syntax_and_dependencies_preflighted_before_output':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Five historical tools unchanged;new successors preflighted and one optional fatigue builder stage added.',flush=True)


if __name__=='__main__':main()
