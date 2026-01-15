# 旅行规划智能助手 - 阶段1：项目初始化实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 初始化项目开发环境，搭建前端和后端基础架构，配置Supabase本地开发环境

**Architecture:** 采用前后端分离架构，前端使用React Native + Expo，后端使用FastAPI + AgentScope，数据层使用Supabase本地部署。项目分为frontend、backend、docs三个目录。

**Tech Stack:** React Native, Expo, TypeScript, FastAPI, Python 3.10+, Supabase CLI, AgentScope

---

## Task 1: 初始化项目结构

**Files:**
- Create: `frontend/package.json`
- Create: `backend/requirements.txt`
- Create: `backend/pyproject.toml`
- Create: `README.md`

**Step 1: Write frontend package.json**

```json
{
  "name": "travel-planner-frontend",
  "version": "0.1.0",
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "test": "jest",
    "lint": "eslint . --ext .ts,.tsx"
  },
  "dependencies": {
    "expo": "~51.0.0",
    "expo-router": "~3.5.0",
    "react": "18.2.0",
    "react-native": "0.74.0",
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/native-stack": "^6.9.17",
    "zustand": "^4.4.7",
    "react-native-paper": "^5.11.0",
    "axios": "^1.6.2",
    "@react-native-async-storage/async-storage": "^1.21.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@types/react": "~18.2.45",
    "typescript": "^5.1.3",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.56.0",
    "jest": "^29.7.0"
  },
  "private": true
}
```

**Step 2: Write backend requirements.txt**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
agentscope==1.0.0
supabase==2.3.4
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
apscheduler==3.10.4
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

**Step 3: Write backend pyproject.toml**

```toml
[tool.poetry]
name = "travel-planner-backend"
version = "0.1.0"
description = "Backend API for Travel Planner"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.5.2"
agentscope = "^1.0.0"
supabase = "^2.3.4"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
python-dotenv = "^1.0.0"
apscheduler = "^3.10.4"

[tool.poetry.dev-dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
httpx = "^0.25.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Step 4: Write project README.md**

```markdown
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
```

**Step 5: Commit**

```bash
git add frontend/package.json backend/requirements.txt backend/pyproject.toml README.md
git commit -m "feat: initialize project structure"
```

---

## Task 2: 初始化前端Expo配置

**Files:**
- Create: `frontend/app.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/babel.config.js`
- Create: `frontend/.gitignore`

**Step 1: Write app.json**

```json
{
  "expo": {
    "name": "旅行规划助手",
    "slug": "travel-planner",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      }
    },
    "web": {
      "favicon": "./assets/favicon.png"
    },
    "plugins": [
      "expo-router"
    ]
  }
}
```

**Step 2: Write tsconfig.json**

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowJs": true,
    "jsx": "react-native",
    "noEmit": true,
    "isolatedModules": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Step 3: Write babel.config.js**

```javascript
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ['expo-router/babel'],
  };
};
```

**Step 4: Write .gitignore**

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Expo
.expo/
.expo-shared/
dist/
web-build/

# Native
*.orig.*
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.pem
*.certSigningRequest

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# MacOS
.DS_Store

# Local env files
.env*.local
.env
```

**Step 5: Commit**

```bash
git add frontend/
git commit -m "feat: initialize frontend Expo configuration"
```

---

## Task 3: 创建前端基础目录结构

**Files:**
- Create: `frontend/src/components/index.ts`
- Create: `frontend/src/screens/index.ts`
- Create: `frontend/src/store/index.ts`
- Create: `frontend/src/services/index.ts`
- Create: `frontend/src/utils/index.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/constants/index.ts`

**Step 1: Create directory structure and index files**

```bash
cd frontend/src
mkdir -p components screens store services utils types constants
```

Write each index.ts with:

```typescript
// Re-export all exports from this directory
export * from './';
```

**Step 2: Create basic types**

Create `frontend/src/types/index.ts`:

