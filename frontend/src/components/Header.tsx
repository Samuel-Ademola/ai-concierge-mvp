import type { AuthUser } from "../services/authApi";

type HeaderProps = {
  sidebarOpen: boolean;
  onMenuToggle: () => void;
  user: AuthUser;
};

export default function Header({
  sidebarOpen,
  onMenuToggle,
  user,
}: HeaderProps) {
  const displayName =
    user.name?.trim() || user.email?.split("@")[0] || "Guest";

  const initial = displayName.charAt(0).toUpperCase();

  return (
    <header className="app-header">
      <div className="app-header__inner">
        <button
          type="button"
          className="menu-button"
          aria-label={
            sidebarOpen
              ? "Close navigation"
              : "Open navigation"
          }
          aria-expanded={sidebarOpen}
          onClick={onMenuToggle}
        >
          <span />
          <span />
          <span />
        </button>

        <div className="app-header__title">
          <p className="app-header__eyebrow">
            Guest Dashboard
          </p>
          <h1>Welcome, {displayName}</h1>
        </div>

        <div className="app-header__guest">
          <div
            className="app-header__avatar"
            aria-hidden="true"
          >
            {initial}
          </div>
        </div>
      </div>
    </header>
  );
}
