import { useState, type ChangeEvent, type FormEvent } from "react";

type GuestPreferencesData = {
  name: string;
  email: string;
  language: string;
  roomPreference: string;
  requests: string;
};

type GuestPreferencesErrors = Partial<{
  name: string;
  email: string;
  language: string;
  roomPreference: string;
  requests: string;
}>;

export default function GuestPreferencesForm() {
  const [formData, setFormData] = useState<GuestPreferencesData>({
    name: "",
    email: "",
    language: "",
    roomPreference: "",
    requests: "",
  });

  const [errors, setErrors] = useState<GuestPreferencesErrors>({});

  const validate = () => {
    const newErrors: GuestPreferencesErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = "Name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(formData.email)
    ) {
      newErrors.email = "Invalid email address";
    }

    if (!formData.language) {
      newErrors.language = "Language is required";
    }

    if (!formData.roomPreference) {
      newErrors.roomPreference = "Room preference is required";
    }

    if (formData.requests.length > 200) {
      newErrors.requests =
        "Special requests must not exceed 200 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (validate()) {
      console.log("Submitted:", formData);
      alert("Preferences saved successfully!");
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h2>Guest Preferences</h2>

      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
        />
        {errors.name && <p>{errors.name}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
        />
        {errors.email && <p>{errors.email}</p>}
      </div>

      <div>
        <label htmlFor="language">Preferred Language</label>
        <select
          id="language"
          name="language"
          value={formData.language}
          onChange={handleChange}
        >
          <option value="">Select a language</option>
          <option value="English">English</option>
          <option value="French">French</option>
          <option value="Spanish">Spanish</option>
        </select>
        {errors.language && <p>{errors.language}</p>}
      </div>

      <div>
        <label htmlFor="roomPreference">Room Preference</label>
        <select
          id="roomPreference"
          name="roomPreference"
          value={formData.roomPreference}
          onChange={handleChange}
        >
          <option value="">Select a room type</option>
          <option value="Single">Single</option>
          <option value="Double">Double</option>
          <option value="Suite">Suite</option>
        </select>
        {errors.roomPreference && <p>{errors.roomPreference}</p>}
      </div>

      <div>
        <label htmlFor="requests">Special Requests</label>
        <textarea
          id="requests"
          name="requests"
          rows={4}
          maxLength={200}
          value={formData.requests}
          onChange={handleChange}
        />
        <small>{formData.requests.length}/200</small>
        {errors.requests && <p>{errors.requests}</p>}
      </div>

      <button type="submit">Save Preferences</button>
    </form>
  );
}
