'use client';

// Project Dialog - Add/Edit project with modern 2025 form patterns

import { useEffect, useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { X, Plus } from 'lucide-react';

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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { useCreateProject, useUpdateProject } from '@/hooks/use-project';
import { getErrorMessage } from '@/lib/error-guards';

// Modern 2025: Zod schema for validation
const ProjectSchema = z.object({
  name: z.string().min(1, 'Project name is required').max(200, 'Project name too long'),
  description: z.string().min(1, 'Description is required').max(2000, 'Description too long'),
  status: z.enum(['ACTIVE', 'STAGING', 'ARCHIVED']).default('ACTIVE'),
  category: z.enum(['DEMO', 'INTERNAL', 'PRODUCTION']).default('PRODUCTION'),
  startDate: z.string().optional(),
  endDate: z.string().optional(),
  technologies: z.array(z.string()).default([]),
  achievements: z.array(z.string()).default([]),
  challenges: z.array(z.string()).default([]),
  client: z.string().max(200, 'Client name too long').optional(),
  scale: z.enum(['SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE']).default('MEDIUM'),
});

type ProjectFormData = z.infer<typeof ProjectSchema>;

interface ProjectDialogProps {
  isOpen: boolean;
  onClose: () => void;
  project: any | null;
  profileId: string;
}

export function ProjectDialog({ isOpen, onClose, project, profileId }: ProjectDialogProps) {
  const createProject = useCreateProject();
  const updateProject = useUpdateProject();
  const isEditing = !!project;

  const [newTechnology, setNewTechnology] = useState('');
  const [newAchievement, setNewAchievement] = useState('');
  const [newChallenge, setNewChallenge] = useState('');

  // Modern 2025: React Hook Form configuration
  const {
    register,
    handleSubmit,
    control,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<ProjectFormData>({
    resolver: zodResolver(ProjectSchema),
    mode: 'onChange',
    reValidateMode: 'onChange',
    shouldFocusError: true,
    defaultValues: {
      name: '',
      description: '',
      status: 'ACTIVE',
      category: 'PRODUCTION',
      startDate: '',
      endDate: '',
      technologies: [],
      achievements: [],
      challenges: [],
      client: '',
      scale: 'MEDIUM',
    },
  });

  const technologies = watch('technologies') || [];
  const achievements = watch('achievements') || [];
  const challenges = watch('challenges') || [];

  // Load project data when editing
  useEffect(() => {
    if (project) {
      reset({
        name: project.name || '',
        description: project.description || '',
        status: project.status || 'ACTIVE',
        category: project.category || 'PRODUCTION',
        startDate: project.startDate || '',
        endDate: project.endDate || '',
        technologies: project.technologies || [],
        achievements: project.achievements || [],
        challenges: project.challenges || [],
        client: project.client || '',
        scale: project.scale || 'MEDIUM',
      });
    } else {
      reset({
        name: '',
        description: '',
        status: 'ACTIVE',
        category: 'PRODUCTION',
        startDate: '',
        endDate: '',
        technologies: [],
        achievements: [],
        challenges: [],
        client: '',
        scale: 'MEDIUM',
      });
    }
  }, [project, reset]);

  const addTechnology = () => {
    if (newTechnology.trim()) {
      setValue('technologies', [...technologies, newTechnology.trim()]);
      setNewTechnology('');
    }
  };

  const removeTechnology = (index: number) => {
    setValue('technologies', technologies.filter((_, i) => i !== index));
  };

  const addAchievement = () => {
    if (newAchievement.trim()) {
      setValue('achievements', [...achievements, newAchievement.trim()]);
      setNewAchievement('');
    }
  };

  const removeAchievement = (index: number) => {
    setValue('achievements', achievements.filter((_, i) => i !== index));
  };

  const addChallenge = () => {
    if (newChallenge.trim()) {
      setValue('challenges', [...challenges, newChallenge.trim()]);
      setNewChallenge('');
    }
  };

  const removeChallenge = (index: number) => {
    setValue('challenges', challenges.filter((_, i) => i !== index));
  };

  const onSubmit = async (data: ProjectFormData) => {
    try {
      if (isEditing) {
        await updateProject.mutateAsync({
          projectId: project.id,
          projectData: data,
        });
      } else {
        await createProject.mutateAsync({
          profileId,
          projectData: data,
        });
      }
      onClose();
    } catch (error) {
      console.error('Failed to save project:', error);
      alert(getErrorMessage(error));
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{isEditing ? 'Edit Project' : 'Add Project'}</DialogTitle>
          <DialogDescription>
            {isEditing
              ? 'Update your project details'
              : 'Add a new project to your profile'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Name & Client */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name" required>
                Project Name
              </Label>
              <Input
                id="name"
                placeholder="e.g., E-commerce Platform"
                {...register('name')}
              />
              {errors.name && (
                <p className="text-sm text-destructive">{errors.name.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="client">Client/Company</Label>
              <Input
                id="client"
                placeholder="e.g., Tech Startup Inc."
                {...register('client')}
              />
              {errors.client && (
                <p className="text-sm text-destructive">{errors.client.message}</p>
              )}
            </div>
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description" required>
              Description
            </Label>
            <Textarea
              id="description"
              placeholder="Describe what the project does, its purpose, and key features..."
              rows={4}
              {...register('description')}
            />
            {errors.description && (
              <p className="text-sm text-destructive">{errors.description.message}</p>
            )}
          </div>

          {/* Status, Category, Scale */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label>Status</Label>
              <Controller
                name="status"
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
                name="category"
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
                name="scale"
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

          {/* Start Date & End Date */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date</Label>
              <Input
                id="startDate"
                type="month"
                {...register('startDate')}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="endDate">End Date</Label>
              <Input
                id="endDate"
                type="month"
                {...register('endDate')}
              />
            </div>
          </div>

          {/* Technologies */}
          <div className="space-y-2">
            <Label>Technologies Used</Label>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., React, Node.js, PostgreSQL"
                value={newTechnology}
                onChange={(e) => setNewTechnology(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTechnology())}
              />
              <Button type="button" onClick={addTechnology} size="sm">
                <Plus className="size-4" />
              </Button>
            </div>
            {technologies.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {technologies.map((tech, idx) => (
                  <Badge key={idx} variant="secondary" className="gap-1">
                    {tech}
                    <X
                      className="size-3 cursor-pointer hover:text-destructive"
                      onClick={() => removeTechnology(idx)}
                    />
                  </Badge>
                ))}
              </div>
            )}
          </div>

          {/* Achievements */}
          <div className="space-y-2">
            <Label>Key Achievements</Label>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Reduced load time by 50%"
                value={newAchievement}
                onChange={(e) => setNewAchievement(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addAchievement())}
              />
              <Button type="button" onClick={addAchievement} size="sm">
                <Plus className="size-4" />
              </Button>
            </div>
            {achievements.length > 0 && (
              <ul className="list-disc list-inside space-y-1 text-sm mt-2">
                {achievements.map((achievement, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="flex-1">{achievement}</span>
                    <X
                      className="size-4 cursor-pointer hover:text-destructive flex-shrink-0"
                      onClick={() => removeAchievement(idx)}
                    />
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Challenges */}
          <div className="space-y-2">
            <Label>Technical Challenges</Label>
            <div className="flex gap-2">
              <Input
                placeholder="e.g., Implemented real-time sync across devices"
                value={newChallenge}
                onChange={(e) => setNewChallenge(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addChallenge())}
              />
              <Button type="button" onClick={addChallenge} size="sm">
                <Plus className="size-4" />
              </Button>
            </div>
            {challenges.length > 0 && (
              <ul className="list-disc list-inside space-y-1 text-sm mt-2">
                {challenges.map((challenge, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="flex-1">{challenge}</span>
                    <X
                      className="size-4 cursor-pointer hover:text-destructive flex-shrink-0"
                      onClick={() => removeChallenge(idx)}
                    />
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : isEditing ? 'Update' : 'Add Project'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
