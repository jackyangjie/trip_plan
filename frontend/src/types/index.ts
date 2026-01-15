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

export interface Trip {
  id: string;
  userId?: string;
  title: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  budget: Budget;
  status: 'planning' | 'confirmed' | 'completed' | 'cancelled';
  itinerary: Itinerary;
  shareToken?: string;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Budget {
  total: number;
  transport: number;
  accommodation: number;
  food: number;
  activities: number;
}

export interface Itinerary {
  days: Day[];
}

export interface Day {
  date: string;
  activities: Activity[];
}

export interface Activity {
  id: string;
  type: 'transport' | 'accommodation' | 'food' | 'attraction';
  title: string;
  location?: {
    lat: number;
    lng: number;
    address: string;
  };
  startTime?: string;
  endTime?: string;
  cost?: number;
  notes?: string;
}
