'use client';

// Work Experience step of the profile wizard

import { useState } from 'react';
import { UseFormRegister, UseFormSetValue, UseFormWatch, FieldErrors } from 'react-hook-form';
import { Plus, Trash2, Calendar, Building, MapPin } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';

interface ExperienceStepProps {
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  watch: UseFormWatch<any>;
  errors: FieldErrors<any>;
}

interface Experience {
  id: string;
  company: string;
  position: string;
  startDate: string;
  endDate?: string;
  isCurrent: boolean;
  description?: string;
  responsibilities: string[];
  achievements: string[];
  technologies: string[];
}

export function ExperienceStep({ register, setValue, watch, errors }: ExperienceStepProps) {
  const experiences = watch('experiences') || [];
  const [editingExperience, setEditingExperience] = useState<string | null>(null);
  const [newResponsibility, setNewResponsibility] = useState('');
  const [newAchievement, setNewAchievement] = useState('');
  const [newTechnology, setNewTechnology] = useState('');

  const addExperience = () => {
    const newExp: Experience = {
      id: Date.now().toString(),
      company: '',
      position: '',
      startDate: '',
      endDate: '',
      isCurrent: false,
      description: '',
      responsibilities: [],
      achievements: [],
      technologies: [],
    };
    
    setValue('experiences', [...experiences, newExp]);
    setEditingExperience(newExp.id);
  };

  const removeExperience = (id: string) => {
    setValue('experiences', experiences.filter((exp: Experience) => exp.id !== id));
    if (editingExperience === id) {
      setEditingExperience(null);
    }
  };

  const updateExperience = (id: string, field: keyof Experience, value: any) => {
    setValue('experiences', experiences.map((exp: Experience) => 
      exp.id === id ? { ...exp, [field]: value } : exp
    ));
  };

  const addResponsibility = (expId: string) => {
    if (!newResponsibility.trim()) return;
    
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'responsibilities', [...exp.responsibilities, newResponsibility]);
      setNewResponsibility('');
    }
  };

  const removeResponsibility = (expId: string, index: number) => {
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'responsibilities', exp.responsibilities.filter((_, i) => i !== index));
    }
  };

  const addAchievement = (expId: string) => {
    if (!newAchievement.trim()) return;
    
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'achievements', [...exp.achievements, newAchievement]);
      setNewAchievement('');
    }
  };

  const removeAchievement = (expId: string, index: number) => {
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'achievements', exp.achievements.filter((_, i) => i !== index));
    }
  };

  const addTechnology = (expId: string) => {
    if (!newTechnology.trim()) return;
    
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'technologies', [...exp.technologies, newTechnology]);
      setNewTechnology('');
    }
  };

  const removeTechnology = (expId: string, index: number) => {
    const exp = experiences.find((e: Experience) => e.id === expId);
    if (exp) {
      updateExperience(expId, 'technologies', exp.technologies.filter((_, i) => i !== index));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium">Work Experience</h3>
          <p className="text-sm text-gray-600">
            Add your professional work experience, starting with the most recent
          </p>
        </div>
        <Button onClick={addExperience} size="sm">
          <Plus className="h-4 w-4 mr-2" />
          Add Experience
        </Button>
      </div>

      {experiences.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Building className="h-12 w-12 text-gray-400 mb-4" />
            <h4 className="font-medium text-gray-900 mb-2">No experience added yet</h4>
            <p className="text-sm text-gray-500 text-center mb-4">
              Start building your professional profile by adding your work experience
            </p>
            <Button onClick={addExperience}>
              <Plus className="h-4 w-4 mr-2" />
              Add Your First Experience
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {experiences.map((exp: Experience, index: number) => (
            <Card key={exp.id} className={editingExperience === exp.id ? 'ring-2 ring-primary' : ''}>
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-base">
                      {exp.position || `Experience ${index + 1}`}
                      {exp.company && ` at ${exp.company}`}
                    </CardTitle>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                      {exp.startDate && (
                        <div className="flex items-center gap-1">
                          <Calendar className="h-3 w-3" />
                          {exp.startDate} - {exp.isCurrent ? 'Present' : exp.endDate || 'Present'}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingExperience(editingExperience === exp.id ? null : exp.id)}
                    >
                      {editingExperience === exp.id ? 'Done' : 'Edit'}
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeExperience(exp.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              
              {editingExperience === exp.id && (
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${exp.id}-position`}>Position *</Label>
                      <Input
                        id={`exp-${exp.id}-position`}
                        placeholder="e.g., Senior Software Engineer"
                        value={exp.position}
                        onChange={(e) => updateExperience(exp.id, 'position', e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${exp.id}-company`}>Company *</Label>
                      <Input
                        id={`exp-${exp.id}-company`}
                        placeholder="e.g., Tech Corp"
                        value={exp.company}
                        onChange={(e) => updateExperience(exp.id, 'company', e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${exp.id}-start`}>Start Date *</Label>
                      <Input
                        id={`exp-${exp.id}-start`}
                        type="month"
                        value={exp.startDate}
                        onChange={(e) => updateExperience(exp.id, 'startDate', e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor={`exp-${exp.id}-end`}>End Date</Label>
                      <div className="flex items-center gap-2">
                        <Input
                          id={`exp-${exp.id}-end`}
                          type="month"
                          value={exp.endDate || ''}
                          onChange={(e) => updateExperience(exp.id, 'endDate', e.target.value)}
                          disabled={exp.isCurrent}
                        />
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            id={`exp-${exp.id}-current`}
                            checked={exp.isCurrent}
                            onCheckedChange={(checked) => {
                              const isChecked = checked === true;
                              updateExperience(exp.id, 'isCurrent', isChecked);
                              if (isChecked) {
                                updateExperience(exp.id, 'endDate', '');
                              }
                            }}
                          />
                          <Label htmlFor={`exp-${exp.id}-current`} className="text-sm">
                            Currently working here
                          </Label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor={`exp-${exp.id}-description`}>Description</Label>
                    <Textarea
                      id={`exp-${exp.id}-description`}
                      placeholder="Brief description of your role and responsibilities..."
                      value={exp.description || ''}
                      onChange={(e) => updateExperience(exp.id, 'description', e.target.value)}
                      rows={3}
                    />
                  </div>

                  {/* Responsibilities */}
                  <div className="space-y-2">
                    <Label>Key Responsibilities</Label>
                    <div className="space-y-2">
                      {exp.responsibilities.map((resp, respIndex) => (
                        <div key={respIndex} className="flex items-center gap-2">
                          <div className="flex-1 p-2 bg-gray-50 rounded text-sm">{resp}</div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeResponsibility(exp.id, respIndex)}
                            className="text-red-600"
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                      <div className="flex gap-2">
                        <Input
                          placeholder="Add a responsibility..."
                          value={newResponsibility}
                          onChange={(e) => setNewResponsibility(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && addResponsibility(exp.id)}
                        />
                        <Button size="sm" onClick={() => addResponsibility(exp.id)}>
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Achievements */}
                  <div className="space-y-2">
                    <Label>Key Achievements</Label>
                    <div className="space-y-2">
                      {exp.achievements.map((ach, achIndex) => (
                        <div key={achIndex} className="flex items-center gap-2">
                          <div className="flex-1 p-2 bg-green-50 rounded text-sm">{ach}</div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeAchievement(exp.id, achIndex)}
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
                          onKeyPress={(e) => e.key === 'Enter' && addAchievement(exp.id)}
                        />
                        <Button size="sm" onClick={() => addAchievement(exp.id)}>
                          <Plus className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>

                  {/* Technologies */}
                  <div className="space-y-2">
                    <Label>Technologies Used</Label>
                    <div className="flex flex-wrap gap-2 mb-2">
                      {exp.technologies.map((tech, techIndex) => (
                        <Badge key={techIndex} variant="secondary" className="flex items-center gap-1">
                          {tech}
                          <button
                            onClick={() => removeTechnology(exp.id, techIndex)}
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
                        onKeyPress={(e) => e.key === 'Enter' && addTechnology(exp.id)}
                      />
                      <Button size="sm" onClick={() => addTechnology(exp.id)}>
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
        <h4 className="font-medium text-blue-900 mb-2">💡 Tips for great experience entries:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Start with action verbs (Led, Developed, Implemented, etc.)</li>
          <li>• Quantify your achievements with numbers and percentages</li>
          <li>• Focus on results and impact, not just responsibilities</li>
          <li>• Include relevant technologies and tools you used</li>
          <li>• Keep descriptions concise but impactful</li>
        </ul>
      </div>
    </div>
  );
}
