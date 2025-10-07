'use client';

// Multi-step Profile Wizard for comprehensive professional profile creation

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import { z } from 'zod';
import { ChevronLeft, ChevronRight, Save, Check } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { useAuth } from '@/contexts/auth-context';
import { getErrorMessage } from '@/lib/error-guards';

// Import step components
import { PersonalInfoStep } from './steps/PersonalInfoStep';
import { ExperienceStep } from './steps/ExperienceStep';
import { ProjectsStep } from './steps/ProjectsStep';
import { SkillsStep } from './steps/SkillsStep';
import { SummaryStep } from './steps/SummaryStep';

// Complete profile schema
const ProfileWizardSchema = z.object({
  // Personal Info
  headline: z.string().min(1, 'Headline is required').max(200, 'Headline too long'),
  summary: z.string().max(2000, 'Summary too long').optional(),
  location: z.string().min(1, 'Location is required').max(100, 'Location too long'),
  visibility: z.enum(['PRIVATE', 'FRIENDS', 'PUBLIC']).default('PRIVATE'),
  contact: z.object({
    email: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().email('Invalid email').optional()),
    phone: z.string().transform(val => val === '' ? undefined : val).optional(),
    linkedin: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().url('Invalid LinkedIn URL').optional()),
    website: z.string().transform(val => val === '' ? undefined : val).pipe(z.string().url('Invalid website URL').optional()),
  }).optional(),
  
  // Experience
  experiences: z.array(z.object({
    company: z.string().min(1, 'Company is required'),
    position: z.string().min(1, 'Position is required'),
    startDate: z.string().min(1, 'Start date is required'),
    endDate: z.string().optional(),
    isCurrent: z.boolean().default(false),
    description: z.string().optional(),
    responsibilities: z.array(z.string()).default([]),
    achievements: z.array(z.string()).default([]),
    technologies: z.array(z.string()).default([]),
  })).default([]),
  
  // Projects
  projects: z.array(z.object({
    name: z.string().min(1, 'Project name is required'),
    description: z.string().min(1, 'Description is required'),
    status: z.enum(['ACTIVE', 'STAGING', 'ARCHIVED']).default('ACTIVE'),
    category: z.enum(['DEMO', 'INTERNAL', 'PRODUCTION']).default('PRODUCTION'),
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    technologies: z.array(z.string()).default([]),
    achievements: z.array(z.string()).default([]),
    challenges: z.array(z.string()).default([]),
    client: z.string().optional(),
    scale: z.enum(['SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE']).default('MEDIUM'),
  })).default([]),
  
  // Skills
  skills: z.array(z.object({
    name: z.string().min(1, 'Skill name is required'),
    category: z.enum(['FRAMEWORK', 'LIBRARY', 'LANGUAGE', 'TOOL', 'DATABASE', 'PLATFORM']),
    level: z.enum(['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']).default('INTERMEDIATE'),
    yearsOfExperience: z.number().min(0).max(50).default(1),
  })).default([]),
});

type ProfileWizardData = z.infer<typeof ProfileWizardSchema>;

const STEPS = [
  { id: 'personal', title: 'Personal Info', description: 'Basic information about yourself' },
  { id: 'experience', title: 'Experience', description: 'Your work experience and career history' },
  { id: 'projects', title: 'Projects', description: 'Notable projects and achievements' },
  { id: 'skills', title: 'Skills', description: 'Technical skills and expertise' },
  { id: 'summary', title: 'Review', description: 'Review and complete your profile' },
] as const;

