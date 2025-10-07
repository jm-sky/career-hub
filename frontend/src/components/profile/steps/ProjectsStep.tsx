'use client';

// Projects step of the profile wizard

import { useState } from 'react';
import { UseFormRegister, UseFormSetValue, UseFormWatch, FieldErrors } from 'react-hook-form';
import { Plus, Trash2, FolderOpen, Calendar, Users, TrendingUp } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface ProjectsStepProps {
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  watch: UseFormWatch<any>;
  errors: FieldErrors<any>;
}

interface Project {
  id: string;
  name: string;
  description: string;
  status: 'ACTIVE' | 'STAGING' | 'ARCHIVED';
  category: 'DEMO' | 'INTERNAL' | 'PRODUCTION';
  startDate?: string;
  endDate?: string;
  technologies: string[];
  achievements: string[];
  challenges: string[];
  client?: string;
  scale: 'SMALL' | 'MEDIUM' | 'LARGE' | 'ENTERPRISE';
}

export function ProjectsStep({ register, setValue, watch, errors }: ProjectsStepProps) {
  const projects = watch('projects') || [];
  const [editingProject, setEditingProject] = useState<string | null>(null);
  const [newAchievement, setNewAchievement] = useState('');
  const [newChallenge, setNewChallenge] = useState('');
  const [newTechnology, setNewTechnology] = useState('');

  const addProject = () => {
    const newProject: Project = {
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
    
    setValue('projects', [...projects, newProject]);
    setEditingProject(newProject.id);
  };

  const removeProject = (id: string) => {
    setValue('projects', projects.filter((project: Project) => project.id !== id));
    if (editingProject === id) {
      setEditingProject(null);
    }
  };

  const updateProject = (id: string, field: keyof Project, value: any) => {
    setValue('projects', projects.map((project: Project) => 
      project.id === id ? { ...project, [field]: value } : project
    ));
  };

  const addAchievement = (projectId: string) => {
    if (!newAchievement.trim()) return;
    
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'achievements', [...project.achievements, newAchievement]);
      setNewAchievement('');
    }
  };

  const removeAchievement = (projectId: string, index: number) => {
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'achievements', project.achievements.filter((_, i) => i !== index));
    }
  };

  const addChallenge = (projectId: string) => {
    if (!newChallenge.trim()) return;
    
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'challenges', [...project.challenges, newChallenge]);
      setNewChallenge('');
    }
  };

  const removeChallenge = (projectId: string, index: number) => {
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'challenges', project.challenges.filter((_, i) => i !== index));
    }
  };

  const addTechnology = (projectId: string) => {
    if (!newTechnology.trim()) return;
    
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'technologies', [...project.technologies, newTechnology]);
      setNewTechnology('');
    }
  };

  const removeTechnology = (projectId: string, index: number) => {
    const project = projects.find((p: Project) => p.id === projectId);
    if (project) {
      updateProject(projectId, 'technologies', project.technologies.filter((_, i) => i !== index));
    }
  };

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
      case 'INTERNAL': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium">Notable Projects</h3>
          <p className="text-sm text-gray-600">
            Showcase your most significant projects and technical achievements
          </p>
        </div>
        <Button onClick={addProject} size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Add Project
        </Button>
      </div>

      {projects.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <FolderOpen className="h-12 w-12 text-gray-400 mb-4" />
            <h4 className="font-medium text-gray-900 mb-2">No projects added yet</h4>
            <p className="text-sm text-gray-500 text-center mb-4">
              Highlight your technical projects, open source contributions, and achievements
            </p>
            <Button onClick={addProject}>
              <Plus className="h-4 w-4 mr-2" />
              Add Your First Project
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {projects.map((project: Project, index: number) => (
            <Card key={project.id} className={editingProject === project.id ? 'ring-2 ring-primary' : ''}>
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
                          {project.startDate} - {project.endDate || 'Ongoing'}
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
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingProject(editingProject === project.id ? null : project.id)}
                    >
                      {editingProject === project.id ? 'Done' : 'Edit'}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeProject(project.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              
              {editingProject === project.id && (
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`project-${project.id}-name`}>Project Name *</Label>
                      <Input
                        id={`project-${project.id}-name`}
                        placeholder="e.g., E-commerce Platform"
                        value={project.name}
                        onChange={(e) => updateProject(project.id, 'name', e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`project-${project.id}-client`}>Client/Company</Label>
                      <Input
                        id={`project-${project.id}-client`}
                        placeholder="e.g., Tech Startup Inc."
                        value={project.client || ''}
                        onChange={(e) => updateProject(project.id, 'client', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`project-${project.id}-description`}>Description *</Label>
                    <Textarea
                      id={`project-${project.id}-description`}
                      placeholder="Describe what the project does, its purpose, and key features..."
                      value={project.description}
                      onChange={(e) => updateProject(project.id, 'description', e.target.value)}
                      rows={4}
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <Label>Status</Label>
                      <Select
                        value={project.status}
                        onValueChange={(value) => updateProject(project.id, 'status', value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="ACTIVE">Active</SelectItem>
                          <SelectItem value="STAGING">Staging</SelectItem>
                          <SelectItem value="ARCHIVED">Archived</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Category</Label>
                      <Select
                        value={project.category}
                        onValueChange={(value) => updateProject(project.id, 'category', value)}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="PRODUCTION">Production</SelectItem>
                          <SelectItem value="DEMO">Demo</SelectItem>
                          <SelectItem value="INTERNAL">Internal</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Scale</Label>
                      <Select
                        value={project.scale}
                        onValueChange={(value) => updateProject(project.id, 'scale', value)}
                      >
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
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`project-${project.id}-start`}>Start Date</Label>
                      <Input
                        id={`project-${project.id}-start`}
                        type="month"
                        value={project.startDate || ''}
                        onChange={(e) => updateProject(project.id, 'startDate', e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`project-${project.id}-end`}>End Date</Label>
                      <Input
                        id={`project-${project.id}-end`}
                        type="month"
                        value={project.endDate || ''}
                        onChange={(e) => updateProject(project.id, 'endDate', e.target.value)}
                      />
                    </div>
                  </div>

                  {/* Achievements */}
                  <div className="space-y-2">
                    <Label>Key Achievements</Label>
                    <div className="space-y-2">
                      {project.achievements.map((ach, achIndex) => (
                        <div key={achIndex} className="flex items-center gap-2">
                          <div className="flex-1 p-2 bg-green-50 rounded text-sm">{ach}</div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeAchievement(project.id, achIndex)}
                            className="text-red-600"
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                      <div className="flex gap-2">
                        <Input
                          placeholder="Add an achievement..."
                          value={newAchievement}
                          onChange={(e) => setNewAchievement(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && addAchievement(project.id)}
                        />
                        <Button size="sm" onClick={() => addAchievement(project.id)}>
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Challenges */}
                  <div className="space-y-2">
                    <Label>Technical Challenges</Label>
                    <div className="space-y-2">
                      {project.challenges.map((challenge, challengeIndex) => (
                        <div key={challengeIndex} className="flex items-center gap-2">
                          <div className="flex-1 p-2 bg-yellow-50 rounded text-sm">{challenge}</div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeChallenge(project.id, challengeIndex)}
                            className="text-red-600"
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                      <div className="flex gap-2">
                        <Input
                          placeholder="Add a challenge you overcame..."
                          value={newChallenge}
                          onChange={(e) => setNewChallenge(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && addChallenge(project.id)}
                        />
                        <Button size="sm" onClick={() => addChallenge(project.id)}>
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Technologies */}
                  <div className="space-y-2">
                    <Label>Technologies Used</Label>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {project.technologies.map((tech, techIndex) => (
                        <Badge key={techIndex} variant="secondary" className="flex items-center gap-1">
                          {tech}
                          <button
                            onClick={() => removeTechnology(project.id, techIndex)}
                            className="ml-1 text-red-600 hover:text-red-800"
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
                        onKeyPress={(e) => e.key === 'Enter' && addTechnology(project.id)}
                      />
                      <Button size="sm" onClick={() => addTechnology(project.id)}>
                        <Plus className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
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
