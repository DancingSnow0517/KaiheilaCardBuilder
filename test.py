from khl_card import Image, Kmarkdown
from khl_card.builder import CardMessageBuilder, CardBuilder, ImageGroupBuilder, ContextBuilder, ContainerBuilder

cm = CardMessageBuilder().card(
    CardBuilder()
    .image_group(
        ImageGroupBuilder()
        .add(Image('http://img.sdadad'))
        .build()
    )
    .context(
        ContextBuilder()
        .add(Kmarkdown('**Test context**'))
        .build()
    )
    .divider()
    .invite('asfws66')
    .container(
        ContainerBuilder()
        .add(Image('http://img.sdadad'))
        .add(Image('http://img.sdadad'))
        .build()
    )
    .header('This is a header')
    .section(Kmarkdown('This is a section'))
    .file('file_url', 'title')
    .audio('src', 'title', 'cover')
    .build()
).build()

print(cm)
