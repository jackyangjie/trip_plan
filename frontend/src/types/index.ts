export interface User {
  id: string;
  email: string;
  nickname: string;
  preferences: UserPreferences;
}

export interface UserPreferences {
  foodTypes: string[];
  attractionTypes: string[];
  budgetRange: {
    min: number;
    max: number;
  };
}

export interface TripBudget {
  total: number;
  transport: number;
  accommodation: number;
  food: number;
  activities: number;
}

export interface TripItineraryItem {
  id: string;
  day: number;
  time: string;
  type: 'transport' | 'accommodation' | 'attraction' | 'food' | 'custom';
  title: string;
  description?: string;
  location?: {
    name: string;
    lat: number;
    lng: number;
  };
  cost?: number;
  duration?: number;
  notes?: string;
}

export interface Trip {
  id: string;
  userId?: string;
  title: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  budget: TripBudget;
  status: 'planning' | 'confirmed' | 'completed' | 'cancelled';
  itinerary: TripItineraryItem[];
  shareToken?: string;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
  isLocal: boolean;
}
