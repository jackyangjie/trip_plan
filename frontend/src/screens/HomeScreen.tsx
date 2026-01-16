import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { FAB, Text, useTheme } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { useTripStore } from '../../stores';
import { useAuthStore } from '../../stores';
import TripCard from './components/TripCard';
import EmptyState from './components/EmptyState';

export default function HomeScreen() {
  const navigation = useNavigation<any>();
  const theme = useTheme();
  const { trips, loadTrips, deleteTrip } = useTripStore();
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadTrips();
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadTrips();
    setRefreshing(false);
  };

  const handleDeleteTrip = async (tripId: string) => {
    await deleteTrip(tripId);
  };

  const handleTripPress = (tripId: string) => {
    navigation.navigate('TripDetail', { tripId });
  };

  const handleAddTrip = () => {
    navigation.navigate('Planning', { mode: 'create' });
  };

  const sortedTrips = [...trips].sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>我的行程</Text>
      </View>

      {trips.length === 0 ? (
        <EmptyState
          icon="map-marker-path"
          title="还没有行程"
          description="开始规划您的第一次旅行吧"
          actionLabel="开始规划"
          onAction={handleAddTrip}
        />
      ) : (
        <FlatList
          data={sortedTrips}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <TripCard
              trip={item}
              onPress={() => handleTripPress(item.id)}
              onDelete={() => handleDeleteTrip(item.id)}
            />
          )}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />
          }
        />
      )}

      <FAB
        icon="plus"
        label="新建行程"
        style={styles.fab}
        onPress={handleAddTrip}
        theme={{ colors: { primary: theme.colors.primary } }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
  },
  listContent: {
    paddingVertical: 16,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 16,
  },
});
