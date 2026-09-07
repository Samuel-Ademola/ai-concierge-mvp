import { useEffect, useState } from "react";
import {
  getGuestRequests,
  type GuestRequest,
} from "../services/requestApi";
import { useAuth } from "../context/AuthContext";

export default function GuestDashboard() {
  const { user } = useAuth();
  const userId = user?.user_id ?? "";

  const [requests, setRequests] = useState<GuestRequest[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!userId) {
      setRequests([]);
      setIsLoading(false);
      return;
    }

    async function loadRequests(showLoading = false) {
      if (showLoading) {
        setIsLoading(true);
      }

      try {
        const data = await getGuestRequests(userId);
        setRequests(data);
      } catch (error) {
        console.error("Failed to load guest requests:", error);
      } finally {
        setIsLoading(false);
      }
    }

    loadRequests(true);

    const handleRequestsUpdated = () => {
      loadRequests(false);
    };

    window.addEventListener(
      "guest-requests-updated",
      handleRequestsUpdated
    );

    return () => {
      window.removeEventListener(
        "guest-requests-updated",
        handleRequestsUpdated
      );
    };
  }, [userId]);

  const confirmedRequests = requests.filter(
    (request) => request.status === "confirmed"
  );

  const pendingRequests = requests.filter(
    (request) => request.status === "pending"
  );

  const latestDiningRequest = requests.find(
    (request) => request.request_type === "dining"
  );

  const formatStatus = (status: string) =>
    status.charAt(0).toUpperCase() + status.slice(1);

  const formatRequestType = (type: string) =>
    type.charAt(0).toUpperCase() + type.slice(1);

  return (
    <section className="dashboard">
      <div className="dashboard-intro">
        <div>
          <p className="dashboard-eyebrow">Your stay</p>
          <h2>Everything you need, in one place.</h2>
          <p className="dashboard-description">
            Manage your requests, discover dining, and get assistance
            throughout your stay.
          </p>
        </div>
      </div>

      <div className="dashboard-stats">
        <article className="stat-card">
          <div className="stat-card__top">
            <span className="stat-card__label">Room</span>
            <span className="stat-card__icon">01</span>
          </div>

          <strong className="stat-card__value">204</strong>

          <p>Suite</p>
        </article>

        <article className="stat-card">
          <div className="stat-card__top">
            <span className="stat-card__label">Confirmed</span>
            <span className="stat-card__icon">✓</span>
          </div>

          <strong className="stat-card__value">
            {confirmedRequests.length}
          </strong>

          <p>Confirmed bookings</p>
        </article>

        <article className="stat-card">
          <div className="stat-card__top">
            <span className="stat-card__label">Pending</span>
            <span className="stat-card__icon">02</span>
          </div>

          <strong className="stat-card__value">
            {pendingRequests.length}
          </strong>

          <p>Awaiting confirmation</p>
        </article>

        <article className="stat-card stat-card--dining">
          <div className="stat-card__top">
            <span className="stat-card__label">Dining</span>
            <span className="stat-card__icon">◆</span>
          </div>

          <strong className="stat-card__status">
            {latestDiningRequest
              ? formatStatus(latestDiningRequest.status)
              : "None"}
          </strong>

          <p>
            {latestDiningRequest
              ? latestDiningRequest.details
              : "No dining request yet"}
          </p>
        </article>
      </div>

      <div className="dashboard-section">
        <div className="section-heading">
          <div>
            <p className="dashboard-eyebrow">Shortcuts</p>
            <h2>Quick actions</h2>
          </div>
        </div>

        <div className="quick-actions">
          <a className="action-card action-card--primary" href="/concierge">
            <span className="action-card__icon">✦</span>
            <span>
              <strong>Ask Concierge</strong>
              <small>Get help with anything during your stay</small>
            </span>
            <span className="action-card__arrow">→</span>
          </a>

          <a className="action-card" href="/concierge">
            <span className="action-card__icon">◆</span>
            <span>
              <strong>Book Dining</strong>
              <small>Find a restaurant for your evening</small>
            </span>
            <span className="action-card__arrow">→</span>
          </a>

          <a className="action-card" href="/concierge">
            <span className="action-card__icon">↗</span>
            <span>
              <strong>Request Transport</strong>
              <small>Arrange airport or local transportation</small>
            </span>
            <span className="action-card__arrow">→</span>
          </a>

          <a className="action-card" href="/concierge">
            <span className="action-card__icon">+</span>
            <span>
              <strong>Hotel Service</strong>
              <small>Request housekeeping or assistance</small>
            </span>
            <span className="action-card__arrow">→</span>
          </a>
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-heading">
          <div>
            <p className="dashboard-eyebrow">Your requests</p>
            <h2>Recent activity</h2>
          </div>

          {requests.length > 0 && (
            <span className="section-count">
              {requests.length} request{requests.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>

        <div className="activity-card">
          {isLoading ? (
            <div className="empty-state">
              <p>Loading your requests...</p>
            </div>
          ) : requests.length === 0 ? (
            <div className="empty-state">
              <span>✦</span>
              <strong>No requests yet</strong>
              <p>Your concierge requests will appear here.</p>
            </div>
          ) : (
            requests.slice(0, 5).map((request) => (
              <article className="activity-row" key={request.id}>
                <div className="activity-row__icon">
                  {request.request_type === "dining" ? "◆" : "•"}
                </div>

                <div className="activity-row__content">
                  <div className="activity-row__title">
                    <strong>
                      {formatRequestType(request.request_type)}
                    </strong>

                    <span
                      className={`status-badge status-badge--${request.status}`}
                    >
                      {formatStatus(request.status)}
                    </span>
                  </div>

                  <p>{request.details}</p>

                  <small>{request.request_id}</small>
                </div>

                <span className="activity-row__arrow">→</span>
              </article>
            ))
          )}
        </div>
      </div>
    </section>
  );
}