import { API_BASE_URL } from "./apiConfig";
import { getAuthHeaders } from "./authApi";

export type GuestPreferences = {
  name: string;
  email: string;
  language: string;
  roomPreference: string;
  requests: string;
};

export type GuestPreferencesResponse = GuestPreferences & {
  id: number;
};

export async function saveGuestPreferences(
  userId: string,
  preferences: GuestPreferences
): Promise<GuestPreferencesResponse> {
  const response = await fetch(
    `${API_BASE_URL}/settings/preferences/${userId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify(preferences),
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to save preferences: ${response.status}`
    );
  }

  return response.json();
}

export async function getGuestPreferences(
  userId: string
): Promise<GuestPreferencesResponse> {
  const response = await fetch(
    `${API_BASE_URL}/settings/preferences/${userId}`,
    {
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load preferences: ${response.status}`
    );
  }

  return response.json();
}
