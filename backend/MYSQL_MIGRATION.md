# MySQL 替代 Supabase 指南

## 概述

本项目已将 Supabase 替换为 MySQL 数据库，使用 SQLAlchemy ORM 进行数据持久化。

## 架构变更

### 原架构（Supabase）
- Supabase URL: `http://localhost:54321`
- Supabase Keys: anon_key, service_role_key
- 未实际使用（代码中未集成）

### 新架构（MySQL）
- MySQL 数据库：`mysql+pymysql://user:password@localhost:3306/travel_planner`
- SQLAlchemy ORM
- 完整的 CRUD 操作

## 已修改的文件

### 1. backend/config.py
**变更**：
- 移除：`supabase_url`, `supabase_anon_key`, `supabase_service_role_key`
- 添加：`mysql_host`, `mysql_port`, `mysql_user`, `mysql_password`, `mysql_database`

### 2. backend/requirements.txt
**变更**：
- 移除：`supabase==2.3.4`
- 添加：
  - `sqlalchemy==2.0.25`（ORM）
  - `pymysql==1.1.0`（MySQL 驱动）

### 3. backend/app/database.py（新增）
**内容**：
- 数据库连接配置
- SQLAlchemy 引擎创建
- 会话管理
- `get_db()` 依赖注入函数
- `init_db()` 数据库初始化函数

### 4. backend/app/db_models.py（新增）
**内容**：
- `User` 模型（用户表）
- `Trip` 模型（行程表）
- SQLAlchemy 声明式映射
- 外键关系：User ↔ Trip

### 5. backend/main.py
**变更**：
- 添加 `lifespan` 上下文管理器，启动时初始化数据库
- 替换模拟数据为真实的数据库操作
- 实现完整 CRUD：
  - `/auth/register`：创建用户并保存到数据库
  - `/auth/login`：验证用户凭据
  - `GET /trips`：查询用户的行程列表
  - `POST /trips`：创建新行程
  - `GET /trips/{trip_id}`：获取单个行程
  - `PUT /trips/{trip_id}`：更新行程
  - `DELETE /trips/{trip_id}`：删除行程

## 安装步骤

### 1. 安装 MySQL 依赖

```bash
cd backend
source venv/bin/activate
pip install sqlalchemy pymysql cryptography
```

### 2. 创建 MySQL 数据库

```sql
CREATE DATABASE travel_planner CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

或使用命令行：

```bash
mysql -u root -p
```

然后在 MySQL 中执行：

```sql
CREATE DATABASE IF NOT EXISTS travel_planner
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# MySQL 数据库配置
mysql_host=localhost
mysql_port=3306
mysql_user=root
mysql_password=your_password
mysql_database=travel_planner

# JWT 密钥（生产环境请修改）
jwt_secret=change-this-in-production
jwt_algorithm=HS256
access_token_expire_minutes=60
refresh_token_expire_days=7
```

### 4. 启动后端

```bash
cd backend
source venv/bin/activate
python main.py
```

数据库表会在启动时自动创建。

## 验证安装

### 健康检查

```bash
curl http://localhost:8000/health
```

预期响应：

```json
{
  "status": "healthy",
  "timestamp": "2026-01-17T..."
}
```

### 测试用户注册

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password",
    "nickname": "Test User"
  }'
```

### 测试用户登录

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password"
  }'
```

返回的 `access_token` 将用于后续 API 请求。

### 测试创建行程

```bash
TOKEN="your_access_token"

curl -X POST http://localhost:8000/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "北京之旅",
    "destinations": ["北京"],
    "start_date": "2026-01-20",
    "end_date": "2026-01-25",
    "travelers": 2,
    "budget": {
      "total": 5000,
      "transport": 1500,
      "accommodation": 1750,
      "food": 1000,
      "activities": 750
    },
    "preferences": {
      "foodTypes": ["川菜", "小吃"]
    }
  }'
