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
