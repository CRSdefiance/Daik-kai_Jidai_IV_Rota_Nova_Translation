"""Bind both dynamic selectors and the two complete cave-in voice tables."""
from scripts.bind_rafael_B221_B240_roles_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'assert len(records)==29 and selectors==[208]': 'assert len(records)==17 and selectors==[207,208]',
    "ctx.execute(env['dynamic'],[207,*selectors])": "ctx.execute(env['dynamic'],selectors)",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::both-original-role-selectors', 'exec'), globals())
