"""Run complete source/current native three-choice contracts for a variable whole-menu batch."""
from scripts import check_rafael_three_choice_single_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "assert len(rows)==doc['typed_choice_objects']==3":"assert len(rows)==doc['typed_choice_objects'] and len(rows)>0 and len(rows)%3==0",
    'assert len(groups)==1':'assert 3*len(groups)==len(rows)',
    'native_provider_alignments=6,bridged_modal_returns=24':'native_provider_alignments=6*len(groups),bridged_modal_returns=24*len(groups)',
    'PASS1 three-choice object/3 labels/6 provider alignments/24 bridged returns/12 complete planes':
        'PASS all complete three-choice objects,all labels,provider alignments,bridged returns andcaption planes',
})
exec(compile(source,__file__+'::same-complete-three-choice-contract-per-source-object', 'exec'),globals())
