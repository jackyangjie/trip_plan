# 旅行规划助手 - 开发文档

## 环境要求

- Node.js 18+
- Python 3.10+
- npm/yarn
- Git
- Docker (用于Supabase)

## 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd travel-planner
```

### 2. 安装依赖

#### 前端
```bash
cd frontend
npm install
```

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Supabase
```bash
npx supabase init
npx supabase start
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑.env文件，填入必要的API密钥
```

### 4. 启动开发服务器

#### 启动前端
```bash
cd frontend
npm start
```

#### 启动后端
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

#### Supabase管理界面
访问: http://localhost:54323

## 项目结构

```
travel-planner/
├── frontend/           # React Native前端
│   ├── src/
│   │   ├── components/
│   │   ├── screens/
│   │   ├── store/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── types/
│   │   └── constants/
│   └── package.json
├── backend/           # FastAPI后端
│   ├── api/
│   ├── agents/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── main.py
├── supabase/          # Supabase配置和迁移
│   ├── migrations/
│   └── config.toml
└── docs/             # 文档
```

## 开发流程

### 添加新功能
1. 创建feature分支
2. 编写测试
3. 实现功能
4. 运行测试
5. 提交代码
6. 创建PR

### 测试
```bash
# 前端测试
cd frontend
npm test

# 后端测试
cd backend
pytest
```

### Linting
```bash
# 前端linting
cd frontend
npm run lint

# 后端linting
cd backend
ruff check .
```

## 常见问题

### Supabase启动失败
```bash
npx supabase stop
npx supabase start
```

### 数据库连接问题
检查`.env`文件中的Supabase URL是否正确

### AgentScope配置问题
确保已配置至少一个AI Provider的API密钥