export function ProfileWizardSteps() {
  const router = useRouter();
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    trigger,
    formState: { errors, isValid },
    reset,
  } = useForm<ProfileWizardData>({
    resolver: zodResolver(ProfileWizardSchema),
    mode: 'onBlur',
    defaultValues: {
      visibility: 'PRIVATE',
      contact: {},
      experiences: [],
      projects: [],
      skills: [],
    },
  });

  // Auto-save draft every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (isValid && currentStep > 0) {
        saveDraft();
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [isValid, currentStep]);

  // Load draft on mount
  useEffect(() => {
    loadDraft();
  }, []);

  const saveDraft = async () => {
    if (!user) return;
    
    setIsSaving(true);
    setSaveStatus('saving');
    
    try {
      const formData = watch();
      const draft = {
        ...formData,
        userId: user.id,
        lastSaved: new Date().toISOString(),
        step: currentStep,
      };
      
      localStorage.setItem(`profile_draft_${user.id}`, JSON.stringify(draft));
      setSaveStatus('saved');
      
      // Clear saved status after 2 seconds
      setTimeout(() => setSaveStatus('idle'), 2000);
    } catch (error) {
      console.error('Failed to save draft:', error);
      setSaveStatus('error');
    } finally {
      setIsSaving(false);
    }
  };

  const loadDraft = () => {
    if (!user) return;
    
    try {
      const saved = localStorage.getItem(`profile_draft_${user.id}`);
      if (saved) {
        const draft = JSON.parse(saved);
        reset(draft);
        
        // Restore step if it exists
        if (typeof draft.step === 'number' && draft.step < STEPS.length) {
          setCurrentStep(draft.step);
        }
      }
    } catch (error) {
      console.error('Failed to load draft:', error);
    }
  };

  const clearDraft = () => {
    if (!user) return;
    localStorage.removeItem(`profile_draft_${user.id}`);
  };

  const validateCurrentStep = async (): Promise<boolean> => {
    const fieldsToValidate = getFieldsForStep(currentStep);
    const isValid = await trigger(fieldsToValidate);
    return isValid;
  };

  const getFieldsForStep = (step: number): (keyof ProfileWizardData)[] => {
    switch (step) {
      case 0: return ['headline', 'location', 'visibility'];
      case 1: return ['experiences'];
      case 2: return ['projects'];
      case 3: return ['skills'];
      case 4: return []; // Summary step doesn't need validation
      default: return [];
    }
  };

  const nextStep = async () => {
    const isValid = await validateCurrentStep();
    if (!isValid) return;

    // Mark current step as completed
    setCompletedSteps(prev => new Set([...prev, currentStep]));
    
    // Save draft before moving to next step
    await saveDraft();
    
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const goToStep = (step: number) => {
    if (step <= currentStep || completedSteps.has(step - 1)) {
      setCurrentStep(step);
    }
  };

  const onSubmit = async (data: ProfileWizardData) => {
    try {
      // Here you would call the API to create the complete profile
      console.log('Creating profile with data:', data);
      
      // Clear draft after successful creation
      clearDraft();
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (error) {
      console.error('Failed to create profile:', error);
    }
  };

  const progress = ((currentStep + 1) / STEPS.length) * 100;

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return (
          <PersonalInfoStep
            register={register}
            setValue={setValue}
            watch={watch}
            errors={errors}
          />
        );
      case 1:
        return (
          <ExperienceStep
            register={register}
            setValue={setValue}
            watch={watch}
            errors={errors}
          />
        );
      case 2:
        return (
          <ProjectsStep
            register={register}
            setValue={setValue}
            watch={watch}
            errors={errors}
          />
        );
      case 3:
        return (
          <SkillsStep
            register={register}
            setValue={setValue}
            watch={watch}
            errors={errors}
          />
        );
      case 4:
        return (
          <SummaryStep
            watch={watch}
            onSubmit={() => handleSubmit(onSubmit)()}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="container mx-auto p-8 max-w-4xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Create Your Professional Profile</h1>
        <p className="text-gray-600">
          Build a comprehensive profile to showcase your expertise and create tailored CVs
        </p>
      </div>

      {/* Progress */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm font-medium">
            Step {currentStep + 1} of {STEPS.length}
          </span>
          <div className="flex items-center gap-2">
            {saveStatus === 'saving' && (
              <span className="text-sm text-gray-500 flex items-center gap-1">
                <Save className="h-3 w-3 animate-pulse" />
                Saving...
              </span>
            )}
            {saveStatus === 'saved' && (
              <span className="text-sm text-green-600 flex items-center gap-1">
                <Check className="h-3 w-3" />
                Saved
              </span>
            )}
          </div>
        </div>
        <Progress value={progress} className="mb-4" />
        
        {/* Step Navigation */}
        <div className="flex items-center justify-between">
          {STEPS.map((step, index) => (
            <button
              key={step.id}
              onClick={() => goToStep(index)}
              className={`flex flex-col items-center p-2 rounded-lg transition-colors ${
                index === currentStep
                  ? 'bg-primary text-primary-foreground'
                  : completedSteps.has(index)
                  ? 'bg-green-100 text-green-700 hover:bg-green-200'
                  : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
              } ${index <= currentStep || completedSteps.has(index - 1) ? 'cursor-pointer' : 'cursor-not-allowed'}`}
              disabled={index > currentStep && !completedSteps.has(index - 1)}
            >
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium mb-1">
                {completedSteps.has(index) ? (
                  <Check className="h-4 w-4" />
                ) : (
                  index + 1
                )}
              </div>
              <span className="text-xs font-medium">{step.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Current Step */}
      <Card>
        <CardHeader>
          <CardTitle>{STEPS[currentStep].title}</CardTitle>
          <CardDescription>{STEPS[currentStep].description}</CardDescription>
        </CardHeader>
        <CardContent>
          {renderStep()}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8">
        <Button
          variant="outline"
          onClick={prevStep}
          disabled={currentStep === 0}
        >
          <ChevronLeft className="h-4 w-4 mr-2" />
          Previous
        </Button>

        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={saveDraft}
            disabled={isSaving}
          >
            <Save className="h-4 w-4 mr-2" />
            Save Draft
          </Button>

          {currentStep === STEPS.length - 1 ? (
            <Button onClick={handleSubmit(onSubmit)} className="bg-green-600 hover:bg-green-700">
              Complete Profile
            </Button>
          ) : (
            <Button onClick={nextStep}>
              Next
              <ChevronRight className="h-4 w-4 ml-2" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
