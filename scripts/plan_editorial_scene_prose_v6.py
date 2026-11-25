"""Keep complete source-bound sentences and the Cape of Good Hope coherent."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/plan_editorial_scene_prose_v5.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "        'DK4_MES_B89_R0067': 'You can say you found it yourself.',":
    """        'DK4_MES_B89_R0067': 'You can say you found it yourself.',
        'DK4_MES_B95_R0026': 'I carried it for years and was very fond of it.',
        'DK4_MES_B102_R0041': "That's all I could find out.",
        'DK4_MES_B103_R0038': "Of course, if I happen to hear something, I'll let you know.",
        'DK4_MES_B104_R0013': "They say he could even see the moon's uneven surface in detail.",""",
    "    pairs=previous.PAIRS|''',":
    "    pairs=previous.PAIRS|{('cape','of'),('of','good'),('good','hope'),(\"i'll\",'let')}|''',",
})
exec(compile(source,__file__+'::automatic-sentence-page-coherence','exec'),globals())
