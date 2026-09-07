import { API_BASE_URL } from "./apiConfig";

const AUTH_TOKEN_KEY = "ai_concierge_access_token";
const AUTH_USER_KEY = "ai_concierge_user";

export type AuthUser = {
  user_id: string;
  name: string;
  email: string;
  role: "guest" | "staff";
};

type LoginResponse = {
  access_token: string;
  token_type: string;
  user_id: string;
  role: "guest" | "staff";
};

export async function login(
  email: string,
  password: string
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!response.ok) {
    throw new Error(
      response.status === 401
        ? "Invalid email or password."
        : `Login failed: ${response.status}`
    );
  }

  const data: LoginResponse = await response.json();

  const user: AuthUser = {
    user_id: data.user_id,
    name: "",
    email,
    role: data.role,
  };

  localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));

  return user;
}

export async function signup(
  name: string,
  email: string,
  password: string
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name,
      email,
      password,
    }),
  });

  if (!response.ok) {
    if (response.status === 409) {
      throw new Error("An account with this email already exists.");
    }

    if (response.status === 422) {
      throw new Error("Please check your name, email, and password.");
    }

    throw new Error(`Sign up failed: ${response.status}`);
  }

  const data: LoginResponse = await response.json();

  const user: AuthUser = {
    user_id: data.user_id,
    name,
    email,
    role: data.role,
  };

  localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));

  return user;
}

export async function getMe(): Promise<AuthUser> {
  const token = getAccessToken();

  if (!token) {
    throw new Error("Not authenticated.");
  }

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 401) {
      logout();
    }

    throw new Error(`Unable to load account: ${response.status}`);
  }

  const user: AuthUser = await response.json();

  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user));

  return user;
}

export function logout(): void {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_USER_KEY);
}

export function getAccessToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

export function getCurrentUser(): AuthUser | null {
  const stored = localStorage.getItem(AUTH_USER_KEY);

  if (!stored) {
    return null;
  }

  try {
    return JSON.parse(stored) as AuthUser;
  } catch {
    logout();
    return null;
  }
}

export function getAuthHeaders(): Record<string, string> {
  const token = getAccessToken();

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

export function isAuthenticated(): boolean {
  return Boolean(getAccessToken());
}

export async function forgotPassword(
  email: string
): Promise<string> {
  const response = await fetch(
    `${API_BASE_URL}/auth/forgot-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
      }),
    }
  );

  if (!response.ok) {
    if (response.status === 422) {
      throw new Error("Please enter a valid email address.");
    }

    throw new Error(
      `Unable to request password reset: ${response.status}`
    );
  }

  const data: { message: string } = await response.json();

  return data.message;
}

export async function resetPassword(
  token: string,
  newPassword: string
): Promise<string> {
  const response = await fetch(
    `${API_BASE_URL}/auth/reset-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
        new_password: newPassword,
      }),
    }
  );

  if (!response.ok) {
    if (response.status === 400) {
      throw new Error(
        "This reset link is invalid or has expired."
      );
    }

    if (response.status === 422) {
      throw new Error(
        "Please check your new password."
      );
    }

    throw new Error(
      `Unable to reset password: ${response.status}`
    );
  }

  const data: { message: string } = await response.json();

  return data.message;
}