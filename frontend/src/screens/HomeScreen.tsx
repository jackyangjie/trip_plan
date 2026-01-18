import React, { useEffect, useState, useRef } from 'react';
import { View, StyleSheet, FlatList, RefreshControl, Animated, Dimensions } from 'react-native';
import { FAB, Text, useTheme, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { useTripStore } from '../stores';
import TripCard from './components/TripCard';
import EmptyState from './components/EmptyState';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

const { width } = Dimensions.get('window');

export default function HomeScreen() {
  const navigation = useNavigation<any>();
  const theme = useTheme();
  const { trips, loadTrips, deleteTrip } = useTripStore();
  const [refreshing, setRefreshing] = useState(false);

  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    loadTrips();

    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
      }),
    ]).start();
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
    navigation.navigate('planning', { mode: 'create' });
  };

  const sortedTrips = [...trips].sort((a, b) =>
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );

  const totalDays = trips.reduce((total, trip) => {
    const startDate = new Date(trip.startDate);
    const endDate = new Date(trip.endDate);
    const days = Math.ceil(
      (endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)
    );
    return total + days;
  }, 0);

  const renderHeader = () => (
    <Animated.View
      style={[
        styles.heroSection,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={styles.heroGradient}>
        <View style={styles.headerContent}>
          <View style={styles.headerTop}>
            <View>
              <Text style={styles.greeting}>你好，旅行者</Text>
              <Text style={styles.subtitle}>探索世界，发现美好</Text>
            </View>
            <IconButton
              icon="bell-outline"
              size={24}
              iconColor={theme.colors.primary}
              style={styles.notificationIcon}
            />
          </View>

          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <View style={styles.statIcon}>
                <Icon name="map-marker" size={20} color={theme.colors.primary} />
              </View>
              <View style={styles.statText}>
                <Text style={styles.statValue}>{trips.length}</Text>
                <Text style={styles.statLabel}>行程</Text>
              </View>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <View style={[styles.statIcon, { backgroundColor: theme.colors.secondaryContainer }]}>
                <Icon name="airplane" size={20} color={theme.colors.secondary} />
              </View>
              <View style={styles.statText}>
                <Text style={styles.statValue}>{totalDays}</Text>
                <Text style={styles.statLabel}>天数</Text>
              </View>
            </View>
          </View>
        </View>
      </View>
    </Animated.View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={sortedTrips}
        keyExtractor={(item) => item.id}
        ListHeaderComponent={renderHeader}
        ListEmptyComponent={
          <EmptyState
            icon="map-marker-path"
            title="还没有行程"
            description="开始规划您的第一次旅行吧"
            actionLabel="开始规划"
            onAction={handleAddTrip}
          />
        }
        renderItem={({ item, index }) => {
          const translateY = slideAnim.interpolate({
            inputRange: [0, 1] as [number, number],
            outputRange: [(index * 15) as number, 0] as [number, number],
          });

          return (
            <Animated.View
              style={{
                opacity: fadeAnim,
                transform: [{ translateY }],
              }}
            >
              <TripCard
                trip={item}
                onPress={() => handleTripPress(item.id)}
                onDelete={() => handleDeleteTrip(item.id)}
              />
            </Animated.View>
          );
        }}
        contentContainerStyle={[
          styles.listContent,
          trips.length === 0 && styles.emptyContent,
        ]}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            colors={[theme.colors.primary]}
            tintColor={theme.colors.primary}
          />
        }
        showsVerticalScrollIndicator={false}
      />

      <FAB
        icon="plus"
        label="新建行程"
        style={[styles.fab, { backgroundColor: theme.colors.primary }]}
        onPress={handleAddTrip}
        color={theme.colors.onPrimary}
        rippleColor="rgba(255, 255, 255, 0.3)"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FAFBFC',
  },
  heroSection: {
    paddingBottom: 20,
  },
  heroGradient: {
    backgroundColor: '#FFFFFF',
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
    shadowColor: '#1A5490',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.08,
    shadowRadius: 16,
    elevation: 4,
  },
  headerContent: {
    padding: 24,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 24,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '800',
    color: '#1A1A1A',
    letterSpacing: -0.5,
    lineHeight: 36,
  },
  subtitle: {
    fontSize: 15,
    fontWeight: '400',
    color: '#475569',
    marginTop: 4,
  },
  notificationIcon: {
    margin: 0,
    backgroundColor: '#F0F4F8',
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    backgroundColor: '#F8FAFC',
    borderRadius: 16,
    padding: 16,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  statIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: '#D3E4FF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statText: {
    flexDirection: 'column',
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: '#1A1A1A',
    lineHeight: 28,
  },
  statLabel: {
    fontSize: 13,
    fontWeight: '500',
    color: '#64748B',
    marginTop: 2,
  },
  statDivider: {
    width: 1,
    height: 40,
    backgroundColor: '#E2E8F0',
  },
  listContent: {
    paddingTop: 20,
    paddingHorizontal: 16,
    paddingBottom: 100,
  },
  emptyContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingVertical: 0,
  },
  fab: {
    position: 'absolute',
    margin: 20,
    right: 0,
    bottom: 20,
    borderRadius: 16,
  },
});
