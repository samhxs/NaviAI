# NaviAI

做一个类似ChatWise+Deep Research的产品

---

## VM + Plugin Demo (虚拟机 + 插件演示)

这是一个演示虚拟机和插件系统集成的项目，展示了如何在虚拟机中运行应用程序，并通过插件系统捕获应用运行时的各种数据。

### 功能特性

- **简单的栈式虚拟机** - 支持基本的算术运算和数据操作
- **应用程序执行** - 可以运行字节码格式的应用程序
- **插件系统** - 灵活的插件架构，支持事件钩子
- **数据提取插件**：
  - 文字提取插件 - 捕获应用显示的所有文本
  - 图片捕获插件 - 记录应用显示的所有图片
  - 声音录制插件 - 跟踪应用播放的所有声音

### 快速开始

#### 1. 运行演示

```bash
# 直接运行demo
python3 demo.py

# 或者给demo.py添加执行权限
chmod +x demo.py
./demo.py
```

#### 2. 查看演示内容

Demo包含三个演示场景：
- **基础演示** - 展示VM运行应用并通过插件捕获数据
- **多应用演示** - 展示同一个VM实例运行多个应用
- **插件搜索演示** - 展示插件的搜索和过滤功能

### 项目结构

```
NaviAI/
├── src/
│   ├── vm/                      # 虚拟机模块
│   │   ├── __init__.py
│   │   ├── core.py             # VM核心实现
│   │   ├── executor.py         # 指令执行器
│   │   └── memory.py           # 内存管理
│   │
│   └── plugins/                 # 插件系统
│       ├── __init__.py
│       ├── base.py             # 插件基类
│       ├── manager.py          # 插件管理器
│       └── examples/           # 示例插件
│           ├── __init__.py
│           ├── text_extractor.py    # 文字提取插件
│           ├── image_capture.py     # 图片捕获插件
│           └── sound_recorder.py    # 声音录制插件
│
├── demo.py                      # 演示程序
├── hello_world.py              # Hello World示例
├── requirements.txt            # 项目依赖
└── README.md                   # 本文件
```

### 使用示例

#### 创建并运行一个简单的应用

```python
from src.vm import VirtualMachine, OpCode
from src.plugins.examples import TextExtractorPlugin

# 创建虚拟机
vm = VirtualMachine()

# 加载文字提取插件
text_plugin = TextExtractorPlugin()
vm.load_plugin(text_plugin)

# 创建一个简单的应用
app = [
    (OpCode.PRINT_TEXT, "Hello, World!"),
    (OpCode.PRINT_TEXT, "你好，世界！"),
    (OpCode.HALT,)
]

# 运行应用
vm.run(app)

# 查看提取的文本
print(text_plugin.get_all_text())
```

#### 创建自定义插件

```python
from src.plugins import Plugin

class MyCustomPlugin(Plugin):
    def __init__(self):
        super().__init__("MyPlugin")

    def on_load(self, vm):
        # 注册事件处理器
        vm.register_event_handler('text_display', self.handle_text)
        print(f"[{self.name}] Loaded!")

    def on_unload(self, vm):
        print(f"[{self.name}] Unloaded!")

    def handle_text(self, text_data):
        # 处理文本数据
        self.collect_data(text_data)
        print(f"[{self.name}] Got text: {text_data}")
```

### VM指令集

当前支持的操作码：

| 指令 | 说明 | 示例 |
|------|------|------|
| `PUSH` | 压入值到栈 | `(OpCode.PUSH, 42)` |
| `POP` | 从栈弹出值 | `(OpCode.POP,)` |
| `ADD` | 加法运算 | `(OpCode.ADD,)` |
| `SUB` | 减法运算 | `(OpCode.SUB,)` |
| `MUL` | 乘法运算 | `(OpCode.MUL,)` |
| `DIV` | 除法运算 | `(OpCode.DIV,)` |
| `LOAD` | 从内存加载 | `(OpCode.LOAD, address)` |
| `STORE` | 存储到内存 | `(OpCode.STORE, address)` |
| `PRINT_TEXT` | 显示文本 | `(OpCode.PRINT_TEXT, "Hello")` |
| `SHOW_IMAGE` | 显示图片 | `(OpCode.SHOW_IMAGE, "pic.png")` |
| `PLAY_SOUND` | 播放声音 | `(OpCode.PLAY_SOUND, "sound.mp3")` |
| `HALT` | 停止执行 | `(OpCode.HALT,)` |

### 插件事件

插件可以监听以下事件：

- `text_display` - 当应用显示文本时触发
- `image_show` - 当应用显示图片时触发
- `sound_play` - 当应用播放声音时触发

### 技术架构

```
┌─────────────────────────────────────────┐
│           Application (App)             │
│         (Bytecode Instructions)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│        Virtual Machine (VM)             │
│  ┌──────────┐  ┌──────────┐            │
│  │  Memory  │  │ Executor │            │
│  └──────────┘  └──────────┘            │
│         │            │                  │
│         │     Event Hooks               │
│         │            │                  │
└─────────┼────────────┼──────────────────┘
          │            │
          ▼            ▼
┌─────────────────────────────────────────┐
│          Plugin System                  │
│  ┌────────────┐  ┌────────────┐        │
│  │   Plugin   │  │   Plugin   │  ...   │
│  │ Manager    │  │   Base     │        │
│  └────────────┘  └────────────┘        │
│                                         │
│  Example Plugins:                       │
│  • TextExtractor                        │
│  • ImageCapture                         │
│  • SoundRecorder                        │
└─────────────────────────────────────────┘
```

### 开发计划

- [x] 实现栈式虚拟机
- [x] 实现插件系统
- [x] 文字提取插件
- [x] 图片捕获插件
- [x] 声音录制插件
- [x] 完整的Demo程序
- [ ] 更多指令集支持
- [ ] 插件热加载/卸载
- [ ] 插件配置系统
- [ ] 性能优化
- [ ] 单元测试

### 许可证

MIT License

### 贡献

欢迎提交 Issue 和 Pull Request！