```

## 数据库表结构

### users 表

| 字段 | 类型 | 说明 |
|--------|------|------|
| id | String(36) | 主键（UUID） |
| email | String(255) | 邮箱（唯一索引） |
| password_hash | String(64) | 密码哈希（SHA256） |
| nickname | String(100) | 昵称 |
| preferences | JSON | 用户偏好 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### trips 表

| 字段 | 类型 | 说明 |
|--------|------|------|
| id | String(36) | 主键（UUID） |
| user_id | String(36) | 用户 ID（外键） |
| title | String(200) | 行程标题 |
| destinations | JSON | 目的地列表 |
| start_date | DateTime | 开始日期 |
| end_date | DateTime | 结束日期 |
| travelers | Integer | 出行人数 |
| status | String(20) | 状态（draft/planning/confirmed/completed/cancelled） |
| budget | JSON | 预算详情 |
| preferences | JSON | 偏好设置 |
| itinerary | JSON | 行程安排 |
| share_token | String(64) | 分享令牌（唯一索引） |
| is_public | Boolean | 是否公开 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 与前端集成

### 认证流程

1. 前端调用 `/auth/login` 获取 access_token
2. 后续所有 API 请求携带 `Authorization: Bearer <token>`
3. 后端验证 token 并获取 user_id

### 数据同步

目前前端使用 `AsyncStorage` 本地存储。如需与后端同步：

1. **注册/登录**：调用后端 API 获取 token
2. **获取行程**：调用 `GET /trips` 从数据库加载
3. **创建行程**：调用 `POST /trips` 保存到数据库
4. **更新行程**：调用 `PUT /trips/{trip_id}` 更新数据
5. **删除行程**：调用 `DELETE /trips/{trip_id}` 删除数据

### 示例：前端集成代码

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// 存储用户 token
export async function storeToken(token: string) {
  await AsyncStorage.setItem('@auth_token', token);
}

// 获取用户 token
export async function getToken() {
  return await AsyncStorage.getItem('@auth_token');
}

// 使用 token 调用 API
export async function fetchTrips() {
  const token = await getToken();
  const response = await fetch('http://localhost:8000/trips', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}
```

## 生产环境部署

### Docker Compose 配置

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: your_secure_password
      MYSQL_DATABASE: travel_planner
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  backend:
    build: ./backend
    environment:
      MYSQL_HOST: mysql
      MYSQL_PORT: 3306
      MYSQL_USER: root
      MYSQL_PASSWORD: your_secure_password
      MYSQL_DATABASE: travel_planner
      JWT_SECRET: your_jwt_secret
    ports:
      - "8000:8000"
    depends_on:
      - mysql

volumes:
  mysql_data:
```

### 数据库备份

```bash
# 备份
mysqldump -u root -p travel_planner > backup_$(date +%Y%m%d).sql

# 恢复
mysql -u root -p travel_planner < backup_20260117.sql
```

## 性能优化建议

### 索引优化

当前已添加的索引：
- `users.email`（用户邮箱唯一性）
- `trips.user_id`（用户行程查询）
- `trips.share_token`（分享功能）

可考虑添加：
- `trips.status`（按状态筛选）
- `trips.created_at`（时间范围查询）

### 连接池配置

```python
# database.py
engine = create_engine(
    MYSQL_DATABASE_URL,
    pool_pre_ping=True,      # 连接健康检查
    pool_recycle=3600,      # 连接回收时间（1小时）
    pool_size=10,            # 连接池大小
    max_overflow=20,          # 最大溢出连接
    echo=False,              # 生产环境关闭 SQL 日志
)
```

## 故障排查

### 连接错误

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError)
(2003, "Can't connect to MySQL server on 'localhost:3306'")
```

**解决方案**：
1. 检查 MySQL 服务是否运行：`systemctl status mysql`
2. 检查端口：`netstat -an | grep 3306`
3. 验证凭据：用户名、密码是否正确

### 表不存在

```
sqlalchemy.exc.NoSuchTableError
```

**解决方案**：
- 确保已调用 `init_db()` 创建表
- 检查数据库名称是否正确

### 认证失败

```
HTTPException(status_code=401, detail="Invalid authentication credentials")
```

**解决方案**：
- 检查 JWT secret 是否配置
- 验证 token 格式：`Bearer <token>`
- 检查 token 是否过期

## 总结

✅ Supabase 已成功替换为 MySQL
✅ 使用 SQLAlchemy ORM 进行数据库操作
✅ 实现完整的用户认证和行程 CRUD API
✅ 数据库表结构已定义
✅ 支持用户注册、登录和权限验证

**下一步**：
1. 启动 MySQL 服务
2. 配置 `.env` 文件
3. 运行 `pip install sqlalchemy pymysql` 安装依赖
4. 启动后端：`python main.py`
5. 测试 API 端点
