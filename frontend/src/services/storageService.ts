import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Trip } from '../types';

const TRIPS_STORAGE_KEY = '@travel_planner_trips';

export async function getLocalTrips(): Promise<Trip[]> {
  try {
    const tripsJson = await AsyncStorage.getItem(TRIPS_STORAGE_KEY);
    return tripsJson ? JSON.parse(tripsJson) : [];
  } catch (error) {
    console.error('Error loading local trips:', error);
    return [];
  }
}

export async function addLocalTrip(trip: Trip): Promise<void> {
  try {
    const trips = await getLocalTrips();
    trips.push(trip);
    await AsyncStorage.setItem(TRIPS_STORAGE_KEY, JSON.stringify(trips));
  } catch (error) {
    console.error('Error adding local trip:', error);
    throw error;
  }
}

export async function updateLocalTrip(trip: Trip): Promise<void> {
  try {
    const trips = await getLocalTrips();
    const index = trips.findIndex((t) => t.id === trip.id);
    if (index !== -1) {
      trips[index] = trip;
      await AsyncStorage.setItem(TRIPS_STORAGE_KEY, JSON.stringify(trips));
    }
  } catch (error) {
    console.error('Error updating local trip:', error);
    throw error;
  }
}

export async function deleteLocalTrip(tripId: string): Promise<void> {
  try {
    const trips = await getLocalTrips();
    const filtered = trips.filter((t) => t.id !== tripId);
    await AsyncStorage.setItem(TRIPS_STORAGE_KEY, JSON.stringify(filtered));
  } catch (error) {
    console.error('Error deleting local trip:', error);
    throw error;
  }
}

export async function clearLocalTrips(): Promise<void> {
  try {
    await AsyncStorage.removeItem(TRIPS_STORAGE_KEY);
  } catch (error) {
    console.error('Error clearing local trips:', error);
    throw error;
  }
}