```typescript
export interface User {
  id: string;
  email: string;
  nickname: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  foodTypes: string[];
  attractionTypes: string[];
  budgetRange: {
    min: number;
    max: number;
  };
}

export interface Trip {
  id: string;
  userId?: string;
  title: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  budget: Budget;
  status: 'planning' | 'confirmed' | 'completed' | 'cancelled';
  itinerary: Itinerary;
  shareToken?: string;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Budget {
  total: number;
  transport: number;
  accommodation: number;
  food: number;
  activities: number;
}

export interface Itinerary {
  days: Day[];
}

export interface Day {
  date: string;
  activities: Activity[];
}

export interface Activity {
  id: string;
  type: 'transport' | 'accommodation' | 'food' | 'attraction';
  title: string;
  location?: {
    lat: number;
    lng: number;
    address: string;
  };
  startTime?: string;
  endTime?: string;
  cost?: number;
  notes?: string;
}
```

**Step 3: Create constants**

Create `frontend/src/constants/index.ts`:

```typescript
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000/api/v1' 
  : 'https://api.travelplanner.com/api/v1';

export const STORAGE_KEYS = {
  USER: 'travel_planner_user',
  TOKEN: 'travel_planner_token',
  LOCAL_TRIPS: 'travel_planner_local_trips',
  PREFERENCES: 'travel_planner_preferences',
} as const;

export const FOOD_TYPES = [
  '川菜', '粤菜', '湘菜', '鲁菜', '苏菜', '浙菜', 
  '闽菜', '徽菜', '日料', '韩料', '西餐', '东南亚菜'
] as const;

export const ATTRACTION_TYPES = [
  '自然风光', '历史古迹', '主题公园', '博物馆', 
  '购物', '美食街', '宗教文化', '现代地标'
] as const;
```

**Step 4: Commit**

```bash
git add frontend/src/
git commit -m "feat: create frontend directory structure and types"
```

---

## Task 4: 创建前端Zustand store

**Files:**
- Create: `frontend/src/store/userStore.ts`
- Create: `frontend/src/store/tripStore.ts`
- Create: `frontend/src/store/index.ts`

**Step 1: Write userStore.ts**

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User } from '../types';

interface UserState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      setToken: (token) => set({ token }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'travel-planner-user-storage',
      storage: {
        getItem: (name) => AsyncStorage.getItem(name).then((data) => data && JSON.parse(data)),
        setItem: (name, value) => AsyncStorage.setItem(name, JSON.stringify(value)),
        removeItem: (name) => AsyncStorage.removeItem(name),
      },
    }
  )
);
```

**Step 2: Write tripStore.ts**

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Trip } from '../types';

interface TripState {
  trips: Trip[];
  currentTrip: Trip | null;
  setTrips: (trips: Trip[]) => void;
  setCurrentTrip: (trip: Trip | null) => void;
  addTrip: (trip: Trip) => void;
  updateTrip: (id: string, updates: Partial<Trip>) => void;
  deleteTrip: (id: string) => void;
}

export const useTripStore = create<TripState>()(
  persist(
    (set) => ({
      trips: [],
      currentTrip: null,
      setTrips: (trips) => set({ trips }),
      setCurrentTrip: (trip) => set({ currentTrip: trip }),
      addTrip: (trip) => set((state) => ({ trips: [...state.trips, trip] })),
      updateTrip: (id, updates) =>
        set((state) => ({
          trips: state.trips.map((trip) =>
            trip.id === id ? { ...trip, ...updates } : trip
          ),
        })),
      deleteTrip: (id) =>
        set((state) => ({
          trips: state.trips.filter((trip) => trip.id !== id),
        })),
    }),
    {
      name: 'travel-planner-trip-storage',
      storage: {
        getItem: (name) => AsyncStorage.getItem(name).then((data) => data && JSON.parse(data)),
        setItem: (name, value) => AsyncStorage.setItem(name, JSON.stringify(value)),
        removeItem: (name) => AsyncStorage.removeItem(name),
      },
    }
  )
);
```

