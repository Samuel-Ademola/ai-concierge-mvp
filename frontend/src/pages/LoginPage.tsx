import { useState, type FormEvent } from "react";
import { forgotPassword, login, resetPassword, signup } from "../services/authApi";
import "./LoginPage.css";

export default function LoginPage() {
  const [isSignup, setIsSignup] = useState(false);
  const [view, setView] = useState<"auth" | "forgot" | "reset">("auth");
  const [resetToken, setResetToken] = useState("");
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

  async function handleForgotPassword(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const message = await forgotPassword(email);

      const tokenMatch = message.match(
        /^Password reset token:\s*(.+)$/
      );

      if (tokenMatch) {
        setResetToken(tokenMatch[1]);
      }

      setView("reset");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to request a password reset."
      );
    } finally {
      setIsLoading(false);
    }
  }
  async function handleResetPassword(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await resetPassword(resetToken, password);

      setPassword("");
      setResetToken("");
      setView("auth");
      setIsSignup(false);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to reset your password."
      );
    } finally {
      setIsLoading(false);
    }
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
            {view === "forgot"
              ? "Reset your password"
              : view === "reset"
                ? "Create a new password"
                : isSignup
                  ? "Create your account"
                  : "Welcome back"}
          </h2>

          <p>
            {view === "forgot"
              ? "Enter your email and we'll help you reset your password."
              : view === "reset"
                ? "Enter your reset token and choose a new password."
                : isSignup
                  ? "Create an account to manage your stay and speak with the concierge."
                  : "Sign in to manage your stay and speak with the concierge."}
          </p>
        </div>

        {view === "forgot" ? (
          <form
            onSubmit={handleForgotPassword}
            className="login-form"
          >
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
                ? "Requesting reset..."
                : "Request password reset"}
            </button>

            <button
              type="button"
              className="login-switch-button"
              onClick={() => {
                setView("auth");
                setError("");
              }}
            >
              Back to sign in
            </button>
          </form>
        ) : view === "reset" ? (
          <form
            onSubmit={handleResetPassword}
            className="login-form"
          >
            <label>
              Reset token
              <input
                type="text"
                value={resetToken}
                onChange={(event) => setResetToken(event.target.value)}
                placeholder="Enter your reset token"
                autoComplete="off"
                required
              />
            </label>

            <label>
              New password
              <div className="password-field">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Create a new password (8+ characters)"
                  autoComplete="new-password"
                  minLength={8}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((current) => !current)}
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
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
                ? "Resetting password..."
                : "Reset password"}
            </button>

            <button
              type="button"
              className="login-switch-button"
              onClick={() => {
                setView("auth");
                setError("");
                setResetToken("");
                setPassword("");
              }}
            >
              Back to sign in
            </button>
          </form>
        ) : (
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
                    isSignup
                      ? "new-password"
                      : "current-password"
                  }
                  minLength={isSignup ? 8 : undefined}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((current) => !current)}
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
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

            {!isSignup && (
              <button
                type="button"
                className="login-forgot"
                onClick={() => {
                  setView("forgot");
                  setError("");
                }}
              >
                Forgot password?
              </button>
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
        )}
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




