import { API_BASE_URL } from "./apiConfig";

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

export async function getPreferences(
  userId: string
): Promise<GuestPreferencesResponse> {
  const response = await fetch(
    `${API_BASE_URL}/settings/preferences/${userId}`
  );

  if (!response.ok) {
    throw new Error(`Failed to load preferences: ${response.status}`);
  }

  return response.json();
}

export async function savePreferences(
  userId: string,
  preferences: GuestPreferences
): Promise<GuestPreferencesResponse> {
  const response = await fetch(
    `${API_BASE_URL}/settings/preferences/${userId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(preferences),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to save preferences: ${response.status}`);
  }

  return response.json();
}
