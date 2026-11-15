"""Refine the final Lil preview and rerun changed display cases."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_rumor_wraps_20261114 as exact_reuse
from scripts import stage_lil_final_wraps_20261114 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = previous.base, previous.sha, previous.prior
FILE, ARM, CLEAN, IlnkContainer = previous.FILE, previous.ARM, previous.CLEAN, previous.IlnkContainer
parent, initial_names = previous.parent, previous.initial_names
CAPTURE = previous.CAPTURE
PRIOR_ROOT = previous.ROOT
ROOT = Path('work/lil_final_wraps_20261114_v2')
RUNTIME = ROOT / 'lil_native_context.json'
REVIEW = previous.REVIEW.with_name('lil_final_wraps_context_v2.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded, expand_bytes = previous.native, previous.expanded, previous.expand_bytes

refinements = {
    (239, 129): ("If he's the thief, he could sell it soon. Hurry!",
                 ("If he's the thief,", 'he could sell it soon.')),
    (243, 18): ("A sailor who'd been to the New World told me about a river there that carries golden sand.",
                ('been to the New World', 'a river there', 'carries golden sand.')),
    (307, 26): ("Golden? Oh, that temple! It's a ways off...",
                ('Oh, that temple!', "It's a ways off...")),
    (319, 18): ("We're known for gold and ivory. They're valuable goods. There's good money in them, but both are in short supply.",
                ("We're known for gold and ivory.", "They're valuable goods.", "There's good money in them,",
                 'but both are in short supply.')),
    (324, 205): ("Oh, for crying out loud! We're going through. Everyone, run to the exit!",
                 ('Oh, for crying out loud!', "We're going through.", 'Everyone, run to the exit!')),
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
    'hodram_rumor_wraps_context_v1.json': 'lil_final_wraps_context_v1.json',
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
