import { useEffect, useState } from "react";

import GuestPreferencesForm from "../components/GuestPreferencesForm";

import {
  getGuestPreferences,
  type GuestPreferences,
} from "../services/guestPreferencesApi";

import { useAuth } from "../context/AuthContext";

import "./PreferencesPage.css";

export default function PreferencesPage() {
  const { user } = useAuth();
  const userId = user?.user_id ?? "";

  const [preferences, setPreferences] =
    useState<GuestPreferences | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!userId) {
      setError(
        "We couldn't identify your account. Please sign in again."
      );
      setIsLoading(false);
      return;
    }

    async function loadPreferences() {
      try {
        const data = await getGuestPreferences(userId);

        setPreferences({
          name: data.name,
          email: data.email,
          language: data.language,
          roomPreference: data.roomPreference,
          requests: data.requests,
        });
      } catch {
        setError(
          "We couldn't load your preferences. Please try again."
        );
      } finally {
        setIsLoading(false);
      }
    }

    loadPreferences();
  }, [userId]);

  if (isLoading) {
    return (
      <section className="preferences-page">
        <div className="preferences-state">
          <div className="preferences-state__spinner" />
          <p>Loading your preferences...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="preferences-page">
        <div className="preferences-state preferences-state--error">
          <strong>Unable to load preferences</strong>
          <p>{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="preferences-page">
      <header className="preferences-page__intro">
        <p className="preferences-page__eyebrow">
          Guest profile
        </p>

        <h2>Your preferences</h2>

        <p className="preferences-page__description">
          Keep your preferences up to date so the concierge
          can serve you better throughout your stay.
        </p>
      </header>

      <GuestPreferencesForm
        initialData={preferences ?? undefined}
      />
    </section>
  );
}