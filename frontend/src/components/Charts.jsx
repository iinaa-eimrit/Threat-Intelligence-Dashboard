import { Bar, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
  Filler
)

const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: '#1e293b',
      borderColor: '#334155',
      borderWidth: 1,
      titleColor: '#f1f5f9',
      bodyColor: '#94a3b8',
      padding: 10,
      cornerRadius: 8,
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(51, 65, 85, 0.5)' },
      ticks: { color: '#64748b', font: { size: 11 } },
    },
    y: {
      grid: { color: 'rgba(51, 65, 85, 0.5)' },
      ticks: { color: '#64748b', font: { size: 11 } },
    },
  },
}

function Charts({ events }) {
  // Top attacking IPs
  const ipCounts = {}
  events.forEach((e) => {
    ipCounts[e.ip] = (ipCounts[e.ip] || 0) + 1
  })
  const sortedIPs = Object.entries(ipCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)

  const ipChartData = {
    labels: sortedIPs.map(([ip]) => ip),
    datasets: [
      {
        label: 'Events',
        data: sortedIPs.map(([, count]) => count),
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
        borderColor: '#3b82f6',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  }

  // Event timeline
  const timeline = {}
  events.forEach((e) => {
    const date = e.timestamp.split('T')[0]
    timeline[date] = (timeline[date] || 0) + 1
  })
  const sortedDates = Object.keys(timeline).sort()

  const timelineData = {
    labels: sortedDates,
    datasets: [
      {
        label: 'Events',
        data: sortedDates.map((d) => timeline[d]),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderWidth: 2,
        pointRadius: 3,
        pointBackgroundColor: '#ef4444',
        fill: true,
        tension: 0.3,
      },
    ],
  }

  if (events.length === 0) {
    return (
      <div className="charts-grid">
        <div className="chart-card">
          <h3>Top Attacking IPs</h3>
          <div className="empty-state">
            <p>No data available yet</p>
          </div>
        </div>
        <div className="chart-card">
          <h3>Event Timeline</h3>
          <div className="empty-state">
            <p>No data available yet</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="charts-grid">
      <div className="chart-card">
        <h3>Top Attacking IPs</h3>
        <div className="chart-wrapper">
          <Bar data={ipChartData} options={chartDefaults} />
        </div>
      </div>
      <div className="chart-card">
        <h3>Event Timeline</h3>
        <div className="chart-wrapper">
          <Line data={timelineData} options={chartDefaults} />
        </div>
      </div>
    </div>
  )
}

export default Charts
