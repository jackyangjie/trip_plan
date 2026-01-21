"""
使用 oh-my-opencode 内置 Playwright 的测试脚本
测试旅行规划表单
"""

import sys
import os

# 使用 oh-my-opencode 的 playwright
playwright_path = "/home/yangjie/.config/opencode/node_modules"
if os.path.exists(playwright_path):
    sys.path.insert(0, playwright_path)
    print(f"已添加 Playwright 路径: {playwright_path}")

from playwright.sync_api import sync_playwright
import time

# 测试数据
TEST_TRIP_DATA = {
    "destinations": "北京、上海、杭州",
    "start_date": "2026-04-01",
    "end_date": "2026-04-08",
    "travelers": "2",
    "budget_total": "10000",
    "food_types": ["川菜", "日料"],
    "attraction_types": ["历史古迹", "博物馆"],
}


def take_screenshot(page, filename):
    """截图并保存"""
    try:
        filepath = f"/tmp/{filename}.png"
        page.screenshot(path=filepath, full_page=True)
        print(f"   截图: {filename}.png")
        return True
    except Exception as e:
        print(f"   截图失败: {e}")
        return False


def test_page_load(page):
    """测试页面加载"""
    print("\n测试1: 页面加载")

    html_path = "/home/yangjie/learn/opencode_test/web_test_form.html"
    page.goto(f"file://{html_path}")
    time.sleep(2)

    title = page.locator("h1").first
    destinations = page.locator('input[name="destinations"]')
    start_date = page.locator('input[name="startDate"]')
    budget = page.locator('input[name="budgetTotal"]')

    print(f"   标题: {'通过' if title.count() > 0 else '失败'}")
    print(f"   目的地输入框: {'通过' if destinations.count() > 0 else '失败'}")
    print(f"   开始日期: {'通过' if start_date.count() > 0 else '失败'}")
    print(f"   预算输入框: {'通过' if budget.count() > 0 else '失败'}")

    take_screenshot(page, "01_page_load")

    return all([title.count() > 0, destinations.count() > 0, start_date.count() > 0])


def test_form_interaction(page):
    """测试表单交互"""
    print("\n测试2: 表单交互")

    destinations = page.locator('input[name="destinations"]')
    destinations.fill(TEST_TRIP_DATA["destinations"])
    time.sleep(0.5)

    start_date = page.locator('input[name="startDate"]')
    end_date = page.locator('input[name="endDate"]')
    start_date.fill(TEST_TRIP_DATA["start_date"])
    time.sleep(0.3)
    end_date.fill(TEST_TRIP_DATA["end_date"])
    time.sleep(0.3)

    travelers = page.locator('input[name="travelers"]')
    travelers.fill(TEST_TRIP_DATA["travelers"])
    time.sleep(0.3)

    budget = page.locator('input[name="budgetTotal"]')
    budget.fill(TEST_TRIP_DATA["budget_total"])
    time.sleep(0.3)

    for food in TEST_TRIP_DATA["food_types"]:
        chip = page.locator("#foodTypes .chip").filter(has_text=food)
        if chip.count() > 0:
            chip.click()
            time.sleep(0.2)

    for attr in TEST_TRIP_DATA["attraction_types"]:
        chip = page.locator("#attractionTypes .chip").filter(has_text=attr)
        if chip.count() > 0:
            chip.click()
            time.sleep(0.2)

    actual_destinations = destinations.input_value()
    print(
        f"   目的地验证: {'通过' if TEST_TRIP_DATA['destinations'] == actual_destinations else '失败'}"
    )

    take_screenshot(page, "02_form_filled")

    return True


def test_budget_calculator(page):
    """测试预算计算器"""
    print("\n测试3: 预算计算器")

    budget = page.locator('input[name="budgetTotal"]')

    budget.fill("10000")
    time.sleep(0.5)

    transport_amt = (
        page.locator(".budget-item").nth(0).locator(".amount").text_content()
    )
    accommodation_amt = (
        page.locator(".budget-item").nth(1).locator(".amount").text_content()
    )

    print(
        f"   交通预算: {transport_amt} {'通过' if '3000' in transport_amt else '失败'}"
    )
    print(
        f"   住宿预算: {accommodation_amt} {'通过' if '3500' in accommodation_amt else '失败'}"
    )

    take_screenshot(page, "03_budget_calculator")

    return "3000" in transport_amt and "3500" in accommodation_amt


