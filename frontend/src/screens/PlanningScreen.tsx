import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { Text } from 'react-native-paper';
import PlanningForm from './components/PlanningForm';

export default function PlanningScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { mode } = route.params || { mode: 'create' };

  const handleSubmit = (data: any) => {
    console.log('Form submitted:', data);
    navigation.navigate('Home');
  };

  const handleAIContinue = () => {
    console.log('AI planning requested');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        {mode === 'create' ? '新建行程' : '编辑行程'}
      </Text>
      <PlanningForm
        onSubmit={handleSubmit}
        onAIContinue={handleAIContinue}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
    padding: 16,
  },
});
