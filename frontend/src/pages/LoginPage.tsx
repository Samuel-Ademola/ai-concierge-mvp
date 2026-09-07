import { useState, type FormEvent } from "react";
import { login, signup } from "../services/authApi";
import "./LoginPage.css";

export default function LoginPage() {
  const [isSignup, setIsSignup] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  function switchMode() {
    setIsSignup((current) => !current);
    setError("");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      if (isSignup) {
        await signup(name, email, password);
      } else {
        await login(email, password);
      }

      window.location.href = "/";
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : isSignup
            ? "Unable to create your account."
            : "Unable to sign in."
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-brand">
          <div className="login-logo">AC</div>

          <div>
            <h1>AI Concierge</h1>
            <p>Your stay, simplified.</p>
          </div>
        </div>

        <div className="login-heading">
          <p className="login-eyebrow">GUEST ACCESS</p>

          <h2>
            {isSignup ? "Create your account" : "Welcome back"}
          </h2>

          <p>
            {isSignup
              ? "Create an account to manage your stay and speak with the concierge."
              : "Sign in to manage your stay and speak with the concierge."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {isSignup && (
            <label>
              Full name
              <input
                type="text"
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Enter your full name"
                autoComplete="name"
                required
              />
            </label>
          )}

          <label>
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="Enter your email"
              autoComplete="email"
              required
            />
          </label>

          <label>
            Password
            <div className="password-field">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder={
                  isSignup
                    ? "Create a password (8+ characters)"
                    : "Enter your password"
                }
                autoComplete={
                  isSignup ? "new-password" : "current-password"
                }
                minLength={isSignup ? 8 : undefined}
                required
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword((current) => !current)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
          </label>

          {error && (
            <p className="login-error" role="alert">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="login-submit"
            disabled={isLoading}
          >
            {isLoading
              ? isSignup
                ? "Creating account..."
                : "Signing in..."
              : isSignup
                ? "Create account"
                : "Sign in"}
          </button>
        </form>

        <div className="login-switch">
          <span>
            {isSignup
              ? "Already have an account?"
              : "Don't have an account?"}
          </span>

          <button
            type="button"
            className="login-switch-button"
            onClick={switchMode}
          >
            {isSignup ? "Sign in" : "Create an account"}
          </button>
        </div>
      </section>
    </main>
  );
}




