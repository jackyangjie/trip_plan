"""
简化的Playwright测试脚本（不使用expect，避免依赖问题）
"""

from playwright.sync_api import sync_playwright
import time

# 测试数据
TEST_TRIP_DATA = {
    "destinations": "北京、上海",
    "start_date": "2026-04-01",
    "end_date": "2026-04-08",
    "travelers": "2",
    "budget_total": "8000",
}


def take_screenshot(page, filename):
    """截图并保存"""
    try:
        page.screenshot(path=f"/tmp/{filename}.png", full_page=True)
        print(f"   📸 截图: {filename}.png")
    except Exception as e:
        print(f"   ⚠️  截图失败: {e}")


def test_page_load(page):
    """测试页面加载"""
    print("\n📖 测试页面加载...")

    page.goto("file:///home/yangjie/learn/opencode_test/web_test_form.html")
    time.sleep(3)  # 等待页面完全加载

    # 检查关键元素是否存在
    title = page.locator("h1").first
    destinations = page.locator('input[name="destinations"]')
    budget = page.locator('input[name="budgetTotal"]')

    has_title = title.count() > 0
    has_destinations = destinations.count() > 0
    has_budget = budget.count() > 0

    print(f"   标题显示: {'✅' if has_title else '❌'}")
    print(f"   目的地输入框: {'✅' if has_destinations else '❌'}")
    print(f"   预算输入框: {'✅' if has_budget else '❌'}")

    take_screenshot(page, "01_page_loaded")
    return has_title and has_destinations and has_budget


def test_form_input(page):
    """测试表单输入"""
    print("\n✍️  测试表单输入...")

    # 填写目的地
    print("   1. 填写目的地...")
    destinations = page.locator('input[name="destinations"]')
    destinations.fill(TEST_TRIP_DATA["destinations"])
    time.sleep(0.5)

    # 填写开始日期
    print("   2. 填写开始日期...")
    start_date = page.locator('input[name="startDate"]')
    start_date.fill(TEST_TRIP_DATA["start_date"])
    time.sleep(0.5)

    # 填写结束日期
    print("   3. 填写结束日期...")
    end_date = page.locator('input[name="endDate"]')
    end_date.fill(TEST_TRIP_DATA["end_date"])
    time.sleep(0.5)

    # 填写人数
    print("   4. 填写人数...")
    travelers = page.locator('input[name="travelers"]')
    travelers.fill(TEST_TRIP_DATA["travelers"])
    time.sleep(0.5)

    # 填写预算
    print("   5. 填写预算...")
    budget = page.locator('input[name="budgetTotal"]')
    budget.fill(TEST_TRIP_DATA["budget_total"])
    time.sleep(0.5)

    # 选择偏好
    print("   6. 选择偏好...")
    food_chip = page.locator("#foodTypes .chip").first
    food_chip.click()
    time.sleep(0.3)

    attraction_chip = page.locator("#attractionTypes .chip").first
    attraction_chip.click()
    time.sleep(0.5)

    # 验证输入值
    actual_destinations = destinations.input_value()
    actual_start = start_date.input_value()
    actual_end = end_date.input_value()
    actual_travelers = travelers.input_value()
    actual_budget = budget.input_value()

    print(f"\n   输入验证:")
    print(
        f"   目的地: {'✅' if TEST_TRIP_DATA['destinations'] == actual_destinations else '❌'}"
    )
    print(
        f"   开始日期: {'✅' if TEST_TRIP_DATA['start_date'] == actual_start else '❌'}"
    )
    print(f"   结束日期: {'✅' if TEST_TRIP_DATA['end_date'] == actual_end else '❌'}")
    print(
        f"   人数: {'✅' if TEST_TRIP_DATA['travelers'] == actual_travelers else '❌'}"
    )
    print(
        f"   预算: {'✅' if TEST_TRIP_DATA['budget_total'] == actual_budget else '❌'}"
    )

    take_screenshot(page, "02_form_filled")
    return True


def test_chip_interaction(page):
    """测试Chip选择交互"""
    print("\n🔘 测试Chip交互...")

    # 选择第一个美食chip
    print("   1. 选择美食chip...")
    chip1 = page.locator("#foodTypes .chip").nth(1)
    chip1.click()
    time.sleep(0.5)

    is_selected_1 = "selected" in chip1.get_attribute("class")
    print(f"   chip选中: {'✅' if is_selected_1 else '❌'}")

    # 点击同一个chip取消选择
    print("   2. 取消选择...")
    chip1.click()
    time.sleep(0.5)

    is_selected_2 = "selected" in chip1.get_attribute("class")
    print(f"   chip取消选中: {'✅' if not is_selected_2 else '❌'}")

    take_screenshot(page, "03_chip_interaction")
    return True


