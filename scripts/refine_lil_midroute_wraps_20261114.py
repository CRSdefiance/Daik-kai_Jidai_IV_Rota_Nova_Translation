"""Keep the item title intact and refine the breaks found in Lil's first preview."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_lil_midroute_wraps_20261114 as prior_preview
from scripts.source_locked_derivation_v5118 import checked_text


base, sha, prior = prior_preview.base, prior_preview.sha, prior_preview.prior
FILE, ARM, CLEAN = prior_preview.FILE, prior_preview.ARM, prior_preview.CLEAN
IlnkContainer, parent = prior_preview.IlnkContainer, prior_preview.parent
CAPTURE = prior_preview.CAPTURE
PRIOR_ROOT = prior_preview.ROOT
ROOT = Path('work/lil_midroute_wraps_20261114_v3')
RUNTIME = ROOT / 'lil_native_context.json'
REVIEW = prior_preview.REVIEW.with_name('lil_midroute_wraps_context_v3.json')
PROOF = ROOT / 'stored_and_native.json'
native, expanded = prior_preview.previous.native, prior_preview.previous.expanded
expand_bytes = prior_preview.previous.expand_bytes
initial_names = prior_preview.previous.opening.initial_names

refinements = {
    (71, 72): ("What are you saying?! I-it's nothing like that!",
               ('What are you saying?!', "I-it's nothing like that!")),
    (73, 304): ("Really?! I was impressive? I'm so, so happy!",
                ('I was impressive?', "I'm so, so happy!")),
    (77, 335): ('With your permission, might I join you on your travels?',
                ('With your permission,', 'might I join you on your travels?')),
    (115, 128): ("The great powers want to divide the whole world among themselves. They seek the Proofs of Conquest to justify their claims. We're collecting them to stop that.",
                 ('The great powers want to divide', 'the whole world among themselves.',
                  'They seek the Proofs of Conquest', 'to justify their claims.', "We're collecting them to stop that.")),
    (128, 135): ("W-wait, {MACRO:FI}! Mr. Speyer, it's a joke! A joke! She's a little... odd...",
                 ('W-wait, {MACRO:FI}!', "Mr. Speyer, it's a joke!", 'A joke!', "She's a little... odd...")),
    (128, 226): ("Sorry, sorry. Let's do it your way, {MACRO:FI}. Fight them or compete by investing.",
                 ('Sorry, sorry.', "Let's do it your way, {MACRO:FI}.", 'Fight them or compete by investing.')),
    (135, 53): (prior_preview.DECISIONS[135, 53][1],
                ('hello, pretty lady.', "Are you after Goddess' Temptation, too?")),
    (136, 9): ('The Upper and Lower Stone Tablets?', ('Upper and Lower Stone Tablets?',)),
}

DECISIONS = prior_preview.DECISIONS.copy()
for key, (draft, phrases) in refinements.items():
    actor, _, meaning, note, _ = DECISIONS[key]
    if key == (71, 72):
        note = 'Make Lil’s baffled protest a short question before her complete stammered reply to Camille’s teasing.'
    DECISIONS[key] = actor, draft, meaning, note, phrases

get_exchanges = FunctionType(prior_preview.get_exchanges.__code__, prior_preview.get_exchanges.__globals__ | globals())
compile_rows = FunctionType(prior_preview.compile_rows.__code__, prior_preview.compile_rows.__globals__ | globals()
                            | {'previous': initial_names})
bind_runtime = FunctionType(prior_preview.bind_runtime.__code__, prior_preview.bind_runtime.__globals__ | globals())
stage_source = checked_text(getsource(prior_preview.main), {
    "assert pages[0]['first_visible_origin'] == [0, 0]":
        "assert pages[0]['first_visible_origin'] == [0, 0], (row['id'], label)",
    "assert len(pages) == row['automatic_layout']['expected_native_pages']":
        "assert len(pages) == row['automatic_layout']['expected_native_pages'], row['id']",
    "assert [p['native_plane_hex'] for p in pages] == [p['native_plane_hex'] for p in unpadded]":
        "assert [p['native_plane_hex'] for p in pages] == [p['native_plane_hex'] for p in unpadded], row['id']",
})
env = prior_preview.main.__globals__ | globals()
exec(compile(stage_source, __file__ + '::native-phrase-and-allocation-checks', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    main(parser.parse_args().preview)
