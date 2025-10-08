'use client';

// Experience Management - CRUD interface for managing work experiences

import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useMyProfile } from '@/hooks/use-profile';
import { useProfileExperiences } from '@/hooks/use-experience';
import { ExperienceList } from './ExperienceList';
import { ExperienceDialog } from './ExperienceDialog';

export function ExperienceManagement() {
  const { data: profile, isLoading: profileLoading } = useMyProfile();
  const { data: experiences, isLoading: experiencesLoading } = useProfileExperiences(profile?.id || '');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingExperience, setEditingExperience] = useState<any | null>(null);

  const handleAdd = () => {
    setEditingExperience(null);
    setIsDialogOpen(true);
  };

  const handleEdit = (experience: any) => {
    setEditingExperience(experience);
    setIsDialogOpen(true);
  };

  const handleClose = () => {
    setIsDialogOpen(false);
    setEditingExperience(null);
  };

  if (profileLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin size-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <p className="text-muted-foreground">Please create a profile first.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="container mx-auto p-8 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Work Experience</h1>
          <p className="text-muted-foreground">
            Manage your professional work experience and career history
          </p>
        </div>
        <Button onClick={handleAdd} size="sm">
          <Plus className="size-4 mr-2" />
          Add Experience
        </Button>
      </div>

      {/* Experience List */}
      <ExperienceList
        experiences={experiences || []}
        isLoading={experiencesLoading}
        onEdit={handleEdit}
      />

      {/* Add/Edit Dialog */}
      <ExperienceDialog
        isOpen={isDialogOpen}
        onClose={handleClose}
        experience={editingExperience}
        profileId={profile.id}
      />
    </div>
  );
}

