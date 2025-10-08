'use client';

// Profile Edit page - Edit user's own profile

import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth/protected-route';
import { useMyProfile, useUpdateProfile } from '@/hooks/use-profile';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { getErrorMessage } from '@/lib/error-guards';

// Modern 2025: Zod schema for validation
const ProfileEditSchema = z.object({
  headline: z.string().min(1, 'Headline is required').max(200, 'Headline too long'),
  summary: z.string().max(2000, 'Summary too long').optional(),
  location: z.string().min(1, 'Location is required').max(100, 'Location too long'),
  visibility: z.enum(['PRIVATE', 'FRIENDS', 'PUBLIC']),
  contact: z.object({
    email: z.string().optional(),
    phone: z.string().optional(),
    linkedin: z.string().optional(),
    website: z.string().optional(),
  }).optional(),
});

type ProfileEditData = z.infer<typeof ProfileEditSchema>;

function EditProfileContent() {
  const router = useRouter();
  const { data: profile, isLoading: profileLoading } = useMyProfile();
  const updateProfile = useUpdateProfile();

  // Modern 2025: React Hook Form configuration
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ProfileEditData>({
    resolver: zodResolver(ProfileEditSchema) as any,
    mode: 'onChange',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      headline: '',
      summary: '',
      location: '',
      visibility: 'PRIVATE',
      contact: {
        email: '',
        phone: '',
        linkedin: '',
        website: '',
      },
    },
  });

  // Load profile data
  useEffect(() => {
    if (profile) {
      reset({
        headline: profile.headline || '',
        summary: profile.summary || '',
        location: profile.location || '',
        visibility: profile.visibility || 'PRIVATE',
        contact: {
          email: profile.contact?.email || '',
          phone: profile.contact?.phone || '',
          linkedin: profile.contact?.linkedin || '',
          website: profile.contact?.website || '',
        },
      });
    }
  }, [profile, reset]);

  const onSubmit = async (data: ProfileEditData) => {
    try {
      if (!profile) return;
      
      await updateProfile.mutateAsync({
        profileId: profile.id,
        profileData: data,
      });
      
      router.push('/dashboard');
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert(getErrorMessage(error));
    }
  };

  if (profileLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin size-12 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto p-8 max-w-4xl">
        <Card>
          <CardContent className="py-12 text-center">
            <h2 className="text-2xl font-bold mb-2">No Profile Found</h2>
            <p className="text-muted-foreground mb-4">
              You need to create a profile first.
            </p>
            <Button onClick={() => router.push('/profile/create')}>
              Create Profile
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Edit Profile</h1>
        <p className="text-muted-foreground">
          Update your professional profile information
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
            <CardDescription>
              Your basic professional information
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Headline */}
            <div className="space-y-2">
              <Label htmlFor="headline" required>
                Professional Headline
              </Label>
              <Input
                id="headline"
                placeholder="e.g., Senior Full-Stack Developer with 8+ years experience"
                {...register('headline')}
              />
              {errors.headline && (
                <p className="text-sm text-destructive">{errors.headline.message}</p>
              )}
            </div>

            {/* Summary */}
            <div className="space-y-2">
              <Label htmlFor="summary">Professional Summary</Label>
              <Textarea
                id="summary"
                placeholder="Describe your professional background, key achievements, and what makes you unique..."
                rows={6}
                {...register('summary')}
              />
              {errors.summary && (
                <p className="text-sm text-destructive">{errors.summary.message}</p>
              )}
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label htmlFor="location" required>
                Location
              </Label>
              <Input
                id="location"
                placeholder="e.g., Warsaw, Poland or Remote"
                {...register('location')}
              />
              {errors.location && (
                <p className="text-sm text-destructive">{errors.location.message}</p>
              )}
            </div>

            {/* Visibility */}
            <div className="space-y-2">
              <Label htmlFor="visibility">Profile Visibility</Label>
              <Controller
                name="visibility"
                control={control}
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="PRIVATE">
                        <div className="flex flex-row items-center gap-4">
                          <div className="min-w-20 font-medium">Private</div>
                          <span className="text-xs text-muted-foreground">Only you can see</span>
                        </div>
                      </SelectItem>
                      <SelectItem value="FRIENDS">
                        <div className="flex flex-row items-center gap-4">
                          <div className="min-w-20 font-medium">Friends</div>
                          <span className="text-xs text-muted-foreground">People you connect with</span>
                        </div>
                      </SelectItem>
                      <SelectItem value="PUBLIC">
                        <div className="flex flex-row items-center gap-4">
                          <div className="min-w-20 font-medium">Public</div>
                          <span className="text-xs text-muted-foreground">Anyone can view</span>
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Contact Information</CardTitle>
            <CardDescription>
              Optional contact details for your profile
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="contact.email">Email</Label>
                <Input
                  id="contact.email"
                  type="email"
                  placeholder="your@email.com"
                  {...register('contact.email')}
                />
                {(errors.contact as any)?.email?.message && (
                  <p className="text-sm text-destructive">{String((errors.contact as any).email.message)}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact.phone">Phone</Label>
                <Input
                  id="contact.phone"
                  placeholder="+48 123 456 789"
                  {...register('contact.phone')}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact.linkedin">LinkedIn</Label>
                <Input
                  id="contact.linkedin"
                  placeholder="https://linkedin.com/in/yourname"
                  {...register('contact.linkedin')}
                />
                {(errors.contact as any)?.linkedin?.message && (
                  <p className="text-sm text-destructive">{String((errors.contact as any).linkedin.message)}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="contact.website">Website</Label>
                <Input
                  id="contact.website"
                  placeholder="https://yourwebsite.com"
                  {...register('contact.website')}
                />
                {(errors.contact as any)?.website?.message && (
                  <p className="text-sm text-destructive">{String((errors.contact as any).website.message)}</p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex items-center justify-end gap-3">
          <Button type="button" variant="outline" onClick={() => router.push('/dashboard')}>
            Cancel
          </Button>
          <Button type="submit" disabled={isSubmitting || updateProfile.isPending}>
            {isSubmitting || updateProfile.isPending ? 'Saving...' : 'Save Changes'}
          </Button>
        </div>
      </form>
    </div>
  );
}

export default function EditProfilePage() {
  return (
    <ProtectedRoute>
      <EditProfileContent />
    </ProtectedRoute>
  );
}