def test_chip_selection(page):
    """测试Chip选择"""
    print("\n测试4: Chip选择")

    chip = page.locator("#foodTypes .chip").first
    chip.click()
    time.sleep(0.3)

    selected_class = chip.get_attribute("class") or ""
    is_selected = "selected" in selected_class
    print(f"   Chip选中: {'通过' if is_selected else '失败'}")

    chip.click()
    time.sleep(0.3)

    deselected_class = chip.get_attribute("class") or ""
    is_deselected = "selected" not in deselected_class
    print(f"   Chip取消: {'通过' if is_deselected else '失败'}")

    take_screenshot(page, "04_chip_selection")

    return is_selected and is_deselected


def test_form_validation(page):
    """测试表单验证"""
    print("\n测试5: 表单验证")

    clear_btn = page.locator("button#btnClear")
    if clear_btn.count() > 0:
        clear_btn.click()
        time.sleep(0.5)

    start_date = page.locator('input[name="startDate"]')
    end_date = page.locator('input[name="endDate"]')

    start_date.fill("2026-04-20")
    time.sleep(0.3)
    end_date.fill("2026-04-15")
    time.sleep(0.5)

    error_msg = page.locator("#dateError")
    is_visible = error_msg.is_visible()
    print(f"   错误显示: {'通过' if is_visible else '失败'}")

    end_date.fill("2026-04-25")
    time.sleep(0.5)

    error_hidden = not error_msg.is_visible()
    print(f"   错误消失: {'通过' if error_hidden else '失败'}")

    take_screenshot(page, "05_validation")

    return is_visible and error_hidden


def test_button_interaction(page):
    """测试按钮交互"""
    print("\n测试6: 按钮交互")

    submit_btn = page.locator("button#btnSubmit")
    ai_btn = page.locator("button#btnAIPlan")

    print(f"   提交按钮存在: {'通过' if submit_btn.count() > 0 else '失败'}")
    print(f"   AI按钮存在: {'通过' if ai_btn.count() > 0 else '失败'}")

    take_screenshot(page, "06_buttons")

    return submit_btn.count() > 0 and ai_btn.count() > 0


def main():
    """主测试函数"""
    print("=" * 60)
    print("使用 oh-my-opencode 内置 Playwright 进行测试")
    print("=" * 60)

    # 检查 playwright 是否可用
    try:
        from playwright import __version__ as pw_version

        print(f"\nPlaywright 版本: {pw_version}")
    except ImportError as e:
        print(f"\nPlaywright 导入失败: {e}")
        print("\n尝试使用 node_modules...")

        try:
            import subprocess

            result = subprocess.run(
                ["node", "-e", 'console.log(require("playwright").chromium)'],
                cwd="/home/yangjie/.config/opencode",
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                print("Node.js Playwright 可用")
        except Exception as node_e:
            print(f"Node.js Playwright 检查失败: {node_e}")

        return

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.set_default_timeout(10000)

            results.append(("页面加载", test_page_load(page)))
            results.append(("表单交互", test_form_interaction(page)))
            results.append(("预算计算器", test_budget_calculator(page)))
            results.append(("Chip选择", test_chip_selection(page)))
            results.append(("表单验证", test_form_validation(page)))
            results.append(("按钮交互", test_button_interaction(page)))

        except Exception as e:
            print(f"\n测试执行失败: {e}")
        finally:
            time.sleep(2)
            browser.close()

    print("\n" + "=" * 60)
    print("测试报告")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n测试统计: {passed}/{total} 通过 ({passed / total * 100:.1f}%)")

    print("\n详细结果:")
    for test_name, result in results:
        icon = "通过" if result else "失败"
        print(f"  {icon} {test_name}")

    if passed == total:
        print("\n所有测试通过!")
    else:
        print(f"\n{total - passed} 个测试失败")


if __name__ == "__main__":
    main()
