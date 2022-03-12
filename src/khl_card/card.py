import json
from typing import Optional, List

from .color import Color
from .modules import _Module

__all__ = ['Card']


class Card:
    """
    构建卡片
    """
    type: str = 'card'
    theme: str
    size: str
    color: [Color, str]
    modules: List[_Module]

    def __init__(self, modules: List[_Module], theme: str = 'primary', size: str = 'lg', color: [Color, str] = None) -> None:
        """
        构建卡片

        :param modules: 卡片模块列表
        :param theme: 卡片主题
        :param size: 目前只支持sm与lg。 lg仅在PC端有效, 在移动端不管填什么，均为sm。
        :param color: 卡片颜色 ex: #55ffff or NamedColor.XXX
        """
        self.modules = modules
        self.theme = theme
        self.size = size
        if isinstance(color, Color):
            self.color = color.__str__()
        if isinstance(color, str):
            self.color = color

    def __getitem__(self, item: int):
        return self.modules[item]

    def build(self) -> dict:
        """
        :return: 构造后卡片
        """
        ret = {'type': self.type, 'theme': self.theme, 'size': self.size, 'modules': []}
        if self.color is not None:
            ret['color'] = self.color
        for i in self.modules:
            ret['modules'].append(i.build())
        return ret

    def build_to_json(self) -> str:
        return json.dumps(self.build(), indent=4, ensure_ascii=False)

    def append(self, module: _Module):
        self.modules.append(module)

    def clear(self):
        self.modules.clear()
