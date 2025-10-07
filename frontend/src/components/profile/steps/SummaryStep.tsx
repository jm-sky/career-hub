'use client';

// Summary and review step of the profile wizard

import { UseFormWatch } from 'react-hook-form';
import { CheckCircle, User, Briefcase, FolderOpen, Code, MapPin, Calendar } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';

interface SummaryStepProps {
  watch: UseFormWatch<any>;
  onSubmit: () => void;
}

export function SummaryStep({ watch, onSubmit }: SummaryStepProps) {
  const formData = watch();
  const { headline, summary, location, visibility, contact, experiences, projects, skills } = formData;

  // Calculate completion percentage
  const calculateCompletion = () => {
    let total = 0;
    let completed = 0;

    // Personal info (40% weight)
    total += 40;
    if (headline && location) completed += 40;

    // Experience (30% weight)
    total += 30;
    if (experiences && experiences.length > 0) completed += 30;

    // Projects (20% weight)
    total += 20;
    if (projects && projects.length > 0) completed += 20;

    // Skills (10% weight)
    total += 10;
    if (skills && skills.length > 0) completed += 10;

    return Math.round((completed / total) * 100);
  };

  const completionPercentage = calculateCompletion();

  const getVisibilityBadge = (visibility: string) => {
    switch (visibility) {
      case 'PUBLIC': return <Badge className="bg-green-100 text-green-800">Public</Badge>;
      case 'FRIENDS': return <Badge className="bg-blue-100 text-blue-800">Friends</Badge>;
      case 'PRIVATE': return <Badge className="bg-gray-100 text-gray-800">Private</Badge>;
      default: return <Badge className="bg-gray-100 text-gray-800">Private</Badge>;
    }
  };

  const getSkillLevelCounts = () => {
    if (!skills || skills.length === 0) return { expert: 0, advanced: 0, intermediate: 0, beginner: 0 };
    
    return skills.reduce((counts: any, skill: any) => {
      counts[skill.level.toLowerCase()]++;
      return counts;
    }, { expert: 0, advanced: 0, intermediate: 0, beginner: 0 });
  };

  const skillCounts = getSkillLevelCounts();

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium mb-2">Profile Summary</h3>
        <p className="text-sm text-gray-600">
          Review your professional profile before completing the setup
        </p>
      </div>

      {/* Completion Progress */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <CheckCircle className="h-4 w-4" />
            Profile Completion
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">
                {completionPercentage}% Complete
              </span>
              <span className="text-sm text-gray-500">
                {completionPercentage >= 80 ? 'Excellent!' : completionPercentage >= 60 ? 'Good progress' : 'Keep going!'}
              </span>
            </div>
            <Progress value={completionPercentage} className="h-3" />
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className={`p-3 rounded-lg ${headline && location ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'}`}>
                <User className="h-6 w-6 mx-auto mb-2" />
                <div className="text-sm font-medium">Personal Info</div>
                <div className="text-xs">{headline && location ? 'Complete' : 'Incomplete'}</div>
              </div>
              <div className={`p-3 rounded-lg ${experiences && experiences.length > 0 ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'}`}>
                <Briefcase className="h-6 w-6 mx-auto mb-2" />
                <div className="text-sm font-medium">Experience</div>
                <div className="text-xs">{experiences?.length || 0} entries</div>
              </div>
              <div className={`p-3 rounded-lg ${projects && projects.length > 0 ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'}`}>
                <FolderOpen className="h-6 w-6 mx-auto mb-2" />
                <div className="text-sm font-medium">Projects</div>
                <div className="text-xs">{projects?.length || 0} entries</div>
              </div>
              <div className={`p-3 rounded-lg ${skills && skills.length > 0 ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'}`}>
                <Code className="h-6 w-6 mx-auto mb-2" />
                <div className="text-sm font-medium">Skills</div>
                <div className="text-xs">{skills?.length || 0} skills</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Personal Information Preview */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <User className="h-4 w-4" />
            Personal Information
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-medium text-lg">{headline || 'Professional Headline'}</h4>
            <div className="flex items-center gap-2 mt-1">
              <MapPin className="h-3 w-3 text-gray-500" />
              <span className="text-sm text-gray-600">{location || 'Location not specified'}</span>
              {getVisibilityBadge(visibility)}
            </div>
          </div>
          
          {summary && (
            <div>
              <h5 className="font-medium text-sm mb-2">Summary</h5>
              <p className="text-sm text-gray-700 leading-relaxed">{summary}</p>
            </div>
          )}

          {contact && (contact.email || contact.phone || contact.linkedin || contact.website) && (
            <div>
              <h5 className="font-medium text-sm mb-2">Contact Information</h5>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                {contact.email && <div>📧 {contact.email}</div>}
                {contact.phone && <div>📱 {contact.phone}</div>}
                {contact.linkedin && <div>💼 {contact.linkedin}</div>}
                {contact.website && <div>🌐 {contact.website}</div>}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Experience Preview */}
      {experiences && experiences.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Briefcase className="h-4 w-4" />
              Work Experience ({experiences.length} {experiences.length === 1 ? 'entry' : 'entries'})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {experiences.slice(0, 3).map((exp: any, index: number) => (
                <div key={index} className="border-l-2 border-blue-200 pl-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h5 className="font-medium">{exp.position || 'Position'}</h5>
                      <p className="text-sm text-gray-600">{exp.company || 'Company'}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Calendar className="h-3 w-3 text-gray-500" />
                        <span className="text-xs text-gray-500">
                          {exp.startDate} - {exp.isCurrent ? 'Present' : exp.endDate || 'Present'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {experiences.length > 3 && (
                <p className="text-sm text-gray-500 italic">
                  +{experiences.length - 3} more experience{experiences.length - 3 !== 1 ? 's' : ''}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Projects Preview */}
      {projects && projects.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <FolderOpen className="h-4 w-4" />
              Projects ({projects.length} {projects.length === 1 ? 'project' : 'projects'})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {projects.slice(0, 3).map((project: any, index: number) => (
                <div key={index} className="flex items-start justify-between">
                  <div className="flex-1">
                    <h5 className="font-medium">{project.name || 'Project Name'}</h5>
                    <p className="text-sm text-gray-600 line-clamp-2">{project.description || 'Project description'}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant="secondary" className="text-xs">
                        {project.status}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {project.category}
                      </Badge>
                      {project.technologies && project.technologies.length > 0 && (
                        <span className="text-xs text-gray-500">
                          {project.technologies.slice(0, 3).join(', ')}
                          {project.technologies.length > 3 && ` +${project.technologies.length - 3} more`}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {projects.length > 3 && (
                <p className="text-sm text-gray-500 italic">
                  +{projects.length - 3} more project{projects.length - 3 !== 1 ? 's' : ''}
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Skills Preview */}
      {skills && skills.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Code className="h-4 w-4" />
              Technical Skills ({skills.length} {skills.length === 1 ? 'skill' : 'skills'})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div className="bg-purple-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-purple-600">{skillCounts.expert}</div>
                  <div className="text-xs text-purple-600">Expert</div>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-green-600">{skillCounts.advanced}</div>
                  <div className="text-xs text-green-600">Advanced</div>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-blue-600">{skillCounts.intermediate}</div>
                  <div className="text-xs text-blue-600">Intermediate</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-gray-600">{skillCounts.beginner}</div>
                  <div className="text-xs text-gray-600">Beginner</div>
                </div>
              </div>
              
              <div>
                <h6 className="font-medium text-sm mb-2">Top Skills</h6>
                <div className="flex flex-wrap gap-2">
                  {skills.slice(0, 10).map((skill: any, index: number) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {skill.name}
                    </Badge>
                  ))}
                  {skills.length > 10 && (
                    <Badge variant="outline" className="text-xs">
                      +{skills.length - 10} more
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Completion Message */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50">
        <CardContent className="pt-6">
          <div className="text-center">
            <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
            <h4 className="font-medium text-lg mb-2">
              {completionPercentage >= 80 
                ? "Excellent! Your profile looks great!" 
                : completionPercentage >= 60 
                ? "Good progress! Your profile is taking shape." 
                : "Keep building! You're on the right track."
              }
            </h4>
            <p className="text-sm text-gray-600 mb-4">
              {completionPercentage >= 80 
                ? "You can complete your profile now or continue adding more details."
                : "Consider adding more experience, projects, or skills to make your profile even stronger."
              }
            </p>
            <Button 
              onClick={onSubmit} 
              size="lg"
              className={completionPercentage >= 60 ? "bg-green-600 hover:bg-green-700" : ""}
            >
              {completionPercentage >= 80 ? "Complete Profile" : "Save Profile & Continue"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
