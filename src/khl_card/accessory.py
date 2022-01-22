from typing import List


class _BaseAccessory:
    """
    元素基类
    """
    type: str

    def build(self) -> dict:
        """
        :return: 构造后元素
        """
        return {'type': self.type}


class _BaseText(_BaseAccessory):
    """
    文字类元素基类
    """

    def build(self) -> dict:
        return {'type': self.type}


class _BaseNonText(_BaseAccessory):
    """
    非文字类元素基类
    """
    def build(self) -> dict:
        return {'type': self.type}


class PlainText(_BaseText):
    """
    构造纯文本元素
    """
    content: str
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


class Kmarkdown(_BaseText):
    """
    构造kmarkdown文本元素
    """
    content: str

    def __init__(self, content: str = '') -> None:
        """
        构造kmarkdown文本

        :param content: kmarkdown文本
        """
        self.type = 'kmarkdown'
        self.content = content

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}


class Paragraph(_BaseText):
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


class Image(_BaseNonText):
    """
    显示图片元素
    """
    src: str
    alt: str
    size: str
    circle: bool

    def __init__(self, src: str, size: str = 'lg', alt: str = '', circle: bool = False) -> None:
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
        self.size = size
        self.circle = circle

    def build(self) -> dict:
        return {'type': self.type, 'src': self.src, 'alt': self.alt, 'size': self.size, 'circle': self.circle}


class Button(_BaseNonText):
    theme: str
    value: str
    click: str
    text: str

    def __init__(self, text: str, theme: str = 'primary', value: str = '', click: str = '') -> None:
        self.type = 'button'
        self.text = text
        self.theme = theme
        self.value = value
        self.click = click

    def build(self) -> dict:
        return {'type': self.type, 'theme': self.theme, 'value': self.theme, 'click': self.click, 'text': self.text}
