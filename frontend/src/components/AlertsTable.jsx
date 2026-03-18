function AlertsTable({ alerts, compact, onRefresh }) {
  const handleAck = async (id) => {
    await fetch(`/api/alerts/${id}/ack`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user: 'analyst' }),
    })
    onRefresh?.()
  }

  const handleResolve = async (id) => {
    await fetch(`/api/alerts/${id}/resolve`, { method: 'POST' })
    onRefresh?.()
  }

  return (
    <div className="data-table-container">
      <div className="table-header">
        <h3>
          {compact ? 'Recent Alerts' : 'All Alerts'}
          <span className="badge" style={{ marginLeft: '0.5rem' }}>
            {alerts.length}
          </span>
        </h3>
      </div>
      {alerts.length === 0 ? (
        <div className="empty-state">
          <div className="icon">🛡️</div>
          <p>No alerts detected</p>
        </div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Severity</th>
              <th>Description</th>
              <th>Status</th>
              <th>Time</th>
              {!compact && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {alerts.map((a) => (
              <tr key={a.id}>
                <td>#{a.id}</td>
                <td>
                  <span className={`severity-badge ${a.severity}`}>
                    {a.severity}
                  </span>
                </td>
                <td>{a.description}</td>
                <td>
                  <span className={`status-badge ${a.status}`}>
                    {a.status}
                  </span>
                </td>
                <td>{new Date(a.created_at).toLocaleString()}</td>
                {!compact && (
                  <td>
                    {a.status === 'open' && (
                      <button
                        className="btn btn-sm btn-outline"
                        onClick={() => handleAck(a.id)}
                      >
                        Ack
                      </button>
                    )}
                    {a.status !== 'resolved' && (
                      <button
                        className="btn btn-sm btn-outline"
                        style={{ marginLeft: '0.25rem' }}
                        onClick={() => handleResolve(a.id)}
                      >
                        Resolve
                      </button>
                    )}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default AlertsTable
