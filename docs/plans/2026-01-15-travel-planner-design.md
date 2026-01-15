# 旅行规划智能助手 - 设计文档

## 项目概述

开发一个基于AI的旅行规划智能助手，支持多平台（iOS/Android/Web），可以根据用户输入的地点、时间、预算、偏好等信息，智能安排用户的行程。

### 核心功能
- 智能行程生成（基于AgentScope多Agent协作）
- 交通建议（高德地图API）
- 住宿推荐
- 景点推荐（支持类型筛选）
- 餐饮推荐（支持类型筛选）
- 分类预算管理
- 行程分享（链接/二维码）
- 跨设备实时同步

### 技术栈
- 前端：React Native + Expo（跨平台）
- 后端：FastAPI + AgentScope（Python）
- 数据库：Supabase（PostgreSQL + 本地开发部署）
- 地图：高德地图API
- AI：多提供商支持（OpenAI、通义千问、Claude等）

## 系统架构

### 三层架构

**前端层**
- React Native构建跨平台应用（iOS、Android、Web）
- React Native Web实现浏览器端
- 状态管理：Zustand
- UI组件库：React Native Paper

**后端层**
- FastAPI（Python异步框架）
- AgentScope负责AI Agent编排和多Agent协作
- 高德地图API集成

**数据层**
- Supabase作为后端即服务
- PostgreSQL存储用户、行程、偏好数据
- Supabase Auth处理邮箱密码认证
- Supabase Realtime实现跨设备实时同步
- Supabase Storage存储图片

## 数据模型

### 核心表结构

**users（用户表）**
- id（主键）
- email（唯一）
- password_hash
- nickname
- preferences（JSON：美食类型、景点类型、预算范围等）
- created_at、updated_at

**trips（行程表）**
- id（主键）
- user_id（外键）
- title（行程标题）
- destination（目的地，支持多个）
- start_date、end_date（日期范围）
- budget（JSON：{total, transport, accommodation, food, activities}）
- status（planning, confirmed, completed, cancelled）
- itinerary（JSON：详细行程安排）
- share_token（分享令牌）
- is_public（是否公开分享）
- created_at、updated_at

**trip_shares（行程分享表）**
- id（主键）
- trip_id（外键）
- share_token
- expires_at
- view_count
- created_at

**agent_sessions（Agent会话表）**
- id（主键）
- user_id（外键）
- trip_id（外键，可选）
- agent_type（Agent类型）
- messages（JSON：对话历史）
- status（active, completed）
- created_at、updated_at

## 核心功能模块

### 1. 用户认证模块
- 注册/登录（邮箱+密码）
- 忘记密码（邮箱验证）
- 用户偏好设置
- 会话管理

**特殊流程**：用户可以在未登录状态下规划行程，仅在保存或分享时提示登录。

### 2. 智能对话模块
- 自然语言对话界面
- 对话历史管理
- AgentScope Agent调度
- 支持多轮对话

### 3. 行程规划模块
- 表单式行程创建
- AI智能生成行程（多Agent协作）
- 行程编辑（拖拽、增删改）
- 行程模板

### 4. 服务Agent模块

**Agent类型**
- **行程规划Agent**：主协调者，生成完整行程
- **交通Agent**：高德地图API，推荐交通方式
- **住宿Agent**：推荐住宿选择
- **景点Agent**：景点推荐（按类型筛选）
- **餐饮Agent**：美食推荐（按类型筛选）
- **预算Agent**：费用估算和分类预算管理

### 5. 地图集成模块
- 高德地图SDK集成
- 地点搜索和POI展示
- 路线规划

### 6. 分享模块
- 生成分享链接/二维码
- 公开行程浏览
- 分享统计

### 7. 同步模块
- Supabase Realtime实时同步
- 离线缓存
- 跨设备同步

## 关键页面

### 页面流程
1. **欢迎页**：应用简介，"开始规划"按钮（无需登录）
2. **行程规划页**：表单输入 + AI对话，数据暂存本地
3. **登录/注册弹窗**：在"保存/分享"时触发
4. **行程列表页**：已登录显示云端行程，未登录显示本地临时行程
5. **行程详情页**：地图 + 时间线展示
6. **对话页面**：AI助手交互
7. **行程编辑页**：表单编辑
8. **分享页面**：生成分享链接

### 本地数据策略
- 未登录：AsyncStorage存储临时行程
- 已登录：Supabase存储 + 本地缓存
- 登录时自动迁移本地数据到云端

## AI Agent工作流程

### 行程规划流程

**阶段1：需求收集**
1. 用户输入需求（表单或自然语言）
2. 提取关键信息：目的地、时间、人数、预算、偏好
3. 查询用户历史偏好

**阶段2：多Agent协作**
1. 行程规划Agent作为主协调者
2. 并行调用：交通Agent、住宿Agent、景点Agent、餐饮Agent
3. 收集各Agent返回的建议

**阶段3：行程整合**
1. 根据预算约束筛选优化
2. 生成时间线（按天、时段）
3. 检查逻辑合理性

**阶段4：用户确认**
1. 展示完整行程（地图+列表）
2. 允许用户调整
3. 预算Agent实时更新费用
4. 保存到数据库

### Agent通信
- AgentScope MsgHub实现Agent间消息传递
- Pipeline模式协调各子Agent
- 支持异步并行执行

## 部署方案

### Supabase部署

**开发阶段（本地部署）**
```bash
npx supabase init
npx supabase start
```

本地包含：
- PostgreSQL数据库
- PostgREST API
- Gotrue（认证）
- Storage
- Realtime
- Studio（管理后台）

**生产阶段**
- 选项A：Supabase云托管（推荐）
- 选项B：Docker自托管到自有服务器

### 应用部署

**前端**
- 开发：Expo Go（真机调试）
- 生产：EAS构建和发布
- Web：Vercel或Netlify

**后端**
- 开发：本地运行
- 生产：Docker + 云服务器

## 技术实现细节

### 前端技术栈
- TypeScript
- React Native 0.73+
- Expo
- React Navigation
- Zustand
- React Native Paper
- Axios
- 高德地图React Native SDK

### 后端技术栈
- Python 3.10+
- FastAPI
- AgentScope
- Pydantic
- Supabase Python SDK
- 高德地图API Python SDK
- Apscheduler

## 错误处理与安全

### 错误处理
- 前端：网络错误重试、AI失败降级
- 后端：全局异常捕获、结构化错误响应
- Supabase：连接失败提示、认证处理

### 安全考虑
- 密码bcrypt加密
- JWT Token管理
- HTTPS传输
- 请求速率限制
- 输入验证
- 用户数据隔离（RLS策略）

### 性能优化
- 前端：虚拟列表、图片懒加载、离线缓存
- 后端：异步处理、查询优化、Agent并行执行
- Supabase：数据库索引、查询优化

## 测试策略

- 单元测试：Agent逻辑、API端点、工具函数
- 集成测试：Agent协作、数据库操作、外部API
- E2E测试：完整用户流程、跨平台测试

## 未来扩展

- 实际预订功能（机票、酒店）
- 更多天气数据
- 社交功能（行程评论、点赞）
- 多语言支持
- 更多支付方式

