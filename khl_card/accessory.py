import json
from abc import ABC, abstractmethod
from typing import List, Union

__all__ = ['PlainText', 'Kmarkdown', 'Paragraph', 'Image', 'Button', '_BaseAccessory', '_BaseText', '_BaseNonText']

from .types import ThemeTypes, SizeTypes


class _BaseAccessory(ABC):
    """
    元素基类
    """

    @abstractmethod
    def build(self) -> dict:
        """
        :return: 构造后元素
        """

    def build_to_json(self) -> str:
        return json.dumps(self.build(), indent=4, ensure_ascii=False)

    @abstractmethod
    def __repr__(self):
        ...


class _BaseText(_BaseAccessory, ABC):
    """
    文字类元素基类
    """
    content: str


class _BaseNonText(_BaseAccessory, ABC):
    """
    非文字类元素基类
    """


class PlainText(_BaseText):
    """
    构造纯文本元素
    """
    emoji: bool

    def __init__(self, content: str = '', emoji=True) -> None:
        """
        构造纯文本

        :param content: 文本内容
        :param emoji: 默认为 true。如果为 true,会把 emoji 的 shortcut 转为 emoji
        """
        self.type = 'plain-text'
        self.content = content
        self.emoji = emoji

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}

    def __repr__(self):
        return f'PlainText(content=\'{self.content}\', emoji={self.emoji})'


class Kmarkdown(_BaseText):
    """
    构造kmarkdown文本元素
    """

    def __init__(self, content: str = '') -> None:
        """
        构造kmarkdown文本

        :param content: kmarkdown文本
        """
        self.type = 'kmarkdown'
        self.content = content

    @classmethod
    def bold(cls, content: str = ''):
        """构造加粗文字"""
        return cls(f'**{content}**')

    @classmethod
    def italic(cls, content: str = ''):
        """构造斜体文字"""
        return cls(f'*{content}*')

    @classmethod
    def bold_italic(cls, content: str = ''):
        """构造加粗斜体文字"""
        return cls(f'***{content}***')

    @classmethod
    def strikethrough(cls, content: str = ''):
        """构造删除线文字"""
        return cls(f'~~{content}~~')

    @classmethod
    def link(cls, text: str, link: str):
        """构造超链接文字"""
        return cls(f'[{text}]({link})')

    @classmethod
    def divider(cls):
        return cls('---')

    @classmethod
    def quote(cls, content: str = ''):
        return cls(f'> {content}')

    @classmethod
    def underline(cls, content: str = ''):
        return cls(f'(ins){content}(ins)')

    @classmethod
    def spoiler(cls, content: str = ''):
        return cls(f'(spl){content}(spl)')

    @classmethod
    def at_channel(cls, channel_id: str):
        return cls(f'(chn){channel_id}(chn)')

    @classmethod
    def at_user(cls, user_id: str):
        return cls(f'(met){user_id}(met)')

    @classmethod
    def at_role(cls, role_id: str):
        return cls(f'(rol){role_id}(rol)')

    @classmethod
    def inline_code(cls, code: str):
        return cls(f'`{code}`')

    @classmethod
    def code_block(cls, code: str, language: str = ''):
        return cls(f'```{language}\n{code}\n```')

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}

    def __repr__(self):
        return f'Kmarkdown(content=\'{self.content}\')'

    def __add__(self, other: 'Kmarkdown') -> 'Kmarkdown':
        self.content += other.content
        return self


class Paragraph(_BaseAccessory):
    """
    构造多列文本元素
    """
    cols: int
    fields: List[_BaseText]

    def __init__(self, cols: int, fields: List[_BaseText]) -> None:
        """
        构造多列文本

        :param cols: 列数 只能为 1-3
        :param fields: 文本组件列表
        """
        if not (1 <= cols <= 3):
            raise Exception('文本列数不为 1-3')
        if len(fields) != cols:
            raise Exception('文本列数与列表不符')
        for i in fields:
            if isinstance(i, Paragraph):
                raise Exception('文本组件不能为paragraph')
        self.type = 'paragraph'
        self.cols = cols
        self.fields = fields

    def build(self) -> dict:
        ret = {'type': self.type, 'cols': self.cols, 'fields': []}
        for i in self.fields:
            ret['fields'].append(i.build())
        return ret

    def __repr__(self):
        return f'Paragraph(cols={self.cols}, fields=[{", ".join([text.__repr__() for text in self.fields])}])'


class Image(_BaseNonText):
    """
    显示图片元素
    """
    src: str
    alt: str
    size: str
    circle: bool

    def __init__(self, src: str, size: Union[str, SizeTypes] = 'lg', alt: str = '', circle: bool = False) -> None:
        """
        显示图片元素

        :param src: 图片地址
        :param size: 图片大小样式 只能为 sm 或 lg
        :param alt: 不知道干嘛用的
        :param circle: 显示圆形图片，在文本+图片时有效
        """
        self.type = 'image'
        self.src = src
        self.alt = alt
        self.size = size.value if isinstance(size, SizeTypes) else size
        self.circle = circle

    def build(self) -> dict:
        return {'type': self.type, 'src': self.src, 'alt': self.alt, 'size': self.size, 'circle': self.circle}

    def __repr__(self):
        return f'Image(src=\'{self.src}\', size=\'{self.size}\', alt=\'{self.alt}\', circle={self.circle})'


class Button(_BaseNonText):
    theme: str
    value: str
    click: str
    text: _BaseText

    def __init__(self, text: _BaseText, theme: Union[str, ThemeTypes] = 'primary', value: str = '',
                 click: str = '') -> None:
        self.type = 'button'
        self.text = text
        self.theme = theme if isinstance(theme, str) else theme.value
        self.value = value
        self.click = click

    def build(self) -> dict:
        return {'type': self.type, 'theme': self.theme, 'value': self.value, 'click': self.click,
                'text': self.text.build()}

    def __repr__(self):
        return f'Button(text={self.text.__repr__()}, theme=\'{self.theme}\', value=\'{self.value}\', click=\'{self.click}\')'
