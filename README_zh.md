# CTUI — CARNIVAL Terminal UI

一个 Gradio 风格的 Python 库，用于构建复古终端 UI。黑色背景、像素字体、键盘驱动的光标导航、鼠标磁吸，以及完整的组件系统。

## 快速开始

```python
from CTUI import TerminalApp

app = TerminalApp("我的应用")

with app.panel("main") as p:
    p.text("欢迎使用 CTUI")
    p.button("设置", target="settings")
    p.long_press("提交").on_activate(lambda v: print("done"))

with app.panel("settings") as p:
    p.switch("声音", ["关", "开", "静音"])
    p.slider("音量", 0, 100, 50)
    p.button("返回", target="main")

app.run()          # 浏览器 http://127.0.0.1:5051
# app.launch()     # pywebview 桌面窗口
# app.save("out.html")  # 导出静态 HTML
```

## 安装

```bash
pip install flask pywebview   # 运行时依赖
```

运行演示：
```bash
python -m CTUI.demo web       # 浏览器模式
python -m CTUI.demo lan       # 内网访问
```

## 组件列表

| 组件 | API | 说明 |
|---|---|---|
| **Text** | `p.text("内容")` | 静态文本，光标跳过 |
| **Button** | `p.button("标签", target="面板")` | 可点击，切换面板或触发回调 |
| **Switch** | `p.switch("标签", ["A","B","C"])` | Enter 循环切换选项 |
| **Toggle** | `p.toggle("标签")` | ON/OFF 二进制开关 |
| **Checkbox** | `p.checkbox("标签")` | `[x]` 样式复选框 |
| **Dropdown** | `p.dropdown("标签", ["A","B"])` | `[选项]` 样式循环选择器 |
| **LongPress** | `p.long_press("标签")` | 长按 2 秒激活，充能进度条动画 |
| **Input** | `p.input("占位符")` | 文本输入框，Enter 提交 |
| **DigitString** | `p.digit_string(6)` | 逐位数字编辑器，方向键 + 数字键 |
| **Slider** | `p.slider("标签", 0, 100, 50)` | 可调数值，Enter 编辑，方向键调整 |
| **DragBar** | `p.dragbar(42, "标签")` | 键盘模式中方向键调整的拖拽条 |
| **ProgressBar** | `p.progress(65, 100)` | 只读进度指示器 |
| **LogGenerator** | `p.log_generator(行列表, 速度)` | 自动滚动的启动日志动画 |
| **CommandConsole** | `p.command_console(提示, 解析器)` | 命令行界面，命令解析引擎 |
| **Keypad** | `p.keypad()` | 屏幕数字键盘，方向键 + Enter |
| **MemoryMatch** | `p.memory_match(行, 列, 配对列表, 计时)` | 记忆配对游戏 |
| **ChoiceGroup** | `p.choice_group(["A","B"])` | 交互式选项按钮，键盘导航 |
| **StoryText** | `p.story_text(行列表)` | 打字机小说阅读器，逐字显示 |
| **ScrollPanel** | `p.scroll_panel(组件列表, 高度)` | 自动滚动容器，用于溢出内容 |
| **Table** | `p.table(表头, 行数据)` | 数据表格展示 |
| **CodeBlock** | `p.code_block("代码")` | 预格式化代码展示 |
| **LogViewer** | `p.log_viewer(["行1"])` | 静态日志查看器 |
| **ScrollView** | `p.scroll_view("内容")` | 可滚动文本区域 |
| **Image** | `p.image("src.png")` | 像素艺术图片展示 |
| **StatusDot** | `p.status_dot("在线", "green")` | 彩色状态指示器，脉冲动画 |
| **GlitchText** | `p.glitch_text("机密")` | 故障抖动 + 色散动画文字 |
| **WebGLShader** | `p.webgl_shader(片段着色器源码)` | 全屏自定义 GLSL 着色器画布 |
| **Separator** | `p.separator()` | 水平分割线 |
| **Spinner** | `p.spinner("加载中")` | CSS 动画加载指示器 |
| **AudioToggle** | `p.audio_toggle()` | 静音/取消静音按钮 |
| **Dialog** | `p.dialog("id", "标题", "消息")` | 覆盖层对话框 |
| **Modal** | `p.modal("id", "标题", "内容")` | 覆盖层模态框 |
| **Typewriter** | `p.set_typewriter(秘密词表)` | 面板级全屏字符显示 + 词汇匹配 |
| **Countdown** | `p.set_countdown("2026-02-17T00:00:00")` | 面板级实时倒计时 |
| **Preloader** | `p.preloader(阶段列表)` | 启动序列进度条 |

## 颜色

条形组件（slider、progress、dragbar）支持 `color` 参数：

```python
p.slider("音量", color="white")    # 白色
p.progress(50, color="teal")        # 蓝绿色
p.dragbar(30, color="yellow")       # 黄色
p.slider("级别", color="red")       # 红色
```

## 回调

为交互组件绑定 Python 回调：

```python
def onClick(val):
    print(f"点击值: {val}")
    return {"action": "set-text", "target": "status", "value": "完成"}

p.button("执行").on_activate(onClick)
p.switch("模式").on_activate(onClick)
p.input("姓名").on_submit(onClick)
p.long_press("按住").on_activate(onClick)
```

返回字典触发前端动作：

| 动作 | 效果 |
|---|---|
| `{"action": "set-text", "target": "id", "value": "..."}` | 设置元素文本 |
| `{"action": "set-text", ..., "show": "#btn-id"}` | 同时显示隐藏元素 |
| `{"action": "set-text", ..., "status": "#el", "statusValue": "..."}` | 更新所有 `[id^="status-s"]` 元素 |
| `{"action": "switch-panel", "target": "panel-id"}` | 切换面板 |
| `{"action": "show-dialog", "dialogId": "id"}` | 打开对话框 |
| `{"action": "hide-dialog", "dialogId": "id"}` | 关闭对话框 |
| `{"action": "set-progress", "target": "id", "value": 50, "max": 100}` | 更新进度条 |
| `{"action": "set-digit", "target": "id", "value": "1234"}` | 填充数字串 |
| `{"action": "set-visible", "target": "id"}` | 切换 `data-visible` 属性 |

## 键盘操作

| 按键 | 操作 |
|---|---|
| `↑ ↓ ← →` | 在组件间移动光标 |
| `Enter` | 激活组件 / 确认 |
| `Enter` (按住) | 长按激活（2 秒） |
| `Escape` | 关闭对话框 / 退出编辑模式 / 跳过故事打字 |
| `↑ ↓`（StoryText 上） | 滚动故事内容（未完成时） |
| `↑ ↓`（ChoiceGroup 上） | 在选项间移动 |
| `↑ ↓ ← →`（Keypad 上） | 在按键间移动 |

## 鼠标

- 默认光标隐藏，复古块状光标（`#terminal-cursor`）跟随指针
- 30px 内磁吸到组件
- 点击激活组件（与键盘 Enter 效果一致）
- 闲置 3 秒：鼠标光标 0.4 秒渐隐，键盘光标渐显
- 鼠标移动：键盘光标立即隐藏

## 服务器

```python
app.run()                        # 仅本地
app.run(allow_lan=True)          # 绑定 0.0.0.0，显示内网地址
app.launch()                     # pywebview 桌面窗口
```

## 许可证

MIT
