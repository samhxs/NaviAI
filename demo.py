#!/usr/bin/env python3
"""
VM + Plugin Demo

Demonstrates a virtual machine that can run apps with plugin support
for extracting images, text, and sound.
"""

from src.vm import VirtualMachine, OpCode
from src.plugins.examples import (
    TextExtractorPlugin,
    ImageCapturePlugin,
    SoundRecorderPlugin
)
from src.plugins import PluginManager
import json


def create_sample_app():
    """
    Create a sample app that displays text, images, and plays sound

    Returns:
        List of VM instructions
    """
    return [
        # Display welcome text
        (OpCode.PRINT_TEXT, "欢迎使用 NaviAI VM+插件演示系统！"),
        (OpCode.PRINT_TEXT, "Welcome to NaviAI VM + Plugin Demo!"),

        # Show some images
        (OpCode.SHOW_IMAGE, "logo.png"),
        (OpCode.SHOW_IMAGE, "banner.jpg"),
        (OpCode.SHOW_IMAGE, "screenshot_001.png"),

        # Play some sounds
        (OpCode.PLAY_SOUND, {"source": "welcome.mp3", "duration": 3.5}),
        (OpCode.PLAY_SOUND, {"source": "notification.wav", "duration": 1.2}),

        # Do some calculations
        (OpCode.PUSH, 10),
        (OpCode.PUSH, 20),
        (OpCode.ADD),
        (OpCode.PRINT_TEXT, "计算结果: 10 + 20 = 30"),

        # Display more content
        (OpCode.PRINT_TEXT, "这是一段中文文本，插件会自动提取"),
        (OpCode.PRINT_TEXT, "This is English text that will be captured"),
        (OpCode.SHOW_IMAGE, "diagram.svg"),
        (OpCode.PLAY_SOUND, {"source": "bgm.mp3", "duration": 120.0}),

        # Final message
        (OpCode.PRINT_TEXT, "程序执行完毕！"),
        (OpCode.PRINT_TEXT, "Program execution completed!"),

        # Halt the VM
        (OpCode.HALT,)
    ]


def create_calculation_app():
    """
    Create a calculation-focused app

    Returns:
        List of VM instructions
    """
    return [
        (OpCode.PRINT_TEXT, "=== 计算器 App ==="),

        # Calculate (5 + 3) * 2
        (OpCode.PUSH, 5),
        (OpCode.PUSH, 3),
        (OpCode.ADD),
        (OpCode.PUSH, 2),
        (OpCode.MUL),
        (OpCode.PRINT_TEXT, "计算: (5 + 3) * 2 = 16"),

        # Show result visualization
        (OpCode.SHOW_IMAGE, "chart_result.png"),

        (OpCode.HALT,)
    ]


