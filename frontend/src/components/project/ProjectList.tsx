'use client';

// Project List component - displays all projects with edit/delete actions

import { FolderOpen, Calendar, Users, TrendingUp, Edit, Trash2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useDeleteProject } from '@/hooks/use-project';
import { useTranslations } from '@/hooks/use-translations';

interface ProjectListProps {
  projects: any[];
  isLoading: boolean;
  onEdit: (project: any) => void;
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'ACTIVE': return 'bg-blue-100 text-blue-800';
    case 'STAGING': return 'bg-yellow-100 text-yellow-800';
    case 'ARCHIVED': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

const getCategoryColor = (category: string) => {
  switch (category) {
    case 'PRODUCTION': return 'bg-green-100 text-green-800';
    case 'DEMO': return 'bg-purple-100 text-purple-800';
    case 'INTERNAL': return 'bg-gray-100 text-gray-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export function ProjectList({ projects, isLoading, onEdit }: ProjectListProps) {
  const t = useTranslations('projects');
  const deleteProject = useDeleteProject();

  const handleDelete = async (projectId: string) => {
    if (confirm(t('deleteConfirm'))) {
      try {
        await deleteProject.mutateAsync(projectId);
      } catch (error) {
        console.error('Failed to delete project:', error);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-center">
          <div className="animate-spin size-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">{t('loading')}</p>
        </div>
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <Card className="border-dashed">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <FolderOpen className="size-12 text-muted-foreground mb-4" />
          <h4 className="font-medium text-foreground mb-2">{t('noProjects')}</h4>
          <p className="text-sm text-muted-foreground text-center">
            {t('noProjectsDescription')}
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {projects.map((project) => (
        <Card key={project.id}>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <CardTitle className="text-lg">
                    {project.name}
                  </CardTitle>
                  <Badge className={getStatusColor(project.status)}>
                    {t(`status.${project.status}`)}
                  </Badge>
                  <Badge variant="secondary" className={getCategoryColor(project.category)}>
                    {t(`category.${project.category}`)}
                  </Badge>
                </div>
                
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  {project.startDate && (
                    <div className="flex items-center gap-1">
                      <Calendar className="size-4" />
                      {project.startDate} - {project.endDate || 'Ongoing'}
                    </div>
                  )}
                  {project.client && (
                    <div className="flex items-center gap-1">
                      <Users className="size-4" />
                      {project.client}
                    </div>
                  )}
                  <div className="flex items-center gap-1">
                    <TrendingUp className="size-4" />
                    {t(`scale.${project.scale}`)}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onEdit(project)}
                >
                  <Edit className="size-4 mr-2" />
                  {t('edit')}
                </Button>
                <Button
                  variant="ghost-destructive"
                  size="sm"
                  onClick={() => handleDelete(project.id)}
                  disabled={deleteProject.isPending}
                >
                  <Trash2 className="size-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">{project.description}</p>
            
            {project.technologies && project.technologies.length > 0 && (
              <div className="mb-4">
                <h5 className="font-medium text-sm mb-2">Technologies:</h5>
                <div className="flex flex-wrap gap-2">
                  {project.technologies.map((tech: string, idx: number) => (
                    <Badge key={idx} variant="secondary">{tech}</Badge>
                  ))}
                </div>
              </div>
            )}
            
            {project.achievements && project.achievements.length > 0 && (
              <div className="mb-4">
                <h5 className="font-medium text-sm mb-2">Key Achievements:</h5>
                <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                  {project.achievements.map((achievement: string, idx: number) => (
                    <li key={idx}>{achievement}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {project.challenges && project.challenges.length > 0 && (
              <div>
                <h5 className="font-medium text-sm mb-2">Technical Challenges:</h5>
                <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                  {project.challenges.map((challenge: string, idx: number) => (
                    <li key={idx}>{challenge}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
