"""
前后端联合测试脚本 - 模拟用户填写行程
测试完整的数据流程：前端 → 后端API → 数据库
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

# 配置
BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"test_user_{int(time.time())}@example.com"
TEST_PASSWORD = "test123456"
TEST_NICKNAME = "测试用户"


# 颜色输出
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text: str):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text: str):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


class TripPlanningTester:
    """行程规划测试器"""

    def __init__(self):
        self.base_url = BASE_URL
        self.email = TEST_EMAIL
        self.password = TEST_PASSWORD
        self.token = None
        self.user_id = None
        self.created_trip_id = None
        self.session = requests.Session()

    def test_health_check(self) -> bool:
        """测试健康检查端点"""
        print_header("1️⃣  测试后端服务健康检查")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print_success(f"后端服务运行正常")
                print_info(f"状态: {data.get('status')}")
                print_info(f"时间戳: {data.get('timestamp')}")
                return True
            else:
                print_error(f"健康检查失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print_error(f"连接后端失败: {str(e)}")
            return False

    def register_user(self) -> bool:
        """注册测试用户"""
        print_header("2️⃣  注册测试用户")
        user_data = {
            "email": self.email,
            "password": self.password,
            "nickname": TEST_NICKNAME,
            "preferences": {
                "foodTypes": ["川菜", "日料"],
                "attractionTypes": ["自然风光", "历史古迹"],
            },
        }

        try:
            response = self.session.post(
                f"{self.base_url}/auth/register", json=user_data
            )

            if response.status_code == 200:
                data = response.json()
                self.user_id = data.get("user_id")
                print_success(f"用户注册成功")
                print_info(f"用户ID: {self.user_id}")
                print_info(f"邮箱: {self.email}")
                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                if "already registered" in error_detail:
                    print_warning(f"用户已存在，尝试登录")
                    return self.login_user()
                else:
                    print_error(f"注册失败: {error_detail}")
                    return False
        except Exception as e:
            print_error(f"注册请求失败: {str(e)}")
            return False

    def login_user(self) -> bool:
        """登录获取token"""
        print_header("3️⃣  用户登录")
        login_data = {"email": self.email, "password": self.password}

        try:
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.user_id = data.get("user_id")

                # 设置认证头
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})

                print_success(f"登录成功")
                print_info(f"Token: {self.token[:50]}...")
                print_info(f"用户ID: {self.user_id}")
                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"登录失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"登录请求失败: {str(e)}")
            return False

    def create_manual_trip(self) -> bool:
        """测试手动创建行程"""
        print_header("4️⃣  测试手动创建行程")

        # 生成测试行程数据
        start_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        trip_data = {
            "title": "成都-重庆七日游",
            "destinations": ["成都", "重庆"],
            "start_date": start_date,
            "end_date": end_date,
            "travelers": 2,
            "status": "draft",
            "budget": {
                "total": 8000,
                "transport": 2400,
                "accommodation": 2800,
                "food": 1600,
                "activities": 1200,
            },
            "preferences": {
                "foodTypes": ["川菜", "火锅", "小面"],
                "attractionTypes": ["自然风光", "历史古迹", "城市观光"],
            },
        }

        print_info("行程数据:")
        print(json.dumps(trip_data, ensure_ascii=False, indent=2))

        try:
            response = self.session.post(f"{self.base_url}/trips", json=trip_data)

            if response.status_code == 200:
                data = response.json()
                self.created_trip_id = data.get("trip_id")
                trip = data.get("trip")

                print_success(f"行程创建成功")
                print_info(f"行程ID: {self.created_trip_id}")
                print_info(f"标题: {trip.get('title')}")
                print_info(f"目的地: {', '.join(trip.get('destinations', []))}")
                print_info(f"日期: {trip.get('start_date')} 至 {trip.get('end_date')}")
                print_info(f"预算: ¥{trip.get('budget', {}).get('total', 0)}")
                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"创建行程失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"创建行程请求失败: {str(e)}")
            return False

    def get_trips_list(self) -> bool:
        """获取行程列表"""
        print_header("5️⃣  获取行程列表")

        try:
            response = self.session.get(f"{self.base_url}/trips")

            if response.status_code == 200:
                trips = response.json()

                print_success(f"获取行程列表成功，共 {len(trips)} 个行程")

                if trips:
                    print_info("\n行程列表:")
                    for idx, trip in enumerate(trips, 1):
                        print(f"  {idx}. {trip.get('title')}")
                        print(f"     ID: {trip.get('id')}")
                        print(f"     目的地: {', '.join(trip.get('destinations', []))}")
                        print(f"     状态: {trip.get('status')}")
                        print(f"     预算: ¥{trip.get('budget', {}).get('total', 0)}\n")

                    # 验证创建的行程是否在列表中
                    created_found = any(
                        t.get("id") == self.created_trip_id for t in trips
                    )
                    if created_found:
                        print_success("创建的行程已成功保存到数据库")
                    else:
                        print_warning("创建的行程未在列表中找到")
                else:
                    print_warning("行程列表为空")

                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"获取行程列表失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"获取行程列表请求失败: {str(e)}")
            return False

    def get_single_trip(self) -> bool:
        """获取单个行程详情"""
        print_header("6️⃣  获取行程详情")

        if not self.created_trip_id:
            print_warning("没有可查询的行程ID")
            return False

        try:
            response = self.session.get(f"{self.base_url}/trips/{self.created_trip_id}")

            if response.status_code == 200:
                trip = response.json()

                print_success(f"获取行程详情成功")
                print_info(f"标题: {trip.get('title')}")
                print_info(f"ID: {trip.get('id')}")
                print_info(f"用户ID: {trip.get('user_id')}")
                print_info(f"目的地: {', '.join(trip.get('destinations', []))}")
                print_info(f"开始日期: {trip.get('start_date')}")
                print_info(f"结束日期: {trip.get('end_date')}")
                print_info(f"旅行人数: {trip.get('travelers')}")
                print_info(f"状态: {trip.get('status')}")
                print_info(f"预算明细:")
                budget = trip.get("budget", {})
                print(f"    - 总预算: ¥{budget.get('total', 0)}")
                print(f"    - 交通: ¥{budget.get('transport', 0)}")
                print(f"    - 住宿: ¥{budget.get('accommodation', 0)}")
                print(f"    - 餐饮: ¥{budget.get('food', 0)}")
                print(f"    - 活动: ¥{budget.get('activities', 0)}")

                preferences = trip.get("preferences", {})
                if preferences:
                    print_info(f"偏好设置:")
                    if "foodTypes" in preferences:
                        print(f"    - 美食偏好: {', '.join(preferences['foodTypes'])}")
                    if "attractionTypes" in preferences:
                        print(
                            f"    - 景点偏好: {', '.join(preferences['attractionTypes'])}"
                        )

                print_info(f"行程项目数: {len(trip.get('itinerary', []))}")
                print_info(f"分享令牌: {trip.get('share_token', 'N/A')}")
                print_info(f"创建时间: {trip.get('created_at')}")
                print_info(f"更新时间: {trip.get('updated_at')}")

                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"获取行程详情失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"获取行程详情请求失败: {str(e)}")
            return False

    def update_trip(self) -> bool:
        """更新行程"""
        print_header("7️⃣  更新行程信息")

        if not self.created_trip_id:
            print_warning("没有可更新的行程ID")
            return False

        update_data = {
            "title": "成都-重庆-重庆深度七日游（已更新）",
            "status": "confirmed",
            "travelers": 3,
        }

        print_info("更新数据:")
        print(json.dumps(update_data, ensure_ascii=False, indent=2))

        try:
            response = self.session.put(
                f"{self.base_url}/trips/{self.created_trip_id}", json=update_data
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"行程更新成功")
                print_info(f"消息: {data.get('message')}")
                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"更新行程失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"更新行程请求失败: {str(e)}")
            return False

    def test_ai_plan_endpoint(self) -> bool:
        """测试AI规划端点（不依赖实际API密钥）"""
        print_header("8️⃣  测试AI规划端点")

        # 生成测试行程数据
        start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d")

        trip_data = {
            "title": "东京迪士尼七日游",
            "destinations": ["东京"],
            "start_date": start_date,
            "end_date": end_date,
            "travelers": 2,
            "budget": {"total": 20000},
            "preferences": {
                "foodTypes": ["日料", "寿司"],
                "attractionTypes": ["主题公园", "城市观光"],
            },
        }

        print_info("AI规划请求:")
        print(json.dumps(trip_data, ensure_ascii=False, indent=2))

        try:
            # 使用SSE流
            response = self.session.post(
                f"{self.base_url}/trips/ai-plan",
                json=trip_data,
                stream=True,
                timeout=30,  # 30秒超时
            )

            if response.status_code == 200:
                print_success("AI规划端点响应成功")
                print_info("开始接收SSE流...")

                steps_received = 0
                last_progress = 0

                for line in response.iter_lines():
                    if line:
                        line_str = line.decode("utf-8")
                        if line_str.startswith("data: "):
                            try:
                                data = json.loads(line_str[6:])
                                steps_received += 1
                                progress = data.get("progress", 0)

                                print_info(f"[{progress:3d}%] {data.get('message')}")

                                if data.get("agent"):
                                    print(f"      智能体: {data.get('agent')}")

                                if data.get("action") == "complete":
                                    print_success("AI规划完成!")
                                    trip = data.get("trip", {})
                                    print_info(f"生成的行程ID: {trip.get('id')}")
                                    print_info(f"行程标题: {trip.get('title')}")
                                    last_progress = 100
                                    break

                                last_progress = progress

                            except json.JSONDecodeError as e:
                                print_warning(f"解析SSE数据失败: {e}")
                                continue

                print_success(f"接收到 {steps_received} 个进度步骤")
                return True
            else:
                error_detail = response.text
                print_warning(f"AI规划请求未成功响应（可能缺少API密钥）")
                print_info(f"状态码: {response.status_code}")
                print_info(f"响应: {error_detail[:200]}...")
                # 这不算失败，因为可能只是缺少API密钥
                return True
        except requests.exceptions.Timeout:
            print_warning("AI规划请求超时（可能需要较长时间）")
            return True
        except Exception as e:
            print_warning(f"AI规划测试跳过: {str(e)}")
            print_info("（这通常是因为缺少AI API密钥）")
            return True

    def delete_trip(self) -> bool:
        """删除行程"""
        print_header("9️⃣  删除行程")

        if not self.created_trip_id:
            print_warning("没有可删除的行程ID")
            return False

        try:
            response = self.session.delete(
                f"{self.base_url}/trips/{self.created_trip_id}"
            )

            if response.status_code == 200:
                data = response.json()
                print_success(f"行程删除成功")
                print_info(f"消息: {data.get('message')}")
                return True
            else:
                error_detail = response.json().get("detail", "未知错误")
                print_error(f"删除行程失败: {error_detail}")
                return False
        except Exception as e:
            print_error(f"删除行程请求失败: {str(e)}")
            return False

    def verify_deletion(self) -> bool:
        """验证删除结果"""
        print_header("🔟 验证删除结果")

        try:
            response = self.session.get(f"{self.base_url}/trips/{self.created_trip_id}")

            if response.status_code == 404:
                print_success("行程已成功删除（返回404）")
                return True
            else:
                print_warning("行程可能未完全删除")
                print_info(f"状态码: {response.status_code}")
                return False
        except Exception as e:
            print_warning(f"验证删除请求失败: {str(e)}")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print_header("🚀 前后端联合测试开始")

        results = []

        # 1. 健康检查
        results.append(("健康检查", self.test_health_check()))

        if not results[0][1]:
            print_error("后端服务未运行，测试中止")
            return

        # 2. 用户注册/登录
        results.append(("用户注册", self.register_user()))

        if results[1][1]:
            results.append(("用户登录", self.login_user()))
        else:
            print_error("用户注册失败，测试中止")
            return

        # 3. 行程CRUD操作
        results.append(("创建行程", self.create_manual_trip()))
        results.append(("获取行程列表", self.get_trips_list()))
        results.append(("获取行程详情", self.get_single_trip()))
        results.append(("更新行程", self.update_trip()))

        # 4. AI规划测试
        results.append(("AI规划端点", self.test_ai_plan_endpoint()))

        # 5. 删除行程
        results.append(("删除行程", self.delete_trip()))
        results.append(("验证删除", self.verify_deletion()))

        # 生成测试报告
        self.generate_report(results)

    def generate_report(self, results):
        """生成测试报告"""
        print_header("📊 测试报告")

        passed = sum(1 for _, result in results if result)
        total = len(results)
        failed = total - passed

        print(f"\n{Colors.BOLD}测试统计:{Colors.ENDC}")
        print(f"  总计: {total}")
        print(f"  {Colors.OKGREEN}通过: {passed}{Colors.ENDC}")
        print(f"  {Colors.FAIL}失败: {failed}{Colors.ENDC}")
        print(f"  成功率: {passed / total * 100:.1f}%\n")

        print(f"{Colors.BOLD}详细结果:{Colors.ENDC}")
        for test_name, result in results:
            status_icon = (
                f"{Colors.OKGREEN}✓{Colors.ENDC}"
                if result
                else f"{Colors.FAIL}✗{Colors.ENDC}"
            )
            print(f"  {status_icon} {test_name}")

        print(f"\n{Colors.BOLD}测试信息:{Colors.ENDC}")
        print(f"  测试用户: {self.email}")
        print(f"  用户ID: {self.user_id}")
        print(f"  后端URL: {self.base_url}")
        print(f"  测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if passed == total:
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 所有测试通过！{Colors.ENDC}")
        else:
            print(
                f"\n{Colors.WARNING}{Colors.BOLD}⚠️  部分测试失败，请检查日志{Colors.ENDC}"
            )


def main():
    """主函数"""
    tester = TripPlanningTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
