import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  Modal,
  TouchableOpacity,
  ScrollView,
  Platform,
  Dimensions,
} from 'react-native';
import { Text, useTheme, Portal } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import dayjs from 'dayjs';

interface DateModalPickerProps {
  visible: boolean;
  initialDate: string;
  onDismiss: () => void;
  onConfirm: (date: string) => void;
  minDate?: string;
  maxDate?: string;
}

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export default function DateModalPicker({
  visible,
  initialDate,
  onDismiss,
  onConfirm,
  minDate,
  maxDate,
}: DateModalPickerProps) {
  const theme = useTheme();

  const [selectedDate, setSelectedDate] = useState(
    initialDate ? dayjs(initialDate) : dayjs()
  );

  const currentYear = dayjs().year();
  const years = Array.from({ length: 10 }, (_, i) => currentYear + i - 2);

  const months = [
    '1月', '2月', '3月', '4月', '5月', '6月',
    '7月', '8月', '9月', '10月', '11月', '12月'
  ];

  const daysInMonth = selectedDate.daysInMonth();
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  const weekDays = ['日', '一', '二', '三', '四', '五', '六'];

  const firstDayOfMonth = selectedDate.date(1).day();

  const handleDateSelect = () => {
    onConfirm(selectedDate.format('YYYY-MM-DD'));
  };

  const handleMonthChange = (monthIndex: number) => {
    setSelectedDate(selectedDate.month(monthIndex));
  };

  const handleYearChange = (year: number) => {
    setSelectedDate(selectedDate.year(year));
  };

  const handleDayPress = (day: number) => {
    setSelectedDate(selectedDate.date(day));
  };

  const canSelectDate = (day: number) => {
    const date = selectedDate.date(day);
    if (minDate && date.isBefore(dayjs(minDate))) return false;
    if (maxDate && date.isAfter(dayjs(maxDate))) return false;
    return true;
  };

  return (
    <Portal>
      <Modal
        visible={visible}
        transparent
        animationType="fade"
        onRequestClose={onDismiss}
      >
        <TouchableOpacity
          style={styles.backdrop}
          activeOpacity={1}
          onPress={onDismiss}
        >
          <View style={styles.modalContainer}>
            <TouchableOpacity activeOpacity={1} onPress={() => {}}>
              <View
                style={[
                  styles.modalContent,
                  { backgroundColor: theme.colors.surface },
                ]}
              >
                <View style={styles.header}>
                  <Text style={[styles.headerTitle, { color: theme.colors.onSurface }]}>
                    选择日期
                  </Text>
                  <TouchableOpacity onPress={onDismiss} style={styles.closeButton}>
                    <Icon
                      name="close"
                      size={24}
                      color={theme.colors.onSurfaceVariant}
                    />
                  </TouchableOpacity>
                </View>

                <View style={styles.yearSelector}>
                  <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    style={styles.yearScroll}
                    contentContainerStyle={styles.yearScrollContent}
                  >
                    {years.map((year) => (
                      <TouchableOpacity
                        key={year}
                        style={[
                          styles.yearItem,
                          selectedDate.year() === year && {
                            backgroundColor: theme.colors.primary,
                          },
                        ]}
                        onPress={() => handleYearChange(year)}
                      >
                        <Text
                          style={[
                            styles.yearText,
                            {
                              color:
                                selectedDate.year() === year
                                  ? theme.colors.onPrimary
                                  : theme.colors.onSurface,
                            },
                          ]}
                        >
                          {year}年
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>

                <View style={styles.monthSelector}>
                  <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    style={styles.monthScroll}
                    contentContainerStyle={styles.monthScrollContent}
                  >
                    {months.map((month, index) => (
                      <TouchableOpacity
                        key={month}
                        style={[
                          styles.monthItem,
                          selectedDate.month() === index && {
                            backgroundColor: theme.colors.primaryContainer,
                            borderColor: theme.colors.primary,
                          },
                        ]}
                        onPress={() => handleMonthChange(index)}
                      >
                        <Text
                          style={[
                            styles.monthText,
                            {
                              color:
                                selectedDate.month() === index
                                  ? theme.colors.primary
                                  : theme.colors.onSurface,
                            },
                          ]}
                        >
                          {month}
                        </Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>
                </View>

                <View style={styles.weekDayRow}>
                  {weekDays.map((day) => (
                    <View key={day} style={styles.weekDayItem}>
                      <Text
                        style={[
                          styles.weekDayText,
                          { color: theme.colors.onSurfaceVariant },
                        ]}
                      >
                        {day}
                      </Text>
                    </View>
                  ))}
                </View>

                <View style={styles.calendarGrid}>
                  {Array.from({ length: firstDayOfMonth }).map((_, index) => (
                    <View key={`empty-${index}`} style={styles.dayCell} />
                  ))}

                  {days.map((day) => {
                    const isToday = dayjs().isSame(selectedDate.date(day), 'day');
                    const isSelected = selectedDate.date() === day;
                    const canSelect = canSelectDate(day);

                    return (
                      <TouchableOpacity
                        key={day}
                        style={[
                          styles.dayCell,
                          isToday && styles.todayCell,
                          isSelected && {
                            backgroundColor: theme.colors.primary,
                            shadowColor: theme.colors.primary,
                          },
                        ]}
                        onPress={() => canSelect && handleDayPress(day)}
                        disabled={!canSelect}
                        activeOpacity={canSelect ? 0.7 : 1}
                      >
                        <Text
                          style={[
                            styles.dayText,
                            {
                              color: isSelected
                                ? theme.colors.onPrimary
                                : canSelect
                                ? theme.colors.onSurface
                                : theme.colors.onSurfaceVariant,
                              opacity: canSelect ? 1 : 0.3,
                            },
                          ]}
                        >
                          {day}
                        </Text>
                        {isSelected && (
                          <View
                            style={[
                              styles.selectedIndicator,
                              { backgroundColor: theme.colors.primary },
                            ]}
                          />
                        )}
                      </TouchableOpacity>
                    );
                  })}
                </View>

                <View style={styles.footer}>
                  <Text
                    style={[
                      styles.selectedDateText,
                      { color: theme.colors.onSurfaceVariant },
                    ]}
                  >
                    已选择: {selectedDate.format('YYYY年MM月DD日')}
                  </Text>
                  <TouchableOpacity
                    style={[
                      styles.confirmButton,
                      { backgroundColor: theme.colors.primary },
                    ]}
                    onPress={handleDateSelect}
                    activeOpacity={0.8}
                  >
                    <Text
                      style={[
                        styles.confirmButtonText,
                        { color: theme.colors.onPrimary },
                      ]}
                    >
                      确认
                    </Text>
                  </TouchableOpacity>
                </View>
              </View>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      </Modal>
    </Portal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    width: SCREEN_WIDTH - 32,
    maxWidth: 500,
  },
  modalContent: {
    borderRadius: 24,
    overflow: 'hidden',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.25,
        shadowRadius: 16,
      },
      android: {
        elevation: 8,
      },
    }),
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 0, 0, 0.05)',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    letterSpacing: -0.3,
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  yearSelector: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 0, 0, 0.05)',
  },
  yearScroll: {
    paddingHorizontal: 12,
  },
  yearScrollContent: {
    gap: 8,
  },
  yearItem: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  yearText: {
    fontSize: 14,
    fontWeight: '600',
  },
  monthSelector: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0, 0, 0, 0.05)',
  },
  monthScroll: {
    paddingHorizontal: 12,
  },
  monthScrollContent: {
    gap: 8,
  },
  monthItem: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  monthText: {
    fontSize: 14,
    fontWeight: '500',
  },
  weekDayRow: {
    flexDirection: 'row',
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: 'rgba(0, 0, 0, 0.02)',
  },
  weekDayItem: {
    flex: 1,
    alignItems: 'center',
  },
  weekDayText: {
    fontSize: 12,
    fontWeight: '600',
  },
  calendarGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 12,
  },
  dayCell: {
    width: `${100 / 7}%`,
    aspectRatio: 1,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  todayCell: {
    borderWidth: 2,
    borderColor: '#00BFA5',
    borderRadius: 12,
  },
  dayText: {
    fontSize: 15,
    fontWeight: '600',
  },
  selectedIndicator: {
    position: 'absolute',
    bottom: 4,
    width: 4,
    height: 4,
    borderRadius: 2,
  },
  footer: {
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: 'rgba(0, 0, 0, 0.05)',
    gap: 12,
  },
  selectedDateText: {
    fontSize: 13,
    fontWeight: '500',
    textAlign: 'center',
  },
  confirmButton: {
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.2,
        shadowRadius: 4,
      },
      android: {
        elevation: 2,
      },
    }),
  },
  confirmButtonText: {
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.3,
  },
});
