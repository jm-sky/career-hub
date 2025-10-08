'use client';

// Project card component for displaying project in collapsed mode

import { memo } from 'react';
import { Trash2, Calendar, Users, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface ProjectCardProps {
  project: any;
  index: number;
  isEditing: boolean;
  onToggleEdit: () => void;
  onRemove: () => void;
  getStatusColor: (status: string) => string;
  getCategoryColor: (category: string) => string;
}

export const ProjectCard = memo(function ProjectCard({
  project,
  index,
  isEditing,
  onToggleEdit,
  onRemove,
  getStatusColor,
  getCategoryColor
}: ProjectCardProps) {
  return (
    <CardHeader className="pb-3">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <CardTitle className="text-base">
              {project.name || `Project ${index + 1}`}
            </CardTitle>
            <Badge className={getStatusColor(project.status)}>
              {project.status}
            </Badge>
            <Badge variant="secondary" className={getCategoryColor(project.category)}>
              {project.category}
            </Badge>
          </div>
          
          {project.startDate && (
            <div className="flex items-center gap-4 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                <span>{project.startDate}</span>
                {project.endDate && <span> - {project.endDate}</span>}
                {!project.endDate && <span> - Ongoing</span>}
              </div>
              {project.client && (
                <div className="flex items-center gap-1">
                  <Users className="h-3 w-3" />
                  {project.client}
                </div>
              )}
              <div className="flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                {project.scale}
              </div>
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={onToggleEdit}
          >
            {isEditing ? 'Done' : 'Edit'}
          </Button>
          <Button
            type="button"
            variant="ghost-destructive"
            size="sm"
            onClick={onRemove}
          >
            <Trash2 className="size-4" />
          </Button>
        </div>
      </div>
    </CardHeader>
  );
});
