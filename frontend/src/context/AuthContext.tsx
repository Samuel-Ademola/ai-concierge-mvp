import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getAccessToken,
  getCurrentUser,
  logout,
  type AuthUser,
} from "../services/authApi";

import { API_BASE_URL } from "../services/apiConfig";

type AuthContextValue = {
  user: AuthUser | null;
  isLoading: boolean;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(
  undefined
);

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(
    getCurrentUser()
  );

  const [isLoading, setIsLoading] = useState(
    Boolean(getAccessToken())
  );

  useEffect(() => {
    const token = getAccessToken();

    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    async function loadCurrentUser() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Authentication failed");
        }

        const data = await response.json();

        const authenticatedUser: AuthUser = {
          user_id: String(data.user_id),
          name: data.name,
          email: data.email,
          role: data.role,
        };

        localStorage.setItem(
          "ai_concierge_user",
          JSON.stringify(authenticatedUser)
        );

        setUser(authenticatedUser);
      } catch {
        logout();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }

    loadCurrentUser();
  }, []);

  const signOut = () => {
    logout();
    setUser(null);
    window.location.href = "/";
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
}
