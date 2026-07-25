function SummaryCard({ title, value, color }) {
  return (
    <div className="summary-card">

      <div
        className="summary-indicator"
        style={{ background: color }}
      ></div>

      <div className="summary-value">
        {value}
      </div>

      <div className="summary-title">
        {title}
      </div>

    </div>
  );
}

export default SummaryCard;