def print_separator(title=""):
    """Print a decorative separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    else:
        print("=" * 70)


def display_plugin_reports(plugin_manager):
    """
    Display reports from all plugins

    Args:
        plugin_manager: PluginManager instance
    """
    print_separator("插件报告 / Plugin Reports")

    reports = plugin_manager.get_all_reports()

    for plugin_name, report in reports.items():
        print(f"\n[{plugin_name}]")
        print(f"  状态 (Status): {'启用 (Enabled)' if report['enabled'] else '禁用 (Disabled)'}")
        print(f"  收集数据量 (Data Count): {report['data_count']}")

        if report['data_count'] > 0:
            print(f"  详细数据 (Details):")
            for i, item in enumerate(report['data'], 1):
                print(f"    {i}. {item}")

    print_separator()


def demo_basic():
    """Run basic VM + Plugin demo"""
    print_separator("基础演示 / Basic Demo")

    # Create VM
    vm = VirtualMachine(memory_size=2048)

    # Create and load plugins
    text_plugin = TextExtractorPlugin()
    image_plugin = ImageCapturePlugin()
    sound_plugin = SoundRecorderPlugin()

    vm.load_plugin(text_plugin)
    vm.load_plugin(image_plugin)
    vm.load_plugin(sound_plugin)

    # Create plugin manager
    plugin_manager = PluginManager()
    plugin_manager.register(text_plugin)
    plugin_manager.register(image_plugin)
    plugin_manager.register(sound_plugin)

    # Run sample app
    app = create_sample_app()
    vm.run(app)

    # Display plugin reports
    display_plugin_reports(plugin_manager)

    # Show collected text
    print_separator("提取的文本内容 / Extracted Text")
    for i, text in enumerate(text_plugin.get_all_text(), 1):
        print(f"{i}. {text}")

    # Show collected images
    print_separator("捕获的图片 / Captured Images")
    for i, image in enumerate(image_plugin.get_all_images(), 1):
        print(f"{i}. {image}")

    # Show collected sounds
    print_separator("录制的声音 / Recorded Sounds")
    for i, sound in enumerate(sound_plugin.get_all_sounds(), 1):
        print(f"{i}. {sound}")

    print_separator()


def demo_multiple_apps():
    """Run multiple apps with the same VM instance"""
    print_separator("多应用演示 / Multiple Apps Demo")

    # Create VM with plugins
    vm = VirtualMachine()

    text_plugin = TextExtractorPlugin()
    image_plugin = ImageCapturePlugin()

    vm.load_plugin(text_plugin)
    vm.load_plugin(image_plugin)

    # Run first app
    print("\n>>> 运行第一个应用 (Running App 1)...")
    app1 = create_sample_app()
    vm.run(app1)

    # Run second app
    print("\n>>> 运行第二个应用 (Running App 2)...")
    app2 = create_calculation_app()
    vm.run(app2)

    # Show aggregated results
    print_separator("聚合结果 / Aggregated Results")
    print(f"总文本数量 (Total text items): {len(text_plugin.get_all_text())}")
    print(f"总图片数量 (Total images): {len(image_plugin.get_all_images())}")

    print_separator()


def demo_plugin_search():
    """Demo plugin search capabilities"""
    print_separator("插件搜索功能演示 / Plugin Search Demo")

    vm = VirtualMachine()
    text_plugin = TextExtractorPlugin()
    vm.load_plugin(text_plugin)

    # Run app
    app = create_sample_app()
    vm.run(app)

    # Search for Chinese text
    print("\n搜索包含'中文'的文本:")
    results = text_plugin.search_text('中文')
    for item in results:
        print(f"  - {item['content']}")

    # Search for English text
    print("\n搜索包含'English'的文本:")
    results = text_plugin.search_text('English')
    for item in results:
        print(f"  - {item['content']}")

    print_separator()


def main():
    """Main demo entry point"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           NaviAI VM + Plugin Demo                                   ║
║           虚拟机 + 插件系统演示                                         ║
║                                                                      ║
║  功能特性 (Features):                                                 ║
║  • 简单的栈式虚拟机 (Simple stack-based VM)                           ║
║  • 支持运行应用程序 (Run apps with bytecode)                          ║
║  • 插件系统 (Plugin system with hooks)                                ║
║  • 文字提取 (Text extraction)                                         ║
║  • 图片捕获 (Image capture)                                           ║
║  • 声音录制 (Sound recording)                                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    try:
        # Run demos
        demo_basic()
        input("\n按 Enter 继续下一个演示 (Press Enter for next demo)...")

        demo_multiple_apps()
        input("\n按 Enter 继续下一个演示 (Press Enter for next demo)...")

        demo_plugin_search()

        print_separator("演示完成 / Demo Complete")
        print("\n✓ 所有演示运行成功！")
        print("✓ All demos completed successfully!")
        print("\n提示: 查看源代码了解更多细节")
        print("Tip: Check the source code for more details\n")

    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消执行")
        print("[Interrupted] User cancelled execution")
    except Exception as e:
        print(f"\n[错误] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
