'use client';

// Modern 2025 Work Experience step with best practices

import { useState, useCallback } from 'react';
import { useFormContext, Controller, useFieldArray } from 'react-hook-form';
import { Plus, Trash2, Calendar, Building, MapPin } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';

// Modern 2025: No props needed - use FormProvider context
export function ExperienceStep() {
  const { control, register, watch, formState: { errors } } = useFormContext();
  
  // Modern 2025: Use useFieldArray for dynamic arrays
  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'experiences'
  });

  // Watch experiences to get real-time values for display
  const watchedExperiences = watch('experiences') || [];

  // Modern 2025: Local state for UI interactions only
  const [editingExperience, setEditingExperience] = useState<number | null>(null);

  // Modern 2025: Memoized callbacks for performance
  const addExperience = useCallback(() => {
    const newExperience = {
      id: Date.now().toString(),
      company: '',
      position: '',
      startDate: '',
      endDate: '',
      isCurrent: false,
      description: '',
      responsibilities: [],
      achievements: [],
      technologies: [],
    };
    append(newExperience);
    setEditingExperience(fields.length); // Edit the newly added item
  }, [append, fields.length]);

  const removeExperience = useCallback((index: number) => {
    remove(index);
    if (editingExperience === index) {
      setEditingExperience(null);
    }
  }, [remove, editingExperience]);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-2">Work Experience</h3>
        <p className="text-gray-600 mb-4">
          Add your professional work experience to showcase your career journey
        </p>
        <Button onClick={addExperience} variant="outline">
          <Plus className="size-4 mr-2" />
          Add Experience
        </Button>
      </div>

      {fields.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Building className="h-12 w-12 text-gray-400 mb-4" />
            <h4 className="font-medium text-gray-900 mb-2">No experience added yet</h4>
            <p className="text-sm text-gray-500 text-center mb-4">
              Start building your professional profile by adding your work experience
            </p>
            <Button onClick={addExperience}>
              <Plus className="size-4 mr-2" />
              Add Your First Experience
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {fields.map((field, index) => {
            const experience = watchedExperiences[index] || field;
            return (
            <Card key={field.id} className={editingExperience === index ? 'ring-2 ring-primary' : ''}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-base">
                      {experience.position || `Experience ${index + 1}`}
                      {experience.company && ` at ${experience.company}`}
                    </CardTitle>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                      {experience.startDate && (
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          <span>{experience.startDate}</span>
                          {experience.endDate && !experience.isCurrent && <span> - {experience.endDate}</span>}
                          {experience.isCurrent && <span> - Present</span>}
                        </div>
                      )}
                      {experience.isCurrent && (
                        <Badge variant="secondary" className="text-xs">
                          Current
                        </Badge>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingExperience(editingExperience === index ? null : index)}
                    >
                      {editingExperience === index ? 'Done' : 'Edit'}
                    </Button>
                    <Button
                      variant="ghost-destructive"
                      size="sm"
                      onClick={() => removeExperience(index)}
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              
              {editingExperience === index && (
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${index}-position`} required>Position</Label>
                      <Input
                        id={`exp-${index}-position`}
                        placeholder="e.g., Senior Software Engineer"
                        {...register(`experiences.${index}.position`)}
                      />
                      {(errors.experiences as any)?.[index]?.position && (
                        <p className="text-sm text-destructive">
                          {String((errors.experiences as any)[index]?.position?.message || '')}
                        </p>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${index}-company`} required>Company</Label>
                      <Input
                        id={`exp-${index}-company`}
                        placeholder="e.g., Tech Corp"
                        {...register(`experiences.${index}.company`)}
                      />
                      {(errors.experiences as any)?.[index]?.company && (
                        <p className="text-sm text-destructive">
                          {String((errors.experiences as any)[index]?.company?.message || '')}
                        </p>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${index}-start`} required>Start Date</Label>
                      <Input
                        id={`exp-${index}-start`}
                        type="month"
                        {...register(`experiences.${index}.startDate`)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${index}-end`}>End Date</Label>
                      <div className="flex items-center gap-2">
                        <Controller
                          name={`experiences.${index}.isCurrent`}
                          control={control}
                          render={({ field: checkboxField }) => (
                            <>
                              <Input
                                id={`exp-${index}-end`}
                                type="month"
                                {...register(`experiences.${index}.endDate`)}
                                disabled={checkboxField.value}
                              />
                              <div className="flex items-center space-x-2">
                                <Checkbox
                                  id={`exp-${index}-current`}
                                  checked={checkboxField.value}
                                  onCheckedChange={(checked) => {
                                    const isChecked = checked === true;
                                    checkboxField.onChange(isChecked);
                                    if (isChecked) {
                                      // Clear end date when current is checked
                                      update(index, {
                                        ...field,
                                        endDate: '',
                                        isCurrent: isChecked
                                      });
                                    }
                                  }}
                                />
                                <Label htmlFor={`exp-${index}-current`} className="text-sm">
                                  Currently working here
                                </Label>
                              </div>
                            </>
                          )}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`exp-${index}-description`}>Description</Label>
                    <Textarea
                      id={`exp-${index}-description`}
                      placeholder="Brief description of your role and responsibilities..."
                      {...register(`experiences.${index}.description`)}
                      rows={3}
                    />
                  </div>
                </CardContent>
              )}
            </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
