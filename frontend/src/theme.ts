import { MD3LightTheme as DefaultTheme } from 'react-native-paper';

// Premium Travel Adventure Theme - Luxury travel magazine aesthetic
export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#1A5490',              // Deep ocean blue
    primaryContainer: '#D3E4FF',     // Light blue container
    secondary: '#E6A157',            // Warm sunset orange
    secondaryContainer: '#FFEBD4',    // Light warm container
    tertiary: '#00BFA5',             // Teal/cyan accent
    background: '#FAFBFC',           // Off-white with subtle warmth
    surface: '#FFFFFF',              // Pure white
    surfaceVariant: '#F0F4F8',       // Light blue-gray
    error: '#DC2626',                // Rich red
    onPrimary: '#FFFFFF',            // White on primary
    onSecondary: '#FFFFFF',          // White on secondary
    onBackground: '#1A1A1A',         // Near black text
    onSurface: '#1A1A1A',            // Near black on surface
    onError: '#FFFFFF',              // White on error
    onSurfaceVariant: '#475569',     // Cool gray for secondary text
    outline: '#CBD5E1',              // Light border color
    outlineVariant: '#E2E8F0',      // Very light border
  },
  // Enhanced typography scale
  fonts: {
    ...DefaultTheme.fonts,
    regular: {
      fontFamily: 'System',
      fontWeight: '400',
    },
    medium: {
      fontFamily: 'System',
      fontWeight: '500',
    },
    light: {
      fontFamily: 'System',
      fontWeight: '300',
    },
    thin: {
      fontFamily: 'System',
      fontWeight: '100',
    },
  },
};

// Spacing tokens for consistent layout
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Animation durations
export const animation = {
  fast: 150,
  normal: 300,
  slow: 500,
};

// Border radius tokens
export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
};

// Shadow presets
export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
};
