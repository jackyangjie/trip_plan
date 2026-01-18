import React from 'react';
import { View, StyleSheet, TouchableOpacity, Animated } from 'react-native';
import { Card, Text, IconButton, useTheme } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { Trip } from '../../types';
import { formatDate, calculateTotalDays } from '../../utils/dateUtils';

interface TripCardProps {
  trip: Trip;
  onPress: () => void;
  onDelete: () => void;
}

export default function TripCard({ trip, onPress, onDelete }: TripCardProps) {
  const theme = useTheme();
  const duration = calculateTotalDays(trip.startDate, trip.endDate);
  const formattedDate = formatDate(trip.startDate);

  const scaleAnim = React.useRef(new Animated.Value(1)).current;

  const handlePressIn = () => {
    Animated.spring(scaleAnim, {
      toValue: 0.98,
      useNativeDriver: true,
      speed: 50,
      bounciness: 4,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      useNativeDriver: true,
      speed: 50,
      bounciness: 4,
    }).start();
  };

  const tripTitle = trip.title || trip.destinations.join('、');
  const destinationText = trip.destinations.join(' → ');

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
      <TouchableOpacity
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.9}
        style={styles.container}
      >
        <Card style={[styles.card, { backgroundColor: '#FFFFFF' }]}>
          <Card.Content style={styles.cardContent}>
            <View style={styles.header}>
              <View style={styles.titleContainer}>
                <View style={styles.titleIconContainer}>
                  <Icon name="map-marker-path" size={20} color={theme.colors.primary} />
                </View>
                <Text style={styles.title} numberOfLines={2}>{tripTitle}</Text>
              </View>
              <IconButton
                icon="delete-outline"
                size={20}
                onPress={onDelete}
                iconColor="#DC2626"
                style={styles.deleteButton}
              />
            </View>

            <View style={styles.destinationRow}>
              <Icon name="map-marker-radius" size={18} color={theme.colors.tertiary} />
              <Text style={styles.destination} numberOfLines={1}>
                {destinationText}
              </Text>
            </View>

            <View style={styles.divider} />

            <View style={styles.infoRow}>
              <View style={styles.infoItem}>
                <View style={styles.infoIconContainer}>
                  <Icon name="calendar-start" size={16} color="#64748B" />
                </View>
                <Text style={styles.infoText}>{formattedDate}</Text>
              </View>
              <View style={[styles.infoItem, { borderLeftWidth: 1, borderLeftColor: '#E2E8F0', paddingLeft: 12 }]}>
                <View style={styles.infoIconContainer}>
                  <Icon name="clock-outline" size={16} color="#64748B" />
                </View>
                <Text style={styles.infoText}>{duration}天</Text>
              </View>
              <View style={[styles.infoItem, { borderLeftWidth: 1, borderLeftColor: '#E2E8F0', paddingLeft: 12 }]}>
                <View style={styles.infoIconContainer}>
                  <Icon name="wallet" size={16} color="#64748B" />
                </View>
                <Text style={styles.infoText}>¥{trip.budget.total.toLocaleString()}</Text>
              </View>
            </View>

            <View style={styles.statusBadge}>
              <View style={[styles.statusDot, { backgroundColor: theme.colors.secondary }]} />
              <Text style={styles.statusText}>
                {trip.status === 'planning' ? '规划中' :
                 trip.status === 'confirmed' ? '已确认' :
                 trip.status === 'completed' ? '已完成' : '已取消'}
              </Text>
            </View>
          </Card.Content>
        </Card>
      </TouchableOpacity>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
    paddingHorizontal: 0,
  },
  card: {
    elevation: 0,
    shadowColor: '#1A5490',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    borderRadius: 20,
  },
  cardContent: {
    padding: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginRight: 8,
  },
  titleIconContainer: {
    width: 32,
    height: 32,
    borderRadius: 10,
    backgroundColor: '#D3E4FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1A1A1A',
    flex: 1,
    letterSpacing: -0.3,
  },
  deleteButton: {
    margin: 0,
    backgroundColor: '#FEE2E2',
    width: 36,
    height: 36,
  },
  destinationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  destination: {
    fontSize: 14,
    fontWeight: '500',
    color: '#475569',
    marginLeft: 8,
    flex: 1,
  },
  divider: {
    height: 1,
    backgroundColor: '#E2E8F0',
    marginVertical: 12,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoIconContainer: {
    width: 28,
    height: 28,
    borderRadius: 8,
    backgroundColor: '#F8FAFC',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  infoText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#64748B',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 6,
    backgroundColor: '#FEF3C7',
    borderRadius: 20,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#92400E',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
});
