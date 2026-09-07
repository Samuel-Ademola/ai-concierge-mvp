import AppShell from "./components/AppShell";
import GuestDashboard from "./pages/GuestDashboard";
import ConciergePage from "./pages/ConciergePage";
import PreferencesPage from "./pages/PreferencesPage";
import LoginPage from "./pages/LoginPage";
import { useAuth } from "./context/AuthContext";
import "./App.css";

function App() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <main>
        <p>Loading...</p>
      </main>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  const path = window.location.pathname;

  let page = <GuestDashboard />;

  if (path === "/concierge") {
    page = <ConciergePage />;
  }

  if (path === "/preferences") {
    page = <PreferencesPage />;
  }

  return <AppShell user={user}>{page}</AppShell>;
}

export default App;
