import { useState, useRef } from 'react'

function LogUpload({ onUploadSuccess }) {
  const [status, setStatus] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const inputRef = useRef(null)

  const handleUpload = async (file) => {
    if (!file) return
    setUploading(true)
    setStatus(null)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await fetch('/api/upload-log', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (res.ok) {
        setStatus({ type: 'success', message: `Uploaded: ${data.filename} (Task: ${data.task_id})` })
        onUploadSuccess?.()
      } else {
        setStatus({ type: 'error', message: data.error || 'Upload failed' })
      }
    } catch {
      setStatus({ type: 'error', message: 'Network error. Is the backend running?' })
    } finally {
      setUploading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const file = e.dataTransfer.files[0]
    handleUpload(file)
  }

  return (
    <div className="upload-section">
      <h3>Upload Log File</h3>
      <div
        className={`upload-zone ${dragging ? 'dragging' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <div className="icon">📤</div>
        <p>
          Drag & drop a log file here, or{' '}
          <span className="browse">browse</span>
        </p>
        <p style={{ fontSize: '0.75rem', marginTop: '0.5rem' }}>
          Supports .log, .txt, .csv files
        </p>
        <input
          ref={inputRef}
          type="file"
          accept=".log,.txt,.csv"
          style={{ display: 'none' }}
          onChange={(e) => handleUpload(e.target.files[0])}
        />
      </div>
      {uploading && (
        <div className="loading-spinner">
          <div className="spinner" />
          Uploading...
        </div>
      )}
      {status && (
        <div className={`upload-status ${status.type}`}>{status.message}</div>
      )}
    </div>
  )
}

export default LogUpload
