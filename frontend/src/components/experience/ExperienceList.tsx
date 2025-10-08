'use client';

// Experience List component - displays all experiences with edit/delete actions

import { Briefcase, Calendar, MapPin, Edit, Trash2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useDeleteExperience } from '@/hooks/use-experience';

interface ExperienceListProps {
  experiences: any[];
  isLoading: boolean;
  onEdit: (experience: any) => void;
}

export function ExperienceList({ experiences, isLoading, onEdit }: ExperienceListProps) {
  const deleteExperience = useDeleteExperience();

  const handleDelete = async (experienceId: string) => {
    if (confirm('Are you sure you want to delete this experience?')) {
      try {
        await deleteExperience.mutateAsync(experienceId);
      } catch (error) {
        console.error('Failed to delete experience:', error);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[200px]">
        <div className="text-center">
          <div className="animate-spin size-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading experiences...</p>
        </div>
      </div>
    );
  }

  if (experiences.length === 0) {
    return (
      <Card className="border-dashed">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <Briefcase className="size-12 text-muted-foreground mb-4" />
          <h4 className="font-medium text-foreground mb-2">No experience added yet</h4>
          <p className="text-sm text-muted-foreground text-center">
            Start building your professional profile by adding your work experience
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {experiences.map((experience) => (
        <Card key={experience.id}>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <CardTitle className="text-lg">
                  {experience.position}
                </CardTitle>
                <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
                  <div className="flex items-center gap-1">
                    <Briefcase className="size-4" />
                    {experience.company}
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="size-4" />
                    {experience.startDate}
                    {experience.isCurrent ? (
                      <Badge variant="secondary" className="ml-2">Current</Badge>
                    ) : (
                      experience.endDate && ` - ${experience.endDate}`
                    )}
                  </div>
                  {experience.location && (
                    <div className="flex items-center gap-1">
                      <MapPin className="size-4" />
                      {experience.location}
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onEdit(experience)}
                >
                  <Edit className="size-4 mr-2" />
                  Edit
                </Button>
                <Button
                  variant="ghost-destructive"
                  size="sm"
                  onClick={() => handleDelete(experience.id)}
                  disabled={deleteExperience.isPending}
                >
                  <Trash2 className="size-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          {experience.description && (
            <CardContent>
              <p className="text-sm text-muted-foreground">{experience.description}</p>
              
              {experience.responsibilities && experience.responsibilities.length > 0 && (
                <div className="mt-4">
                  <h5 className="font-medium text-sm mb-2">Key Responsibilities:</h5>
                  <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                    {experience.responsibilities.map((resp: string, idx: number) => (
                      <li key={idx}>{resp}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {experience.technologies && experience.technologies.length > 0 && (
                <div className="mt-4">
                  <h5 className="font-medium text-sm mb-2">Technologies:</h5>
                  <div className="flex flex-wrap gap-2">
                    {experience.technologies.map((tech: string, idx: number) => (
                      <Badge key={idx} variant="secondary">{tech}</Badge>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          )}
        </Card>
      ))}
    </div>
  );
}

