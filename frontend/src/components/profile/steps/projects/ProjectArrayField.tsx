'use client';

// Reusable component for project array fields (achievements, challenges, technologies)

import { useState, memo } from 'react';
import { Plus, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface ProjectArrayFieldProps {
  label: string;
  placeholder: string;
  items: string[];
  onAdd: (value: string) => void;
  onRemove: (index: number) => void;
  bgColor?: string;
}

export const ProjectArrayField = memo(function ProjectArrayField({
  label,
  placeholder,
  items = [],
  onAdd,
  onRemove,
  bgColor = 'bg-gray-50'
}: ProjectArrayFieldProps) {
  const [newValue, setNewValue] = useState('');

  const handleAdd = () => {
    if (newValue.trim()) {
      onAdd(newValue.trim());
      setNewValue('');
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
      <Label>{label}</Label>
      <div className="space-y-2">
        {items.map((item, itemIndex) => (
          <div key={itemIndex} className="flex items-center gap-2">
            <div className={`flex-1 p-2 ${bgColor} rounded text-sm`}>{item}</div>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => onRemove(itemIndex)}
              className="text-destructive"
            >
              <Trash2 className="h-3 w-3" />
            </Button>
          </div>
        ))}
        <div className="flex gap-2">
          <Input
            placeholder={placeholder}
            value={newValue}
            onChange={(e) => setNewValue(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <Button type="button" size="sm" onClick={handleAdd}>
            <Plus className="h-3 w-3" />
          </Button>
        </div>
      </div>
    </div>
  );
});
