import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Card, Text, IconButton } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import type { Trip } from '../../types';
import { formatDate, calculateTotalDays } from '../../utils/dateUtils';

interface TripCardProps {
  trip: Trip;
  onPress: () => void;
  onDelete: () => void;
}

export default function TripCard({ trip, onPress, onDelete }: TripCardProps) {
  const duration = calculateTotalDays(trip.startDate, trip.endDate);
  const formattedDate = formatDate(trip.startDate);

  return (
    <TouchableOpacity onPress={onPress} style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.header}>
            <Text style={styles.title} numberOfLines={1}>{trip.title}</Text>
            <IconButton
              icon="delete-outline"
              size={20}
              onPress={onDelete}
              iconColor="#F44336"
            />
          </View>

          <View style={styles.destinationRow}>
            <Icon name="map-marker" size={16} color="#1976D2" />
            <Text style={styles.destination} numberOfLines={1}>
              {trip.destinations.join(' → ')}
            </Text>
          </View>

          <View style={styles.infoRow}>
            <View style={styles.infoItem}>
              <Icon name="calendar" size={14} color="#666" />
              <Text style={styles.infoText}>{formattedDate}</Text>
            </View>
            <View style={styles.infoItem}>
              <Icon name="clock-outline" size={14} color="#666" />
              <Text style={styles.infoText}>{duration}天</Text>
            </View>
            <View style={styles.infoItem}>
              <Icon name="currency-cny" size={14} color="#666" />
              <Text style={styles.infoText}>¥{trip.budget.total.toLocaleString()}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
    paddingHorizontal: 16,
  },
  card: {
    elevation: 2,
    borderRadius: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    flex: 1,
    marginRight: 8,
  },
  destinationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  destination: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
    flex: 1,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoText: {
    fontSize: 12,
    color: '#666',
    marginLeft: 4,
  },
});
