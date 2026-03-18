function StatsCards({ alerts, events }) {
  const highAlerts = alerts.filter(
    (a) => a.severity === 'high' || a.severity === 'critical'
  ).length
  const openAlerts = alerts.filter((a) => a.status === 'open').length
  const uniqueIPs = new Set(events.map((e) => e.ip)).size

  return (
    <div className="stats-grid">
      <div className="stat-card blue">
        <div className="label">Total Events</div>
        <div className="value">{events.length}</div>
      </div>
      <div className="stat-card red">
        <div className="label">Active Alerts</div>
        <div className="value">{openAlerts}</div>
      </div>
      <div className="stat-card orange">
        <div className="label">High Severity</div>
        <div className="value">{highAlerts}</div>
      </div>
      <div className="stat-card purple">
        <div className="label">Unique IPs</div>
        <div className="value">{uniqueIPs}</div>
      </div>
    </div>
  )
}

export default StatsCards
