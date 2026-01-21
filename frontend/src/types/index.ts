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

export interface DayBudget {
  total: number;
  transport: number;
  accommodation: number;
  food: number;
  activities: number;
}

export interface TripBudget {
  totalBudget: number;
  totalSpent: number;
  transportSpent: number;
  accommodationSpent: number;
  foodSpent: number;
  activitiesSpent: number;
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

export interface Attraction {
  id?: string;
  name: string;
  description?: string;
  location: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  category?: string;
  rating?: number;
  ticketPrice?: number;
  openingHours?: string;
  recommendedDuration?: number;
  imageUrl?: string;
  tags: string[];
  bestVisitTime?: string;
  tips?: string;
}

export interface Transport {
  id?: string;
  type: 'flight' | 'train' | 'bus' | 'car' | 'taxi' | 'metro' | 'walk';
  fromLocation: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  toLocation: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  departureTime?: string;
  arrivalTime?: string;
  duration?: number;
  price?: number;
  provider?: string;
  details?: Record<string, any>;
  bookingUrl?: string;
  notes?: string;
}

export interface Hotel {
  id?: string;
  name: string;
  location: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  starRating?: number;
  roomType?: string;
  pricePerNight?: number;
  rating?: number;
  amenities: string[];
  checkInTime?: string;
  checkOutTime?: string;
  imageUrl?: string;
  description?: string;
  contact?: {
    phone?: string;
    website?: string;
  };
  distanceToAttractions?: Array<{
    attractionId: string;
    attractionName: string;
    distance: number;
    unit: string;
  }>;
}

export interface Food {
  id?: string;
  name: string;
  type: string;
  cuisine?: string;
  location: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  rating?: number;
  priceRange?: string;
  avgPricePerPerson?: number;
  signatureDishes: string[];
  openingHours?: string;
  imageUrl?: string;
  description?: string;
  tags: string[];
  tips?: string;
  contact?: {
    phone?: string;
    website?: string;
  };
}

export interface Weather {
  location: string;
  date: string;
  temperatureMin: number;
  temperatureMax: number;
  weatherCondition: string;
  weatherIcon?: string;
  humidity?: number;
  windSpeed?: number;
  precipitation?: number;
  tips?: string;
}

export interface DetailedItineraryItem {
  id?: string;
  day: number;
  time: string;
  type: 'transport' | 'accommodation' | 'attraction' | 'food' | 'custom';
  title: string;
  description?: string;
  location?: {
    name: string;
    lat: number;
    lng: number;
    address: string;
  };
  cost?: number;
  duration?: number;
  notes?: string;
  data?: Record<string, any>;
}

export interface DayPlan {
  day: number;
  date: string;
  budget: DayBudget;
  attractions: Attraction[];
  transports: Transport[];
  hotel?: Hotel;
  foods: Food[];
  weather?: Weather;
  itinerary: DetailedItineraryItem[];
}

export interface DetailedTripPlan {
  id?: string;
  userId?: string;
  title: string;
  destinations: string[];
  startDate: string;
  endDate: string;
  travelers: number;
  budget: TripBudget;
  status: 'planning' | 'confirmed' | 'completed' | 'cancelled';

  days: DayPlan[];

  shareToken?: string;
  isPublic: boolean;
  createdAt?: string;
  updatedAt?: string;
}
