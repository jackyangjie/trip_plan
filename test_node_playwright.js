/**
 * 使用 oh-my-opencode 内置 Playwright (Node.js 版本)
 * 测试旅行规划表单
 */

const { chromium } = require('playwright');

// 测试数据
const TEST_TRIP_DATA = {
    destinations: "北京、上海、杭州",
    start_date: "2026-04-01",
    end_date: "2026-04-08",
    travelers: "2",
    budget_total: "10000",
    food_types: ["川菜", "日料"],
    attraction_types: ["历史古迹", "博物馆"]
};

let passed = 0;
let failed = 0;

/**
 * 截图辅助函数
 */
async function takeScreenshot(page, filename) {
    try {
        const filepath = `/tmp/${filename}.png`;
        await page.screenshot({ path: filepath, fullPage: true });
        console.log(`   📸 截图: ${filename}.png`);
        return true;
    } catch (e) {
        console.log(`   ⚠️  截图失败: ${e.message}`);
        return false;
    }
}

/**
 * 测试1: 页面加载
 */
async function testPageLoad(page) {
    console.log("\n📖 测试1: 页面加载");
    
    const htmlPath = '/home/yangjie/learn/opencode_test/web_test_form.html';
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(2000);
    
    // 检查关键元素
    const title = await page.locator('h1').first();
    const destinations = await page.locator('input[name="destinations"]');
    const startDate = await page.locator('input[name="startDate"]');
    const budget = await page.locator('input[name="budgetTotal"]');
    
    const titleCount = await title.count();
    const destCount = await destinations.count();
    const startCount = await startDate.count();
    const budgetCount = await budget.count();
    
    console.log(`   标题: ${titleCount > 0 ? '✅' : '❌'}`);
    console.log(`   目的地输入框: ${destCount > 0 ? '✅' : '❌'}`);
    console.log(`   开始日期: ${startCount > 0 ? '✅' : '❌'}`);
    console.log(`   预算输入框: ${budgetCount > 0 ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "01_page_load");
    
    return titleCount > 0 && destCount > 0 && startCount > 0;
}

/**
 * 测试2: 表单交互
 */
async function testFormInteraction(page) {
    console.log("\n✍️ 测试2: 表单交互");
    
    // 填写目的地
    const destinations = page.locator('input[name="destinations"]');
    await destinations.fill(TEST_TRIP_DATA.destinations);
    await page.waitForTimeout(500);
    
    // 填写日期
    const startDate = page.locator('input[name="startDate"]');
    const endDate = page.locator('input[name="endDate"]');
    await startDate.fill(TEST_TRIP_DATA.start_date);
    await page.waitForTimeout(300);
    await endDate.fill(TEST_TRIP_DATA.end_date);
    await page.waitForTimeout(300);
    
    // 填写人数
    const travelers = page.locator('input[name="travelers"]');
    await travelers.fill(TEST_TRIP_DATA.travelers);
    await page.waitForTimeout(300);
    
    // 填写预算
    const budget = page.locator('input[name="budgetTotal"]');
    await budget.fill(TEST_TRIP_DATA.budget_total);
    await page.waitForTimeout(300);
    
    // 选择美食偏好
    for (const food of TEST_TRIP_DATA.food_types) {
        const chip = page.locator('#foodTypes .chip', { hasText: food });
        if (await chip.count() > 0) {
            await chip.click();
            await page.waitForTimeout(200);
        }
    }
    
    // 选择景点偏好
    for (const attr of TEST_TRIP_DATA.attraction_types) {
        const chip = page.locator('#attractionTypes .chip', { hasText: attr });
        if (await chip.count() > 0) {
            await chip.click();
            await page.waitForTimeout(200);
        }
    }
    
    // 验证输入值
    const actualDestinations = await destinations.inputValue();
    console.log(`\n   验证结果:`);
    console.log(`   目的地: ${TEST_TRIP_DATA.destinations === actualDestinations ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "02_form_filled");
    
    return true;
}

/**
 * 测试3: 预算计算器
 */
async function testBudgetCalculator(page) {
    console.log("\n💰 测试3: 预算计算器");
    
    const budget = page.locator('input[name="budgetTotal"]');
    
    await budget.fill("10000");
    await page.waitForTimeout(500);
    
    const transportAmt = await page.locator('.budget-item').nth(0).locator('.amount').textContent();
    const accommodationAmt = await page.locator('.budget-item').nth(1).locator('.amount').textContent();
    
    console.log(`   交通预算: ${transportAmt} ${transportAmt.includes('3000') ? '✅' : '❌'}`);
    console.log(`   住宿预算: ${accommodationAmt} ${accommodationAmt.includes('3500') ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "03_budget_calculator");
    
    return transportAmt.includes('3000') && accommodationAmt.includes('3500');
}

/**
 * 测试4: Chip选择
 */
async function testChipSelection(page) {
    console.log("\n🔘 测试4: Chip选择");
    
    const chip = page.locator('#foodTypes .chip').first();
    await chip.click();
    await page.waitForTimeout(300);
    
    const selectedClass = await chip.getAttribute('class');
    const isSelected = selectedClass && selectedClass.includes('selected');
    console.log(`   Chip选中: ${isSelected ? '✅' : '❌'}`);
    
    await chip.click();
    await page.waitForTimeout(300);
    
    const deselectedClass = await chip.getAttribute('class');
    const isDeselected = !deselectedClass || !deselectedClass.includes('selected');
    console.log(`   Chip取消: ${isDeselected ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "04_chip_selection");
    
    return isSelected && isDeselected;
}

/**
 * 测试5: 表单验证
 */
async function testFormValidation(page) {
    console.log("\n🔍 测试5: 表单验证");
    
    // 清空表单
    const clearBtn = page.locator('button#btnClear');
    if (await clearBtn.count() > 0) {
        await clearBtn.click();
        await page.waitForTimeout(500);
    }
    
    const startDate = page.locator('input[name="startDate"]');
    const endDate = page.locator('input[name="endDate"]');
    
    // 结束日期早于开始日期
    await startDate.fill("2026-04-20");
    await page.waitForTimeout(300);
    await endDate.fill("2026-04-15");
    await page.waitForTimeout(500);
    
    const errorMsg = page.locator('#dateError');
    const isVisible = await errorMsg.isVisible();
    console.log(`   错误显示: ${isVisible ? '✅' : '❌'}`);
    
    // 修复日期
    await endDate.fill("2026-04-25");
    await page.waitForTimeout(500);
    
    const errorHidden = !(await errorMsg.isVisible());
    console.log(`   错误消失: ${errorHidden ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "05_validation");
    
    return isVisible && errorHidden;
}

/**
 * 测试6: 按钮交互
 */
async function testButtonInteraction(page) {
    console.log("\n🎮 测试6: 按钮交互");
    
    const submitBtn = page.locator('button#btnSubmit');
    const aiBtn = page.locator('button#btnAIPlan');
    
    const submitCount = await submitBtn.count();
    const aiCount = await aiBtn.count();
    
    console.log(`   提交按钮: ${submitCount > 0 ? '✅' : '❌'}`);
    console.log(`   AI按钮: ${aiCount > 0 ? '✅' : '❌'}`);
    
    await takeScreenshot(page, "06_buttons");
    
    return submitCount > 0 && aiCount > 0;
}

/**
 * 主测试函数
 */
async function main() {
    console.log("=".repeat(60));
    console.log("🎭 使用 oh-my-opencode 内置 Playwright (Node.js)");
    console.log("=".repeat(60));
    
    let browser;
    
    try {
        // 启动浏览器
        browser = await chromium.launch({ 
            headless: false,
            args: ['--no-sandbox']
        });
        
        const context = await browser.newContext();
        const page = await context.newPage();
        
        // 设置超时
        page.setDefaultTimeout(10000);
        
        // 运行测试
        const results = [];
        
        results.push(["页面加载", await testPageLoad(page)]);
        results.push(["表单交互", await testFormInteraction(page)]);
        results.push(["预算计算器", await testBudgetCalculator(page)]);
        results.push(["Chip选择", await testChipSelection(page)]);
        results.push(["表单验证", await testFormValidation(page)]);
        results.push(["按钮交互", await testButtonInteraction(page)]);
        
        // 生成报告
        console.log("\n" + "=".repeat(60));
        console.log("📊 测试报告");
        console.log("=".repeat(60));
        
        let passCount = 0;
        for (const [name, result] of results) {
            if (result) passCount++;
            console.log(`  ${result ? '✅' : '❌'} ${name}`);
        }
        
        const total = results.length;
        console.log(`\n测试统计: ${passCount}/${total} 通过 (${(passCount/total*100).toFixed(1)}%)`);
        
        if (passCount === total) {
            console.log("\n🎉 所有测试通过!");
        } else {
            console.log(`\n⚠️  ${total - passCount} 个测试失败`);
        }
        
        console.log("\n📸 截图位置: /tmp/");
        console.log("  - 01_page_load.png");
        console.log("  - 02_form_filled.png");
        console.log("  - 03_budget_calculator.png");
        console.log("  - 04_chip_selection.png");
        console.log("  - 05_validation.png");
        console.log("  - 06_buttons.png");
        
    } catch (error) {
        console.error(`\n❌ 测试执行失败: ${error.message}`);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// 运行测试
main().catch(console.error);
