import { supabase } from './supabaseClient';

export async function login(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    throw new Error(error.message);
  }

  return data;
}

export async function register(email: string, password: string, nickname?: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        nickname: nickname || email.split('@')[0],
      },
    },
  });

  if (error) {
    throw new Error(error.message);
  }

  return data;
}

export async function logout() {
  const { error } = await supabase.auth.signOut();
  if (error) {
    throw new Error(error.message);
  }
}

export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) {
    throw new Error(error.message);
  }
  return user;
}

export async function syncLocalTrips(trips: any[]) {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return;

  for (const trip of trips) {
    if (trip.isLocal) {
      const { error } = await supabase
        .from('trips')
        .insert({
          user_id: user.id,
          title: trip.title,
          destinations: trip.destinations,
          start_date: trip.startDate,
          end_date: trip.endDate,
          budget: trip.budget,
          status: trip.status,
          itinerary: trip.itinerary,
          share_token: trip.shareToken,
          is_public: trip.isPublic,
        });

      if (!error) {
        trip.isLocal = false;
      }
    }
  }
}
