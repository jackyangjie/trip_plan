import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware/async-storage';
import AsyncStorage from '@react-native-async-storage/async-storage';
import type { Trip } from '../types';
import * as storageService from '../services/storageService';

interface TripState {
  trips: Trip[];
  currentTrip: Trip | null;
  isLoading: boolean;

  loadTrips: () => Promise<void>;
  addTrip: (trip: Trip) => Promise<void>;
  updateTrip: (trip: Trip) => Promise<void>;
  deleteTrip: (tripId: string) => Promise<void>;
  setCurrentTrip: (trip: Trip | null) => void;
}

export const useTripStore = create<TripState>()(
  persist(
    (set, get) => ({
      trips: [],
      currentTrip: null,
      isLoading: false,

      loadTrips: async () => {
        set({ isLoading: true });
        try {
          const trips = await storageService.getLocalTrips();
          set({ trips, isLoading: false });
        } catch (error) {
          console.error('Error loading trips:', error);
          set({ isLoading: false });
        }
      },

      addTrip: async (trip: Trip) => {
        try {
          await storageService.addLocalTrip(trip);
          set((state) => ({ trips: [...state.trips, trip] }));
        } catch (error) {
          console.error('Error adding trip:', error);
          throw error;
        }
      },

      updateTrip: async (trip: Trip) => {
        try {
          await storageService.updateLocalTrip(trip);
          set((state) => ({
            trips: state.trips.map((t) => (t.id === trip.id ? trip : t)),
            currentTrip: state.currentTrip?.id === trip.id ? trip : state.currentTrip,
          }));
        } catch (error) {
          console.error('Error updating trip:', error);
          throw error;
        }
      },

      deleteTrip: async (tripId: string) => {
        try {
          await storageService.deleteLocalTrip(tripId);
          set((state) => ({
            trips: state.trips.filter((t) => t.id !== tripId),
            currentTrip: state.currentTrip?.id === tripId ? null : state.currentTrip,
          }));
        } catch (error) {
          console.error('Error deleting trip:', error);
          throw error;
        }
      },

      setCurrentTrip: (trip: Trip | null) => {
        set({ currentTrip: trip });
      },
    }),
    {
      name: 'trip-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ trips: state.trips }),
    }
  )
);
