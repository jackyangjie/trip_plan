# 旅行规划智能助手 - 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a multi-platform AI travel planner with React Native frontend, FastAPI + AgentScope backend, and Supabase database.

**Architecture:** 
- Three-tier architecture: React Native frontend → FastAPI/AgentScope backend → Supabase database
- Multi-Agent collaboration using AgentScope for intelligent trip planning
- Local-first approach: users can plan without login, sync to cloud on authentication
- High-performance async backend with Python FastAPI and AgentScope

**Tech Stack:**
- Frontend: React Native + Expo + TypeScript + Zustand + React Native Paper
- Backend: Python 3.10+ + FastAPI + AgentScope + Pydantic
- Database: Supabase (PostgreSQL) + Supabase CLI (local development)
- Maps: Amap (高德地图) API
- AI: AgentScope with multi-model support (OpenAI, Claude, Tongyi, etc.)
- Testing: pytest + Jest + React Native Testing Library

---

## Phase 1: 项目初始化与环境搭建

### Task 1: 创建项目目录结构和Monorepo配置

**Files:**
- Create: `travel-planner/`
- Create: `travel-planner/mobile/` (React Native)
- Create: `travel-planner/server/` (FastAPI)
- Create: `travel-planner/shared/` (Shared TypeScript types)
- Create: `travel-planner/docs/`
- Create: `travel-planner/docker-compose.yml`
- Create: `travel-planner/README.md`

**Step 1: 创建根目录和基础文件**

```bash
mkdir -p travel-planner/{mobile,server,shared,docs}
cd travel-planner

# 创建 monorepo 配置文件
cat > package.json << 'MONOREPO'
{
  "name": "travel-planner",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "mobile",
    "shared"
  ],
  "scripts": {
    "mobile:start": "cd mobile && npm start",
    "mobile:ios": "cd mobile && npm run ios",
    "mobile:web": "cd mobile && npm run web",
    "server:dev": "cd server && uvicorn app.main:app --reload",
    "server:test": "cd server && pytest",
    "lint": "npm run lint --workspaces",
    "test": "npm run test --workspaces"
  }
}
MONOREPO

# 创建 docker-compose.yml 用于本地 Supabase
cat > docker-compose.yml << 'DOCKER'
version: '3.8'

services:
  supabase:
    image: supabase/supabase:latest
    ports:
      - "54321:54321"  # API
      - "54322:54322"  # Studio
      - "54323:54323"  # DB
    volumes:
      - supabase_data:/var/lib/postgresql
      - ./docker-compose.init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  supabase_data:
DOCKER

cat > README.md << 'README'
# Travel Planner AI

Multi-platform AI travel planner with intelligent itinerary generation.

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker Desktop

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner

# Start Supabase locally
docker-compose up -d

# Install dependencies
npm install

# Start mobile app
npm run mobile:start

# Start backend (new terminal)
npm run server:dev
\`\`\`

## Features

- 🤖 AI-powered trip planning with multi-Agent collaboration
- 🗺️ Amap integration for location services
- 💰 Budget management with category tracking
- 📱 Cross-platform (iOS, Android, Web)
- 🔄 Real-time sync across devices
- 🔗 Share trips with friends

## Tech Stack

- React Native + Expo
- FastAPI + AgentScope
- Supabase (PostgreSQL)
- TypeScript
- Amap API

## License

MIT
README
```

**Step 2: 提交**

```bash
git add .
git commit -m "chore: create project structure with monorepo and docker-compose"
```

---

### Task 2: 配置Supabase本地开发环境

**Files:**
- Create: `travel-planner/docker-compose.init.sql`
- Create: `travel-planner/server/.env.example`
- Create: `travel-planner/mobile/.env.example`
- Create: `travel-planner/supabase/config.toml`

**Step 1: 编写数据库初始化SQL**

