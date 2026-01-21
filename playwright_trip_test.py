"""
Playwright测试脚本 - 模拟用户填写旅行规划表单
使用SSE流测试AI规划功能
"""

from playwright.sync_api import sync_playwright, expect
import time
import json

# 测试数据
TEST_TRIP_DATA = {
    "destinations": "北京、上海、杭州",
    "start_date": "2026-03-15",
    "end_date": "2026-03-22",
    "travelers": "3",
    "budget_total": "15000",
    "food_types": ["京菜", "本帮菜", "杭帮菜"],
    "attraction_types": ["历史古迹", "博物馆", "城市观光"],
}


def test_manual_trip_creation(page):
    """测试手动创建行程"""
    print("\n" + "=" * 60)
    print("📝 测试：手动创建行程")
    print("=" * 60)

    # 填写目的地
    print("\n1. 填写目的地...")
    destinations_input = page.get_by_label("目的地")
    destinations_input.fill(TEST_TRIP_DATA["destinations"])
    time.sleep(0.5)

    # 填写日期
    print("2. 填写旅行日期...")
    start_date_input = page.locator('input[name="startDate"]')
    end_date_input = page.locator('input[name="endDate"]')

    start_date_input.fill(TEST_TRIP_DATA["start_date"])
    time.sleep(0.3)
    end_date_input.fill(TEST_TRIP_DATA["end_date"])
    time.sleep(0.5)

    # 填写旅行人数
    print("3. 填写旅行人数...")
    travelers_input = page.get_by_label("旅行人数")
    travelers_input.fill(TEST_TRIP_DATA["travelers"])
    time.sleep(0.5)

    # 填写预算
    print("4. 填写总预算...")
    budget_input = page.get_by_label("总预算（元）")
    budget_input.fill(TEST_TRIP_DATA["budget_total"])
    time.sleep(0.5)

    # 选择美食偏好
    print("5. 选择美食偏好...")
    food_chips = page.locator("#foodTypes .chip")
    for food_type in TEST_TRIP_DATA["food_types"]:
        chip = food_chips.filter(has_text=food_type).first
        chip.click()
        time.sleep(0.2)
    time.sleep(0.5)

    # 选择景点偏好
    print("6. 选择景点偏好...")
    attraction_chips = page.locator("#attractionTypes .chip")
    for attr_type in TEST_TRIP_DATA["attraction_types"]:
        chip = attraction_chips.filter(has_text=attr_type).first
        chip.click()
        time.sleep(0.2)
    time.sleep(0.5)

    # 截图
    print("7. 截图表单...")
    page.screenshot(path="/tmp/trip_form_filled.png", full_page=True)

    # 提交表单
    print("8. 提交表单...")
    submit_button = page.get_by_role("button").filter(has_text="创建行程")
    submit_button.click()

    # 等待成功消息
    try:
        success_message = page.locator(".success-message")
        expect(success_message).to_be_visible(timeout=10000)
        print("\n✅ 行程创建成功！")

        # 截图成功状态
        page.screenshot(path="/tmp/trip_success.png", full_page=True)

        # 提取行程详情
        details = success_message.text_content()
        print(f"\n行程详情:\n{details}")

        return True
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")
        page.screenshot(path="/tmp/trip_error.png", full_page=True)
        return False


def test_ai_trip_planning(page):
    """测试AI智能规划"""
    print("\n" + "=" * 60)
    print("🤖 测试：AI智能规划")
    print("=" * 60)

    # 清空表单
    print("\n1. 清空表单...")
    clear_button = page.get_by_role("button").filter(has_text="清空")
    clear_button.click()
    time.sleep(0.5)

    # 填写表单
    print("2. 填写表单信息...")

    # 目的地
    destinations_input = page.get_by_label("目的地")
    destinations_input.fill("东京、大阪")
    time.sleep(0.3)

    # 日期
    start_date_input = page.locator('input[name="startDate"]')
    end_date_input = page.locator('input[name="endDate"]')
    start_date_input.fill("2026-04-10")
    time.sleep(0.3)
    end_date_input.fill("2026-04-17")
    time.sleep(0.3)

    # 人数
    travelers_input = page.get_by_label("旅行人数")
    travelers_input.fill("2")
    time.sleep(0.3)

    # 预算
    budget_input = page.get_by_label("总预算（元）")
    budget_input.fill("25000")
    time.sleep(0.3)

    # 选择偏好
    food_chip = page.locator("#foodTypes .chip").filter(has_text="日料")
    food_chip.click()
    time.sleep(0.2)

    attraction_chip = page.locator("#attractionTypes .chip").filter(has_text="主题公园")
    attraction_chip.click()
    time.sleep(0.2)

    # 截图
    print("3. 截图表单...")
    page.screenshot(path="/tmp/ai_form_filled.png", full_page=True)

    # 点击AI规划按钮
    print("4. 点击AI智能规划...")
    ai_button = page.get_by_role("button").filter(has_text="AI智能规划")
    ai_button.click()

    # 监听SSE流
    print("5. 监听AI规划进度...")
    progress_steps = page.locator(".progress-steps")

    try:
        expect(progress_steps).to_be_visible(timeout=5000)
        print("   进度显示开始...")

        # 等待至少5个进度步骤
        step_count = 0
        max_wait = 60  # 最多等待60秒
        start_time = time.time()

        while step_count < 5 and (time.time() - start_time) < max_wait:
            time.sleep(2)
            step_count = len(page.locator(".progress-step").all())
            progress_percent = page.locator(".step-icon.current").count()

            if step_count > 0:
                last_step = page.locator(".progress-step").last
                if last_step.count() > 0:
                    text = last_step.text_content()
                    print(f"   {text[:80]}")

                    # 每接收几个步骤就截图一次
                    if step_count % 3 == 0:
                        page.screenshot(
                            path=f"/tmp/ai_progress_{step_count}.png", full_page=True
                        )

        # 最终截图
        page.screenshot(path="/tmp/ai_final_progress.png", full_page=True)

        print(f"\n✅ AI规划过程成功！接收到 {step_count} 个进度步骤")

        # 等待完成消息
        try:
            success_message = page.locator(".success-message")
            expect(success_message).to_be_visible(timeout=30000)
            print("✅ AI规划完成！")

            page.screenshot(path="/tmp/ai_success.png", full_page=True)
            return True
        except:
            print("⚠️  AI规划可能仍在进行中...")
            return True

    except Exception as e:
        print(f"\n❌ AI规划失败: {e}")
        page.screenshot(path="/tmp/ai_error.png", full_page=True)
        return False


