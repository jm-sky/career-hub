'use client';

// Projects step of the profile wizard - Modern 2025 architecture

import { useState, useCallback, useEffect, useRef } from 'react';
import { useFormContext, useFieldArray } from 'react-hook-form';
import { Plus, FolderOpen } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ProjectCard } from './projects/ProjectCard';
import { ProjectForm } from './projects/ProjectForm';

export function ProjectsStep() {
  const { control, watch } = useFormContext();
  
  // Modern 2025: Use useFieldArray for dynamic arrays
  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'projects'
  });

  // Watch projects to get real-time values for display
  const watchedProjects = watch('projects') || [];

  const [editingProject, setEditingProject] = useState<number | null>(null);
  const previousLength = useRef(fields.length);

  // Modern 2025: Auto-open newly added project
  useEffect(() => {
    if (fields.length > previousLength.current) {
      const newIndex = fields.length - 1;
      setEditingProject(newIndex);
    }
    previousLength.current = fields.length;
  }, [fields.length]);

  // Modern 2025: Memoized callbacks for performance
  const addProject = useCallback(() => {
    const newProject = {
      id: Date.now().toString(),
      name: '',
      description: '',
      status: 'PRODUCTION',
      category: 'PRODUCTION',
      startDate: '',
      endDate: '',
      technologies: [],
      achievements: [],
      challenges: [],
      client: '',
      scale: 'MEDIUM',
    };
    append(newProject);
  }, [append]);

  // Helper to update nested arrays
  const updateProjectField = useCallback((projectIndex: number, field: string, value: any) => {
    const currentProject = fields[projectIndex];
    if (currentProject) {
      update(projectIndex, { ...currentProject, [field]: value });
    }
  }, [fields, update]);

  // Array field handlers
  const createArrayHandler = useCallback((projectIndex: number, fieldName: string) => ({
    add: (value: string) => {
      const project = watchedProjects[projectIndex];
      if (project) {
        updateProjectField(projectIndex, fieldName, [...(project[fieldName] || []), value]);
      }
    },
    remove: (itemIndex: number) => {
      const project = watchedProjects[projectIndex];
      if (project) {
        updateProjectField(projectIndex, fieldName, (project[fieldName] || []).filter((_: any, i: number) => i !== itemIndex));
      }
    }
  }), [watchedProjects, updateProjectField]);

  // Helper functions for colors
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE': return 'bg-green-100 text-green-800';
      case 'STAGING': return 'bg-yellow-100 text-yellow-800';
      case 'ARCHIVED': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'PRODUCTION': return 'bg-blue-100 text-blue-800';
      case 'DEMO': return 'bg-purple-100 text-purple-800';
      case 'INTERNAL': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-semibold mb-1">Notable Projects</h3>
          <p className="text-sm text-gray-600">
            Showcase your most significant projects and technical achievements
          </p>
        </div>
        <Button onClick={addProject} size="sm">
          <Plus className="size-4 mr-2" />
          Add Project
        </Button>
      </div>

      {fields.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <FolderOpen className="h-12 w-12 text-gray-400 mb-4" />
            <h4 className="font-medium text-gray-900 mb-2">No projects added yet</h4>
            <p className="text-sm text-gray-500 text-center mb-4">
              Highlight your technical projects, open source contributions, and achievements
            </p>
            <Button onClick={addProject}>
              <Plus className="size-4 mr-2" />
              Add Your First Project
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {fields.map((field, index: number) => {
            const project = watchedProjects[index] || field;
            const handlers = createArrayHandler(index, '');
            
            return (
              <Card key={field.id} className={editingProject === index ? 'ring-2 ring-primary' : ''}>
                <ProjectCard
                  project={project}
                  index={index}
                  isEditing={editingProject === index}
                  onToggleEdit={() => setEditingProject(editingProject === index ? null : index)}
                  onRemove={() => remove(index)}
                  getStatusColor={getStatusColor}
                  getCategoryColor={getCategoryColor}
                />
                
                {editingProject === index && (
                  <ProjectForm
                    index={index}
                    project={project}
                    onAddAchievement={(value) => {
                      const h = createArrayHandler(index, 'achievements');
                      h.add(value);
                    }}
                    onRemoveAchievement={(itemIndex) => {
                      const h = createArrayHandler(index, 'achievements');
                      h.remove(itemIndex);
                    }}
                    onAddChallenge={(value) => {
                      const h = createArrayHandler(index, 'challenges');
                      h.add(value);
                    }}
                    onRemoveChallenge={(itemIndex) => {
                      const h = createArrayHandler(index, 'challenges');
                      h.remove(itemIndex);
                    }}
                    onAddTechnology={(value) => {
                      const h = createArrayHandler(index, 'technologies');
                      h.add(value);
                    }}
                    onRemoveTechnology={(itemIndex) => {
                      const h = createArrayHandler(index, 'technologies');
                      h.remove(itemIndex);
                    }}
                  />
                )}
              </Card>
            );
          })}
        </div>
      )}

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Tips for great project entries:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Include both personal and professional projects</li>
          <li>• Highlight technical complexity and scale</li>
          <li>• Mention specific technologies and frameworks</li>
          <li>• Quantify impact (users served, performance improvements, etc.)</li>
          <li>• Include challenges you overcame and lessons learned</li>
        </ul>
      </div>
    </div>
  );
}