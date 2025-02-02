import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Switch } from '../components/ui/switch'
import { Slider } from '../components/ui/slider'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Label } from '../components/ui/label'

interface BotSettings {
  auto_answer_dilemmas: boolean
  navigation_interval: number
  max_dilemmas_per_day: number
  preferred_categories: string[]
}

interface ConfigPanelProps {
  settings: BotSettings
  onUpdate: (settings: BotSettings) => void
}

export function ConfigPanel({ settings, onUpdate }: ConfigPanelProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Bot Configuration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex items-center justify-between">
          <Label htmlFor="auto-answer">Auto Answer Dilemmas</Label>
          <Switch
            id="auto-answer"
            checked={settings.auto_answer_dilemmas}
            onCheckedChange={(checked) => 
              onUpdate({ ...settings, auto_answer_dilemmas: checked })
            }
          />
        </div>

        <div className="space-y-2">
          <Label>Navigation Interval (minutes)</Label>
          <Slider
            value={[settings.navigation_interval]}
            onValueChange={([value]) => 
              onUpdate({ ...settings, navigation_interval: value })
            }
            min={5}
            max={60}
            step={5}
          />
        </div>

        <div className="space-y-2">
          <Label>Max Dilemmas Per Day</Label>
          <Slider
            value={[settings.max_dilemmas_per_day]}
            onValueChange={([value]) => 
              onUpdate({ ...settings, max_dilemmas_per_day: value })
            }
            min={1}
            max={20}
            step={1}
          />
        </div>

        <div className="space-y-2">
          <Label>Preferred Categories</Label>
          <Select
            value={settings.preferred_categories.join(',')}
            onValueChange={(value) => 
              onUpdate({ 
                ...settings, 
                preferred_categories: value.split(',').filter(Boolean)
              })
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Select categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="economy">Economy</SelectItem>
              <SelectItem value="military">Military</SelectItem>
              <SelectItem value="social">Social</SelectItem>
              <SelectItem value="environment">Environment</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardContent>
    </Card>
  )
}
