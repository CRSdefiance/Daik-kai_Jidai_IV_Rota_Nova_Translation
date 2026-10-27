"""Register Hamburg after the complete V1945 stack; no promotion."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/register_lil_speyer_v1944.py')
SOURCE_SHA = '8f833fa1349e2951d12d06d982fc037dac69aa1beccb5a0ed4152e5e81948dad'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_speyer_editorial':'lil_hamburg_editorial',
        'scripts.approve_lil_speyer_references_v1942':'scripts.approve_lil_hamburg_references_v1968',
        'lil_Speyer_release_v1944':'lil_Hamburg_release_v1970',
        "PROFILE='all-routes-unified-v1945'":"PROFILE='all-routes-unified-v1971'",
        'out/all_routes_combined_v1909_candidate.nds':'out/all_routes_combined_v1945_candidate.nds',
        'work/analysis/lil_Speyer_research_v1929/lil_Speyer_V1909_derived_RESEARCH_ONLY.nds':
            'work/analysis/lil_Hamburg_research_v1961/lil_Hamburg_V1945_derived_RESEARCH_ONLY.nds',
        "assert sha(PARENT.read_bytes())=='fdc6757a13af0a04c4f2355ade3c66163a6382a0a7081efa03a457b1198dd1d1'":
            "assert sha(PARENT.read_bytes())=='c2432768da7e12c6fce7af9e4d887af932de2532a2d3a16eddbbe407067f6caf'",
        "assert sha(RESEARCH.read_bytes())=='c2432768da7e12c6fce7af9e4d887af932de2532a2d3a16eddbbe407067f6caf'":
            "assert sha(RESEARCH.read_bytes())=='c4c998e446b7ac410d2294563fc4e5d5181cef6938c25254b1bd3679492efa20'",
        'dk4tool/dialogue/lil_speyer_profile.py':'dk4tool/dialogue/lil_hamburg_profile.py',
        'work/analysis/lil_Speyer_approval_v1942/final_source_reference_approval.json':
            'work/analysis/lil_Hamburg_approval_v1968/final_source_reference_approval.json',
        'dk4-lil-speyer-editorial-release-v1':'dk4-lil-hamburg-editorial-release-v1',
        'speyer_report':'hamburg_report',
        'speyer_batch':'hamburg_batch',
        'Speyer':'Hamburg',
        "len(plan['changed_records'])==59":"len(plan['changed_records'])==81",
        '[25,128]':'[74]',
        "sum(r['growth_bytes']for r in plan['blocks'])==108":"sum(r['growth_bytes']for r in plan['blocks'])==168",
        "['blocks'][1]":"['blocks'][0]",
        "replace('SPEAKER:1D','SPEAKER:98')":"replace('SPEAKER:02','SPEAKER:10')",
        'all-routes-unified-v1909':'all-routes-unified-v1945',
        'release_stack_v1944_pending.json':'release_stack_v1970_pending.json',
        'Complete V1909 stack plus57 contextually reviewed Hamburg speeches and two choice labels.':
            'Complete V1945 stack plus79 contextually reviewed Hamburg recruitment and battle-lesson speeches and two choice labels.',
        'Only SC2 B25/B128 grow108bytes total;137commands48typed spans;51actual speeches102holds,two complete visible labels,sixspeech offline. Original Hamburg79 captures remain separate/unreviewed. Identity/patch/startup pending;V1492 stays promoted.':
            'Only SC2 B74 grows168bytes;123commands20typed spans;79actual speeches158holds,three FE panels,six FE holds,two complete visible labels andthe original join panel. Choice1 source/native-VM only. Identity/patch/startup pending;V1492 stays promoted.',
    }
    for old,new in changes.items():
        assert old in text,old
        text = text.replace(old,new)
    # Two Hamburg-specific negative controls exercise the separate FE consumer.
    old = "'missing_macro','changed_choice_label','duplicate_choice_index','unreviewed_choice','missing_choice')"
    new = "'missing_macro','FE_as_progressive','false_FE_actual','changed_choice_label','duplicate_choice_index','unreviewed_choice','missing_choice')"
    assert text.count(old) == 1
    text = text.replace(old,new)
    anchor = "        elif label=='changed_choice_label':value['records'][0]['english']+=' Extra words.'"
    addition = """        elif label=='FE_as_progressive':
            row=next(r for r in value['records']if r['source_presentation_prefix_hex']=='fe')
            row['native_display_consumer']='original_progressive_54020'
        elif label=='false_FE_actual':
            actual=deepcopy(read(value['actual_visual_review']))
            actual['all3_FE_panels_six_actual_holds_match_separate_paper_planes']=False
            actual_path=ROOT/'false_FE_actual_proof.json'
            save(actual_path,actual)
            value['actual_visual_review']=str(actual_path)
            bad['dependencies'][str(actual_path)]=sha(actual_path.read_bytes())
"""
    assert text.count(anchor) == 1
    text = text.replace(anchor,addition+anchor)
    assert text.count('assert len(negatives)==18') == 1
    text = text.replace('assert len(negatives)==18','assert len(negatives)==20')
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
