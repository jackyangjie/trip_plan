import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Text, useTheme } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import dayjs from 'dayjs';
import DateModalPicker from './DateModalPicker';

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  error?: string;
}

export default function DateRangePicker({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  error,
}: DateRangePickerProps) {
  const theme = useTheme();

  const [showStartPicker, setShowStartPicker] = useState(false);
  const [showEndPicker, setShowEndPicker] = useState(false);

  const formatDate = (date: string) => {
    if (!date) return 'YYYY-MM-DD';
    return dayjs(date).format('YYYY年MM月DD日');
  };

  const getValidationError = () => {
    if (!startDate || !endDate) return null;

    const start = dayjs(startDate);
    const end = dayjs(endDate);

    if (end.isBefore(start)) {
      return '结束日期不能早于开始日期';
    }

    if (end.isSame(start)) {
      return '结束日期不能与开始日期相同';
    }

    return null;
  };

  const validationError = getValidationError();

  const handleStartDatePress = () => {
    setShowStartPicker(true);
  };

  const handleEndDatePress = () => {
    setShowEndPicker(true);
  };

  const handleStartDateConfirm = (date: string) => {
    onStartDateChange(date);
    setShowStartPicker(false);

    if (endDate && dayjs(date).isAfter(dayjs(endDate))) {
      onEndDateChange('');
    }
  };

  const handleEndDateConfirm = (date: string) => {
    onEndDateChange(date);
    setShowEndPicker(false);
  };

  const getMinDateForEnd = () => {
    if (!startDate) return undefined;
    return startDate;
  };

  const getMinDateForStart = () => {
    return dayjs().format('YYYY-MM-DD');
  };

  return (
    <View style={styles.container}>
      <View style={styles.dateInputsRow}>
        <View style={styles.dateInputWrapper}>
          <TouchableOpacity
            style={[
              styles.dateInput,
              (error || validationError) && styles.dateInputError,
            ]}
            onPress={handleStartDatePress}
            activeOpacity={0.7}
          >
            <Icon
              name="calendar-start"
              size={20}
              color={startDate ? theme.colors.primary : theme.colors.onSurfaceVariant}
              style={styles.dateIcon}
            />
            <Text
              style={[
                styles.dateText,
                {
                  color: startDate ? theme.colors.onSurface : theme.colors.onSurfaceVariant,
                },
              ]}
              numberOfLines={1}
            >
              {formatDate(startDate)}
            </Text>
          </TouchableOpacity>
          <Text style={styles.inputLabel}>开始日期</Text>
        </View>

        <View style={styles.arrowContainer}>
          <Icon name="arrow-right" size={24} color={theme.colors.primary} />
        </View>

        <View style={styles.dateInputWrapper}>
          <TouchableOpacity
            style={[
              styles.dateInput,
              (error || validationError) && styles.dateInputError,
            ]}
            onPress={handleEndDatePress}
            activeOpacity={0.7}
            disabled={!startDate}
          >
            <Icon
              name="calendar-end"
              size={20}
              color={endDate ? theme.colors.secondary : theme.colors.onSurfaceVariant}
              style={styles.dateIcon}
            />
            <Text
              style={[
                styles.dateText,
                {
                  color: endDate ? theme.colors.onSurface : theme.colors.onSurfaceVariant,
                  opacity: startDate ? 1 : 0.4,
                },
              ]}
              numberOfLines={1}
            >
              {formatDate(endDate)}
            </Text>
          </TouchableOpacity>
          <Text style={styles.inputLabel}>结束日期</Text>
        </View>
      </View>

      {(error || validationError) && (
        <View style={styles.errorRow}>
          <Icon name="alert-circle" size={16} color={theme.colors.error} />
          <Text style={[styles.errorText, { color: theme.colors.error }]}>
            {error || validationError}
          </Text>
        </View>
      )}

      <DateModalPicker
        visible={showStartPicker}
        initialDate={startDate || getMinDateForStart()}
        onDismiss={() => setShowStartPicker(false)}
        onConfirm={handleStartDateConfirm}
        minDate={getMinDateForStart()}
      />

      <DateModalPicker
        visible={showEndPicker}
        initialDate={endDate || startDate}
        onDismiss={() => setShowEndPicker(false)}
        onConfirm={handleEndDateConfirm}
        minDate={getMinDateForEnd()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 0,
  },
  dateInputsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  dateInputWrapper: {
    flex: 1,
  },
  dateInput: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F8FAFC',
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: '#E2E8F0',
    paddingHorizontal: 12,
    paddingVertical: 14,
    minHeight: 48,
  },
  dateInputError: {
    borderColor: '#DC2626',
    backgroundColor: '#FEF2F2',
  },
  dateIcon: {
    marginRight: 8,
  },
  dateText: {
    flex: 1,
    fontSize: 15,
    fontWeight: '500',
  },
  inputLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#64748B',
    marginTop: 6,
    marginLeft: 4,
  },
  arrowContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 14,
  },
  errorRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: '#FEF2F2',
    borderRadius: 8,
  },
  errorText: {
    fontSize: 13,
    fontWeight: '500',
    marginLeft: 6,
    flex: 1,
  },
});
