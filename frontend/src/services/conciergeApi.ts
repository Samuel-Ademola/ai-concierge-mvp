import { API_BASE_URL } from "./apiConfig";
import { getAuthHeaders } from "./authApi";

export class ApiError extends Error {
  status?: number;
  kind: "network" | "http";

  constructor(
    message: string,
    kind: "network" | "http",
    status?: number
  ) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.status = status;
  }
}

export type ChatRequest = {
  message: string;
  user_id?: string;
};

export type Recommendation = {
  id: string;
  name: string;
  cuisine: string;
  type: string;
  location: string;
  price_range: string;
  rating: number;
};

export type ChatResponse = {
  user_id: string;
  message: string;
  intent: string;
  response: string;
  recommendations?: Recommendation[];
};

export type GuestRequest = {
  id: number;
  request_id: string;
  user_id: string;
  request_type: string;
  details: string;
  status: string;
  created_at: string;
};

async function parseError(
  response: Response,
  fallback: string
): Promise<ApiError> {
  return new ApiError(
    fallback,
    "http",
    response.status
  );
}

export async function sendMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw await parseError(
        response,
        "The concierge service returned an error."
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      "Unable to reach the concierge service.",
      "network"
    );
  }
}

export async function resetConversation(
  userId: string
): Promise<void> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/chat/reset`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          user_id: userId,
          message: "",
        }),
      }
    );

    if (!response.ok) {
      throw await parseError(
        response,
        "Could not reset the conversation."
      );
    }
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      "Unable to reach the concierge service.",
      "network"
    );
  }
}

export async function createGuestRequest(
  userId: string,
  requestType: string,
  details: string
): Promise<GuestRequest> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/requests`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          user_id: userId,
          request_type: requestType,
          details,
        }),
      }
    );

    if (!response.ok) {
      throw await parseError(
        response,
        "The request service returned an error."
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      "Unable to reach the request service.",
      "network"
    );
  }
}

export async function getGuestRequests(
  userId: string
): Promise<GuestRequest[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/requests/${userId}`,
      {
        headers: getAuthHeaders(),
      }
    );

    if (!response.ok) {
      throw await parseError(
        response,
        "Could not load guest requests."
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    throw new ApiError(
      "Unable to reach the request service.",
      "network"
    );
  }
}
