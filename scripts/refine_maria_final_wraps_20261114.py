"""Refine the final Maria previews and rerun changed display cases."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_rumor_wraps_20261114 as exact_reuse
from scripts import stage_maria_final_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
parent, initial_names = previous.parent, previous.initial_names
CAPTURE = previous.CAPTURE
PRIOR_ROOT = previous.ROOT
ROOT = Path('work/maria_final_wraps_20261114_v2')
RUNTIME = ROOT / 'maria_native_context.json'
REVIEW = previous.REVIEW.with_name('maria_final_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded, expand_bytes = previous.native, previous.expanded, previous.expand_bytes

refinements = {
    (200, 15): ("Fear of the blade can make you pull back halfway through a move. That's when you're most likely to get badly hurt. You've got to keep your nerve and face that fear.",
                ('Fear of the blade', 'pull back halfway', 'most likely to get badly hurt.', 'keep your nerve', 'face that fear.')),
    (249, 14): ("He prowls the Mediterranean, or so I hear. I'm counting on you. Here's your advance.",
                ('prowls the Mediterranean,', 'or so I hear.', "I'm counting on you.", "Here's your advance.")),
    (253, 5): ("There you are! You're {MACRO:FA}, right? The London Guild asked for you.",
               ("You're {MACRO:FA}, right?", "The London Guild asked for you.")),
}
DECISIONS = previous.DECISIONS.copy()
for key, (draft, phrases) in refinements.items():
    actor, _, meaning, note, _ = DECISIONS[key]
    DECISIONS[key] = actor, draft, meaning, note, phrases

get_exchanges = FunctionType(previous.get_exchanges.__code__, previous.get_exchanges.__globals__ | globals())
compile_rows = FunctionType(previous.compile_rows.__code__, previous.compile_rows.__globals__ | globals()
                            | {'previous': initial_names})
bind_runtime = FunctionType(previous.bind_runtime.__code__, previous.bind_runtime.__globals__ | globals())
reuse_source = checked_text(getsource(exact_reuse.native_runner), {
    'hodram_rumor_wraps_context_v1.json': 'maria_final_wraps_context_v1.json',
    "for row in review['records']:": "for row in review['records'] + review['unchanged_leads']:",
    'previous.native(ctx, selector, body': 'native(ctx, selector, body',
})
env = globals().copy()
exec(compile(reuse_source, __file__ + '::verified-page-reuse', 'exec'), env)
native_runner = env['native_runner']
env = previous.main.__globals__ | globals()
exec(compile(exact_reuse.source, __file__ + '::fresh-phrase-refinements-and-exact-reuse', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
