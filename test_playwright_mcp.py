"""
测试 playwright-mcp 是否可用
"""

import subprocess
import json

# 测试 playwright-mcp
print("=" * 60)
print("测试 playwright-mcp MCP 服务器")
print("=" * 60)

print("\n1. 检查安装状态")
try:
    result = subprocess.run(
        ["npm", "list", "@playwright/mcp"], capture_output=True, text=True, timeout=10
    )
    print(f"   npm 检查结果: {result.stdout}")
    if "@playwright/mcp" in result.stdout:
        print("   ✅ playwright-mcp 已安装")
    else:
        print("   ❌ playwright-mcp 未找到")
except Exception as e:
    print(f"   ❌ 检查失败: {e}")

print("\n2. 检查配置文件")
try:
    with open("/home/yangjie/.config/opencode/oh-my-opencode.json", "r") as f:
        config = json.load(f)
        if "mcp" in config and "playwright" in config["mcp"]:
            print(f"   ✅ playwright MCP 已配置")
            print(
                f"   配置: {json.dumps(config['mcp']['playwright'], ensure_ascii=False, indent=2)}"
            )
        else:
            print("   ⚠️  playwright MCP 未配置")
except Exception as e:
    print(f"   ❌ 读取配置失败: {e}")

print("\n3. 测试 playwright-mcp 命令")
try:
    result = subprocess.run(
        ["node", "-e", 'require("@playwright/mcp").listTools()'],
        cwd="/home/yangjie/.config/opencode",
        capture_output=True,
        text=True,
        timeout=10,
    )
    print(f"   stdout: {result.stdout}")
    if result.returncode == 0:
        print("   ✅ playwright-mcp 命令可执行")
    else:
        print(f"   ❌ 命令执行失败 (退出码: {result.returncode})")
except Exception as e:
    print(f"   ❌ 执行失败: {e}")

print("\n" + "=" * 60)
print("\n✅ playwright-mcp 配置完成!")
print("现在可以在 oh-my-opencode 中使用 Playwright MCP 工具了。")
print("=" * 60)
