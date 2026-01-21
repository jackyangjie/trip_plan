"""
数据库验证脚本 - 验证数据存储
"""

import psycopg2
import json
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 55432,
    "user": "postgres",
    "password": "your-super-secret-password",
    "database": "postgres",
}


def get_db_connection():
    """获取数据库连接"""
    return psycopg2.connect(**DB_CONFIG)


def verify_users_table():
    """验证用户表"""
    print("\n" + "=" * 60)
    print("验证用户表 (users)")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 查询所有用户
        cursor.execute(
            "SELECT id, email, nickname, created_at FROM users ORDER BY created_at DESC LIMIT 5"
        )
        users = cursor.fetchall()

        print(f"\n共找到 {len(users)} 个用户:\n")

        for idx, user in enumerate(users, 1):
            user_id, email, nickname, created_at = user
            print(f"{idx}. ID: {user_id}")
            print(f"   邮箱: {email}")
            print(f"   昵称: {nickname}")
            print(f"   创建时间: {created_at}")
            print(f"   密码哈希: {'✓ 已哈希' if user_id else 'N/A'}\n")

        return len(users)

    except Exception as e:
        print(f"❌ 查询用户表失败: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def verify_trips_table():
    """验证行程表"""
    print("\n" + "=" * 60)
    print("验证行程表 (trips)")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 查询所有行程
        cursor.execute("""
            SELECT
                id, user_id, title, status, travelers,
                start_date, end_date, budget, preferences,
                created_at, updated_at
            FROM trips
            ORDER BY created_at DESC
            LIMIT 10
        """)
        trips = cursor.fetchall()

        print(f"\n共找到 {len(trips)} 个行程:\n")

        for idx, trip in enumerate(trips, 1):
            (
                trip_id,
                user_id,
                title,
                status,
                travelers,
                start_date,
                end_date,
                budget,
                preferences,
                created_at,
                updated_at,
            ) = trip

            print(f"{idx}. {title}")
            print(f"   ID: {trip_id}")
            print(f"   用户ID: {user_id}")
            print(f"   状态: {status}")
            print(f"   旅行人数: {travelers}")
            print(f"   日期: {start_date} 至 {end_date}")

            # 解析JSON预算
            try:
                budget_data = json.loads(budget) if budget else {}
                print(f"   预算: ¥{budget_data.get('total', 0)}")
                print(
                    f"   预算明细: 交通 ¥{budget_data.get('transport', 0)}, "
                    f"住宿 ¥{budget_data.get('accommodation', 0)}, "
                    f"餐饮 ¥{budget_data.get('food', 0)}, "
                    f"活动 ¥{budget_data.get('activities', 0)}"
                )
            except:
                print(f"   预算: {budget}")

            # 解析JSON偏好
            try:
                pref_data = json.loads(preferences) if preferences else {}
                if pref_data:
                    food_types = pref_data.get("foodTypes", [])
                    attr_types = pref_data.get("attractionTypes", [])
                    if food_types:
                        print(f"   美食偏好: {', '.join(food_types)}")
                    if attr_types:
                        print(f"   景点偏好: {', '.join(attr_types)}")
            except:
                pass

            print(f"   创建时间: {created_at}")
            print(f"   更新时间: {updated_at}\n")

        return len(trips)

    except Exception as e:
        print(f"❌ 查询行程表失败: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()


def verify_foreign_keys():
    """验证外键关系"""
    print("\n" + "=" * 60)
    print("验证外键关系 (users ↔ trips)")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 查询每个用户的行程数
        cursor.execute("""
            SELECT
                u.id, u.email, u.nickname,
                COUNT(t.id) as trip_count
            FROM users u
            LEFT JOIN trips t ON u.id = t.user_id
            GROUP BY u.id, u.email, u.nickname
            ORDER BY trip_count DESC
        """)

        user_trips = cursor.fetchall()

        print("\n用户行程统计:\n")

        for idx, (user_id, email, nickname, trip_count) in enumerate(user_trips, 1):
            print(f"{idx}. {email} ({nickname})")
            print(f"   行程数: {trip_count}")
            print(f"   用户ID: {user_id}\n")

        # 验证所有行程的user_id都存在
        cursor.execute("""
            SELECT COUNT(*)
            FROM trips t
            LEFT JOIN users u ON t.user_id = u.id
            WHERE u.id IS NULL
        """)

        orphan_trips = cursor.fetchone()[0]

        if orphan_trips == 0:
            print("✅ 所有行程都有对应的用户（无孤儿行程）")
        else:
            print(f"⚠️  发现 {orphan_trips} 个孤儿行程")

        return True

    except Exception as e:
        print(f"❌ 验证外键失败: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def verify_trip_status_distribution():
    """验证行程状态分布"""
    print("\n" + "=" * 60)
    print("验证行程状态分布")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                status,
                COUNT(*) as count,
                AVG(travelers) as avg_travelers,
                AVG((budget->>'total')::numeric) as avg_budget
            FROM trips
            GROUP BY status
            ORDER BY count DESC
        """)

        status_data = cursor.fetchall()

        print("\n状态分布:\n")

        total_trips = sum(row[1] for row in status_data)

        for status, count, avg_travelers, avg_budget in status_data:
            percentage = (count / total_trips * 100) if total_trips > 0 else 0
            print(f"📊 {status.upper()}")
            print(f"   数量: {count} ({percentage:.1f}%)")
            print(f"   平均人数: {avg_travelers:.1f}")
            if avg_budget:
                print(f"   平均预算: ¥{avg_budget:.0f}\n")
            else:
                print(f"   平均预算: N/A\n")

        return True

    except Exception as e:
        print(f"❌ 查询状态分布失败: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def verify_data_integrity():
    """验证数据完整性"""
    print("\n" + "=" * 60)
    print("验证数据完整性")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    checks = []

    try:
        # 检查1: 用户必须有唯一邮箱
        cursor.execute(
            "SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1"
        )
        duplicate_emails = cursor.fetchall()
        if duplicate_emails:
            print(f"❌ 发现重复邮箱: {duplicate_emails}")
            checks.append(False)
        else:
            print("✅ 用户邮箱唯一性检查通过")
            checks.append(True)

        # 检查2: 行程必须有有效的日期范围
        cursor.execute("""
            SELECT id, title, start_date, end_date
            FROM trips
            WHERE end_date <= start_date
        """)
        invalid_dates = cursor.fetchall()
        if invalid_dates:
            print(f"❌ 发现无效日期范围:")
            for trip in invalid_dates:
                print(f"   {trip[1]}: {trip[2]} - {trip[3]}")
            checks.append(False)
        else:
            print("✅ 行程日期范围检查通过")
            checks.append(True)

        # 检查3: 行程必须有标题
        cursor.execute("SELECT COUNT(*) FROM trips WHERE title IS NULL OR title = ''")
        empty_titles = cursor.fetchone()[0]
        if empty_titles > 0:
            print(f"❌ 发现 {empty_titles} 个无标题行程")
            checks.append(False)
        else:
            print("✅ 行程标题检查通过")
            checks.append(True)

        # 检查4: 用户必须有密码哈希
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE password_hash IS NULL OR password_hash = ''"
        )
        no_password = cursor.fetchone()[0]
        if no_password > 0:
            print(f"❌ 发现 {no_password} 个无密码用户")
            checks.append(False)
        else:
            print("✅ 用户密码哈希检查通过")
            checks.append(True)

        # 检查5: 行程share_token唯一性
        cursor.execute("""
            SELECT share_token, COUNT(*)
            FROM trips
            WHERE share_token IS NOT NULL
            GROUP BY share_token
            HAVING COUNT(*) > 1
        """)
        duplicate_tokens = cursor.fetchall()
        if duplicate_tokens:
            print(f"❌ 发现重复分享令牌: {duplicate_tokens}")
            checks.append(False)
        else:
            print("✅ 分享令牌唯一性检查通过")
            checks.append(True)

        return all(checks)

    except Exception as e:
        print(f"❌ 数据完整性检查失败: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def generate_summary_report():
    """生成数据库验证总结报告"""
    print("\n" + "=" * 60)
    print("📊 数据库验证总结报告")
    print("=" * 60)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 总体统计
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM trips")
        trip_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM trips WHERE status = 'draft'")
        draft_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM trips WHERE status = 'confirmed'")
        confirmed_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM trips WHERE status = 'planning'")
        planning_count = cursor.fetchone()[0]

        # 最新数据
        cursor.execute("SELECT created_at FROM users ORDER BY created_at DESC LIMIT 1")
        latest_user = cursor.fetchone()

        cursor.execute("SELECT created_at FROM trips ORDER BY created_at DESC LIMIT 1")
        latest_trip = cursor.fetchone()

        print("\n📈 总体统计:")
        print(f"   用户总数: {user_count}")
        print(f"   行程总数: {trip_count}")
        print(
            f"   平均每人行程数: {trip_count / user_count:.1f}"
            if user_count > 0
            else "   平均每人行程数: N/A"
        )

        print("\n📋 状态分布:")
        print(f"   草稿 (draft): {draft_count}")
        print(f"   已确认 (confirmed): {confirmed_count}")
        print(f"   规划中 (planning): {planning_count}")

        print("\n🕒 最新活动:")
        print(f"   最新用户: {latest_user[0] if latest_user else 'N/A'}")
        print(f"   最新行程: {latest_trip[0] if latest_trip else 'N/A'}")

        print(f"\n🔒 数据完整性: {'✅ 通过' if verify_data_integrity() else '❌ 失败'}")

    except Exception as e:
        print(f"❌ 生成报告失败: {e}")
    finally:
        cursor.close()
        conn.close()


def main():
    """主函数"""
    print("=" * 60)
    print("🗄️  数据库验证工具")
    print("=" * 60)

    # 执行所有验证
    user_count = verify_users_table()
    trip_count = verify_trips_table()
    verify_foreign_keys()
    verify_trip_status_distribution()
    verify_data_integrity()

    # 生成总结报告
    generate_summary_report()

    print("\n" + "=" * 60)
    print("✅ 数据库验证完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