```sql
-- 启用UUID扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建自定义类型
CREATE TYPE trip_status AS ENUM ('planning', 'confirmed', 'completed', 'cancelled');
CREATE TYPE agent_type AS ENUM ('planner', 'transport', 'accommodation', 'attraction', 'food', 'budget');
CREATE TYPE session_status AS ENUM ('active', 'completed');

-- users表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- trips表
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    destination TEXT[],
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget JSONB DEFAULT '{"total": 0, "transport": 0, "accommodation": 0, "food": 0, "activities": 0}',
    status trip_status DEFAULT 'planning',
    itinerary JSONB DEFAULT '[]',
    share_token VARCHAR(64) UNIQUE,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- trip_shares表
CREATE TABLE trip_shares (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trip_id UUID REFERENCES trips(id) ON DELETE CASCADE,
    share_token VARCHAR(64) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- agent_sessions表
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES trips(id) ON DELETE SET NULL,
    agent_type agent_type NOT NULL,
    messages JSONB DEFAULT '[]',
    status session_status DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_trips_user_id ON trips(user_id);
CREATE INDEX idx_trips_status ON trips(status);
CREATE INDEX idx_trips_start_date ON trips(start_date);
CREATE INDEX idx_trip_shares_token ON trip_shares(share_token);
CREATE INDEX idx_agent_sessions_user_id ON agent_sessions(user_id);

-- RLS策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE trip_shares ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);
```

**Step 2: 创建环境变量模板**

```bash
# server/.env.example
SUPABASE_URL=http://localhost:54321
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
JWT_SECRET=your-super-secret-jwt-key
AMAP_API_KEY=your-amap-api-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
TONGYI_API_KEY=your-tongyi-key
```

**Step 3: 提交**

```bash
git add .
git commit -m "chore: add Supabase schema and environment templates"
```

---

### Task 3: 初始化React Native移动应用

**Files:**
- Create: `travel-planner/mobile/package.json`
- Create: `travel-planner/mobile/tsconfig.json`
- Create: `travel-planner/mobile/app.config.ts`
- Create: `travel-planner/mobile/babel.config.js`
- Create: `travel-planner/mobile/App.tsx`

**Step 1: 创建移动应用配置**

```bash
cd travel-planner/mobile

# package.json
cat > package.json << 'MOBILE_JSON'
{
  "name": "travel-planner-mobile",
  "version": "1.0.0",
  "main": "node_modules/expo/AppEntry.js",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "test": "jest",
    "lint": "eslint . --ext .ts,.tsx"
  },
  "dependencies": {
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/native-stack": "^6.9.17",
    "@react-navigation/bottom-tabs": "^6.5.11",
    "@supabase/supabase-js": "^2.39.0",
    "@react-native-async-storage/async-storage": "^1.21.0",
    "react": "18.2.0",
    "react-native": "0.73.2",
    "expo": "~50.0.0",
    "expo-status-bar": "~1.11.0",
    "react-native-paper": "^5.11.0",
    "react-native-screens": "~3.29.0",
    "react-native-safe-area-context": "4.8.2",
    "@amap/amap-react-native": "^1.0.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "dayjs": "^1.11.10",
    "@tanstack/react-query": "^5.17.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@types/react": "~18.2.45",
    "@types/react-native": "~0.73.0",
    "@typescript-eslint/eslint-plugin": "^6.17.0",
    "@typescript-eslint/parser": "^6.17.0",
    "eslint": "^8.56.0",
    "typescript": "^5.3.3"
  },
  "private": true
}
MOBILE_JSON
```

**Step 2: 创建应用入口**

```bash
# 创建必要的目录
mkdir -p mobile/src/{screens,components,hooks,stores,services,types,utils,navigation,theme}

# App.tsx
cat > App.tsx << 'APP_TSX'
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { PaperProvider } from 'react-native-paper';
import { NavigationContainer } from '@react-navigation/native';
import { theme } from './src/theme';
import RootNavigator from './src/navigation/RootNavigator';

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <NavigationContainer>
        <RootNavigator />
        <StatusBar style="auto" />
      </NavigationContainer>
    </PaperProvider>
  );
}
APP_TSX
```

