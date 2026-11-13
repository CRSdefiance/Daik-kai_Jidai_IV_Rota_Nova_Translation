"""Match complete emulator pages and dynamic headers, then make readable QA crops."""
from pathlib import Path

from scripts.analyze_reviewed_dynamic_fixture_v1 import dynamic_headers
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE = Path('scripts/analyze_reviewed_scene_fixture.py')
source = checked_text(TEMPLATE.read_text(encoding='utf-8'), {
    "exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
        """source=checked_text(dynamic_headers(source),{
        'range(0, len(selected), 6)':'range(0,len(selected),15)',
        'selected[first:first+6]':'selected[first:first+15]',
        "(1536, 1600), '#eee'":"(1536, ((len(group)+2)//3)*270), '#eee'",
        'index // 3 * 800':'index // 3 * 270',
        ".convert('RGB').resize((512, 768), Image.Resampling.NEAREST)":
            ".convert('RGB').crop((0,263,256,384)).resize((512,242), Image.Resampling.NEAREST)",
    })
    exec(compile(source,__file__+'::complete-dynamic-headers-and-body-crops','exec'),globals())""",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::fixture-body-and-dynamic-header-verification', 'exec'), globals())

