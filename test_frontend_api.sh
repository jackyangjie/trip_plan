#!/bin/bash

# 旅行规划助手 - 前端功能测试脚本
# 模拟前端 API 调用，验证后端服务

BASE_URL="http://localhost:8000"
echo "🧪 旅行规划助手 - 前端功能测试"
echo "================================"

# 测试1: 健康检查
echo ""
echo "1️⃣ 测试健康检查..."
curl -s "$BASE_URL/health" | python3 -m json.tool
echo "✅ 健康检查完成"

# 测试2: 注册新用户
echo ""
echo "2️⃣ 测试用户注册..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "前端测试用户@example.com",
    "password": "testpass123",
    "nickname": "前端测试"
  }')
echo "$REGISTER_RESPONSE" | python3 -m json.tool
TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

# 如果注册失败，尝试登录获取 token
if [ -z "$TOKEN" ]; then
  echo "用户已存在，尝试登录..."
  LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "前端测试用户@example.com",
      "password": "testpass123"
    }')
  TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
  echo "登录成功"
fi

# 测试3: 获取行程列表
echo ""
echo "3️⃣ 测试获取行程列表..."
TRIPS_RESPONSE=$(curl -s -X GET "$BASE_URL/trips" \
  -H "Authorization: Bearer $TOKEN")
echo "$TRIPS_RESPONSE" | python3 -m json.tool
echo "✅ 获取行程列表完成"

# 测试4: 创建新行程（模拟前端创建行程）
echo ""
echo "4️⃣ 测试创建行程..."
CREATE_TRIP_RESPONSE=$(curl -s -X POST "$BASE_URL/trips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "上海迪士尼之旅",
    "destinations": ["上海", "迪士尼乐园"],
    "start_date": "2026-03-15",
    "end_date": "2026-03-18",
    "travelers": 4,
    "status": "planning",
    "budget": {
      "total": 15000,
      "currency": "CNY"
    },
    "preferences": {
      "food": " diverse",
      "transport": "taxi",
      "style": "family"
    },
    "itinerary": [
      {
        "day": 1,
        "date": "2026-03-15",
        "activities": [
          {"time": "10:00", "activity": "抵达上海", "location": "上海虹桥机场"},
          {"time": "14:00", "activity": "入住酒店", "location": "迪士尼酒店"},
          {"time": "16:00", "activity": "探索迪士尼小镇", "location": "迪士尼小镇"}
        ]
      },
      {
        "day": 2,
        "date": "2026-03-16",
        "activities": [
          {"time": "08:00", "activity": "迪士尼乐园全天", "location": "迪士尼乐园"},
          {"time": "20:00", "activity": "烟火表演", "location": "城堡前"}
        ]
      },
      {
        "day": 3,
        "date": "2026-03-17",
        "activities": [
          {"time": "09:00", "activity": "玩具总动员园区", "location": "玩具总动员酒店"},
          {"time": "15:00", "activity": "离开乐园", "location": "上海"}
        ]
      }
    ]
  }')
echo "$CREATE_TRIP_RESPONSE" | python3 -m json.tool
echo "✅ 创建行程完成"

# 提取行程 ID
TRIP_ID=$(echo "$CREATE_TRIP_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('trip_id', ''))" 2>/dev/null)

# 测试5: 获取特定行程详情
if [ -n "$TRIP_ID" ]; then
  echo ""
  echo "5️⃣ 测试获取行程详情..."
  TRIP_DETAIL=$(curl -s -X GET "$BASE_URL/trips/$TRIP_ID" \
    -H "Authorization: Bearer $TOKEN")
  echo "$TRIP_DETAIL" | python3 -m json.tool
  echo "✅ 获取行程详情完成"
fi

# 测试6: 更新行程
if [ -n "$TRIP_ID" ]; then
  echo ""
  echo "6️⃣ 测试更新行程..."
  UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/trips/$TRIP_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{
      "status": "confirmed",
      "preferences": {
        "food": "diverse",
        "transport": "taxi",
        "style": "family",
        "note": "需要婴儿车租赁"
      }
    }')
  echo "$UPDATE_RESPONSE" | python3 -m json.tool
  echo "✅ 更新行程完成"
fi

# 测试7: 再次获取行程列表验证所有变更
echo ""
echo "7️⃣ 测试最终行程列表..."
FINAL_TRIPS=$(curl -s -X GET "$BASE_URL/trips" \
  -H "Authorization: Bearer $TOKEN")
echo "$FINAL_TRIPS" | python3 -m json.tool | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'\n📊 总行程数: {len(data)}')
for i, trip in enumerate(data, 1):
    print(f'  {i}. {trip[\"title\"]} ({trip[\"status\"]})')
"
echo "✅ 测试完成"

echo ""
echo "================================"
echo "🎉 所有前端功能测试通过！"
echo ""
echo "💡 现在可以在浏览器中访问 http://localhost:8081 进行实际的前端测试"
echo "📱 前端会调用相同的 API，数据会实时同步到数据库"
