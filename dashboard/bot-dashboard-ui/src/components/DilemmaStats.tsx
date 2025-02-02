import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface DilemmaStatistics {
  total: number
  choices: Record<string, number>
  categories: Record<string, number>
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

export function DilemmaStats({ stats }: { stats: DilemmaStatistics }) {
  const choiceData = Object.entries(stats.choices).map(([choice, count], index) => ({
    name: `Choice ${choice}`,
    value: count,
    color: COLORS[index % COLORS.length]
  }))

  const categoryData = Object.entries(stats.categories).map(([category, count], index) => ({
    name: category,
    value: count,
    color: COLORS[index % COLORS.length]
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dilemma Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-lg font-semibold mb-4">
          Total Dilemmas: {stats.total}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="h-[300px]">
            <h3 className="text-sm font-medium mb-2">Choices Distribution</h3>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={choiceData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {choiceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="h-[300px]">
            <h3 className="text-sm font-medium mb-2">Category Distribution</h3>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
