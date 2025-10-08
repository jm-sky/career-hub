'use client';

// Skills step of the profile wizard

import { useState, useCallback } from 'react';
import { useFormContext, useFieldArray } from 'react-hook-form';
import { Plus, Trash2, Code, Star, Clock } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';

// Modern 2025: No props needed - use FormProvider context
interface Skill {
  id: string;
  name: string;
  category: 'FRAMEWORK' | 'LIBRARY' | 'LANGUAGE' | 'TOOL' | 'DATABASE' | 'PLATFORM';
  level: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED' | 'EXPERT';
  yearsOfExperience: number;
}

const SKILL_CATEGORIES = [
  { value: 'LANGUAGE', label: 'Programming Languages', icon: '💻' },
  { value: 'FRAMEWORK', label: 'Frameworks', icon: '🏗️' },
  { value: 'LIBRARY', label: 'Libraries', icon: '📚' },
  { value: 'TOOL', label: 'Tools', icon: '🔧' },
  { value: 'DATABASE', label: 'Databases', icon: '🗄️' },
  { value: 'PLATFORM', label: 'Platforms', icon: '☁️' },
] as const;

const SKILL_LEVELS = [
  { value: 'BEGINNER', label: 'Beginner', color: 'bg-gray-100 text-gray-800', progress: 25 },
  { value: 'INTERMEDIATE', label: 'Intermediate', color: 'bg-blue-100 text-blue-800', progress: 50 },
  { value: 'ADVANCED', label: 'Advanced', color: 'bg-green-100 text-green-800', progress: 75 },
  { value: 'EXPERT', label: 'Expert', color: 'bg-purple-100 text-purple-800', progress: 100 },
] as const;

