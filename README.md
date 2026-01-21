# 旅行规划智能助手

基于AI的旅行规划智能助手，支持多平台（iOS/Android/Web）

## 项目结构

```
.
├── frontend/          # React Native前端
├── backend/           # FastAPI后端
├── docs/             # 文档
└── supabase/         # Supabase配置
```

## 多智能体旅行规划系统

### AI规划API端点

```bash
# 启动后端服务
cd backend
python main.py
```

```bash
# 测试AI规划端点（需要配置AI API密钥）
curl -X POST http://localhost:8000/trips/ai-plan \
  -H "Content-Type: application/json" \
  -d '{
    "title": "上海三日游",
    "destinations": ["上海"],
    "start_date": "2026-03-01",
    "end_date": "2026-03-03",
    "travelers": 2,
    "budget": {"total": 3000}
  }'
```

API将返回：
- 实时进度更新（SSE流式）
- 6个智能体并行工作
- 完整的行程JSON响应

### 架构概述

系统使用 AgentScope 框架构建了6个专门化的 AI 智能体，它们协作生成综合旅行计划。

**核心组件：**
- **AgentScope 框架**: AI 智能体的核心框架
- **ReActAgent**: 可以自动调用工具的推理智能体
- **Toolkit**: 管理 MCP (Model Context Protocol) 工具集成
- **MsgHub**: 协调多智能体通信
- **amap-mcp-server**: 通过 MCP 提供实时地图服务

**专门化智能体：**
1. **TransportAgent** - 推荐交通方案（航班、高铁等）
2. **AccommodationAgent** - 推荐住宿和酒店
3. **AttractionAgent** - 推荐景点和活动
4. **FoodAgent** - 推荐餐厅和当地美食
5. **BudgetAgent** - 分析和优化旅行预算
6. **PlannerAgent** - 将所有推荐整合为最终行程

### 智能体工作流程

1. 初始化：协调器创建所有6个智能体（具有ReAct推理能力）
2. 注入MCP工具：智能体接收地图工具（地理编码、搜索、路线规划）
3. 广播任务：MsgHub向所有智能体发送规划任务
4. 并行执行：每个智能体处理其专门领域
5. 整合：PlannerAgent合并所有推荐
6. 生成：最终行程包含每日时间表
7. 返回：包含所有推荐的完整旅行计划

更多详细信息请参阅 [多智能体系统指南](docs/multi-agent-guide.md)

## 快速开始

### 前端
```bash
cd frontend
npm install
npm start
```

### 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Supabase
```bash
npx supabase init
npx supabase start
```
