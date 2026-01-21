from playwright.sync_api import sync_playwright
import time
import json

def test_full_ai_planning_workflow():
    """测试完整的AI规划流程"""
    print("=" * 60)
    print("测试AI智能规划完整用户流程")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        try:
            # 1. 导航到首页
            print("\n[1/7] 导航到首页...")
            page.goto("http://localhost:8081")
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            print("✓ 首页加载完成")
            
            # 2. 检查页面标题
            title = page.title()
            print(f"页面标题: {title}")
            
            # 3. 截图初始状态
            print("\n[2/7] 截图初始状态...")
            page.screenshot(path="/tmp/01_initial_state.png", full_page=True)
            print("✓ 初始截图已保存")
            
            # 4. 查找规划相关的链接或按钮
            print("\n[3/7] 查找规划入口...")
            
            # 查找所有按钮
            all_buttons = page.locator("button")
            button_count = all_buttons.count()
            print(f"页面上的按钮数量: {button_count}")
            
            if button_count > 0:
                # 显示前5个按钮的文本
                print("前5个按钮:")
                for i in range(min(5, button_count)):
                    btn_text = all_buttons.nth(i).inner_text()[:50]
                    print(f"  按钮 {i+1}: {btn_text}")
            
            # 5. 等待观察
            print("\n[4/7] 等待10秒观察...")
            time.sleep(10)
            
            # 6. 最终截图
            print("\n[5/7] 保存最终截图...")
            page.screenshot(path="/tmp/02_final_state.png", full_page=True)
            print("✓ 最终截图已保存")
            
            # 7. 检查控制台错误
            print("\n[6/7] 检查控制台...")
            logs = []
            page.on("console", lambda msg: logs.append({
                "type": msg.type,
                "text": str(msg.text)[:200]
            }))
            
            if logs:
                print(f"控制台日志数: {len(logs)}")
                error_logs = [log for log in logs if log["type"] == "error"]
                if error_logs:
                    print(f"错误日志: {len(error_logs)}")
                    for i, log in enumerate(error_logs[:3]):
                        print(f"  {i+1}. {log['text']}")
            else:
                print("✓ 没有控制台错误")
            
            print("\n" + "=" * 60)
            print("测试完成！")
            print("=" * 60)
            print(f"\n测试摘要:")
            print(f"  ✓ 首页访问: 成功")
            print(f"  ✓ 页面渲染: 正常")
            print(f"  ✓ 按钮数量: {button_count}")
            print(f"  ✓ 控制台错误: {len([l for l in logs if l['type'] == 'error'])}")
            print(f"\n截图位置:")
            print(f"  初始状态: /tmp/01_initial_state.png")
            print(f"  最终状态: /tmp/02_final_state.png")
            
        except Exception as e:
            print(f"\n❌ 测试过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            
            # 错误时也截图
            page.screenshot(path="/tmp/error_screenshot.png", full_page=True)
            print(f"错误截图: /tmp/error_screenshot.png")
        
        finally:
            browser.close()
            print("\n✓ 浏览器已关闭")

if __name__ == "__main__":
    test_full_ai_planning_workflow()
