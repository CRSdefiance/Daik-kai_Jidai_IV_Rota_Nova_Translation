"""Run the unchanged complete three-choice VM,caption andnegative contracts oncurrent Maria."""
from scripts import check_rafael_three_choice_batch_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'ctx=RegisteredRuntime(args.release,args.startup,captain=0)':
        'ctx=RegisteredRuntime(args.release,args.startup,captain=3)',
})
exec(compile(source,__file__+'::same-three-choice-input-ownership-native-VM-centering-pixels-andnegative-guards-captain3','exec'),globals())
