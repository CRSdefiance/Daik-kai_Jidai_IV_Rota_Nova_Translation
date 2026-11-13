"""Use the qualified fully guarded three-choice consumer with explicit Maria runtime."""
from scripts import check_rafael_three_choice_single_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'ctx=RegisteredRuntime(args.release,args.startup,captain=0)': 'ctx=RegisteredRuntime(args.release,args.startup,captain=3)',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-three-choice-provider-pixels-canaries-andindices-Maria', 'exec'), globals())