**Step 3: 提交**

```bash
git add mobile/
git commit -m "chore: initialize React Native mobile app with Expo"
```

---

## Phase 2: 核心功能实现

### Task 4: 实现本地存储和状态管理

**Files:**
- Create: `travel-planner/mobile/src/stores/tripStore.ts`
- Create: `travel-planner/mobile/src/stores/authStore.ts`
- Create: `travel-planner/mobile/src/services/storageService.ts`
- Create: `travel-planner/mobile/src/types/index.ts`

**Step 1: 定义TypeScript类型**

```typescript
// Trip types
export interface TripBudget {
  total: number;
  transport: number;
  accommodation: number;
  food: number;
  activities: number;
}

export interface TripItineraryItem {
  id: string;
  day: number;
  time: string;
  type: 'transport' | 'accommodation' | 'attraction' | 'food' | 'custom';
  title: string;
  description?: string;
  location?: {
    name: string;
    lat: number;
    lng: number;
  };
  cost?: number;
  duration?: number;
  notes?: string;
}

export interface Trip {
  id: string;
  title: string;
  destination: string[];
  startDate: string;
  endDate: string;
  budget: TripBudget;
  status: 'planning' | 'confirmed' | 'completed' | 'cancelled';
  itinerary: TripItineraryItem[];
  shareToken?: string;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
  isLocal: boolean;
}
```

**Step 2: 创建Zustand stores**

```typescript
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware/async-storage';
import type { Trip } from '../types';
import * as storageService from '../services/storageService';

interface TripState {
  trips: Trip[];
  currentTrip: Trip | null;
  isLoading: boolean;
  
  loadTrips: () => Promise<void>;
  addTrip: (trip: Trip) => Promise<void>;
  updateTrip: (trip: Trip) => Promise<void>;
  deleteTrip: (tripId: string) => Promise<void>;
  setCurrentTrip: (trip: Trip | null) => void;
}

export const useTripStore = create<TripState>()(
  persist(
    (set, get) => ({
      trips: [],
      currentTrip: null,
      isLoading: false,

      loadTrips: async () => {
        set({ isLoading: true });
        try {
          const trips = await storageService.getLocalTrips();
          set({ trips, isLoading: false });
        } catch (error) {
          console.error('Error loading trips:', error);
          set({ isLoading: false });
        }
      },

      addTrip: async (trip: Trip) => {
        try {
          await storageService.addLocalTrip(trip);
          set((state) => ({ trips: [...state.trips, trip] }));
        } catch (error) {
          console.error('Error adding trip:', error);
          throw error;
        }
      },

      updateTrip: async (trip: Trip) => {
        try {
          await storageService.updateLocalTrip(trip);
          set((state) => ({
            trips: state.trips.map((t) => (t.id === trip.id ? trip : t)),
            currentTrip: state.currentTrip?.id === trip.id ? trip : state.currentTrip,
          }));
        } catch (error) {
          console.error('Error updating trip:', error);
          throw error;
        }
      },

      deleteTrip: async (tripId: string) => {
        try {
          await storageService.deleteLocalTrip(tripId);
          set((state) => ({
            trips: state.trips.filter((t) => t.id !== tripId),
            currentTrip: state.currentTrip?.id === tripId ? null : state.currentTrip,
          }));
        } catch (error) {
          console.error('Error deleting trip:', error);
          throw error;
        }
      },

      setCurrentTrip: (trip: Trip | null) => {
        set({ currentTrip: trip });
      },
    }),
    {
      name: 'trip-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ trips: state.trips }),
    }
  )
);
```

**Step 3: 提交**

```bash
git add mobile/src/{stores,services,types}/
git commit -m "feat: add local storage and Zustand state management"
```

---

### Task 5: 实现Supabase客户端和认证服务

