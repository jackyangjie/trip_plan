import { Stack } from 'expo-router';
import { PaperProvider } from 'react-native-paper';
import { theme } from '../src/theme';

export default function Layout() {
  return (
    <PaperProvider theme={theme}>
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: theme.colors.primary,
            elevation: 0,
            shadowOpacity: 0,
            borderBottomWidth: 0,
          } as any,
          headerTintColor: theme.colors.onPrimary,
          headerTitleStyle: {
            fontWeight: '700',
            fontSize: 18,
          } as any,
          headerBackTitleVisible: false,
          contentStyle: {
            backgroundColor: theme.colors.background,
          },
        }}
      >
        <Stack.Screen
          name="index"
          options={{
            title: '我的行程',
            headerShown: false,
          }}
        />
        <Stack.Screen
          name="planning"
          options={{
            title: '新建行程',
            presentation: 'card',
          }}
        />
      </Stack>
    </PaperProvider>
  );
}
