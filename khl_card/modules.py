import json
import time
from abc import abstractmethod, ABC
from typing import Optional, Tuple, Union

from .accessory import _BaseText, _BaseNonText, _BaseAccessory, PlainText, Image, Button, Paragraph

__all__ = ['Header', 'Section', 'ImageGroup', 'Container', 'Context', 'ActionGroup', 'File', 'Audio', 'Video',
           'Divider', 'Invite', 'Countdown', '_Module']


class _Module(ABC):
    """
    模块基类
    """

    @abstractmethod
    def build(self) -> dict:
        """
        构建模块

        :return: 构造后模块
        """

    def build_to_json(self) -> str:
        return json.dumps(self.build(), indent=4, ensure_ascii=False)


class Header(_Module):
    """
    构建标题模块

    标题模块只能支持展示标准文本（text），突出标题样式。
    """
    text: PlainText

    def __init__(self, text: str = '') -> None:
        """
        构建标题模块

        标题模块只能支持展示标准文本（text），突出标题样式。

        :param text: 标题内容
        """
        self.type = 'header'
        self.text = PlainText(content=text)

    def build(self) -> dict:
        return {"type": self.type, "text": self.text.build()}


class Section(_Module):
    """
    构建内容模块

    结构化的内容，显示文本+其它元素。
    """
    mode: str
    text: _BaseText
    accessory: _BaseNonText

    def __init__(self, text: Union[_BaseText, Paragraph], *, mode: str = 'right', accessory: _BaseNonText = None) -> None:
        """
        构建内容模块

        结构化的内容，显示文本+其它元素。

        :param mode: accessory在左侧还是在右侧 只能为 left|right
        :param text: 文本元素，和结构体
        :param accessory: 非文本元素
        """
        self.type = 'section'
        self.mode = mode
        self.text = text
        self.accessory = accessory

    def build(self) -> dict:
        ret = {'type': self.type, 'mode': self.mode, 'text': self.text.build()}
        if self.accessory is None:
            return ret
        ret['accessory'] = self.accessory.build()
        return ret


class ImageGroup(_Module):
    """
    构建图片组模块

    1 到多张图片的组合
    """
    elements: Tuple[Image]

    def __init__(self, *elements: Image) -> None:
        """
        构建图片组模块

        1 到多张图片的组合

        :param elements: 图片元素，其它元素无效
        """
        self.type = 'image-group'
        if len(elements) > 9:
            raise Exception('图片元素最多为9个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class Container(_Module):
    """
    构建容器模块
    """
    elements: Tuple[Image]

    def __init__(self, *elements: Image) -> None:
        """
        构建容器模块

        1 到多张图片的组合，与图片组模块不同，图片并不会裁切为正方形。多张图片会纵向排列。

        :param elements: 图片元素，其它元素无效
        """
        self.type = 'container'
        if len(elements) > 9:
            raise Exception('图片元素最多为9个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class ActionGroup(_Module):
    """
    构建交互模块

    交互模块中包含交互控件元素，目前支持的交互控件为按钮（button）
    """
    elements: Tuple[Button]

    def __init__(self, *elements: Button) -> None:
        """
        构建交互模块

        交互模块中包含交互控件元素，目前支持的交互控件为按钮（button）

        :param elements: 按钮元素，其他无效
        """
        self.type = 'action-group'
        if len(elements) > 4:
            raise Exception('按钮元素最多为4个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class Context(_Module):
    """
    构建备注模块

    展示图文混合的内容。
    """
    elements: Tuple[_BaseAccessory]

    def __init__(self, *elements: _BaseAccessory) -> None:
        """
        构建备注模块

        展示图文混合的内容

        :param elements: 文本元素以及图片元素
        """
        self.type = 'context'
        if len(elements) > 10:
            raise Exception('元素最多为10个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class Divider(_Module):
    """
    构建分割线模块

    展示分割线。
    """

    def __init__(self) -> None:
        """
        构建分割线模块

        展示分割线。
        """
        self.type = 'divider'

    def build(self) -> dict:
        return {'type': self.type}


class Countdown(_Module):
    """
    构建倒计时模块

    展示倒计时。
    """
    endTime: int
    startTime: int
    mode: str

    def __init__(self, endtime: int, mode: str, starttime: int = time.time() * 1000) -> None:
        """
        构建倒计时模块

        展示倒计时

        :param mode: 倒计时样式, 按天显示，按小时显示或者按秒显示
        :param endtime: 到期的毫秒时间戳
        :param starttime: 起始的毫秒时间戳，仅当mode为second才有这个字段，默认为当前时间
        """
        self.type = 'countdown'
        if mode != 'day' and mode != 'hour' and mode != 'second':
            raise Exception('mode必须为 day|hour|second')
        self.mode = mode
        if endtime < starttime:
            raise Exception('结束时间要大于开始时间')
        self.endTime = endtime
        self.startTime = int(starttime)

    @classmethod
    def new_countdown(cls, end_time: str, mode):
        """
        :param mode: 倒计时模式
        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        """
        time_stamp = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        return cls(int(time_stamp * 1000), mode)

    @classmethod
    def new_day_countdown(cls, end_time: str):
        """
        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        """
        return cls.new_countdown(end_time, 'day')

    @classmethod
    def new_hour_countdown(cls, end_time: str):
        """
        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        """
        return cls.new_countdown(end_time, 'hour')

    @classmethod
    def new_second_countdown(cls, end_time: str, start_time: Optional[str] = None):
        """
        :param end_time: 结束时间 ex: 2022-05-05 08:00:00
        :param start_time: 开始时间 ex: 2022-05-05 08:00:00 留空则为当前时间
        """
        time_stamp = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        if start_time is None:
            start_time = time.time()
        else:
            start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        return cls(int(time_stamp * 1000), 'second', starttime=int(start_time * 1000))

    def build(self) -> dict:
        return {'type': self.type, 'mode': self.mode, 'endTime': self.endTime, 'startTime': self.startTime}


class Invite(_Module):
    """
    构建邀请模块

    提供服务器邀请/语音频道邀请
    """
    code: str

    def __init__(self, code: str) -> None:
        """
        构建邀请模块

        提供服务器邀请/语音频道邀请

        :param code: 邀请链接或者邀请码
        """
        self.type = 'invite'
        self.code = code

    def build(self) -> dict:
        return {'type': self.type, 'code': self.code}


class _FileModule(_Module):
    """
    文件模块基类
    """
    src: str
    title: str

    def __init__(self, src: str, title: str) -> None:
        self.src = src
        self.title = title

    def build(self) -> dict:
        return {'type': self.type, 'src': self.src, 'title': self.title}


class File(_FileModule):
    """
    构建文件模块

    展示文件
    """

    def __init__(self, src: str, title: str) -> None:
        """
        :param src: 文件地址
        :param title: 标题
        """
        super().__init__(src, title)
        self.type = 'file'


class Video(_FileModule):
    """
    构建视频模块

    展示视频
    """

    def __init__(self, src: str, title: str) -> None:
        """
        构建视频模块

        展示视频

        :param src: 视频地址
        :param title: 标题
        """
        super().__init__(src, title)
        self.type = 'video'


class Audio(_FileModule):
    """
    构建音频模块

    展示音频
    """
    cover: str

    def __init__(self, src: str, title: str, cover: str) -> None:
        """
        构建音频模块

        展示音频

        :param src: 音频地址
        :param title: 标题
        :param cover: 封面地址
        """
        super().__init__(src, title)
        self.type = 'audio'
        self.cover = cover

    def build(self) -> dict:
        ret = super().build()
        ret['cover'] = self.cover
        return ret
