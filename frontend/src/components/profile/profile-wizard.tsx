'use client';

// Profile creation wizard component

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { z } from 'zod';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useCreateProfile } from '@/hooks/use-profile';
import { getErrorMessage } from '@/lib/error-guards';

// Profile creation schema
const ProfileCreateSchema = z.object({
  headline: z.string().min(1, 'Headline is required').max(200, 'Headline too long'),
  summary: z.string().max(2000, 'Summary too long').optional(),
  location: z.string().min(1, 'Location is required').max(100, 'Location too long'),
  visibility: z.enum(['PRIVATE', 'FRIENDS', 'PUBLIC']).default('PRIVATE'),
  contact: z.object({
    email: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().email('Invalid email').optional()),
    phone: z.string().transform(val => val === '' ? undefined : val).optional(),
    linkedin: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().url('Invalid LinkedIn URL').optional()),
    website: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().url('Invalid website URL').optional()),
  }).optional(),
});

type ProfileFormData = z.infer<typeof ProfileCreateSchema>;

export function ProfileWizard() {
  const router = useRouter();
  const createProfile = useCreateProfile();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(ProfileCreateSchema),
    defaultValues: {
      visibility: 'PRIVATE',
      contact: {},
    },
  });

  const visibility = watch('visibility');

  const onSubmit = async (data: ProfileFormData) => {
    setError(null);

    try {
      await createProfile.mutateAsync({
        headline: data.headline,
        summary: data.summary,
        location: data.location,
        visibility: data.visibility,
        contact: data.contact || {},
      });

      // Redirect to dashboard after successful creation
      router.push('/dashboard');
    } catch (error: unknown) {
      const errorMessage = getErrorMessage(error);
      setError(errorMessage);
    }
  };

  const isLoading = isSubmitting || createProfile.isPending;

  return (
    <div className="container mx-auto p-8 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Create Your Professional Profile</CardTitle>
          <CardDescription>
            Tell us about yourself to get started with CareerHub
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {error}
              </div>
            )}

            {/* Headline */}
            <div className="space-y-2">
              <Label htmlFor="headline" required>Professional Headline</Label>
              <Input
                id="headline"
                placeholder="e.g., Senior Full-Stack Developer"
                disabled={isLoading}
                {...register('headline')}
              />
              {errors.headline && (
                <p className="text-sm text-red-600">{errors.headline.message}</p>
              )}
              <p className="text-xs text-gray-500">
                A brief title that describes your professional role
              </p>
            </div>

            {/* Summary */}
            <div className="space-y-2">
              <Label htmlFor="summary">Professional Summary</Label>
              <Textarea
                id="summary"
                placeholder="Tell us about your experience, skills, and what makes you unique..."
                rows={6}
                disabled={isLoading}
                {...register('summary')}
              />
              {errors.summary && (
                <p className="text-sm text-red-600">{errors.summary.message}</p>
              )}
              <p className="text-xs text-gray-500">
                Optional. Describe your experience and expertise to make your profile more compelling.
              </p>
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label htmlFor="location" required>Location</Label>
              <Input
                id="location"
                placeholder="e.g., Warsaw, Poland"
                disabled={isLoading}
                {...register('location')}
              />
              {errors.location && (
                <p className="text-sm text-red-600">{errors.location.message}</p>
              )}
            </div>

            {/* Visibility */}
            <div className="space-y-2">
              <Label htmlFor="visibility">Profile Visibility</Label>
              <Select
                value={visibility}
                onValueChange={(value) => setValue('visibility', value as 'PRIVATE' | 'FRIENDS' | 'PUBLIC')}
                disabled={isLoading}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PRIVATE">Private - Only you can see</SelectItem>
                  <SelectItem value="FRIENDS">Friends - People you connect with</SelectItem>
                  <SelectItem value="PUBLIC">Public - Anyone can view</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500">
                You can change this later in your profile settings
              </p>
            </div>

            {/* Contact Information */}
            <div className="space-y-4">
              <Label>Contact Information (Optional)</Label>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="contact.email">Email</Label>
                  <Input
                    id="contact.email"
                    type="email"
                    placeholder="your@email.com"
                    disabled={isLoading}
                    {...register('contact.email')}
                  />
                  {errors.contact?.email && (
                    <p className="text-sm text-red-600">{errors.contact.email.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contact.phone">Phone</Label>
                  <Input
                    id="contact.phone"
                    placeholder="+48 123 456 789"
                    disabled={isLoading}
                    {...register('contact.phone')}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contact.linkedin">LinkedIn</Label>
                  <Input
                    id="contact.linkedin"
                    placeholder="https://linkedin.com/in/yourname"
                    disabled={isLoading}
                    {...register('contact.linkedin')}
                  />
                  {errors.contact?.linkedin && (
                    <p className="text-sm text-red-600">{errors.contact.linkedin.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contact.website">Website</Label>
                  <Input
                    id="contact.website"
                    placeholder="https://yourwebsite.com"
                    disabled={isLoading}
                    {...register('contact.website')}
                  />
                  {errors.contact?.website && (
                    <p className="text-sm text-red-600">{errors.contact.website.message}</p>
                  )}
                </div>
              </div>
            </div>

            <div className="flex gap-4 pt-4">
              <Button asChild variant="outline" disabled={isLoading} className="flex-1">
                <Link href="/dashboard">
                  Skip for Now
                </Link>
              </Button>
              <Button
                type="submit"
                disabled={isLoading}
                className="flex-1"
              >
                {isLoading ? 'Creating Profile...' : 'Create Profile'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