**Files:**
- Create: `travel-planner/mobile/src/services/supabaseClient.ts`
- Create: `travel-planner/mobile/src/services/authService.ts`

**Step 1: 创建Supabase客户端**

```typescript
import { createClient } from '@supabase/supabase-js';
import Constants from 'expo-constants';

const supabaseUrl = Constants.expoConfig?.extra?.supabaseUrl || process.env.EXPO_PUBLIC_SUPABASE_URL;
const supabaseKey = Constants.expoConfig?.extra?.supabaseKey || process.env.EXPO_PUBLIC_SUPABASE_KEY;

export const supabase = createClient(supabaseUrl || '', supabaseKey || '', {
  auth: {
    storage: {
      getItem: async (key: string) => {
        const { AsyncStorage } = await import('@react-native-async-storage/async-storage');
        return AsyncStorage.getItem(key);
      },
      setItem: async (key: string, value: string) => {
        const { AsyncStorage } = await import('@react-native-async-storage/async-storage');
        await AsyncStorage.setItem(key, value);
      },
      removeItem: async (key: string) => {
        const { AsyncStorage } = await import('@react-native-async-storage/async-storage');
        await AsyncStorage.removeItem(key);
      },
    },
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
  },
});
```

**Step 2: 提交**

```bash
git add mobile/src/services/
git commit -m "feat: add Supabase client and authentication service"
```

---

### Task 6: 实现首页和行程列表

**Files:**
- Create: `travel-planner/mobile/src/screens/HomeScreen.tsx`
- Create: `travel-planner/mobile/src/screens/components/TripCard.tsx`

**Step 1: 创建行程卡片组件**

```typescript
import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Card, Text, Chip, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { Trip } from '../../types';
import { formatDate, calculateTotalDays } from '../../utils/dateUtils';

interface TripCardProps {
  trip: Trip;
  onPress: () => void;
  onDelete: () => void;
}

export default function TripCard({ trip, onPress, onDelete }: TripCardProps) {
  const duration = calculateTotalDays(trip.startDate, trip.endDate);
  const formattedDate = formatDate(trip.startDate);

  return (
    <TouchableOpacity onPress={onPress} style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <Text style={styles.title} numberOfLines={1}>{trip.title}</Text>
            <IconButton
              icon="delete-outline"
              size={20}
              onPress={onDelete}
              iconColor="#F44336"
            />
          </View>

          <View style={styles.destinationRow}>
            <Icon name="map-marker" size={16} color="#1976D2" />
            <Text style={styles.destination} numberOfLines={1}>
              {trip.destination.join(' → ')}
            </Text>
          </View>

          <View style={styles.infoRow}>
            <View style={styles.infoItem}>
              <Icon name="calendar" size={14} color="#666" />
              <Text style={styles.infoText}>{formattedDate}</Text>
            </View>
            <View style={styles.infoItem}>
              <Icon name="clock-outline" size={14} color="#666" />
              <Text style={styles.infoText}>{duration}天</Text>
            </View>
            <View style={styles.infoItem}>
              <Icon name="currency-cny" size={14} color="#666" />
              <Text style={styles.infoText}>¥{trip.budget.total.toLocaleString()}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  card: {
    elevation: 2,
    borderRadius: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    flex: 1,
    marginRight: 8,
  },
  destinationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  destination: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
    flex: 1,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
});
```

**Step 2: 创建首页**

