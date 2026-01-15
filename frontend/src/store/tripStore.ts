import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Trip } from '../types';

interface TripState {
  trips: Trip[];
  currentTrip: Trip | null;
  setTrips: (trips: Trip[]) => void;
  setCurrentTrip: (trip: Trip | null) => void;
  addTrip: (trip: Trip) => void;
  updateTrip: (id: string, updates: Partial<Trip>) => void;
  deleteTrip: (id: string) => void;
}

export const useTripStore = create<TripState>()(
  persist(
    (set) => ({
      trips: [],
      currentTrip: null,
      setTrips: (trips) => set({ trips }),
      setCurrentTrip: (trip) => set({ currentTrip: trip }),
      addTrip: (trip) => set((state) => ({ trips: [...state.trips, trip] })),
      updateTrip: (id, updates) =>
        set((state) => ({
          trips: state.trips.map((trip) =>
            trip.id === id ? { ...trip, ...updates } : trip
          ),
        })),
      deleteTrip: (id) =>
        set((state) => ({
          trips: state.trips.filter((trip) => trip.id !== id),
        })),
    }),
    {
      name: 'travel-planner-trip-storage',
      storage: {
        getItem: (name) => AsyncStorage.getItem(name).then((data) => data && JSON.parse(data)),
        setItem: (name, value) => AsyncStorage.setItem(name, JSON.stringify(value)),
        removeItem: (name) => AsyncStorage.removeItem(name),
      },
    }
  )
);
