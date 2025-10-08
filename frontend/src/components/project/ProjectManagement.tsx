'use client';

// Project Management - CRUD interface for managing projects

import { useState } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { useMyProfile } from '@/hooks/use-profile';
import { useProfileProjects } from '@/hooks/use-project';
import { ProjectList } from './ProjectList';
import { ProjectDialog } from './ProjectDialog';

export function ProjectManagement() {
  const { data: profile, isLoading: profileLoading } = useMyProfile();
  const { data: projects, isLoading: projectsLoading } = useProfileProjects(profile?.id || '');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<any | null>(null);

  const handleAdd = () => {
    setEditingProject(null);
    setIsDialogOpen(true);
  };

  const handleEdit = (project: any) => {
    setEditingProject(project);
    setIsDialogOpen(true);
  };

  const handleClose = () => {
    setIsDialogOpen(false);
    setEditingProject(null);
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
          <h1 className="text-3xl font-bold mb-2">Projects</h1>
          <p className="text-muted-foreground">
            Manage your notable projects and technical achievements
          </p>
        </div>
        <Button onClick={handleAdd} size="sm">
          <Plus className="size-4 mr-2" />
          Add Project
        </Button>
      </div>

      {/* Project List */}
      <ProjectList
        projects={projects || []}
        isLoading={projectsLoading}
        onEdit={handleEdit}
      />

      {/* Add/Edit Dialog */}
      <ProjectDialog
        isOpen={isDialogOpen}
        onClose={handleClose}
        project={editingProject}
        profileId={profile.id}
      />
    </div>
  );
}