export function SkillsStep() {
  const { control, register, watch, formState: { errors } } = useFormContext();
  
  // Modern 2025: Use useFieldArray for dynamic arrays
  const { fields, append, remove, update } = useFieldArray({
    control,
    name: 'skills'
  });

  // Watch skills to get real-time values for display
  const watchedSkills = watch('skills') || [];

  const [editingSkill, setEditingSkill] = useState<string | null>(null);
  const [newSkillName, setNewSkillName] = useState('');
  const [newSkillCategory, setNewSkillCategory] = useState<Skill['category']>('LANGUAGE');
  const [newSkillLevel, setNewSkillLevel] = useState<Skill['level']>('INTERMEDIATE');
  const [newSkillYears, setNewSkillYears] = useState(1);

  const addSkill = useCallback(() => {
    if (!newSkillName.trim()) return;

    const newSkill = {
      id: Date.now().toString(),
      name: newSkillName.trim(),
      category: newSkillCategory,
      level: newSkillLevel,
      yearsOfExperience: newSkillYears,
    };
    
    append(newSkill);
    setNewSkillName('');
    setNewSkillYears(1);
  }, [newSkillName, newSkillCategory, newSkillLevel, newSkillYears, append]);

  const removeSkill = useCallback((id: string) => {
    const index = fields.findIndex(f => f.id === id);
    if (index !== -1) {
      remove(index);
      if (editingSkill === id) {
        setEditingSkill(null);
      }
    }
  }, [fields, remove, editingSkill]);

  const updateSkill = useCallback((id: string, field: string, value: any) => {
    const index = fields.findIndex(f => f.id === id);
    if (index !== -1) {
      update(index, { ...fields[index], [field]: value });
    }
  }, [fields, update]);

  const getSkillsByCategory = useCallback((category: string) => {
    return watchedSkills.filter((skill: any) => skill.category === category);
  }, [watchedSkills]);

  const getLevelInfo = (level: string) => {
    return SKILL_LEVELS.find(l => l.value === level) || SKILL_LEVELS[0];
  };

  const getCategoryInfo = (category: string) => {
    return SKILL_CATEGORIES.find(c => c.value === category) || SKILL_CATEGORIES[0];
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addSkill();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium">Technical Skills</h3>
          <p className="text-sm text-gray-600">
            Showcase your technical expertise and proficiency levels
          </p>
        </div>
      </div>

      {/* Add New Skill */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Add New Skill</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="skill-name" required>Skill Name</Label>
              <Input
                id="skill-name"
                placeholder="e.g., React, Python, AWS"
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                onKeyPress={handleKeyPress}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="skill-category">Category</Label>
              <Select
                value={newSkillCategory}
                onValueChange={(value) => setNewSkillCategory(value as Skill['category'])}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {SKILL_CATEGORIES.map((category) => (
                    <SelectItem key={category.value} value={category.value}>
                      <div className="flex items-center gap-2">
                        <span>{category.icon}</span>
                        <span>{category.label}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="skill-level">Proficiency Level</Label>
              <Select
                value={newSkillLevel}
                onValueChange={(value) => setNewSkillLevel(value as Skill['level'])}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {SKILL_LEVELS.map((level) => (
                    <SelectItem key={level.value} value={level.value}>
                      <div className="flex items-center gap-2">
                        <Badge className={level.color}>{level.label}</Badge>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="skill-years">Years of Experience</Label>
              <Input
                id="skill-years"
                type="number"
                min="0"
                max="50"
                value={newSkillYears}
                onChange={(e) => setNewSkillYears(parseInt(e.target.value) || 0)}
              />
            </div>
          </div>
          <div className="mt-4">
            <Button onClick={addSkill} disabled={!newSkillName.trim()}>
              <Plus className="size-4 mr-2" />
              Add Skill
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Skills by Category */}
      {watchedSkills.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Code className="h-12 w-12 text-gray-400 mb-4" />
            <h4 className="font-medium text-gray-900 mb-2">No skills added yet</h4>
            <p className="text-sm text-gray-500 text-center mb-4">
              Add your technical skills to showcase your expertise
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {SKILL_CATEGORIES.map((category) => {
            const categorySkills = getSkillsByCategory(category.value);
            if (categorySkills.length === 0) return null;

            return (
              <Card key={category.value}>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <span>{category.icon}</span>
                    {category.label}
                    <Badge variant="secondary">{categorySkills.length}</Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {categorySkills.map((skill: Skill) => {
                      const levelInfo = getLevelInfo(skill.level);
                      
                      return (
                        <div key={skill.id} className="border rounded-lg p-4 space-y-3">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h4 className="font-medium">{skill.name}</h4>
                              <div className="flex items-center gap-2 mt-1">
                                <Badge className={levelInfo.color}>{levelInfo.label}</Badge>
                                <div className="flex items-center gap-1 text-xs text-gray-500">
                                  <Clock className="h-3 w-3" />
                                  {skill.yearsOfExperience} year{skill.yearsOfExperience !== 1 ? 's' : ''}
                                </div>
                              </div>
                            </div>
                            <Button
                              variant="ghost-destructive"
                              size="sm"
                              onClick={() => removeSkill(skill.id)}
                            >
                              <Trash2 className="h-3 w-3" />
                            </Button>
                          </div>
                          
                          <div className="space-y-1">
                            <div className="flex items-center justify-between text-xs">
                              <span>Proficiency</span>
                              <span>{levelInfo.progress}%</span>
                            </div>
                            <Progress value={levelInfo.progress} className="h-2" />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Skills Summary */}
      {watchedSkills.length > 0 && (
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Star className="size-4" />
              Skills Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-600">{watchedSkills.length}</div>
                <div className="text-sm text-gray-600">Total Skills</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">
                  {watchedSkills.filter((s: any) => s.level === 'EXPERT').length}
                </div>
                <div className="text-sm text-gray-600">Expert Level</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">
                  {watchedSkills.filter((s: any) => s.level === 'ADVANCED').length}
                </div>
                <div className="text-sm text-gray-600">Advanced</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">
                  {Math.round(watchedSkills.reduce((sum: number, s: any) => sum + s.yearsOfExperience, 0) / watchedSkills.length * 10) / 10}
                </div>
                <div className="text-sm text-gray-600">Avg. Experience</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Tips for great skills entries:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Be honest about your proficiency levels</li>
          <li>• Include both technical and soft skills</li>
          <li>• Focus on skills relevant to your target roles</li>
          <li>• Update your experience years regularly</li>
          <li>• Consider adding certifications and courses</li>
        </ul>
      </div>
    </div>
  );
}
