'use client';

// Project form component for editing project details

import { memo } from 'react';
import { useFormContext, Controller } from 'react-hook-form';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { CardContent } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ProjectArrayField } from './ProjectArrayField';
import { ProjectTechnologies } from './ProjectTechnologies';

interface ProjectFormProps {
  index: number;
  project: any;
  onAddAchievement: (value: string) => void;
  onRemoveAchievement: (index: number) => void;
  onAddChallenge: (value: string) => void;
  onRemoveChallenge: (index: number) => void;
  onAddTechnology: (value: string) => void;
  onRemoveTechnology: (index: number) => void;
}

export const ProjectForm = memo(function ProjectForm({
  index,
  project,
  onAddAchievement,
  onRemoveAchievement,
  onAddChallenge,
  onRemoveChallenge,
  onAddTechnology,
  onRemoveTechnology
}: ProjectFormProps) {
  const { control, register } = useFormContext();

  return (
    <CardContent className="space-y-4">
      {/* Basic Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor={`projects.${index}.name`} required>Project Name</Label>
          <Input
            id={`projects.${index}.name`}
            placeholder="e.g., E-commerce Platform"
            {...register(`projects.${index}.name`)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor={`projects.${index}.client`}>Client/Company</Label>
          <Input
            id={`projects.${index}.client`}
            placeholder="e.g., Tech Startup Inc."
            {...register(`projects.${index}.client`)}
          />
        </div>
      </div>

      {/* Description */}
      <div className="space-y-2">
        <Label htmlFor={`projects.${index}.description`} required>Description</Label>
        <Textarea
          id={`projects.${index}.description`}
          placeholder="Describe what the project does, its purpose, and key features..."
          {...register(`projects.${index}.description`)}
          rows={4}
        />
      </div>

      {/* Status, Category, Scale */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-2">
          <Label>Status</Label>
          <Controller
            name={`projects.${index}.status`}
            control={control}
            render={({ field }) => (
              <Select value={field.value} onValueChange={field.onChange}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ACTIVE">Active</SelectItem>
                  <SelectItem value="STAGING">Staging</SelectItem>
                  <SelectItem value="ARCHIVED">Archived</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
        </div>
        <div className="space-y-2">
          <Label>Category</Label>
          <Controller
            name={`projects.${index}.category`}
            control={control}
            render={({ field }) => (
              <Select value={field.value} onValueChange={field.onChange}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PRODUCTION">Production</SelectItem>
                  <SelectItem value="DEMO">Demo</SelectItem>
                  <SelectItem value="INTERNAL">Internal</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
        </div>
        <div className="space-y-2">
          <Label>Scale</Label>
          <Controller
            name={`projects.${index}.scale`}
            control={control}
            render={({ field }) => (
              <Select value={field.value} onValueChange={field.onChange}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="SMALL">Small</SelectItem>
                  <SelectItem value="MEDIUM">Medium</SelectItem>
                  <SelectItem value="LARGE">Large</SelectItem>
                  <SelectItem value="ENTERPRISE">Enterprise</SelectItem>
                </SelectContent>
              </Select>
            )}
          />
        </div>
      </div>

      {/* Dates */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor={`projects.${index}.startDate`}>Start Date</Label>
          <Input
            id={`projects.${index}.startDate`}
            type="month"
            {...register(`projects.${index}.startDate`)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor={`projects.${index}.endDate`}>End Date</Label>
          <Input
            id={`projects.${index}.endDate`}
            type="month"
            {...register(`projects.${index}.endDate`)}
          />
        </div>
      </div>

      {/* Array Fields */}
      <div className="space-y-4">
        <ProjectArrayField
          label="Key Achievements"
          placeholder="Add an achievement..."
          items={project.achievements || []}
          onAdd={onAddAchievement}
          onRemove={onRemoveAchievement}
          bgColor="bg-green-50"
        />

        <ProjectArrayField
          label="Technical Challenges"
          placeholder="Add a challenge you overcame..."
          items={project.challenges || []}
          onAdd={onAddChallenge}
          onRemove={onRemoveChallenge}
          bgColor="bg-orange-50"
        />

        <ProjectTechnologies
          technologies={project.technologies || []}
          onAdd={onAddTechnology}
          onRemove={onRemoveTechnology}
        />
      </div>
    </CardContent>
  );
});
