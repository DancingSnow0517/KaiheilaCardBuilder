from abc import ABC, abstractmethod
from typing import Union, Optional, List

from .modules import Header, Section, ImageGroup, Container, ActionGroup, Context, Divider, Invite, File, Video, Audio, \
    Countdown
from .accessory import PlainText, _BaseText, _BaseNonText, Paragraph, Image, Button, _BaseAccessory
from .card import CardMessage, Card


class AbstractBuilder(ABC):
    @abstractmethod
    def build(self):
        ...


class CardMessageBuilder(AbstractBuilder):

    def __init__(self) -> None:
        self.__card_message = CardMessage()

    def card(self, card: Card):
        self.__card_message.append(card)
        return self

    def build(self) -> CardMessage:
        return self.__card_message


class CardBuilder(AbstractBuilder):
    def __init__(self) -> None:
        self._card = Card()

    def header(self, text: Union[str, PlainText] = ''):
        self._card.append(Header(text))
        return self

    def section(self, text: Union[_BaseText, Paragraph], *, mode: str = 'right',
                accessory: _BaseNonText = None):
        self._card.append(Section(text, mode=mode, accessory=accessory))
        return self

    def image_group(self, image_group: ImageGroup):
        self._card.append(image_group)
        return self

    def container(self, container: Container):
        self._card.append(container)
        return self

    def action_group(self, action_group: ActionGroup):
        self._card.append(action_group)
        return self

    def context(self, context: Context):
        self._card.append(context)
        return self

    def divider(self):
        self._card.append(Divider())
        return self

    def day_countdown(self, end_time: str):
        self._card.append(Countdown.new_day_countdown(end_time))
        return self

    def hour_countdown(self, end_time: str):
        self._card.append(Countdown.new_hour_countdown(end_time))
        return self

    def second_countdown(self, end_time: str, start_time: Optional[str] = None):
        self._card.append(Countdown.new_second_countdown(end_time, start_time))
        return self

    def invite(self, code: str):
        self._card.append(Invite(code))
        return self

    def file(self, src: str, title: str):
        self._card.append(File(src, title))
        return self

    def video(self, src: str, title: str):
        self._card.append(Video(src, title))
        return self

    def audio(self, src: str, title: str, cover: Optional[str] = None):
        self._card.append(Audio(src, title, cover))
        return self

    def build(self) -> Card:
        return self._card

    @property
    def card(self):
        """非必要不访问"""
        return self._card


class MultiBuilder(AbstractBuilder, ABC):
    elements: List[_BaseAccessory]

    def __init__(self) -> None:
        self.elements = []

    @abstractmethod
    def add(self, accessory: _BaseAccessory):
        ...

    @abstractmethod
    def build(self):
        ...


class ImageGroupBuilder(MultiBuilder):
    def add(self, accessory: Image):
        self.elements.append(accessory)
        return self

    def build(self) -> ImageGroup:
        return ImageGroup(*self.elements)


class ContainerBuilder(MultiBuilder):

    def add(self, accessory: Image):
        self.elements.append(accessory)
        return self

    def build(self) -> Container:
        return Container(*self.elements)


class ActionGroupBuilder(MultiBuilder):
    def add(self, accessory: Button):
        self.elements.append(accessory)
        return self

    def build(self) -> ActionGroup:
        return ActionGroup(*self.elements)


class ContextBuilder(MultiBuilder):
    def add(self, accessory: _BaseAccessory):
        self.elements.append(accessory)
        return self

    def build(self) -> Context:
        return Context(*self.elements)