```typescript
import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { FAB, Text, useTheme } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { useTripStore } from '../stores';
import TripCard from './components/TripCard';
import EmptyState from './components/EmptyState';

export default function HomeScreen() {
  const navigation = useNavigation<any>();
  const theme = useTheme();
  const { trips, loadTrips, deleteTrip } = useTripStore();
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadTrips();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadTrips();
    setRefreshing(false);
  };

  const handleDeleteTrip = async (tripId: string) => {
    await deleteTrip(tripId);
  };

  const handleTripPress = (tripId: string) => {
    navigation.navigate('TripDetail', { tripId });
  };

  const handleAddTrip = () => {
    navigation.navigate('Planning', { mode: 'create' });
  };

  const sortedTrips = [...trips].sort((a, b) => 
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>我的行程</Text>
      </View>

      {trips.length === 0 ? (
        <EmptyState
          icon="map-marker-path"
          title="还没有行程"
          description="开始规划您的第一次旅行吧"
          actionLabel="开始规划"
          onAction={handleAddTrip}
        />
      ) : (
        <FlatList
          data={sortedTrips}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <TripCard
              trip={item}
              onPress={() => handleTripPress(item.id)}
              onDelete={() => handleDeleteTrip(item.id)}
            />
          )}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
          }
        />
      )}

      <FAB
        icon="plus"
        label="新建行程"
        style={styles.fab}
        onPress={handleAddTrip}
        theme={{ colors: { primary: theme.colors.primary } }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
  },
  listContent: {
    paddingVertical: 16,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 16,
  },
});
```

**Step 3: 提交**

```bash
git add mobile/src/screens/
git commit -m "feat: implement home screen and trip list"
```

---

### Task 7: 实现行程规划页面

**Files:**
- Create: `travel-planner/mobile/src/screens/PlanningScreen.tsx`
- Create: `travel-planner/mobile/src/screens/components/PlanningForm.tsx`

**Step 1: 创建规划表单组件**

```typescript
import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, TextInput, Button, Chip, useTheme, Divider } from 'react-native-paper';
import DateRangePicker from './DateRangePicker';
import type { UserPreferences, TripBudget } from '../../types';
import { useAuthStore } from '../../stores';

const FOOD_TYPES = ['川菜', '粤菜', '湘菜', '东北菜', '西餐', '日料', '韩料', '泰国菜', '素食', '小吃'];
const ATTRACTION_TYPES = ['自然风光', '历史古迹', '主题公园', '博物馆', '海滩', '山区', '城市观光', '民俗风情'];

export default function PlanningForm({ onSubmit, onAIContinue }: any) {
  const theme = useTheme();
  const { user } = useAuthStore();
  
  const [destinations, setDestinations] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [travelers, setTravelers] = useState('2');
  const [budgetTotal, setBudgetTotal] = useState('5000');
  const [selectedFoodTypes, setSelectedFoodTypes] = useState<string[]>([]);
  const [selectedAttractionTypes, setSelectedAttractionTypes] = useState<string[]>([]);

  const handleFoodTypeToggle = (type: string) => {
    setSelectedFoodTypes(prev => 
      prev.includes(type) 
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  const handleSubmit = () => {
    const budget: TripBudget = {
      total: parseInt(budgetTotal) || 5000,
      transport: Math.round((parseInt(budgetTotal) || 5000) * 0.3),
      accommodation: Math.round((parseInt(budgetTotal) || 5000) * 0.35),
      food: Math.round((parseInt(budgetTotal) || 5000) * 0.2),
      activities: Math.round((parseInt(budgetTotal) || 5000) * 0.15),
    };

    const data = {
      destinations: destinations.split('、').map(d => d.trim()).filter(d => d),
      startDate,
      endDate,
      travelers: parseInt(travelers) || 2,
      budget,
      preferences: {
        foodTypes: selectedFoodTypes,
        attractionTypes: selectedAttractionTypes,
      },
      userId: user?.id,
    };

    onSubmit(data);
  };

  const isFormValid = destinations.length > 0 && startDate && endDate;

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>基本信息</Text>
        
        <Text style={styles.label}>目的地</Text>
        <TextInput
          mode="outlined"
          value={destinations}
          onChangeText={setDestinations}
          placeholder="例如: 北京、上海、杭州"
          style={styles.input}
        />
        
        <DateRangePicker
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
        />
        
        <Text style={styles.label}>出行人数</Text>
        <TextInput
          mode="outlined"
          value={travelers}
          onChangeText={setTravelers}
          keyboardType="numeric"
          style={styles.input}
        />
      </View>

      <Divider style={styles.divider} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>预算设置</Text>
        
        <Text style={styles.label}>总预算 (元)</Text>
        <TextInput
          mode="outlined"
          value={budgetTotal}
          onChangeText={setBudgetTotal}
          keyboardType="numeric"
          left={<TextInput.Affix text="¥" />}
          style={styles.input}
        />
      </View>

      <Divider style={styles.divider} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>偏好设置</Text>
        
        <Text style={styles.label}>美食偏好</Text>
        <View style={styles.chipGroup}>
          {FOOD_TYPES.map(type => (
            <Chip
              key={type}
              mode={selectedFoodTypes.includes(type) ? 'flat' : 'outlined'}
              selected={selectedFoodTypes.includes(type)}
              onPress={() => handleFoodTypeToggle(type)}
              style={styles.chip}
            >
              {type}
            </Chip>
          ))}
        </View>
      </View>

      <View style={styles.buttonGroup}>
        <Button
          mode="contained"
          onPress={handleSubmit}
          disabled={!isFormValid}
          style={styles.button}
          contentStyle={styles.buttonContent}
        >
          生成行程
        </Button>
        
        <Button
          mode="outlined"
          onPress={onAIContinue}
          style={styles.button}
          contentStyle={styles.buttonContent}
          icon="auto-fix"
        >
          AI智能规划
        </Button>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    marginTop: 8,
  },
  input: {
    marginBottom: 8,
  },
  divider: {
    marginHorizontal: 16,
    backgroundColor: '#E0E0E0',
  },
  chipGroup: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    marginBottom: 4,
  },
  buttonGroup: {
    padding: 16,
    gap: 12,
  },
  button: {
    borderRadius: 8,
  },
  buttonContent: {
    paddingVertical: 8,
  },
});
```

