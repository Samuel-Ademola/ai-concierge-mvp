import ConciergeChat from "../components/ConciergeChat";

export default function ConciergePage() {
  return (
    <section className="concierge-page">
      <div className="concierge-page__intro">
        <p className="concierge-page__eyebrow">AI Concierge</p>

        <h2>How can I help with your stay?</h2>

        <p className="concierge-page__description">
          Ask about dining, transportation, hotel services, or anything
          you need during your stay.
        </p>
      </div>

      <ConciergeChat />
    </section>
  );
}
