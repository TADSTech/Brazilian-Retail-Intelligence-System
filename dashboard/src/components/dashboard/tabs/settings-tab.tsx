import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Label } from '../../ui/label';
import { Switch } from '../../ui/switch';
import { Button } from '../../ui/button';
import { useTheme } from '../../theme-provider';

export function SettingsTab() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
          <CardDescription>Customize the look and feel of the dashboard.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between space-x-2">
            <Label htmlFor="dark-mode" className="flex flex-col space-y-1">
              <span>Dark Mode</span>
              <span className="font-normal leading-snug text-muted-foreground">
                Switch between light and dark themes.
              </span>
            </Label>
            <Switch 
              id="dark-mode" 
              checked={theme === 'dark'}
              onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Data Refresh</CardTitle>
          <CardDescription>Manage how often the dashboard data updates.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between space-x-2">
            <Label htmlFor="auto-refresh" className="flex flex-col space-y-1">
              <span>Auto Refresh</span>
              <span className="font-normal leading-snug text-muted-foreground">
                Automatically refresh data every 5 minutes.
              </span>
            </Label>
            <Switch id="auto-refresh" defaultChecked />
          </div>
          <Button variant="outline" className="w-full sm:w-auto">
            Clear Cache
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
