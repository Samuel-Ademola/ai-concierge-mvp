import { API_BASE_URL } from "./apiConfig";
import { getAuthHeaders } from "./authApi";

export type GuestRequest = {
  id: number;
  request_id: string;
  user_id: string;
  request_type: string;
  details: string;
  status: string;
  created_at: string;
};

export async function getGuestRequests(
  userId: string
): Promise<GuestRequest[]> {
  const response = await fetch(
    `${API_BASE_URL}/requests/${userId}`,
    {
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load requests: ${response.status}`
    );
  }

  return response.json();
}
