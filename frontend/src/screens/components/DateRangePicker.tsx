import React from 'react';
import { View, StyleSheet } from 'react-native';
import { TextInput, Button, useTheme } from 'react-native-paper';
import dayjs from 'dayjs';
import DatePicker from 'react-native-date-picker';

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
}

export default function DateRangePicker({ startDate, endDate, onStartDateChange, onEndDateChange }: DateRangePickerProps) {
  const theme = useTheme();

  return (
    <View style={styles.container}>
      <View style={styles.datePicker}>
        <TextInput
          mode="outlined"
          label="开始日期"
          value={startDate}
          onChangeText={onStartDateChange}
          placeholder="YYYY-MM-DD"
          style={styles.input}
        />
      </View>

      <View style={styles.datePicker}>
        <TextInput
          mode="outlined"
          label="结束日期"
          value={endDate}
          onChangeText={onEndDateChange}
          placeholder="YYYY-MM-DD"
          style={styles.input}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  datePicker: {
    flex: 1,
  },
  input: {
    marginBottom: 8,
  },
});
