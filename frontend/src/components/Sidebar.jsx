function Sidebar({ activePage, onNavigate }) {
  const items = [
    { id: 'dashboard', icon: '📊', label: 'Dashboard' },
    { id: 'alerts', icon: '🚨', label: 'Alerts' },
    { id: 'events', icon: '📋', label: 'Events' },
    { id: 'upload', icon: '📁', label: 'Upload Logs' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h2>ThreatIntel</h2>
        <span>Detection System</span>
      </div>
      <ul className="sidebar-nav">
        {items.map((item) => (
          <li key={item.id}>
            <button
              className={activePage === item.id ? 'active' : ''}
              onClick={() => onNavigate(item.id)}
            >
              <span className="icon">{item.icon}</span>
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  )
}

export default Sidebar
