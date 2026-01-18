export const API_BASE_URL = __DEV__
  ? 'http://localhost:8890'
  : 'https://api.travelplanner.com';

// Supabase 配置 - 使用本地 Docker 实例
export const SUPABASE_URL = 'http://localhost:54321';
export const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wZW5jb2RlX3Rlc3QiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczNjgwMDAwMCwiZXhwIjoyMDUyMzc2MDAwfQ.placeholder';

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
