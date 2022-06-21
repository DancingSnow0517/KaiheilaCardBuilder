# KaiheilaCardBuilder

一个构造开黑啦卡片的工具

## 使用方法

```python
from khl_card.card import Card
from khl_card.modules import *
from khl_card import *

# 新建卡片
# 这里构建了一个卡片，带有一个模块
card = Card(Section(Kmarkdown('测试卡片')))

# 给卡片添加模块，这里是分割线
card.append(Divider())

# 拥有的模块列表，具体用法参考开黑啦官方文档
['Header', 'Section', 'ImageGroup', 'Container', 'Context', 'ActionGroup', 'File', 'Audio', 'Video', 'Divider',
 'Invite', 'Countdown']

# 拥有的元素列表，具体用法参考开黑啦官方文档
['PlainText', 'Kmarkdown', 'Paragraph', 'Image', 'Button', '_BaseAccessory']

# 倒计时模块的简便创建
card.append(Countdown.new_day_countdown('2022-07-05 08:00:00'))
card.append(Countdown.new_hour_countdown('2022-07-05 08:00:00'))
card.append(Countdown.new_second_countdown('2022-07-05 08:00:00'))

# 现在支持链式调用
card.append(Section(Kmarkdown('调用1'))).append(Section(Kmarkdown('调用2'))).append(Section(Kmarkdown('调用3')))


# 构建卡片，返回的卡片的字典
card.build()

# 构建卡片，返回官方编辑器可以用的 json 文本
print(card.build_to_json())

# 输出：
{
    "type": "card",
    "theme": "primary",
    "size": "lg",
    "modules": [
        {
            "type": "section",
            "mode": "right",
            "text": {
                "type": "kmarkdown",
                "content": "测试卡片"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "countdown",
            "mode": "day",
            "endTime": 1656979200000,
            "startTime": 1655827836854
        },
        {
            "type": "countdown",
            "mode": "hour",
            "endTime": 1656979200000,
            "startTime": 1655827836854
        },
        {
            "type": "countdown",
            "mode": "second",
            "endTime": 1656979200000,
            "startTime": 1655827836891
        },
        {
            "type": "section",
            "mode": "right",
            "text": {
                "type": "kmarkdown",
                "content": "调用1"
            }
        },
        {
            "type": "section",
            "mode": "right",
            "text": {
                "type": "kmarkdown",
                "content": "调用2"
            }
        },
        {
            "type": "section",
            "mode": "right",
            "text": {
                "type": "kmarkdown",
                "content": "调用3"
            }
        }
    ]
}

```

## 更新日志

### 1.2.2

添加 `Card` 的链式调用

### 1.2.1

现在 `Card` 构建使用可变参数

### 1.1.1

卡片按钮现在使用 ``PlainText`` 或 ``Kmarkdown``

### 1.1.0

添加 ``Card`` 的一些方法

修复 ``Button`` 的构建 bug

修复 ``Color`` 中 ``__str__`` 的问题

为倒计时模块添加快速创建方法

```python
from khl_card.modules import *

Countdown.new_day_countdown('2022-05-05 08:00:00')
Countdown.new_hour_countdown('2022-05-05 08:00:00')
Countdown.new_second_countdown('2022-05-05 08:00:00')
```