**Step 2: 提交**

```bash
git add mobile/src/screens/PlanningScreen.tsx mobile/src/screens/components/
git commit -m "feat: implement trip planning screen with form"
```

---

### Task 8: 实现后端FastAPI基础结构

**Files:**
- Create: `travel-planner/server/app/main.py`
- Create: `travel-planner/server/app/config.py`
- Create: `travel-planner/server/app/models.py`
- Create: `travel-planner/server/requirements.txt`

**Step 1: 创建后端项目结构**

```bash
cd travel-planner/server
mkdir -p app/{agents,routers,services,utils}
mkdir -p tests/

# requirements.txt
cat > requirements.txt << 'REQUIREMENTS'
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
supabase==2.3.4
python-dotenv==1.0.0
python-multipart==0.0.6
httpx==0.26.0
agentscope==1.0.0
amap-geo-py==1.0.0
apscheduler==3.10.4
pytest==7.4.4
pytest-asyncio==0.23.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
REQUIREMENTS
```

**Step 2: 创建FastAPI主文件**

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from datetime import datetime
import jwt
from datetime import timedelta

from app.config import settings
from app.database import get_supabase, init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    print("🚀 Travel Planner API started")
    yield
    print("👋 Travel Planner API stopped")

app = FastAPI(
    title="Travel Planner API",
    description="AI-powered travel planning assistant API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        return {"user_id": user_id, "email": email}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/auth/register")
async def register(user_data: dict):
    supabase = get_supabase()
    import hashlib
    password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
    user = supabase.table('users').insert({
        'email': user_data['email'],
        'password_hash': password_hash,
        'nickname': user_data.get('nickname', user_data['email'].split('@')[0]),
    }).execute()
    
    return {"message": "User created successfully", "user_id": user.data[0]['id']}