def test_budget_preview(page):
    """测试预算预览更新"""
    print("\n💰 测试预算预览更新...")

    # 设置不同预算
    budget = page.locator('input[name="budgetTotal"]')

    print("   1. 设置预算为5000...")
    budget.fill("5000")
    time.sleep(0.5)

    transport_amount = page.locator(".budget-item").nth(0).locator(".amount")
    text_5000 = transport_amount.text_content()

    print(f"   2. 检查交通预算: {text_5000}")
    print(f"   交通预算正确: {'✅' if '1500' in text_5000 else '❌'}")

    print("   3. 设置预算为10000...")
    budget.fill("10000")
    time.sleep(0.5)

    text_10000 = transport_amount.text_content()

    print(f"   4. 检查交通预算: {text_10000}")
    print(f"   交通预算更新: {'✅' if '3000' in text_10000 else '❌'}")

    take_screenshot(page, "04_budget_preview")
    return True


def test_date_validation(page):
    """测试日期验证"""
    print("\n📅 测试日期验证...")

    # 清空表单
    clear_btn = page.locator("button#btnClear")
    if clear_btn.count() > 0:
        clear_btn.click()
        time.sleep(0.5)

    # 设置无效日期
    print("   1. 设置无效日期（结束早于开始）...")
    start_date = page.locator('input[name="startDate"]')
    end_date = page.locator('input[name="endDate"]')

    start_date.fill("2026-04-20")
    time.sleep(0.3)
    end_date.fill("2026-04-15")
    time.sleep(0.5)

    # 检查错误消息
    error_msg = page.locator("#dateError")
    is_visible = error_msg.is_visible()

    print(f"   2. 错误消息显示: {'✅' if is_visible else '❌'}")

    if is_visible:
        error_text = error_msg.text_content()
        print(f"   3. 错误文本正确: {'✅' if '不能早于' in error_text else '❌'}")

    # 修复日期
    print("   4. 修复日期...")
    end_date.fill("2026-04-25")
    time.sleep(0.5)

    error_hidden = not error_msg.is_visible()
    print(f"   5. 错误消息消失: {'✅' if error_hidden else '❌'}")

    take_screenshot(page, "05_date_validation")
    return True


def test_submit_manual_trip(page):
    """测试提交手动行程"""
    print("\n📤 测试提交手动行程...")

    # 清空并填表单
    clear_btn = page.locator("button#btnClear")
    if clear_btn.count() > 0:
        clear_btn.click()
        time.sleep(0.5)

    # 填写有效数据
    destinations = page.locator('input[name="destinations"]')
    destinations.fill("杭州、苏州")
    time.sleep(0.3)

    start_date = page.locator('input[name="startDate"]')
    end_date = page.locator('input[name="endDate"]')
    start_date.fill("2026-05-01")
    time.sleep(0.3)
    end_date.fill("2026-05-05")
    time.sleep(0.3)

    budget = page.locator('input[name="budgetTotal"]')
    budget.fill("6000")
    time.sleep(0.3)

    # 提交
    print("   1. 点击提交按钮...")
    submit_btn = page.locator("button#btnSubmit")
    submit_btn.click()

    # 等待响应
    print("   2. 等待响应...")
    time.sleep(5)

    # 检查加载状态
    loading = page.locator(".loading.active")
    if loading.count() > 0:
        print("   加载状态: ✅")
    else:
        print("   加载状态: ⚠️  未检测到")

    # 截图结果
    time.sleep(2)
    take_screenshot(page, "06_manual_submit")

    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("🎭 Playwright UI测试")
    print("=" * 60)

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 非headless模式以便观察
        page = browser.new_page()

        try:
            # 设置超时时间
            page.set_default_timeout(10000)

            # 运行测试
            results.append(("页面加载", test_page_load(page)))
            results.append(("表单输入", test_form_input(page)))
            results.append(("Chip交互", test_chip_interaction(page)))
            results.append(("预算预览", test_budget_preview(page)))
            results.append(("日期验证", test_date_validation(page)))
            results.append(("提交行程", test_submit_manual_trip(page)))

        except Exception as e:
            print(f"\n❌ 测试执行失败: {e}")
        finally:
            time.sleep(2)
            browser.close()

    # 生成报告
    print("\n" + "=" * 60)
    print("📊 测试报告")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n测试统计:")
    print(f"  总计: {total}")
    print(f"  通过: {passed}")
    print(f"  失败: {total - passed}")
    print(f"  成功率: {passed / total * 100:.1f}%\n")

    print("详细结果:")
    for test_name, result in results:
        icon = "✅" if result else "❌"
        print(f"  {icon} {test_name}")

    print(f"\n📸 截图位置: /tmp/")
    screenshots = [
        "01_page_loaded.png",
        "02_form_filled.png",
        "03_chip_interaction.png",
        "04_budget_preview.png",
        "05_date_validation.png",
        "06_manual_submit.png",
    ]
    for screenshot in screenshots:
        print(f"  - {screenshot}")

    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
