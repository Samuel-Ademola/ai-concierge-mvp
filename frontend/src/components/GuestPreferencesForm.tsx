import {
  useEffect,
  useState,
  type ChangeEvent,
  type FormEvent,
} from "react";

import {
  getGuestPreferences,
  saveGuestPreferences,
  type GuestPreferences,
} from "../services/guestPreferencesApi";

import { useAuth } from "../context/AuthContext";
import "./GuestPreferencesForm.css";

type GuestPreferencesErrors = Partial<
  Record<keyof GuestPreferences, string>
>;

type GuestPreferencesFormProps = {
  initialData?: GuestPreferences;
};

const EMPTY_FORM: GuestPreferences = {
  name: "",
  email: "",
  language: "",
  roomPreference: "",
  requests: "",
};

export default function GuestPreferencesForm({
  initialData,
}: GuestPreferencesFormProps) {
  const { user } = useAuth();
  const userId = user?.user_id ?? "";

  const [formData, setFormData] = useState<GuestPreferences>(
    initialData ?? EMPTY_FORM
  );

  const [errors, setErrors] = useState<GuestPreferencesErrors>({});
  const [isLoading, setIsLoading] = useState(!initialData);
  const [isSaving, setIsSaving] = useState(false);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState<"success" | "error" | "">("");
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
      setIsLoading(false);
      return;
    }

    if (!userId) {
      setLoadError("We couldn't identify your account.");
      setIsLoading(false);
      return;
    }

    async function loadPreferences() {
      try {
        const preferences = await getGuestPreferences(userId);

        setFormData({
          name: preferences.name,
          email: preferences.email,
          language: preferences.language,
          roomPreference: preferences.roomPreference,
          requests: preferences.requests,
        });
      } catch {
        setLoadError("We couldn't load your preferences.");
      } finally {
        setIsLoading(false);
      }
    }

    loadPreferences();
  }, [initialData, userId]);

  const validate = () => {
    const newErrors: GuestPreferencesErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = "Name is required.";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required.";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(
        formData.email.trim()
      )
    ) {
      newErrors.email = "Enter a valid email address.";
    }

    if (!formData.language) {
      newErrors.language = "Please select a language.";
    }

    if (!formData.roomPreference) {
      newErrors.roomPreference = "Please select a room preference.";
    }

    if (formData.requests.length > 200) {
      newErrors.requests =
        "Special requests must not exceed 200 characters.";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (
    event: ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));

    setStatus("");
    setStatusType("");

    setErrors((previous) => ({
      ...previous,
      [name]: undefined,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!validate() || isSaving || !userId) {
      return;
    }

    setIsSaving(true);
    setStatus("");
    setStatusType("");

    try {
      const saved = await saveGuestPreferences(
        userId,
        {
          ...formData,
          name: formData.name.trim(),
          email: formData.email.trim(),
          requests: formData.requests.trim(),
        }
      );

      setFormData({
        name: saved.name,
        email: saved.email,
        language: saved.language,
        roomPreference: saved.roomPreference,
        requests: saved.requests,
      });

      setStatus("Your preferences have been saved.");
      setStatusType("success");

      window.dispatchEvent(new Event("guest-preferences-updated"));
    } catch {
      setStatus(
        "We couldn't save your preferences. Please try again."
      );
      setStatusType("error");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="preferences-form-state">
        <div className="preferences-state__spinner" />
        <p>Loading your preferences...</p>
      </div>
    );
  }

  return (
    <form
      className="preferences-form"
      onSubmit={handleSubmit}
      noValidate
    >
      <div className="preferences-form__header">
        <span className="preferences-form__section-label">
          Personal details
        </span>

        <h3>Guest Preferences</h3>

        <p>
          These details help the concierge personalize your experience.
        </p>
      </div>

      {loadError && (
        <div className="preferences-alert preferences-alert--error">
          {loadError}
        </div>
      )}

      <div className="preferences-form__grid">
        <div className="preferences-field">
          <label htmlFor="name">Name</label>

          <input
            id="name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleChange}
            autoComplete="name"
            aria-invalid={Boolean(errors.name)}
          />

          {errors.name && (
            <span className="preferences-field__error">
              {errors.name}
            </span>
          )}
        </div>

        <div className="preferences-field">
          <label htmlFor="email">Email</label>

          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            autoComplete="email"
            aria-invalid={Boolean(errors.email)}
          />

          {errors.email && (
            <span className="preferences-field__error">
              {errors.email}
            </span>
          )}
        </div>

        <div className="preferences-field">
          <label htmlFor="language">Preferred language</label>

          <select
            id="language"
            name="language"
            value={formData.language}
            onChange={handleChange}
            aria-invalid={Boolean(errors.language)}
          >
            <option value="">Select a language</option>
            <option value="English">English</option>
            <option value="French">French</option>
            <option value="Spanish">Spanish</option>
          </select>

          {errors.language && (
            <span className="preferences-field__error">
              {errors.language}
            </span>
          )}
        </div>

        <div className="preferences-field">
          <label htmlFor="roomPreference">Room preference</label>

          <select
            id="roomPreference"
            name="roomPreference"
            value={formData.roomPreference}
            onChange={handleChange}
            aria-invalid={Boolean(errors.roomPreference)}
          >
            <option value="">Select a room type</option>
            <option value="Single">Single</option>
            <option value="Double">Double</option>
            <option value="Suite">Suite</option>
          </select>

          {errors.roomPreference && (
            <span className="preferences-field__error">
              {errors.roomPreference}
            </span>
          )}
        </div>
      </div>

      <div className="preferences-field preferences-field--full">
        <div className="preferences-field__label-row">
          <label htmlFor="requests">Special requests</label>

          <span>{formData.requests.length}/200</span>
        </div>

        <textarea
          id="requests"
          name="requests"
          rows={5}
          maxLength={200}
          value={formData.requests}
          onChange={handleChange}
          placeholder="Anything you'd like the hotel or concierge to know?"
          aria-invalid={Boolean(errors.requests)}
        />

        {errors.requests && (
          <span className="preferences-field__error">
            {errors.requests}
          </span>
        )}
      </div>

      <div className="preferences-form__footer">
        <p className="preferences-form__note">
          Your preferences are saved to your guest profile.
        </p>

        <button
          type="submit"
          className="preferences-save-button"
          disabled={isSaving}
        >
          {isSaving ? "Saving..." : "Save preferences"}
        </button>
      </div>

      {status && (
        <div
          className={`preferences-alert ${
            statusType === "success"
              ? "preferences-alert--success"
              : "preferences-alert--error"
          }`}
        >
          {status}
        </div>
      )}
    </form>
  );
}