@app.post("/auth/login")
async def login(email: str, password: str):
    supabase = get_supabase()
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = supabase.table('users').select('*').eq('email', email).eq('password_hash', password_hash).execute()
    
    if not user.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = jwt.encode(
        {"sub": user.data[0]['id'], "email": email, "exp": datetime.utcnow() + access_token_expires},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    
    return {"access_token": access_token}

@app.get("/trips")
async def get_trips(current_user: dict = Depends(get_current_user)):
    supabase = get_supabase()
    trips = supabase.table('trips').select('*').eq('user_id', current_user['user_id']).execute()
    return trips.data

@app.post("/trips")
async def create_trip(trip_data: dict, current_user: dict = Depends(get_current_user)):
    supabase = get_supabase()
    trip_data['user_id'] = current_user['user_id']
    trip = supabase.table('trips').insert(trip_data).execute()
    return trip.data[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Step 3: 提交**

```bash
git add server/
git commit -m "feat: add FastAPI backend with basic structure"
```

---

## Phase 3: AI Agent实现

### Task 9: 实现AgentScope Agent模块

**Files:**
- Create: `travel-planner/server/app/agents/base.py`
- Create: `travel-planner/server/app/agents/planner.py`
- Create: `travel-planner/server/app/agents/transport.py`
- Create: `travel-planner/server/app/agents/accommodation.py`
- Create: `travel-planner/server/app/agents/attraction.py`
- Create: `travel-planner/server/app/agents/food.py`
- Create: `travel-planner/server/app/agents/budget.py`
- Create: `travel-planner/server/app/agents/coordinator.py`

**Step 1: 创建Agent基类和协调器**

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class AgentMessage(BaseModel):
    sender: str
    receiver: str
    content: Any
    timestamp: str
    message_type: str = "text"

class BaseAgent(ABC):
    name: str
    description: str
    
    def __init__(self):
        self.memory: List[AgentMessage] = []
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class AgentResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
```

**Step 2: 创建专业Agent**

```python
# planner.py
from typing import Dict, Any
from datetime import datetime, timedelta
from app.agents.base import BaseAgent, AgentResult

class PlannerAgent(BaseAgent):
    name = "planner"
    description = "Analyzes travel requests and generates comprehensive trip plans"
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        action = input_data.get('action', 'analyze')
        
        if action == 'analyze':
            return await self._analyze_request(input_data.get('request', {}))
        elif action == 'generate':
            return await self._generate_itinerary(input_data)
        
        return AgentResult(success=False, error=f"Unknown action: {action}")
    
    async def _analyze_request(self, request: Dict[str, Any]) -> AgentResult:
        analysis = {
            'destinations': request.get('destinations', []),
            'duration_days': self._calculate_duration(request.get('start_date', ''), request.get('end_date', '')),
            'travelers': request.get('travelers', 1),
            'budget_range': self._categorize_budget(request.get('budget', {})),
            'preferences': request.get('preferences', {}),
        }
        return AgentResult(success=True, data=analysis)
    
    def _calculate_duration(self, start_date: str, end_date: str) -> int:
        if not start_date or not end_date:
            return 1
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            return max(1, (end - start).days + 1)
        except:
            return 1
    
    def _categorize_budget(self, budget: Dict[str, int]) -> str:
        total = budget.get('total', 0)
        if total < 2000:
            return 'budget'
        elif total < 8000:
            return 'medium'
        return 'luxury'
```

**Step 3: 创建协调器**

```python
# coordinator.py
from typing import Dict, List, Any
from app.agents.base import BaseAgent, AgentResult
from app.agents.planner import PlannerAgent
from app.agents.transport import TransportAgent
from app.agents.accommodation import AccommodationAgent
from app.agents.attraction import AttractionAgent
from app.agents.food import FoodAgent
from app.agents.budget import BudgetAgent

class AgentCoordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.transport = TransportAgent()
        self.accommodation = AccommodationAgent()
        self.attraction = AttractionAgent()
        self.food = FoodAgent()
        self.budget = BudgetAgent()
    
    async def plan_trip(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1: Planning phase
        plan = await self.planner.process({'action': 'analyze', 'request': request})
        
        # Step 2: Parallel execution of specialized agents
        transport_result = await self.transport.process({'action': 'recommend', **request})
        accommodation_result = await self.accommodation.process({'action': 'recommend', **request})
        attraction_result = await self.attraction.process({'action': 'recommend', **request})
        food_result = await self.food.process({'action': 'recommend', **request})
        
        # Step 3: Budget analysis
        budget_result = await self.budget.process({
            'action': 'analyze',
            'transport': transport_result.data if transport_result.success else None,
            'accommodation': accommodation_result.data if accommodation_result.success else None,
            'attractions': attraction_result.data if attraction_result.success else None,
            'food': food_result.data if food_result.success else None,
            'budget': request.get('budget', {}),
        })
        
        # Step 4: Generate final itinerary
        final_plan = await self.planner.process({
            'action': 'generate',
            'request': request,
            'transport': transport_result.data if transport_result.success else {},
            'accommodation': accommodation_result.data if accommodation_result.success else {},
            'attractions': attraction_result.data if attraction_result.success else {},
            'food': food_result.data if food_result.success else {},
            'budget_analysis': budget_result.data if budget_result.success else {},
        })
        
        return {
            'success': final_plan.get('success', False),
            'itinerary': final_plan.get('itinerary', []),
            'budget': final_plan.get('budget', {}),
            'recommendations': {
                'transport': transport_result.data if transport_result.success else None,
                'accommodation': accommodation_result.data if accommodation_result.success else None,
                'attractions': attraction_result.data if attraction_result.success else None,
                'food': food_result.data if food_result.success else None,
            },
            'budget_analysis': budget_result.data if budget_result.success else None,
        }
```

**Step 4: 提交**

```bash
git add server/app/agents/
git commit -m "feat: implement AgentScope agents for trip planning"
```

---

## Phase 4: 测试与部署

### Task 10: 创建测试和文档

**Files:**
- Create: `travel-planner/server/tests/test_agents.py`
- Create: `travel-planner/server/tests/test_api.py`
- Create: `travel-planner/docker-compose.yml`

**Step 1: 创建测试**

```python
# tests/test_agents.py
import pytest
from app.agents.planner import PlannerAgent

@pytest.mark.asyncio
async def test_planner_analyze():
    agent = PlannerAgent()
    request = {
        'destinations': ['北京'],
        'start_date': '2024-03-01',
        'end_date': '2024-03-05',
        'travelers': 2,
        'budget': {'total': 5000}
    }
    
    result = await agent.process({'action': 'analyze', 'request': request})
    
    assert result.success == True
    assert result.data['destinations'] == ['北京']
    assert result.data['duration_days'] == 5
    assert result.data['budget_range'] == 'medium'
```

**Step 2: 创建docker-compose.yml**

```yaml
version: '3.8'

services:
  supabase:
    image: supabase/supabase:latest
    ports:
      - "54321:54321"
      - "54322:54322"
      - "54323:54323"
    volumes:
      - supabase_data:/var/lib/postgresql

volumes:
  supabase_data:
```

**Step 3: 提交**

```bash
git add tests/ docker-compose.yml
git commit -m "test: add tests and docker configuration"
```

---

## 实施计划总结

**总阶段数**: 4

**总任务数**: 10

**预计开发时间**: 8-12周

**关键里程碑**:
- Phase 1: 项目初始化和环境搭建（1周）
- Phase 2: 核心功能实现（4周）
- Phase 3: AI Agent实现（2周）
- Phase 4: 测试和部署（1周）

**下一步操作**:
1. 创建新的git worktree用于开发
2. 按照任务顺序逐步实现
3. 每个任务完成后进行代码审查
4. 集成测试和端到端测试
5. 部署到生产环境

---

## 执行选项

**Plan complete and saved to `docs/plans/2026-01-15-travel-planner-implementation.md`. Two execution options:**

**1. Subagent-Driven (this session)** - 我 dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
