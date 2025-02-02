import { useState, useEffect } from 'react'
import { Button } from './components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card'
import { Play, Square } from 'lucide-react'

interface BotStatus {
  version: string
  is_running: boolean
  last_activity: string
  nation_name: string | null
}

interface BotLog {
  timestamp: string
  message: string
  type: string
}

function App() {
  const [status, setStatus] = useState<BotStatus>()
  const [logs, setLogs] = useState<BotLog[]>([])
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const status = await fetch('http://localhost:8000/api/status').then(r => r.json())
        const logs = await fetch('http://localhost:8000/api/logs').then(r => r.json())
        setStatus(status)
        setLogs(logs)
      } catch (error) {
        console.error('Failed to fetch data:', error)
      }
    }
    
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleStart = async () => {
    await fetch('http://localhost:8000/api/start', { method: 'POST' })
  }

  const handleStop = async () => {
    await fetch('http://localhost:8000/api/stop', { method: 'POST' })
  }

  return (
    <div className="container mx-auto p-4">
      <Card className="mb-4">
        <CardHeader>
          <CardTitle>NationStatesBot Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4 mb-4">
            <div className="flex-1">
              <p>Status: <span className={status?.is_running ? "text-green-500" : "text-red-500"}>
                {status?.is_running ? "Running" : "Stopped"}
              </span></p>
              <p>Version: {status?.version}</p>
              <p>Nation: {status?.nation_name || "Not configured"}</p>
              <p>Last Activity: {status?.last_activity ? new Date(status.last_activity).toLocaleString() : "Never"}</p>
            </div>
            <div className="flex gap-2">
              <Button 
                onClick={handleStart}
                disabled={status?.is_running}
                className="bg-green-500 hover:bg-green-600"
              >
                <Play className="mr-2 h-4 w-4" /> Start Bot
              </Button>
              <Button
                onClick={handleStop}
                disabled={!status?.is_running}
                variant="destructive"
              >
                <Square className="mr-2 h-4 w-4" /> Stop Bot
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Bot Logs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 overflow-y-auto border rounded-lg">
            {logs.map((log, i) => (
              <div key={i} className="p-2 border-b last:border-b-0">
                <span className="text-sm text-gray-500">{new Date(log.timestamp).toLocaleString()}</span>
                <span className={`ml-2 ${
                  log.type === 'error' ? 'text-red-500' :
                  log.type === 'dilemma' ? 'text-blue-500' : 'text-gray-700'
                }`}>{log.message}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default App
