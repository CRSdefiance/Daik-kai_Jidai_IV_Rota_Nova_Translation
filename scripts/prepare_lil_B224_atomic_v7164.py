"""Derive the flat strict-runtime compiler; retain its executed predecessor unchanged."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_atomic_tools_v7164')
if __name__=='__main__':
    assert not ROOT.exists()
    a='dk4tool/patch/lil_B222_editorial_v1.py';b='dk4tool/patch/lil_B224_editorial_v1.py'
    changes={
      'B222':'B224','seal_lil_B222_references_v7063':'seal_lil_B224_references_v7161',
      'sixteen-speech':'fifteen-speech','all16':'all15','len(rows)==len(ids)==16':'len(rows)==len(ids)==15',
      "{'revise':12,'retain-wording':4}":"{'revise':10,'retain-wording':5}",'{2:6,16:10}':'{26:7,197:8}',
      'sixteen decisions/two actors':'fifteen decisions/two actors',"r['block']==222":"r['block']==224",
      '(222,1112,1112,0,1336,1336,0)':'(224,960,958,2,1040,1040,0)',
      'blocks[222]':'blocks[224]','len(block)==1112':'len(block)==960',
      "struct.unpack_from('<H',block,4)[0]==1112":"struct.unpack_from('<H',block,4)[0]==958",'block[1108:]==bytes(4)':'block[954:]==bytes(6)',
      '00a0ffff44000110':'00a0ffff46000110','original_A000_source_offset1100_target1324_observed':'original_C200_source_offset952_target1034_observed',
      "actual['actual_unique_speeches']==16":"actual['actual_unique_speeches']==15",
      "naming['two_contextual_name_retentions_approved_no_asset_change']":"naming['two_contextual_name_retentions_no_asset_or_duplicate_credit']",
      "{2:3,16:1}":"{26:2,197:0}",'block=222':'block=224',
      "patches=[];changes=[];pads=0":"from dk4tool.patch.lil_B224_atomic_support_v1 import audit_sealed_scope\n    audit_sealed_scope(doc,mapping,seal,load,require)\n    patches=[];changes=[];pads=0",
      "pads==8":"pads==9",'eight zero-ink parity tails':'nine zero-ink parity tails',
      'block[last:1112]':'block[last:958]','mapped(1112)==1336':'mapped(958)==1040',
      "struct.pack_into('<H',logical,4,1328)":"struct.pack_into('<H',logical,4,1032)",
      "[(1100,1324,'00a0ffff44000110')]":"[(944,1026,'00a0ffff46000110')]",
      "[(1108,1332,'00000000')]":"[(954,1036,'00000000')] and [(e['source_offset'],e['target_offset'],e['source_hex']) for e in spec['original_C200_map']]==[(952,1034,'00c2')]",
      'A000/normal end':'A000/C200/normal end',
      'target[:1336]':'target[:1040]',"struct.pack_into('<H',inverse,4,1104)":"struct.pack_into('<H',inverse,4,950)",
      'block[1112:]':'block[958:]','complete1112-byte inverse':'complete960-byte inverse including tail2',
      'source_bytes=1112,target_bytes=1336,source_logical_end=1112,target_logical_end=1336':'source_bytes=960,target_bytes=1040,source_logical_end=958,target_logical_end=1040',
      'original_A000_normal_end_residual_value_and_no_tail_preserved':'original_A000_C200_normal_end_residual_value_source_tail2_target_no_tail_preserved',
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),changes)
    row=derive(a,b,changes);ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_atomic_compiler.json',dict(tool=row,all_native_high_integer_constants_and_multiplicity_preserved=True,source960_logical958_tail2_target1040_no_tail=True,all_gates_before_sole_archive_write=True,exact_QA_and_CP932_palette_support_required=True,new_credit=0,full_goal_complete=False))
