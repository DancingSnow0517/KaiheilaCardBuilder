from typing import Union, Optional

from . import PlainText, CardMessage, Card, Header, Section, ImageGroup, Container, ActionGroup, Context, Divider, \
    Invite, File, Video, Audio
from .accessory import _BaseText, _BaseNonText, Paragraph, Image, Button, _BaseAccessory


class CardMessageBuilder:

    def __init__(self) -> None:
        self.__card_message = CardMessage()

    def add_card(self, card: Card):
        self.__card_message.append(card)
        return self

    def build(self) -> CardMessage:
        return self.__card_message


class CardBuilder:
    def __init__(self) -> None:
        self.__card = Card()

    def add_header(self, text: Union[str, PlainText] = ''):
        self.__card.append(Header(text))
        return self

    def add_section(self, text: Union[_BaseText, Paragraph], *, mode: str = 'right',
                 accessory: _BaseNonText = None):
        self.__card.append(Section(text, mode=mode, accessory=accessory))
        return self

    def add_image_group(self, *elements: Image):
        self.__card.append(ImageGroup(*elements))
        return self

    def add_container(self, *elements: Image):
        self.__card.append(Container(*elements))
        return self

    def add_action_group(self, *elements: Button):
        self.__card.append(ActionGroup(*elements))
        return self

    def add_context(self, *elements: _BaseAccessory):
        self.__card.append(Context(*elements))
        return self

    def add_divider(self):
        self.__card.append(Divider())
        return self

    # TODO: Countdown

    def add_invite(self, code: str):
        self.__card.append(Invite(code))
        return self

    def add_file(self, src: str, title: str):
        self.__card.append(File(src, title))
        return self

    def add_video(self, src: str, title: str):
        self.__card.append(Video(src, title))
        return self

    def add_audio(self, src: str, title: str, cover: Optional[str] = None):
        self.__card.append(Audio(src, title, cover))
        return self

    def build(self) -> Card:
        return self.__card