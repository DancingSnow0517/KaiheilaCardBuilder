from abc import ABC, abstractmethod
from typing import Union, Optional, List

from .modules import Header, Section, ImageGroup, Container, ActionGroup, Context, Divider, Invite, File, Video, Audio, \
    Countdown
from .accessory import PlainText, _BaseText, _BaseNonText, Paragraph, Image, Button, _BaseAccessory
from .card import CardMessage, Card

__all__ = ['CardMessageBuilder', 'CardBuilder', 'ImageGroupBuilder', 'ContainerBuilder', 'ContextBuilder',
           'ActionGroupBuilder']


class AbstractBuilder(ABC):
    @abstractmethod
    def build(self):
        ...


class CardMessageBuilder(AbstractBuilder):

    def __init__(self) -> None:
        self.__card_message = CardMessage()

    def card(self, card: Card):
        """添加一个卡片到卡片消息中"""
        self.__card_message.append(card)
        return self

    def build(self) -> CardMessage:
        """构造为 CardMessage"""
        return self.__card_message


class CardBuilder(AbstractBuilder):
    def __init__(self) -> None:
        self._card = Card()

    def header(self, text: Union[str, PlainText] = ''):
        """
        为卡片添加一个 header

        :param text: 标题内容
        """
        self._card.append(Header(text))
        return self

    def section(self, text: Union[_BaseText, Paragraph], *, mode: str = 'right',
                accessory: _BaseNonText = None):
        """
        为卡片添加一个 section

        :param text: 文本元素或结构体
        :param mode: accessory在左侧还是在右侧 只能为 left|right
        :param accessory: 非文本元素
        """
        self._card.append(Section(text, mode=mode, accessory=accessory))
        return self

    def image_group(self, image_group: ImageGroup):
        """
        为卡片添加一个 image_group

        :param image_group: 要添加的 ImageGroup
        """
        self._card.append(image_group)
        return self

    def container(self, container: Container):
        """
        为卡片添加一个 container

        :param container: 要添加的 Container
        """
        self._card.append(container)
        return self

    def action_group(self, action_group: ActionGroup):
        """
        为卡片添加一个 action_group

        :param action_group: 要添加的 ActionGroup
        """
        self._card.append(action_group)
        return self

    def context(self, context: Context):
        """
        为卡片添加一个 context

        :param context: 要添加的 Context
        """
        self._card.append(context)
        return self

    def divider(self):
        """为卡片添加一个 divider"""
        self._card.append(Divider())
        return self

    def day_countdown(self, end_time: str):
        """
        为卡片添加一个 天-倒计时

        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        """
        self._card.append(Countdown.new_day_countdown(end_time))
        return self

    def hour_countdown(self, end_time: str):
        """
        为卡片添加一个 小时-倒计时

        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        """
        self._card.append(Countdown.new_hour_countdown(end_time))
        return self

    def second_countdown(self, end_time: str, start_time: Optional[str] = None):
        """
        为卡片添加一个 秒-倒计时

        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        :param start_time: 开始时间 ex: 2022-05-05 08:00:00 留空则为当前时间
        """
        self._card.append(Countdown.new_second_countdown(end_time, start_time))
        return self

    def invite(self, code: str):
        """
        为卡片添加一个 invite

        :param code: 邀请码
        """
        self._card.append(Invite(code))
        return self

    def file(self, src: str, title: str):
        """
        为卡片添加一个 file

        :param src: 文件链接
        :param title: 文件标题
        """
        self._card.append(File(src, title))
        return self

    def video(self, src: str, title: str):
        """
        为卡片添加一个 video

        :param src: 视频链接
        :param title: 视频标题
        """
        self._card.append(Video(src, title))
        return self

    def audio(self, src: str, title: str, cover: Optional[str] = None):
        """
        为卡片添加一个 audio

        :param src: 音乐链接
        :param title: 音乐标题
        :param cover: 音乐封面
        """
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
