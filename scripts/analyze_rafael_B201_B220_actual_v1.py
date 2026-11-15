"""Compare exact ordered emulator body and nameplate pixels, retaining compact QA sheets."""
from dk4tool.patch.grand_race_menu_release import sha
from scripts import analyze_rafael_B168_B169_actual_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


prior.SPECIAL={'DK4_MES_B208_R0008':'8163'}
prior.PIXEL_COUNTS={'DK4_MES_B208_R0008':6}
prior.sha=sha
exact_masks=prior.exact_masks

source=checked_text(prior.SOURCE, {
    "    exec(compile(source,__file__+'::ordered-body-and-header-with-exact-native-punctuation-masks','exec'),globals())":
        """    source=checked_text(source,{
        'range(0, len(selected), 6)':'range(0,len(selected),15)',
        'selected[first:first+6]':'selected[first:first+15]',
        "(1536, 1600), '#eee'":"(1536, ((len(group)+2)//3)*270), '#eee'",
        'index // 3 * 800':'index // 3 * 270',
        '.convert(\\'RGB\\').resize((512, 768), Image.Resampling.NEAREST)':
            ".convert('RGB').crop((0,263,256,384)).resize((512,242), Image.Resampling.NEAREST)",
    })
    exec(compile(source,__file__+'::ordered-body-and-header-with-exact-native-punctuation-masks','exec'),globals())""",
})

if __name__=='__main__':
    exec(compile(source,__file__+'::same-pixel-verification-with-legible-body-and-header-crops', 'exec'),globals())

