import type { AuthUser } from "../services/authApi";
import { useAuth } from "../context/AuthContext";

type SidebarProps = {
  open: boolean;
  onNavigate: () => void;
  user: AuthUser;
};

const navigation = [
  { label: "Dashboard", href: "/", icon: "D" },
  { label: "Concierge", href: "/concierge", icon: "C" },
  { label: "Preferences", href: "/preferences", icon: "P" },
];

export default function Sidebar({
  open,
  onNavigate,
  user,
}: SidebarProps) {
  const { signOut } = useAuth();
  const currentPath = window.location.pathname;

  const displayName =
    user.name?.trim() ||
    user.email?.split("@")[0] ||
    "Guest";

  const initial = displayName.charAt(0).toUpperCase();

  return (
    <aside
      className={`app-sidebar ${open ? "app-sidebar--open" : ""}`}
      aria-hidden={!open}
    >
      <div className="app-sidebar__brand">
        <div className="app-sidebar__logo">AC</div>

        <div className="app-sidebar__brand-copy">
          <h2>AI Concierge</h2>
          <p>Your stay, simplified.</p>
        </div>
      </div>

      <nav
        className="app-sidebar__nav"
        aria-label="Main navigation"
      >
        <p className="app-sidebar__label">MENU</p>

        <div className="app-sidebar__nav-list">
          {navigation.map((item) => {
            const isActive =
              item.href === "/"
                ? currentPath === "/"
                : currentPath === item.href;

            return (
              <a
                key={item.href}
                href={item.href}
                className={`app-sidebar__link ${
                  isActive ? "is-active" : ""
                }`}
                onClick={onNavigate}
              >
                <span className="app-sidebar__link-icon">
                  {item.icon}
                </span>

                <span>{item.label}</span>
              </a>
            );
          })}
        </div>
      </nav>

      <div className="app-sidebar__bottom">
        <div className="app-sidebar__stay">
          <p className="app-sidebar__label">YOUR STAY</p>

          <div className="app-sidebar__room">
            <span>Room</span>
            <strong>204</strong>
          </div>

          <span className="app-sidebar__room-type">
            Suite
          </span>
        </div>

        <div className="app-sidebar__guest">
          <div className="app-sidebar__avatar">
            {initial}
          </div>

          <div className="app-sidebar__guest-copy">
            <strong>{displayName}</strong>
            <span>{user.role === "staff" ? "Staff" : "Guest"}</span>
          </div>
        </div>

        <button
          type="button"
          className="app-sidebar__sign-out"
          onClick={signOut}
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