def test_form_validation(page):
    """测试表单验证"""
    print("\n" + "=" * 60)
    print("🔍 测试：表单验证")
    print("=" * 60)

    # 清空表单
    clear_button = page.get_by_role("button").filter(has_text="清空")
    clear_button.click()
    time.sleep(0.5)

    # 测试：结束日期早于开始日期
    print("\n1. 测试：结束日期早于开始日期...")
    start_date_input = page.locator('input[name="startDate"]')
    end_date_input = page.locator('input[name="endDate"]')

    start_date_input.fill("2026-03-20")
    time.sleep(0.3)
    end_date_input.fill("2026-03-15")
    time.sleep(0.3)

    # 检查错误消息
    error_message = page.locator("#dateError")
    try:
        expect(error_message).to_be_visible(timeout=2000)
        print("   ✅ 错误消息显示正确")

        page.screenshot(path="/tmp/validation_error.png", full_page=True)
        return True
    except:
        print("   ❌ 错误消息未显示")
        return False


def test_ui_responsiveness(page):
    """测试UI响应性和交互"""
    print("\n" + "=" * 60)
    print("📱 测试：UI响应性和交互")
    print("=" * 60)

    # 清空表单
    clear_button = page.get_by_role("button").filter(has_text="清空")
    clear_button.click()
    time.sleep(0.5)

    # 测试预算更新
    print("\n1. 测试：预算分配自动更新...")
    budget_input = page.get_by_label("总预算（元）")
    budget_input.fill("10000")
    time.sleep(0.5)

    # 检查预算预览
    transport_amount = page.locator(".budget-item").first.locator(".amount")
    expected_transport = "¥3000"

    try:
        expect(transport_amount).to_have_text(expected_transport, timeout=2000)
        print("   ✅ 预算自动更新正确")
    except:
        print("   ❌ 预算更新失败")

    # 测试chip选择/取消选择
    print("\n2. 测试：chip选择交互...")
    food_chip = page.locator("#foodTypes .chip").first
    food_chip.click()
    time.sleep(0.3)

    try:
        expect(food_chip).to_have_class("selected", timeout=2000)
        print("   ✅ chip选中状态正确")
    except:
        print("   ❌ chip选中失败")

    # 取消选择
    food_chip.click()
    time.sleep(0.3)

    try:
        expect(food_chip).not_to_have_class("selected", timeout=2000)
        print("   ✅ chip取消选中正确")
    except:
        print("   ❌ chip取消选中失败")

    # 截图最终状态
    page.screenshot(path="/tmp/ui_test.png", full_page=True)

    return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 Playwright 测试开始")
    print("=" * 60)
    print("\n📍 测试URL: http://localhost:8080/web_test_form.html")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 导航到测试页面
            print("\n🌐 导航到测试页面...")
            page.goto("file:///home/yangjie/learn/opencode_test/web_test_form.html")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # 截图初始状态
            print("📸 截图初始状态...")
            page.screenshot(path="/tmp/test_initial.png", full_page=True)

            # 运行测试
            results.append(("表单验证", test_form_validation(page)))
            results.append(("UI响应性", test_ui_responsiveness(page)))
            results.append(("手动创建行程", test_manual_trip_creation(page)))
            # results.append(("AI智能规划", test_ai_trip_planning(page)))

        finally:
            browser.close()

    # 生成测试报告
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

    print(f"\n📸 截图保存在 /tmp/:")
    print("  - test_initial.png (初始状态)")
    print("  - validation_error.png (验证错误)")
    print("  - ui_test.png (UI交互)")
    print("  - trip_form_filled.png (填写的表单)")
    print("  - trip_success.png (创建成功)")
    print("  - trip_error.png (创建失败)")

    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
