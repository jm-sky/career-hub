'use client';

// User Profile page - Edit user account data (name, email, password)

import { useState } from 'react';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useAuth } from '@/contexts/auth-context';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { ChangePasswordForm } from '@/components/auth/change-password-form';
import { User, Mail, Lock, Shield } from 'lucide-react';

function UserProfileContent() {
  const { user } = useAuth();
  const [isEditingName, setIsEditingName] = useState(false);
  const [name, setName] = useState(user?.name || '');

  const handleSaveName = async () => {
    // TODO: Implement API call to update user name
    console.log('Saving name:', name);
    setIsEditingName(false);
  };

  return (
    <div className="container mx-auto p-8 max-w-4xl space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">User Profile</h1>
        <p className="text-muted-foreground">
          Manage your account information and security settings
        </p>
      </div>

      {/* Personal Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="size-5" />
            Personal Information
          </CardTitle>
          <CardDescription>
            Your basic account information
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name">Full Name</Label>
            <div className="flex gap-2">
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={!isEditingName}
              />
              {isEditingName ? (
                <div className="flex gap-2">
                  <Button onClick={handleSaveName}>Save</Button>
                  <Button 
                    variant="outline" 
                    onClick={() => {
                      setName(user?.name || '');
                      setIsEditingName(false);
                    }}
                  >
                    Cancel
                  </Button>
                </div>
              ) : (
                <Button variant="outline" onClick={() => setIsEditingName(true)}>
                  Edit
                </Button>
              )}
            </div>
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email">Email Address</Label>
            <div className="flex gap-2">
              <Input
                id="email"
                type="email"
                value={user?.email}
                disabled
              />
              <Button variant="outline" disabled>
                Change
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Contact support to change your email address.
            </p>
          </div>

          {/* Account Tier */}
          <div className="space-y-2">
            <Label>Account Tier</Label>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-primary/10 text-primary rounded-md font-medium capitalize">
                {user?.tier || 'free'}
              </span>
            </div>
          </div>

          {/* Account Status */}
          <div className="space-y-2">
            <Label>Account Status</Label>
            <div className="flex items-center gap-2">
              {user?.isActive ? (
                <span className="px-3 py-1 bg-green-100 text-green-800 rounded-md font-medium">
                  Active
                </span>
              ) : (
                <span className="px-3 py-1 bg-red-100 text-red-800 rounded-md font-medium">
                  Inactive
                </span>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Security - Change Password */}
      <div className="flex flex-col items-center">
        <ChangePasswordForm />
      </div>

      {/* Two-Factor Authentication */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="size-5" />
            Two-Factor Authentication
          </CardTitle>
          <CardDescription>
            Add an extra layer of security to your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button variant="outline" disabled>
            Enable 2FA
          </Button>
          <p className="text-sm text-muted-foreground mt-2">
            Coming soon: Protect your account with two-factor authentication.
          </p>
        </CardContent>
      </Card>

      {/* Danger Zone */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive">Danger Zone</CardTitle>
          <CardDescription>
            Irreversible and destructive actions
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-medium mb-2">Delete Account</h4>
            <p className="text-sm text-muted-foreground mb-4">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <Button variant="destructive" disabled>
              Delete My Account
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function UserProfilePage() {
  return (
    <ProtectedRoute>
      <UserProfileContent />
    </ProtectedRoute>
  );
}
