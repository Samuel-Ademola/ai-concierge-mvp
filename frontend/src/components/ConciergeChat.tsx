import {
  useEffect,
  useState,
  type FormEvent,
} from "react";

import { useAuth } from "../context/AuthContext";

import {
  ApiError,
  createGuestRequest,
  getGuestRequests,
  resetConversation,
  sendMessage,
  type GuestRequest,
  type Recommendation,
} from "../services/conciergeApi";

type ChatMessage = {
  role: "guest" | "concierge";
  content: string;
  recommendations?: Recommendation[];
};

type BookingState = {
  requestId: string;
  status: string;
  message: string;
};

const SUGGESTIONS = [
  "Find dinner",
  "Book a restaurant",
  "Arrange airport transfer",
  "Request housekeeping",
];

export default function ConciergeChat() {
  const { user } = useAuth();
  const userId = user?.user_id ?? "";

  const storageKey = userId
    ? `concierge-messages-${userId}`
    : "";

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    if (!userId || !storageKey) {
      return [];
    }

    try {
      const stored = localStorage.getItem(storageKey);

      if (!stored) {
        return [];
      }

      return JSON.parse(stored) as ChatMessage[];
    } catch {
      return [];
    }
  });

  const [existingRequests, setExistingRequests] = useState<
    GuestRequest[]
  >([]);

  const [isLoading, setIsLoading] = useState(false);
  const [requestingRestaurant, setRequestingRestaurant] =
    useState("");

  const [bookingStates, setBookingStates] = useState<
    Record<string, BookingState>
  >({});

  const [expandedRestaurant, setExpandedRestaurant] =
    useState<string | null>(null);

  const [error, setError] = useState("");

  useEffect(() => {
    if (!storageKey) {
      return;
    }

    localStorage.setItem(
      storageKey,
      JSON.stringify(messages)
    );
  }, [messages, storageKey]);

  useEffect(() => {
    if (!userId) {
      return;
    }

    async function loadExistingRequests() {
      try {
        const requests = await getGuestRequests(userId);

        setExistingRequests(requests);
      } catch {
        // Request history is useful but not required for chat.
      }
    }

    loadExistingRequests();
  }, [userId]);

  const submitMessage = async (text: string) => {
    const trimmedMessage = text.trim();

    if (!trimmedMessage || isLoading || !userId) {
      return;
    }

    setError("");

    setMessages((previous) => [
      ...previous,
      {
        role: "guest",
        content: trimmedMessage,
      },
    ]);

    setMessage("");
    setIsLoading(true);

    try {
      const result = await sendMessage({
        message: trimmedMessage,
        user_id: userId,
      });

      setMessages((previous) => [
        ...previous,
        {
          role: "concierge",
          content: result.response,
          recommendations: result.recommendations,
        },
      ]);
    } catch (requestError) {
      if (
        requestError instanceof ApiError &&
        requestError.kind === "network"
      ) {
        setError(
          "I can't connect to the concierge right now. Check your connection and try again."
        );
      } else {
        setError(
          "The concierge is temporarily unavailable. Please try again."
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    await submitMessage(message);
  };

  const handleSuggestion = async (suggestion: string) => {
    await submitMessage(suggestion);
  };

  const handleNewConversation = async () => {
    if (isLoading || !userId) {
      return;
    }

    setError("");

    try {
      await resetConversation(userId);

      setMessages([]);
      setMessage("");
      setBookingStates({});
      setExpandedRestaurant(null);

      if (storageKey) {
        localStorage.removeItem(storageKey);
      }
    } catch (requestError) {
      if (
        requestError instanceof ApiError &&
        requestError.kind === "network"
      ) {
        setError(
          "I couldn't reset the conversation because the concierge is unreachable."
        );
      } else {
        setError(
          "Couldn't start a new conversation. Please try again."
        );
      }
    }
  };

  const buildDiningDetails = (
    restaurant: Recommendation
  ) =>
    `${restaurant.type.replace("_", " ")} - ${restaurant.cuisine} at ${restaurant.name}, ${restaurant.location}`;

  const findExistingBooking = (
    restaurant: Recommendation
  ) => {
    const details = buildDiningDetails(restaurant);

    return existingRequests.find(
      (request) =>
        request.request_type === "dining" &&
        request.details === details &&
        (request.status === "pending" ||
          request.status === "confirmed")
    );
  };

  const handleRestaurantRequest = async (
    restaurant: Recommendation
  ) => {
    if (requestingRestaurant || !userId) {
      return;
    }

    const existing = findExistingBooking(restaurant);

    if (existing) {
      setBookingStates((previous) => ({
        ...previous,
        [restaurant.id]: {
          requestId: existing.request_id,
          status: existing.status,
          message:
            "This restaurant has already been requested.",
        },
      }));

      return;
    }

    setRequestingRestaurant(restaurant.id);

    setBookingStates((previous) => ({
      ...previous,
      [restaurant.id]: {
        requestId: "",
        status: "submitting",
        message: "Submitting booking request...",
      },
    }));

    try {
      const request = await createGuestRequest(
        userId,
        "dining",
        buildDiningDetails(restaurant)
      );

      setBookingStates((previous) => ({
        ...previous,
        [restaurant.id]: {
          requestId: request.request_id,
          status: request.status,
          message: "Booking request submitted.",
        },
      }));

      setExistingRequests((previous) => {
        const alreadyIncluded = previous.some(
          (item) =>
            item.request_id === request.request_id
        );

        return alreadyIncluded
          ? previous
          : [request, ...previous];
      });

      window.dispatchEvent(
        new Event("guest-requests-updated")
      );
    } catch (requestError) {
      const errorMessage =
        requestError instanceof ApiError &&
        requestError.kind === "network"
          ? "We couldn't reach the booking service. Please try again."
          : "We couldn't submit this booking request. Please try again.";

      setBookingStates((previous) => ({
        ...previous,
        [restaurant.id]: {
          requestId: "",
          status: "error",
          message: errorMessage,
        },
      }));
    } finally {
      setRequestingRestaurant("");
    }
  };

  return (
    <div className="concierge-panel">
      <div className="concierge-panel__header">
        <div>
          <div className="concierge-panel__online">
            <span className="concierge-panel__online-dot" />
            Concierge online
          </div>

          <h3>Personal assistance</h3>

          <p>
            Tell me what you need and I'll help arrange it.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            type="button"
            className="concierge-new-button"
            onClick={handleNewConversation}
            disabled={isLoading}
          >
            New conversation
          </button>
        )}
      </div>

      <div className="concierge-panel__conversation">
        {messages.length === 0 ? (
          <div className="concierge-empty">
            <div className="concierge-empty__icon">
              AI
            </div>

            <h3>How can I help?</h3>

            <p>
              Ask me about dining, transportation, hotel
              services, or anything else you need during your
              stay.
            </p>

            <div className="concierge-empty__suggestions">
              {SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() =>
                    handleSuggestion(suggestion)
                  }
                  disabled={isLoading}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="concierge-messages">
            {messages.map((chatMessage, index) => (
              <div
                key={`${chatMessage.role}-${index}`}
                className={`concierge-message concierge-message--${chatMessage.role}`}
              >
                {chatMessage.role === "concierge" && (
                  <div className="concierge-message__avatar">
                    AI
                  </div>
                )}

                <div className="concierge-message__content">
                  <span className="concierge-message__label">
                    {chatMessage.role === "guest"
                      ? "You"
                      : "Concierge"}
                  </span>

                  <div className="concierge-message__bubble">
                    {chatMessage.content}
                  </div>

                  {chatMessage.recommendations &&
                    chatMessage.recommendations.length > 0 && (
                      <div className="concierge-recommendations">
                        {chatMessage.recommendations.map(
                          (restaurant) => {
                            const booking =
                              bookingStates[restaurant.id];

                            const existing =
                              findExistingBooking(
                                restaurant
                              );

                            const alreadyRequested =
                              Boolean(
                                booking &&
                                  booking.status !== "error"
                              ) || Boolean(existing);

                            const expanded =
                              expandedRestaurant ===
                              restaurant.id;

                            return (
                              <article
                                key={restaurant.id}
                                className="restaurant-card"
                              >
                                <div className="restaurant-card__header">
                                  <div>
                                    <span className="restaurant-card__type">
                                      {restaurant.type.replace(
                                        "_",
                                        " "
                                      )}
                                    </span>

                                    <h4>
                                      {restaurant.name}
                                    </h4>
                                  </div>

                                  <span className="restaurant-card__rating">
                                    {restaurant.rating.toFixed(
                                      1
                                    )}
                                  </span>
                                </div>

                                <div className="restaurant-card__details">
                                  <span>
                                    {restaurant.cuisine}
                                  </span>

                                  <span>
                                    {restaurant.price_range}
                                  </span>

                                  <span>
                                    {restaurant.location}
                                  </span>
                                </div>

                                {expanded && (
                                  <div className="restaurant-card__expanded">
                                    <div>
                                      <span>Type</span>
                                      <strong>
                                        {restaurant.type.replace(
                                          "_",
                                          " "
                                        )}
                                      </strong>
                                    </div>

                                    <div>
                                      <span>Cuisine</span>
                                      <strong>
                                        {restaurant.cuisine}
                                      </strong>
                                    </div>

                                    <div>
                                      <span>Location</span>
                                      <strong>
                                        {restaurant.location}
                                      </strong>
                                    </div>

                                    <div>
                                      <span>Price</span>
                                      <strong>
                                        {restaurant.price_range}
                                      </strong>
                                    </div>

                                    <div>
                                      <span>Rating</span>
                                      <strong>
                                        {restaurant.rating.toFixed(
                                          1
                                        )}
                                      </strong>
                                    </div>
                                  </div>
                                )}

                                <div className="restaurant-card__actions">
                                  <button
                                    type="button"
                                    className="restaurant-card__details-button"
                                    onClick={() =>
                                      setExpandedRestaurant(
                                        expanded
                                          ? null
                                          : restaurant.id
                                      )
                                    }
                                  >
                                    {expanded
                                      ? "Hide details"
                                      : "View details"}
                                  </button>

                                  <button
                                    type="button"
                                    className="restaurant-card__button"
                                    onClick={() =>
                                      handleRestaurantRequest(
                                        restaurant
                                      )
                                    }
                                    disabled={
                                      requestingRestaurant ===
                                        restaurant.id ||
                                      alreadyRequested
                                    }
                                  >
                                    {requestingRestaurant ===
                                    restaurant.id
                                      ? "Submitting..."
                                      : alreadyRequested
                                        ? "Requested"
                                        : "Request booking"}
                                  </button>
                                </div>

                                {booking && (
                                  <div
                                    className={`restaurant-card__result ${
                                      booking.status === "error"
                                        ? "restaurant-card__result--error"
                                        : "restaurant-card__result--success"
                                    }`}
                                  >
                                    <strong>
                                      {booking.status ===
                                      "error"
                                        ? booking.message
                                        : `? ${booking.message}`}
                                    </strong>

                                    {booking.requestId && (
                                      <span>
                                        Request ID:{" "}
                                        {booking.requestId}
                                      </span>
                                    )}

                                    {booking.status !==
                                      "error" &&
                                      booking.status !==
                                        "submitting" && (
                                        <span>
                                          Status:{" "}
                                          {booking.status}
                                        </span>
                                      )}
                                  </div>
                                )}
                              </article>
                            );
                          }
                        )}
                      </div>
                    )}
                </div>
              </div>
            ))}
          </div>
        )}

        {isLoading && (
          <div className="concierge-thinking">
            <div className="concierge-thinking__avatar">
              AI
            </div>

            <div>
              <span className="concierge-message__label">
                Concierge
              </span>

              <div className="concierge-thinking__bubble">
                <span />
                <span />
                <span />
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="concierge-error">
            {error}
          </div>
        )}
      </div>

      <form
        className="concierge-input"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          placeholder="Ask the concierge anything..."
          disabled={isLoading}
          aria-label="Message the concierge"
        />

        <button
          type="submit"
          disabled={isLoading || !message.trim()}
          aria-label="Send message"
        >
          <span>{isLoading ? "..." : "Send"}</span>

          {!isLoading && (
            <span aria-hidden="true">?</span>
          )}
        </button>
      </form>
    </div>
  );
}
