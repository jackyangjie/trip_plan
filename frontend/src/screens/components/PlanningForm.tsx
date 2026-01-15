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
