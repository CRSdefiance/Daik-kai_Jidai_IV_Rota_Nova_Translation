"""Source-faithful successor: keep the opening trade limitation broad and grammatical."""
from copy import deepcopy
from scripts import lil_trade_lesson_Fernando_cards_prose_v3271 as prior

SPEECH=deepcopy(prior.SPEECH)
CHOICES=deepcopy(prior.CHOICES)
SPEECH[(126,57)]=(
    'Buy goods cheaply and sell them dearly: the basic principle of trade. At first, the number of goods one can handle is limited...',
    'Buy low, sell high. That\'s the basis of trading. You won\'t be able to trade much at first...',
    'Preserve the initial trading limitation without turning it into advice or inferring a specific assortment restriction; the following cargo-hold and market-share explanation supplies the quantity context.')
