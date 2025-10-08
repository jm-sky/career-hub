'use client';

// Technologies component with badge layout

import { useState, memo } from 'react';
import { Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';

interface ProjectTechnologiesProps {
  technologies: string[];
  onAdd: (value: string) => void;
  onRemove: (index: number) => void;
}

export const ProjectTechnologies = memo(function ProjectTechnologies({
  technologies = [],
  onAdd,
  onRemove
}: ProjectTechnologiesProps) {
  const [newTechnology, setNewTechnology] = useState('');

  const handleAdd = () => {
    if (newTechnology.trim()) {
      onAdd(newTechnology.trim());
      setNewTechnology('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAdd();
    }
  };

  return (
    <div className="space-y-2">
      <Label>Technologies Used</Label>
      <div className="flex flex-wrap gap-2 mb-2">
        {technologies.map((tech, techIndex) => (
          <Badge key={techIndex} variant="secondary" className="flex items-center gap-1">
            {tech}
            <button
              type="button"
              onClick={() => onRemove(techIndex)}
              className="ml-1 text-destructive hover:text-red-800 font-bold"
            >
              ×
            </button>
          </Badge>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          placeholder="Add a technology..."
          value={newTechnology}
          onChange={(e) => setNewTechnology(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <Button type="button" size="sm" onClick={handleAdd}>
          <Plus className="h-3 w-3" />
        </Button>
      </div>
    </div>
  );
});
