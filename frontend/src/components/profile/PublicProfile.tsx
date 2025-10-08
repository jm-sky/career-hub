'use client';

// Public Profile component - displays user's public profile

import { useQuery } from '@tanstack/react-query';
import { MapPin, Mail, Phone, Linkedin, Globe, Briefcase, FolderOpen, Code, Calendar, Users, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { apiClient } from '@/lib/api-client';

interface PublicProfileProps {
  username: string;
}

const fetchPublicProfile = async (username: string) => {
  const response = await apiClient.get(`/profiles/public/${username}`);
  return response.data;
};

export function PublicProfile({ username }: PublicProfileProps) {
  const { data: profile, isLoading, error } = useQuery({
    queryKey: ['publicProfile', username],
    queryFn: () => fetchPublicProfile(username),
    retry: false,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin size-12 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="container mx-auto p-8 max-w-4xl">
        <Card>
          <CardContent className="py-12 text-center">
            <h2 className="text-2xl font-bold mb-2">Profile Not Found</h2>
            <p className="text-muted-foreground">
              The profile you're looking for doesn't exist or is not public.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

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

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'EXPERT': return 'bg-purple-100 text-purple-800';
      case 'ADVANCED': return 'bg-green-100 text-green-800';
      case 'INTERMEDIATE': return 'bg-blue-100 text-blue-800';
      case 'BEGINNER': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto p-8 max-w-5xl">
        {/* Header */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex flex-col md:flex-row gap-6">
              <Avatar className="size-24">
                <AvatarFallback className="bg-primary/10 text-primary text-2xl font-bold">
                  {getInitials(profile.user.name)}
                </AvatarFallback>
              </Avatar>
              
              <div className="flex-1">
                <h1 className="text-3xl font-bold mb-2">{profile.user.name}</h1>
                <p className="text-xl text-muted-foreground mb-4">{profile.headline}</p>
                
                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                  {profile.location && (
                    <div className="flex items-center gap-1">
                      <MapPin className="size-4" />
                      {profile.location}
                    </div>
                  )}
                  {profile.contact?.email && (
                    <a href={`mailto:${profile.contact.email}`} className="flex items-center gap-1 hover:text-primary">
                      <Mail className="size-4" />
                      {profile.contact.email}
                    </a>
                  )}
                  {profile.contact?.phone && (
                    <div className="flex items-center gap-1">
                      <Phone className="size-4" />
                      {profile.contact.phone}
                    </div>
                  )}
                  {profile.contact?.linkedin && (
                    <a href={profile.contact.linkedin} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-primary">
                      <Linkedin className="size-4" />
                      LinkedIn
                    </a>
                  )}
                  {profile.contact?.website && (
                    <a href={profile.contact.website} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 hover:text-primary">
                      <Globe className="size-4" />
                      Website
                    </a>
                  )}
                </div>
              </div>
            </div>
            
            {profile.summary && (
              <div className="mt-6 pt-6 border-t">
                <p className="text-muted-foreground whitespace-pre-line">{profile.summary}</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Experience */}
        {profile.experiences && profile.experiences.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="size-5" />
                Work Experience
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {profile.experiences.map((exp: any) => (
                <div key={exp.id} className="border-b pb-6 last:border-b-0 last:pb-0">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="text-lg font-semibold">{exp.position}</h3>
                      <p className="text-muted-foreground">{exp.company}</p>
                    </div>
                    {exp.isCurrent && (
                      <Badge variant="secondary">Current</Badge>
                    )}
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mb-3">
                    <div className="flex items-center gap-1">
                      <Calendar className="size-4" />
                      {exp.startDate} - {exp.isCurrent ? 'Present' : exp.endDate || 'N/A'}
                    </div>
                  </div>
                  
                  {exp.description && (
                    <p className="text-sm text-muted-foreground mb-3">{exp.description}</p>
                  )}
                  
                  {exp.responsibilities && exp.responsibilities.length > 0 && (
                    <div className="mb-3">
                      <h4 className="font-medium text-sm mb-2">Key Responsibilities:</h4>
                      <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                        {exp.responsibilities.map((resp: string, idx: number) => (
                          <li key={idx}>{resp}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {exp.technologies && exp.technologies.length > 0 && (
                    <div>
                      <h4 className="font-medium text-sm mb-2">Technologies:</h4>
                      <div className="flex flex-wrap gap-2">
                        {exp.technologies.map((tech: string, idx: number) => (
                          <Badge key={idx} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Projects */}
        {profile.projects && profile.projects.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FolderOpen className="size-5" />
                Notable Projects
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {profile.projects.map((project: any) => (
                <div key={project.id} className="border-b pb-6 last:border-b-0 last:pb-0">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-lg font-semibold">{project.name}</h3>
                    <Badge className={getStatusColor(project.status)}>{project.status}</Badge>
                    <Badge variant="secondary" className={getCategoryColor(project.category)}>
                      {project.category}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mb-3">
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
                      {project.scale}
                    </div>
                  </div>
                  
                  <p className="text-sm text-muted-foreground mb-3">{project.description}</p>
                  
                  {project.technologies && project.technologies.length > 0 && (
                    <div className="mb-3">
                      <h4 className="font-medium text-sm mb-2">Technologies:</h4>
                      <div className="flex flex-wrap gap-2">
                        {project.technologies.map((tech: string, idx: number) => (
                          <Badge key={idx} variant="secondary">{tech}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {project.achievements && project.achievements.length > 0 && (
                    <div className="mb-3">
                      <h4 className="font-medium text-sm mb-2">Key Achievements:</h4>
                      <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                        {project.achievements.map((achievement: string, idx: number) => (
                          <li key={idx}>{achievement}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {project.challenges && project.challenges.length > 0 && (
                    <div>
                      <h4 className="font-medium text-sm mb-2">Technical Challenges:</h4>
                      <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                        {project.challenges.map((challenge: string, idx: number) => (
                          <li key={idx}>{challenge}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Skills */}
        {profile.skills && profile.skills.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="size-5" />
                Technical Skills
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {profile.skills.map((skill: any) => (
                  <div key={skill.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{skill.name}</p>
                      <p className="text-xs text-muted-foreground">{skill.category}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge className={getLevelColor(skill.level)}>{skill.level}</Badge>
                      <span className="text-xs text-muted-foreground">{skill.yearsOfExperience}y</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
