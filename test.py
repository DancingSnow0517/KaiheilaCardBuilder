from khl_card import CardMessage, Card, ActionGroup, Button, Kmarkdown
from khl_card.builder import CardMessageBuilder, CardBuilder

cm = CardMessageBuilder().add_card(
    CardBuilder()
    .add_header('Test Header')
    .add_invite("12345sdaf")
    .build()
).build()

for card in cm:
    print(card)