**Step 3: Update store/index.ts**

```typescript
export { useUserStore } from './userStore';
export { useTripStore } from './tripStore';
```

**Step 4: Commit**

```bash
git add frontend/src/store/
git commit -m "feat: create Zustand stores for user and trip management"
```

---

## Task 5: 初始化后端FastAPI应用

**Files:**
- Create: `backend/main.py`
- Create: `backend/.env.example`
- Create: `backend/.gitignore`
- Create: `backend/config.py`

**Step 1: Write main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Configuration will be loaded later
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Travel Planner Backend...")
    yield
    # Shutdown
    print("Shutting down Travel Planner Backend...")

app = FastAPI(
    title="Travel Planner API",
    description="API for Travel Planner Application",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "travel-planner-api"}

# API routes will be added here
# from api.v1 import router
# app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Step 2: Write .env.example**

```env
# Supabase
SUPABASE_URL=http://localhost:54321
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Providers (AgentScope)
OPENAI_API_KEY=your-openai-api-key
TONGYI_API_KEY=your-tongyi-api-key
CLAUDE_API_KEY=your-claude-api-key

# Amap (高德地图)
AMAP_API_KEY=your-amap-api-key
AMAP_WEB_API_KEY=your-amap-web-api-key

# App Settings
APP_NAME=Travel Planner
APP_VERSION=0.1.0
DEBUG=True
```

**Step 3: Write .gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/
```

**Step 4: Write config.py**

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Supabase
    supabase_url: str = "http://localhost:54321"
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    
    # JWT
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    
    # AI Providers
    openai_api_key: str = ""
    tongyi_api_key: str = ""
    claude_api_key: str = ""
    
    # Amap
    amap_api_key: str = ""
    amap_web_api_key: str = ""
    
    # App
    app_name: str = "Travel Planner"
    app_version: str = "0.1.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

**Step 5: Commit**

```bash
git add backend/
git commit -m "feat: initialize FastAPI backend application"
```

---

## Task 6: 初始化Supabase本地开发环境

**Files:**
- Create: `supabase/config.toml`
- Create: `supabase/migrations/001_initial_schema.sql`

**Step 1: Write supabase/config.toml**

```toml
# Supabase configuration
project_id = "travel-planner-local"

[api]
port = 54321
schemas = ["public", "graphql_public"]
extra_search_path = ["public"]
max_rows = 1000

[db]
port = 54322
shadow_port = 54320
major_version = 15

[studio]
port = 54323

[ingest]
port = 54324

[storage]
file_size_limit = "5MiB"
image_transformation_enabled = true

[auth]
site_url = "http://localhost:19006"
additional_redirect_urls = ["http://localhost:19000"]
jwt_expiry = 3600

