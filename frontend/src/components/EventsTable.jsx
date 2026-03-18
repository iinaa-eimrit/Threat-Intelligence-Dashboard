function EventsTable({ events }) {
  return (
    <div className="data-table-container">
      <div className="table-header">
        <h3>
          Parsed Events
          <span className="badge" style={{ marginLeft: '0.5rem' }}>
            {events.length}
          </span>
        </h3>
      </div>
      {events.length === 0 ? (
        <div className="empty-state">
          <div className="icon">📋</div>
          <p>No events yet. Upload a log file to get started.</p>
        </div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>IP Address</th>
              <th>Event</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {events.map((e) => (
              <tr key={e.id}>
                <td>#{e.id}</td>
                <td>
                  <code style={{ color: 'var(--accent-blue)' }}>{e.ip}</code>
                </td>
                <td>{e.event}</td>
                <td>{new Date(e.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default EventsTable
