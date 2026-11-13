from scripts.bind_rafael_B221_B240_roles_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {'len(records)==29': 'len(records)==14'})
if __name__ == '__main__':
    exec(compile(source, __file__+'::exact-fourteen-alternative-role-binding', 'exec'), globals())
