from typing import Optional, List

from modules import _Module
from color import Color


class Card:
    """
    构建卡片
    """
    type: str = 'card'
    theme: str
    size: str
    color: Optional[Color]
    modules: List[_Module]

    def __init__(self, modules: List[_Module], theme: str = 'primary', size: str = 'lg', color: Color = None) -> None:
        """
        构建卡片

        :param modules: 卡片模块列表
        :param theme: 卡片主题
        :param size: 目前只支持sm与lg。 lg仅在PC端有效, 在移动端不管填什么，均为sm。
        :param color: 卡片颜色
        """
        self.modules = modules
        self.theme = theme
        self.size = size
        self.color = color

    def build(self) -> dict:
        """
        :return: 构造后卡片
        """
        ret = {'type': self.type, 'theme': self.theme, 'size': self.size, 'modules': []}
        if self.color is not None:
            ret['color'] = self.color.__str__()
        for i in self.modules:
            ret['modules'].append(i.build())
        return ret
