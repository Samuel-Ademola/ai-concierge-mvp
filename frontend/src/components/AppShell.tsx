import { useState, type ReactNode } from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import type { AuthUser } from "../services/authApi";

type AppShellProps = {
  children: ReactNode;
  user: AuthUser;
};

export default function AppShell({
  children,
  user,
}: AppShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar
        open={sidebarOpen}
        onNavigate={() => setSidebarOpen(false)}
        user={user}
      />

      <div className="app-shell__content">
        <Header
          sidebarOpen={sidebarOpen}
          onMenuToggle={() =>
            setSidebarOpen((open) => !open)
          }
          user={user}
        />

        {sidebarOpen && (
          <button
            type="button"
            className="sidebar-backdrop"
            aria-label="Close navigation"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        <main className="app-content">
          {children}
        </main>
      </div>
    </div>
  );
}