[analytics]
port = 54327
```

**Step 2: Write initial migration**

Create `supabase/migrations/001_initial_schema.sql`:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (additional to Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    nickname TEXT,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Trips table
CREATE TABLE IF NOT EXISTS public.trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    destinations TEXT[] NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'planning',
    itinerary JSONB NOT NULL DEFAULT '{}',
    share_token TEXT UNIQUE,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Trip shares table
CREATE TABLE IF NOT EXISTS public.trip_shares (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID NOT NULL REFERENCES public.trips(id) ON DELETE CASCADE,
    share_token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Agent sessions table
CREATE TABLE IF NOT EXISTS public.agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES public.trips(id) ON DELETE SET NULL,
    agent_type TEXT NOT NULL,
    messages JSONB NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_trips_user_id ON public.trips(user_id);
CREATE INDEX IF NOT EXISTS idx_trips_status ON public.trips(status);
CREATE INDEX IF NOT EXISTS idx_trip_shares_trip_id ON public.trip_shares(trip_id);
CREATE INDEX IF NOT EXISTS idx_trip_shares_token ON public.trip_shares(share_token);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_user_id ON public.agent_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_trip_id ON public.agent_sessions(trip_id);

-- Row Level Security (RLS)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trip_shares ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_sessions ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Users can only access their own profile
CREATE POLICY "Users can view own profile"
    ON public.user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.user_profiles FOR UPDATE
    USING (auth.uid() = id);

-- Trips: Users can view their own trips
CREATE POLICY "Users can view own trips"
    ON public.trips FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create trips"
    ON public.trips FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own trips"
    ON public.trips FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own trips"
    ON public.trips FOR DELETE
    USING (auth.uid() = user_id);

-- Public trips can be viewed by anyone
CREATE POLICY "Public trips are viewable by all"
    ON public.trips FOR SELECT
    USING (is_public = true);

-- Trip shares
CREATE POLICY "Anyone can view shared trips"
    ON public.trip_shares FOR SELECT
    USING (true);

-- Agent sessions
CREATE POLICY "Users can view own agent sessions"
    ON public.agent_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create agent sessions"
    ON public.agent_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own agent sessions"
    ON public.agent_sessions FOR UPDATE
    USING (auth.uid() = user_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to auto-update updated_at
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trips_updated_at
    BEFORE UPDATE ON public.trips
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_sessions_updated_at
    BEFORE UPDATE ON public.agent_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Step 3: Create README for Supabase**

Create `supabase/README.md`:

```markdown
# Supabase Development Environment

## Setup

```bash
# Initialize Supabase
npx supabase init

# Start local Supabase
npx supabase start

# Stop local Supabase
npx supabase stop
```

## Access

- Studio: http://localhost:54323
- API: http://localhost:54321
- Database: postgresql://postgres:postgres@localhost:54322/postgres

## Migrations

```bash
# Create new migration
npx supabase db diff -f new_migration.sql

# Apply migrations
npx supabase db push

# Reset database
npx supabase db reset
```
```

**Step 4: Commit**

```bash
git add supabase/
git commit -m "feat: initialize Supabase local development environment and schema"
```

---

## Task 7: 安装依赖并验证环境

**Files:**
- Test: `verify_installation.sh`

**Step 1: Create verification script**

```bash
cat > verify_installation.sh << 'SCRIPT'
#!/bin/bash

echo "=== 验证前端依赖 ==="
cd frontend
npm install
echo "✓ Frontend dependencies installed"

echo "=== 验证后端依赖 ==="
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✓ Backend dependencies installed"

echo "=== 验证Supabase ==="
cd ..
npx supabase start
echo "✓ Supabase started successfully"

echo "=== 验证后端启动 ==="
cd backend
source venv/bin/activate
python -c "import agentscope; print('✓ AgentScope installed')"
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import supabase; print('✓ Supabase Python client installed')"

echo "=== 所有依赖验证完成 ==="
SCRIPT

chmod +x verify_installation.sh
```

**Step 2: Run verification script**

```bash
./verify_installation.sh
```

**Expected output:**
- All dependencies installed successfully
- No errors
- Supabase services running

**Step 3: Commit**

```bash
git add verify_installation.sh
git commit -m "chore: add installation verification script"
```

---

## Task 8: 创建开发文档

**Files:**
- Create: `docs/development.md`

**Step 1: Write development documentation**

```markdown
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
```

**Step 2: Commit**

```bash
git add docs/development.md
git commit -m "docs: add development documentation"
```

---

## 阶段1完成检查清单

- [x] 项目结构初始化
- [x] 前端Expo配置完成
- [x] 前端基础目录和类型定义
- [x] Zustand状态管理配置
- [x] 后端FastAPI应用初始化
- [x] Supabase本地环境配置
- [x] 数据库Schema创建
- [x] 依赖安装验证
- [x] 开发文档完成

## 下一步

完成阶段1后，进入**阶段2：数据库和认证模块**，包括：
- 实现用户认证API
- 实现前端登录/注册界面
- 集成Supabase Auth
