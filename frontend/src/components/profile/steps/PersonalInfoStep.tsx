'use client';

// Personal Information step of the profile wizard

// Modern 2025: Use FormProvider context instead of props
import { useFormContext, Controller } from 'react-hook-form';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

// Modern 2025: No props needed - use FormProvider context
export function PersonalInfoStep() {
  const { control, register, formState: { errors } } = useFormContext();

  return (
    <div className="space-y-6">
      {/* Headline */}
      <div className="space-y-2">
        <Label htmlFor="headline" className="text-sm font-medium" required>
          Professional Headline
        </Label>
        <Input
          id="headline"
          placeholder="e.g., Senior Full-Stack Developer with 8+ years experience"
          {...register('headline')}
        />
        {errors.headline && (
          <p className="text-sm text-destructive">{String(errors.headline.message || '')}</p>
        )}
        <p className="text-xs text-gray-500">
          A compelling headline that describes your professional role and expertise
        </p>
      </div>

      {/* Summary */}
      <div className="space-y-2">
        <Label htmlFor="summary" className="text-sm font-medium">
          Professional Summary
        </Label>
        <Textarea
          id="summary"
          placeholder="Describe your professional background, key achievements, and what makes you unique. Focus on your value proposition and career highlights..."
          rows={6}
          {...register('summary')}
        />
        {errors.summary && (
          <p className="text-sm text-destructive">{String(errors.summary.message || '')}</p>
        )}
        <p className="text-xs text-gray-500">
          Optional. A comprehensive summary of your professional journey and expertise.
        </p>
      </div>

      {/* Location */}
      <div className="space-y-2">
        <Label htmlFor="location" className="text-sm font-medium" required>
          Location
        </Label>
        <Input
          id="location"
          placeholder="e.g., Warsaw, Poland or Remote"
          {...register('location')}
        />
        {errors.location && (
          <p className="text-sm text-destructive">{String(errors.location.message || '')}</p>
        )}
      </div>

      {/* Visibility */}
      <div className="space-y-2">
        <Label htmlFor="visibility" className="text-sm font-medium">
          Profile Visibility
        </Label>
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
                    <span className="text-xs text-gray-500">Only you can see this profile</span>
                  </div>
                </SelectItem>
                <SelectItem value="FRIENDS">
                  <div className="flex flex-row items-center gap-4">
                    <div className="min-w-20 font-medium">Friends</div>
                    <span className="text-xs text-gray-500">People you connect with can view</span>
                  </div>
                </SelectItem>
                <SelectItem value="PUBLIC">
                  <div className="flex flex-row items-center gap-4">
                    <div className="min-w-20 font-medium">Public</div>
                    <span className="text-xs text-gray-500">Anyone can view this profile</span>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          )}
        />
        <p className="text-xs text-gray-500">
          You can change this later in your profile settings
        </p>
      </div>

      {/* Contact Information */}
      <div className="space-y-4">
        <Label className="text-sm font-medium">Contact Information (Optional)</Label>
        <p className="text-xs text-gray-500">
          Add your contact details to make it easier for potential employers or clients to reach you
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="contact.email" className="text-sm font-medium">Email</Label>
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
            <Label htmlFor="contact.phone" className="text-sm font-medium">Phone</Label>
            <Input
              id="contact.phone"
              placeholder="+48 123 456 789"
              {...register('contact.phone')}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="contact.linkedin" className="text-sm font-medium">LinkedIn</Label>
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
            <Label htmlFor="contact.website" className="text-sm font-medium">Website</Label>
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
      </div>

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Tips for a great profile:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Use specific keywords that recruiters search for</li>
          <li>• Include your years of experience in the headline</li>
          <li>• Make your summary results-oriented with quantifiable achievements</li>
          <li>• Be authentic and professional in your tone</li>
        </ul>
      </div>
    </div>
  );
}
