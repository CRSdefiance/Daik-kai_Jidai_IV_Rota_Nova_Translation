"""Preserve the proven atomic compiler andderive B225's exact reviewed contract."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_atomic_tools_v7226')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
      'sixteen-speech B222':'thirteen-speech B225','lil_B222_profile_v1':'lil_B225_profile_v2','lil_B222_layout_v1':'lil_B225_layout_v2','seal_lil_B222_references_v7063':'seal_lil_B225_references_v7225','B222':'B225',
      "seal['all16_five_gates_and_exact_references_approved']":"seal['all13_five_gates_andexact_references_approved']",
      "len(rows)==len(ids)==16":"len(rows)==len(ids)==13", "{'revise':12,'retain-wording':4}":"{'revise':8,'retain-wording':5}",'{2:6,16:10}':'{2:4,16:7,151:1,162:1}',
      '==222':'==225','blocks[222]':'blocks[225]','block=222':'block=225',
      '(222,1112,1112,0,1336,1336,0)':'(225,976,974,2,1072,1072,0)',
      "not spec['target_native_skip_cases']":"not spec['target_native_skip_cases'] and not spec['original_C200_map']",
      'len(block)==1112':'len(block)==976', "==1112 and block[1108:]==bytes(4)":"==974 and block[970:]==bytes(6)",
      "controls['source_A000']['source_command_hex']=='00a0ffff44000110' and controls['relocated_A000']['error'] is None":"all(c['source']['error'] is None and c['relocated']['error'] is None for c in controls['source_andrelocated630B_A000_structural_cases'])",
      "actual['actual_unique_speeches']==16":"actual['actual_unique_speeches']==13", "actual['all27_commands_observed']":"actual['all25_commands_observed']", "actual['original_A000_source_offset1100_target1324_observed']":"actual['original_630B_source78_target88_observed']",
      "naming['two_contextual_name_retentions_approved_no_asset_change']":"naming['four_contextual_progressive_name_retentions_no_asset_or_duplicate_credit']", "len(naming['records'])==2":"len(naming['records'])==4",
      "patches=[];changes=[];pads=0":"from dk4tool.patch.lil_B225_atomic_support_v1 import audit_sealed_scope\n    audit_sealed_scope(doc,mapping,seal,load,require)\n    patches=[];changes=[];pads=0",
      '{2:3,16:1}[raw[0]]':'{2:3,16:1,151:4,162:0}[raw[0]]',
      "require(len(fonts[ident]['pages'])==len(stores[ident]['complete_pages']['pages'])==row['native_page_count']==1 and row['native_profile_maximum_total_rows']==row['original_physical_native_rows_per_page']==4,'single bounded page:'+ident);a,z=fonts[ident]['pages'][0],stores[ident]['complete_pages']['pages'][0];require(Path(a['native_plane']).read_bytes()==Path(z['native_plane']).read_bytes() and sha(Path(z['native_plane']).read_bytes())==z['native_plane_sha256']==a['native_plane_sha256'],'native complete ink:'+ident);panel=panels[ident]":"require(len(fonts[ident]['pages'])==len(stores[ident]['complete_pages']['pages'])==row['native_page_count']==b['native_page_count'] and row['native_profile_maximum_total_rows']==b['maximum_total_rows'] and row['original_physical_native_rows_per_page']==4,'original bounded pages:'+ident)\n        for a,z in zip(fonts[ident]['pages'],stores[ident]['complete_pages']['pages'],strict=True):require(Path(a['native_plane']).read_bytes()==Path(z['native_plane']).read_bytes() and sha(Path(z['native_plane']).read_bytes())==z['native_plane_sha256']==a['native_plane_sha256'],'native complete ink:'+ident)\n        panel=panels[ident]",
      "panel['native_pages']==1":"panel['native_pages']==b['native_page_count']", "pads==8":"pads==6", 'eight zero-ink':'six zero-ink',
      'block[last:1112]':'block[last:974]', 'mapped(1112)==1336':'mapped(974)==1072', "logical,4,1328":"logical,4,1064", "==18,'all18":"==16,'all16",
      "[(1100,1324,'00a0ffff44000110')]":"[(962,1060,'00a0ffff48000110')]", "[(1108,1332,'00000000')]":"[(970,1068,'00000000')]",
      'target[:1336]':'target[:1072]', 'inverse,4,1104':'inverse,4,966', 'block[1112:]':'block[974:]', 'complete1112-byte':'complete976-byte',
      'source_bytes=1112,target_bytes=1336,source_logical_end=1112,target_logical_end=1336,source_commands=18':'source_bytes=976,target_bytes=1072,source_logical_end=974,target_logical_end=1072,source_commands=16',
      'all16_objects16_pages_actual_complete':'all13_objects14_pages_actual_complete','two_contextual_name_retentions_no_asset_or_duplicate_credit':'four_contextual_name_retentions_no_asset_or_duplicate_credit',
      'original_A000_normal_end_residual_value_and_no_tail_preserved':'original630B_A000_normal_end_residual_value_and_source_tail_inverse_preserved'
    }
    report=derive('dk4tool/patch/lil_B222_editorial_v1.py','dk4tool/patch/lil_B225_editorial_v1.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_compiler.json',report)
    print('B225 atomic compiler derived;positive reconstruction required before registration.')
