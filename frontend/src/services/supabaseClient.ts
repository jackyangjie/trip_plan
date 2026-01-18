import { createClient } from '@supabase/supabase-js';
import { SUPABASE_URL, SUPABASE_KEY } from '../constants';

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL || SUPABASE_URL;
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_KEY || SUPABASE_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey, {
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
