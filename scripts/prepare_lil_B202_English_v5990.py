"""Prepare the complete English scene and exact paired source-capture audit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save,read
ROOT=Path('work/analysis/lil_B202_English_tools_v5990')
if __name__=='__main__':
    assert not ROOT.exists();plan=read('work/analysis/lil_B202_relocation_v5983/nested_source_relocation_research.json');b=plan['blocks'][0];assert b['block']==202 and b['source_bytes']==588 and b['source_logical_end']==586
    tools=[derive('scripts/research_lil_B200_English_fixture_v5859.py','scripts/research_lil_B202_English_fixture_v5990.py',{
      'B200':'B202','prepare_lil_B200_reference_tools_v5850':'prepare_lil_B202_references_v5982','English_fixture_v5859':'English_fixture_v5990','English_v5859':'English_v5990','source_fixture_v5835':'source_fixture_v5967',
      'bank[200]':'bank[202]','source_block=200':'source_block=202',
      'assert len(bank[200])==end==828':"assert len(bank[202])==plan['blocks'][0]['research_bytes'] and end==plan['blocks'][0]['research_logical_end']",
      'len(native)==31':'len(native)==26','len(commands)==40':'len(commands)==35','all40':'all35','all31':'all26','event200_activation':'event202_activation',
      'source_fixture_v5836':'source_fixture_v5968','English_fixture_v5860':'English_fixture_v5991','source_run_v5836':'source_run_v5968','source_v5836':'source_v5968','English_run_v5860':'English_run_v5991','English_v5860':'English_v5991','31 original+9':'26 original+9'}))]
    tools.append(derive('scripts/audit_lil_B200_actual_v5861.py','scripts/audit_lil_B202_actual_v5992.py',{
      'B200':'B202','actual_v5861':'actual_v5992','source_fixture_v5835':'source_fixture_v5967','English_fixture_v5859':'English_fixture_v5990','source_run_v5836':'source_run_v5968','English_run_v5860':'English_run_v5991',
      'fonts_v5848':'fonts_v5978','all19_progressive_FE_native_planes_and152_alignment_cases':'all19_progressive_native_planes_and152_alignment_cases',
      '[5,9,13,17,21,25,29,33,37,40,44,47,50,54,58,62,65,69,72]':'[5,9,13,16,20,23,27,31,35,39,43,47,51,55,58,61,65,68,72]',
      "pairs[-1]['source_offset']==926":"pairs[-1]['source_offset']==582",'len(pairs)==40':'len(pairs)==35',
      "sum(r['prefix']==254 for r in actual)==2":"sum(r['prefix']==254 for r in actual)==0",'all31_source_commands':'all26_source_commands','end926':'end582','event200_activation':'event202_activation'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_English_fixture_and_audit_tools.json',dict(tools=tools,source_bytes=588,source_logical_end=586,target_bytes=b['research_bytes'],target_logical_end=b['research_logical_end'],all26_source_commands_and9_initializers_preserved=True,new_review_credit=0,full_goal_complete=False));print('Complete B202 English fixture/run and19-panel paired audit prepared;stored/logical extents taken from exact relocation proof.')
