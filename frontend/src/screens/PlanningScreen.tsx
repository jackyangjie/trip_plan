import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, ScrollView, ActivityIndicator } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { Text, IconButton, useTheme } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import PlanningForm from './components/PlanningForm';
import PlanningStepDisplay from './components/PlanningStepDisplay';
import { useTripStore, useAuthStore } from '../stores';

export default function PlanningScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const theme = useTheme();
  const { addTrip } = useTripStore();
  const { token } = useAuthStore();
  const params = route.params as any || {};
  const { mode = 'create' } = params;

  const [isPlanning, setIsPlanning] = useState(false);
  const [currentStep, setCurrentStep] = useState(null);
  const [formData, setFormData] = useState(null);

  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 400,
      useNativeDriver: true,
    }).start();
  }, []);

  const handleSubmit = async (data: any) => {
    const newTrip: any = {
      id: Date.now().toString(),
      title: data.destinations?.join('、') || '未命名行程',
      destinations: data.destinations,
      startDate: data.startDate,
      endDate: data.endDate,
      travelers: data.travelers,
      budget: data.budget,
      status: 'planning',
      itinerary: [],
      isPublic: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      isLocal: true,
    };

    if (data.userId) {
      newTrip.userId = data.userId;
    }

    try {
      await addTrip(newTrip);
      navigation.navigate('index' as never);
    } catch (error) {
      console.error('Error adding trip:', error);
    }
  };

  const handleAIContinue = async (data: any) => {
    console.log('开始 AI 规划...', data);
    setFormData(data);
    setIsPlanning(true);
    setCurrentStep(null);

    try {
      const { aiPlanTripGenerator } = await import('../services/tripService');

      for await (const step of aiPlanTripGenerator(data, token)) {
        console.log('规划步骤:', step);
        setCurrentStep(step);

        if (step.action === 'complete' && step.trip) {
          const newTrip: any = {
            id: step.trip.id,
            title: step.trip.title,
            destinations: step.trip.destinations,
            startDate: step.trip.start_date,
            endDate: step.trip.end_date,
            travelers: step.trip.travelers,
            budget: step.trip.budget,
            status: step.trip.status,
            itinerary: step.trip.itinerary,
            isPublic: step.trip.is_public,
            createdAt: step.trip.created_at,
            updatedAt: step.trip.updated_at,
            isLocal: false,
          };

          await addTrip(newTrip);
          setIsPlanning(false);
          navigation.navigate('index' as never);
        }
      }
    } catch (error) {
      console.error('AI 规划失败:', error);
      setIsPlanning(false);
    }
  };

  const title = mode === 'create' ? '新建行程' : '编辑行程';

  return (
    <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.headerIcon}>
            <Icon name="map-marker-plus" size={20} color={theme.colors.onPrimary} />
          </View>
          <Text style={styles.title}>{title}</Text>
        </View>
      </View>

      {isPlanning && (
        <PlanningStepDisplay
          isPlanning={isPlanning}
          currentStep={currentStep}
        />
      )}

      <ScrollView style={styles.formContainer}>
        <PlanningForm
          onSubmit={handleSubmit}
          onAIContinue={handleAIContinue}
          disabled={isPlanning}
        />
      </ScrollView>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FAFBFC',
  },
  header: {
    backgroundColor: '#1A5490',
    paddingHorizontal: 20,
    paddingVertical: 24,
    paddingTop: 40,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerIcon: {
    width: 40,
    height: 40,
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#FFFFFF',
    letterSpacing: -0.5,
  },
  formContainer: {
    flex: 1,
  },
});
