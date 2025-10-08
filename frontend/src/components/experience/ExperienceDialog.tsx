'use client';

// Experience Dialog - Add/Edit experience with modern 2025 form patterns

import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { X } from 'lucide-react';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { useCreateExperience, useUpdateExperience } from '@/hooks/use-experience';
import { getErrorMessage } from '@/lib/error-guards';

// Modern 2025: Zod schema for validation
const ExperienceSchema = z.object({
  company: z.string().min(1, 'Company is required').max(200, 'Company name too long'),
  position: z.string().min(1, 'Position is required').max(200, 'Position too long'),
  startDate: z.string().min(1, 'Start date is required'),
  endDate: z.string().optional(),
  isCurrent: z.boolean().default(false),
  location: z.string().max(200, 'Location too long').optional(),
  description: z.string().max(2000, 'Description too long').optional(),
  responsibilities: z.array(z.string()).default([]),
  technologies: z.array(z.string()).default([]),
});

type ExperienceFormData = z.infer<typeof ExperienceSchema>;

interface ExperienceDialogProps {
  isOpen: boolean;
  onClose: () => void;
  experience: any | null;
  profileId: string;
}

export function ExperienceDialog({ isOpen, onClose, experience, profileId }: ExperienceDialogProps) {
  const createExperience = useCreateExperience();
  const updateExperience = useUpdateExperience();
  const isEditing = !!experience;

  // Modern 2025: React Hook Form configuration
  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<ExperienceFormData>({
    resolver: zodResolver(ExperienceSchema) as any,
    mode: 'onChange',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      company: '',
      position: '',
      startDate: '',
      endDate: '',
      isCurrent: false,
      location: '',
      description: '',
      responsibilities: [],
      technologies: [],
    },
  });

  const isCurrent = watch('isCurrent');

  // Load experience data when editing
  useEffect(() => {
    if (experience) {
      reset({
        company: experience.companyName || experience.company || '',
        position: experience.position || '',
        startDate: experience.startDate || '',
        endDate: experience.endDate || '',
        isCurrent: experience.isCurrent || false,
        location: experience.companyLocation || experience.location || '',
        description: experience.description || '',
        responsibilities: experience.responsibilities || [],
        technologies: experience.technologies || [],
      });
    } else {
      reset({
        company: '',
        position: '',
        startDate: '',
        endDate: '',
        isCurrent: false,
        location: '',
        description: '',
        responsibilities: [],
        technologies: [],
      });
    }
  }, [experience, reset]);

  const onSubmit = async (data: ExperienceFormData) => {
    try {
      // Map form data to API format (company -> companyName)
      const apiData = {
        companyName: data.company,
        position: data.position,
        startDate: data.startDate,
        endDate: data.endDate,
        isCurrent: data.isCurrent,
        companyLocation: data.location,
        description: data.description,
        responsibilities: data.responsibilities,
        technologies: data.technologies,
      };

      if (isEditing) {
        await updateExperience.mutateAsync({
          experienceId: experience.id,
          experienceData: apiData,
        });
      } else {
        await createExperience.mutateAsync({
          profileId,
          experienceData: apiData,
        });
      }
      onClose();
    } catch (error) {
      console.error('Failed to save experience:', error);
      alert(getErrorMessage(error));
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{isEditing ? 'Edit Experience' : 'Add Experience'}</DialogTitle>
          <DialogDescription>
            {isEditing
              ? 'Update your work experience details'
              : 'Add a new work experience to your profile'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Company & Position */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="company" required>
                Company
              </Label>
              <Input
                id="company"
                placeholder="e.g., Tech Corp"
                {...register('company')}
              />
              {errors.company && (
                <p className="text-sm text-destructive">{errors.company.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="position" required>
                Position
              </Label>
              <Input
                id="position"
                placeholder="e.g., Senior Software Engineer"
                {...register('position')}
              />
              {errors.position && (
                <p className="text-sm text-destructive">{errors.position.message}</p>
              )}
            </div>
          </div>

          {/* Location */}
          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              placeholder="e.g., Warsaw, Poland"
              {...register('location')}
            />
            {errors.location && (
              <p className="text-sm text-destructive">{errors.location.message}</p>
            )}
          </div>

          {/* Start Date & End Date */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate" required>
                Start Date
              </Label>
              <Input
                id="startDate"
                type="month"
                {...register('startDate')}
              />
              {errors.startDate && (
                <p className="text-sm text-destructive">{errors.startDate.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="endDate">End Date</Label>
              <div className="space-y-2">
                <Input
                  id="endDate"
                  type="month"
                  {...register('endDate')}
                  disabled={isCurrent}
                />
                <div className="flex items-center space-x-2">
                  <Controller
                    name="isCurrent"
                    control={control}
                    render={({ field }) => (
                      <Checkbox
                        id="isCurrent"
                        checked={field.value}
                        onCheckedChange={(checked) => {
                          const isChecked = checked === true;
                          field.onChange(isChecked);
                          if (isChecked) {
                            setValue('endDate', '');
                          }
                        }}
                      />
                    )}
                  />
                  <Label htmlFor="isCurrent" className="text-sm font-normal cursor-pointer">
                    Currently working here
                  </Label>
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              placeholder="Brief description of your role and responsibilities..."
              rows={4}
              {...register('description')}
            />
            {errors.description && (
              <p className="text-sm text-destructive">{errors.description.message}</p>
            )}
            <p className="text-xs text-muted-foreground">
              Describe your role, key responsibilities, and achievements
            </p>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : isEditing ? 'Update' : 'Add Experience'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}