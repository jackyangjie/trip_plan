import React, { useEffect, useRef, useState } from 'react';
import { View, Text, StyleSheet, Animated, ActivityIndicator } from 'react-native';
import { useTheme, ProgressBar, Card, IconButton } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

interface PlanningStep {
  step: number;
  message: string;
  action: string;
  progress: number;
  agent?: string;
  data?: any;
  error?: string;
}

interface Props {
  isPlanning: boolean;
  currentStep: PlanningStep | null;
}

export default function PlanningStepDisplay({ isPlanning, currentStep }: Props) {
  const theme = useTheme();
  const [progress, setProgress] = useState(0);
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: currentStep?.progress || 0,
      duration: 500,
      useNativeDriver: true,
    }).start(() => {
      setProgress(currentStep?.progress || 0);
    });
  }, [currentStep?.progress]);

  const getIconName = (action: string) => {
    switch (action) {
      case 'init':
      case 'init_complete':
        return 'playlist-plus';
      case 'analyzing':
        return 'brain';
      case 'transport':
      case 'transport_complete':
      case 'transport_error':
        return 'train-car';
      case 'accommodation':
      case 'accommodation_complete':
      case 'accommodation_error':
        return 'bed';
      case 'attraction':
      case 'attraction_complete':
      case 'attraction_error':
        return 'map-marker';
      case 'food':
      case 'food_complete':
      case 'food_error':
        return 'silverware';
      case 'budget':
      case 'budget_complete':
      case 'budget_error':
        return 'cash-multiple';
      case 'generate':
        return 'playlist-edit';
      case 'complete':
        return 'check-circle';
      default:
        return 'dots-horizontal';
    }
  };

  const getStepColor = () => {
    if (currentStep?.error) return '#FF5252';
    if (currentStep?.action.includes('_complete')) return '#4CAF50';
    return theme.colors.primary;
  };

  if (!isPlanning) {
    return null;
  }

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <View style={styles.header}>
          <View style={styles.iconContainer}>
            <Icon
              name={getIconName(currentStep?.action || '')}
              size={32}
              color={getStepColor()}
            />
          </View>
          <View style={styles.titleContainer}>
            <Text style={styles.stepTitle}>
              AI 智能规划 {currentStep?.step}/10
            </Text>
            {currentStep?.agent && (
              <Text style={styles.agentText}>
                {currentStep.agent}
              </Text>
            )}
          </View>
        </View>

        <Text style={styles.message}>{currentStep?.message}</Text>

        <View style={styles.progressContainer}>
          <ProgressBar
            progress={progress / 100}
            color={getStepColor()}
            style={styles.progressBar}
          />
          <Text style={styles.progressText}>
            {Math.round(progress)}%
          </Text>
        </View>

        {currentStep?.error && (
          <View style={styles.errorContainer}>
            <Icon name="alert-circle" size={20} color="#FF5252" />
            <Text style={styles.errorText}>{currentStep.error}</Text>
          </View>
        )}

        {currentStep?.data && currentStep.action.includes('_complete') && (
          <View style={styles.dataPreview}>
            <Text style={styles.dataPreviewTitle}>推荐结果预览</Text>
            <Text style={styles.dataPreviewText}>
              {JSON.stringify(currentStep.data, null, 2)}
            </Text>
          </View>
        )}
      </Card>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  card: {
    borderRadius: 16,
    padding: 20,
    elevation: 4,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    backgroundColor: '#FFFFFF',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  iconContainer: {
    width: 64,
    height: 64,
    borderRadius: 16,
    backgroundColor: '#E3F2FD',
    justifyContent: 'center',
    alignItems: 'center',
  },
  titleContainer: {
    flex: 1,
    marginLeft: 16,
  },
  stepTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1A5490',
    marginBottom: 4,
  },
  agentText: {
    fontSize: 14,
    color: '#666666',
    fontStyle: 'italic',
  },
  message: {
    fontSize: 16,
    color: '#333333',
    lineHeight: 24,
    marginBottom: 20,
  },
  progressContainer: {
    marginBottom: 16,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1A5490',
    marginTop: 8,
    textAlign: 'center',
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFEBEE',
    padding: 12,
    borderRadius: 8,
    marginTop: 8,
  },
  errorText: {
    flex: 1,
    marginLeft: 8,
    fontSize: 14,
    color: '#C62828',
  },
  dataPreview: {
    backgroundColor: '#F5F5F5',
    padding: 12,
    borderRadius: 8,
    marginTop: 12,
    borderLeftWidth: 3,
    borderLeftColor: '#1A5490',
  },
  dataPreviewTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#1A5490',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  dataPreviewText: {
    fontSize: 12,
    color: '#666666',
    fontFamily: 'monospace',
  },
});
