<script setup lang="ts">
import { Check, Copy } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import AuthenticatedLayout from '@/layouts/AuthenticatedLayout.vue'

const { t } = useI18n()
const copied = ref(false)

const aiContextMarkdown = computed(() => {
  return `# CareerHub - AI Context

## Overview
CareerHub is a full-stack web application for managing a professional profile and generating tailored CVs from it. Users build a single master profile — experiences, projects, skills, education, certifications, achievements — and curate named CV versions as selective views over that master data, rather than maintaining separate documents per application.

## Key Capabilities
- **Multi-User Platform** - Secure user accounts with authentication and authorization
- **Freemium Tiers** - Free / Pro / Expert plans gate CV version limits, watermarking, AI features, and custom domain
- **Curated CV Generation** - Named CV versions select which experiences/projects/skills/education/certs to include, with an optional custom summary override
- **Public Profile** - Shareable profile page at a unique slug with Private/Friends/Public visibility
- **Data Portability** - LinkedIn import, copy-paste text import fallback, full JSON export

## Core Features

### Profile
- Rich profile: headline, summary, location, contact info, profile photo
- Multi-step wizard with per-step draft autosave
- Completeness score to nudge users toward a fuller profile
- Three-level visibility: Private, Friends, Public

### Experience & Projects
- Rich per-role experience data: company, position, employment type, dates, responsibilities, technologies
- Projects documented independently of experiences, then explicitly linked to one or more experiences and skills - supports cross-company/portfolio work
- Anonymization - hide the real company/client name behind a placeholder for NDA-restricted work, as a first-class field
- User-orderable sections (drag-and-drop reordering)

### Skills
- Categorized skills (Technical/Tools/Soft) with 1-5 proficiency level and years of experience
- Linkable to specific projects
- AI-suggested skills for a target role (Pro/Expert)

### CV Generation
- Multiple named CV versions per profile, each an explicit curated selection over the master profile
- Template choice per CV version
- Async PDF generation (background job)
- Free tier PDFs are watermarked

### AI Features (Pro/Expert)
- Optimize responsibility/description text
- Suggest missing responsibilities for a role + seniority level
- Gap analysis against a target role (match score, strengths, gaps, recommendations)

### Import/Export
- LinkedIn import (async job)
- Copy-paste text fallback parser
- Full JSON export of profile data

## Business Features

### User Management & Security
- Email/password authentication with secure password hashing
- OAuth social login (Google, GitHub)
- Email verification
- Two-factor authentication (2FA) - TOTP and WebAuthn (passkeys)
- Password management - reset and change
- reCAPTCHA v3 protection
- JWT tokens with automatic refresh
- GDPR-compliant account deletion

### Subscription & Billing
- Free / Pro / Expert plans via Stripe
- Feature gating per plan (CV version limits, watermark, AI access, custom domain, API access)

### Multi-Language Support
- English and Polish fully supported
- Automatic locale detection
- Manual language switching
- All UI text, validation messages, and emails localized

### Theming
- Dark mode with system preference detection
- Theme persistence per user account

## Technical Stack

### Frontend
- Vue 3.5+ with TypeScript & Composition API
- Pinia for state management
- Vue Router for navigation
- TailwindCSS v4 + shadcn-vue components
- VeeValidate + Zod for form validation
- TanStack Query for server state management
- vue-i18n for internationalization

### Backend
- FastAPI (Python) with async/await
- PostgreSQL database, ULID primary keys
- SQLAlchemy ORM with async support
- JWT authentication with refresh tokens
- Rate limiting and reCAPTCHA protection
- Modular architecture (auth, two-factor, billing, feature_limits, ai, career)

## Architecture
- **Module-Based Frontend** - Each feature is self-contained in modules (services/composables/types/routes/i18n)
- **Backend Modules** - FastAPI modular pattern with routers, services, repositories
- **JSONB for flexible fields** - responsibilities, achievements, CV section selection
- **Async job pattern** - long operations (PDF generation, LinkedIn import) run as background jobs, polled via job id`
})

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(aiContextMarkdown.value)
    copied.value = true
    toast.success(t('aiContext.copied', 'Context copied to clipboard'))
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (error) {
    toast.error(t('common.error'))
    console.error('Error copying to clipboard:', error)
  }
}
</script>

<template>
  <AuthenticatedLayout>
    <div class="space-y-8">
      <div class="space-y-2">
        <h1 class="text-3xl font-bold tracking-tight">
          {{ t('about.title', 'About CareerHub') }}
        </h1>
        <p class="text-muted-foreground">
          {{ t('about.subtitle', 'A single professional profile that generates as many tailored CVs as you need') }}
        </p>
      </div>

      <!-- Table of Contents -->
      <nav class="flex flex-row flex-wrap items-center gap-2 text-sm text-muted-foreground">
        <a href="#overview" class="text-primary hover:underline">
          {{ t('about.overview.title', 'Overview') }}
        </a>
        <span>|</span>
        <a href="#capabilities" class="text-primary hover:underline">
          {{ t('about.capabilities.title', 'Key Capabilities') }}
        </a>
        <span>|</span>
        <a href="#core-features" class="text-primary hover:underline">
          {{ t('about.coreFeatures.title', 'Core Features') }}
        </a>
        <span>|</span>
        <a href="#business-features" class="text-primary hover:underline">
          {{ t('about.businessFeatures.title', 'Business Features') }}
        </a>
        <span>|</span>
        <a href="#technical-stack" class="text-primary hover:underline">
          {{ t('about.technical.title', 'Technical Stack') }}
        </a>
        <span>|</span>
        <a href="#ai-context" class="text-primary hover:underline">
          {{ t('aiContext.title', 'AI Context') }}
        </a>
      </nav>

      <!-- Overview -->
      <section id="overview" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('about.overview.title', 'Overview') }}
        </h2>
        <p class="text-muted-foreground">
          {{ t('about.overview.description', 'CareerHub is a full-stack application for building one master professional profile — experience, projects, skills, education, certifications — and generating multiple tailored CVs from it. It combines an intuitive front-end interface with a robust backend to keep your career data in sync across devices.') }}
        </p>
      </section>

      <!-- Key Capabilities -->
      <section id="capabilities" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('about.capabilities.title', 'Key Capabilities') }}
        </h2>
        <ul class="list-disc list-inside space-y-2 text-muted-foreground">
          <li>{{ t('about.capabilities.multiUser', 'Multi-User Platform - Secure user accounts with authentication and authorization') }}</li>
          <li>{{ t('about.capabilities.hybrid', 'Freemium Tiers - Free, Pro, and Expert plans gate CV limits, watermarking, AI features, and custom domain') }}</li>
          <li>{{ t('about.capabilities.organization', 'Curated CVs - Named CV versions select which experiences, projects, skills, and education to include') }}</li>
          <li>{{ t('about.capabilities.metadata', 'Rich Metadata - Track responsibilities, technologies, anonymized clients, achievements, and certifications') }}</li>
          <li>{{ t('about.capabilities.portability', 'Data Portability - LinkedIn import, copy-paste import fallback, and full JSON export') }}</li>
        </ul>
      </section>

      <!-- Core Features -->
      <section id="core-features" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('about.coreFeatures.title', 'Core Features') }}
        </h2>
        <div class="space-y-6">
          <div id="container-system" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.coreFeatures.containers.title', 'Profile') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.coreFeatures.containers.multiple', 'Multi-step profile wizard with per-step draft autosave') }}</li>
              <li>{{ t('about.coreFeatures.containers.hierarchical', 'Completeness score to nudge you toward a fuller profile') }}</li>
              <li>{{ t('about.coreFeatures.containers.colors', 'Three-level visibility - Private, Friends, or Public') }}</li>
              <li>{{ t('about.coreFeatures.containers.metadata', 'Public profile page at a shareable slug, SEO-friendly') }}</li>
              <li>{{ t('about.coreFeatures.containers.cycle', 'Contact info, headline, summary, and profile photo') }}</li>
            </ul>
          </div>

          <div id="item-management" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.coreFeatures.items.title', 'Experience & Projects') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.coreFeatures.items.rich', 'Rich per-role data: company, position, employment type, dates, responsibilities, technologies') }}</li>
              <li>{{ t('about.coreFeatures.items.categorization', 'Projects documented independently of roles, then explicitly linked to one or more experiences and skills') }}</li>
              <li>{{ t('about.coreFeatures.items.status', 'Anonymization - hide the real company/client name behind a placeholder for NDA-restricted work') }}</li>
              <li>{{ t('about.coreFeatures.items.priority', 'User-orderable sections via drag-and-drop') }}</li>
              <li>{{ t('about.coreFeatures.items.expiration', 'Track achievements, challenges, and scale (team size, duration, users, budget)') }}</li>
            </ul>
          </div>

          <div id="analytics-insights" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.coreFeatures.analytics.title', 'Skills') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.coreFeatures.analytics.weight', 'Categorized skills (Technical/Tools/Soft) with 1-5 proficiency level and years of experience') }}</li>
              <li>{{ t('about.coreFeatures.analytics.readiness', 'Linkable to specific projects to show where a skill was applied') }}</li>
              <li>{{ t('about.coreFeatures.analytics.charts', 'AI-suggested skills for a target role (Pro/Expert)') }}</li>
              <li>{{ t('about.coreFeatures.analytics.statistics', 'A shared technology catalog reused across profiles') }}</li>
            </ul>
          </div>

          <div id="search-filtering" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.coreFeatures.search.title', 'CV Generation') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.coreFeatures.search.smart', 'Multiple named CV versions per profile, each a curated selection over the master profile') }}</li>
              <li>{{ t('about.coreFeatures.search.filtering', 'Optional custom summary override per CV version') }}</li>
              <li>{{ t('about.coreFeatures.search.sorting', 'Template choice per CV version') }}</li>
              <li>{{ t('about.coreFeatures.search.expired', 'Asynchronous PDF generation as a background job; Free tier PDFs are watermarked') }}</li>
            </ul>
          </div>

          <div id="import-export" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.coreFeatures.importExport.title', 'Import/Export') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.coreFeatures.importExport.json', 'Full JSON export/import of your profile data') }}</li>
              <li>{{ t('about.coreFeatures.importExport.markdown', 'LinkedIn import as a background job') }}</li>
              <li>{{ t('about.coreFeatures.importExport.csv', 'Copy-paste text fallback parser when a LinkedIn export is unavailable') }}</li>
              <li>{{ t('about.coreFeatures.importExport.crossDevice', 'Cross-device access - your profile is stored server-side, not just on one device') }}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Business Features -->
      <section id="business-features" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('about.businessFeatures.title', 'Business Features') }}
        </h2>
        <div class="space-y-6">
          <div id="user-management-security" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.businessFeatures.security.title', 'User Management & Security') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.businessFeatures.security.auth', 'User registration & login - email/password authentication with secure password hashing') }}</li>
              <li>{{ t('about.businessFeatures.security.oauth', 'OAuth social login - sign in with Google, Facebook, or GitHub') }}</li>
              <li>{{ t('about.businessFeatures.security.email', 'Email verification - confirm email addresses for account security') }}</li>
              <li>{{ t('about.businessFeatures.security.2fa', 'Two-factor authentication (2FA) - TOTP (authenticator apps) and WebAuthn (passkeys/security keys)') }}</li>
              <li>{{ t('about.businessFeatures.security.password', 'Password management - reset forgotten passwords, change password for authenticated users') }}</li>
              <li>{{ t('about.businessFeatures.security.recaptcha', 'reCAPTCHA v3 protection - invisible bot protection on login, registration, and password reset') }}</li>
              <li>{{ t('about.businessFeatures.security.session', 'Session management - JWT tokens with automatic refresh, secure logout') }}</li>
              <li>{{ t('about.businessFeatures.security.deletion', 'Account deletion - GDPR-compliant soft delete with confirmation') }}</li>
            </ul>
          </div>

          <div id="user-profile" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.businessFeatures.profile.title', 'User Profile') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.businessFeatures.profile.management', 'Profile management - update name, email, and preferences') }}</li>
              <li>{{ t('about.businessFeatures.profile.avatar', 'Avatar support - OAuth providers automatically provide profile pictures') }}</li>
              <li>{{ t('about.businessFeatures.profile.settings', 'Preferred settings - language, theme preferences') }}</li>
              <li>{{ t('about.businessFeatures.profile.security', 'Security settings - manage 2FA methods, view security status') }}</li>
            </ul>
          </div>

          <div id="multi-language-support" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.businessFeatures.i18n.title', 'Multi-Language Support') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.businessFeatures.i18n.languages', 'English and Polish fully supported') }}</li>
              <li>{{ t('about.businessFeatures.i18n.detection', 'Automatic locale detection from browser') }}</li>
              <li>{{ t('about.businessFeatures.i18n.switching', 'Manual language switching in settings') }}</li>
              <li>{{ t('about.businessFeatures.i18n.localized', 'All UI text, validation messages, and emails localized') }}</li>
            </ul>
          </div>

          <div id="theming" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.businessFeatures.theming.title', 'Theming') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>{{ t('about.businessFeatures.theming.dark', 'Dark mode - full dark theme support with system preference detection') }}</li>
              <li>{{ t('about.businessFeatures.theming.persistence', 'Theme persistence - settings saved per user account') }}</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Technical Stack -->
      <section id="technical-stack" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('about.technical.title', 'Technical Stack') }}
        </h2>
        <div class="space-y-4">
          <div id="frontend" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.technical.frontend.title', 'Frontend') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>Vue 3.5+ with TypeScript & Composition API</li>
              <li>Pinia for state management</li>
              <li>Vue Router for navigation</li>
              <li>TailwindCSS v4 + shadcn-vue components</li>
              <li>VeeValidate + Zod for form validation</li>
              <li>TanStack Query for server state management</li>
              <li>vue-i18n for internationalization</li>
            </ul>
          </div>

          <div id="backend" class="space-y-2 scroll-mt-18">
            <h3 class="text-xl font-semibold">
              {{ t('about.technical.backend.title', 'Backend') }}
            </h3>
            <ul class="list-disc list-inside space-y-1 text-muted-foreground ml-4">
              <li>FastAPI (Python) with async/await</li>
              <li>PostgreSQL database</li>
              <li>SQLAlchemy ORM with async support</li>
              <li>JWT authentication with refresh tokens</li>
              <li>Rate limiting and reCAPTCHA protection</li>
              <li>Modular architecture (auth, two-factor, email)</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- AI Context -->
      <section id="ai-context" class="space-y-4 scroll-mt-18">
        <h2 class="text-2xl font-semibold">
          {{ t('aiContext.title', 'AI Context') }}
        </h2>
        <p class="text-muted-foreground">
          {{ t('aiContext.subtitle', 'Short description of CareerHub in Markdown format for AI assistants like ChatGPT') }}
        </p>

        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>
                  {{ t('aiContext.card.title', 'Copy Context to Clipboard') }}
                </CardTitle>
                <CardDescription>
                  {{ t('aiContext.card.description', 'Click the button below to copy the context description. You can then paste it into ChatGPT or other AI assistants to provide context about CareerHub.') }}
                </CardDescription>
              </div>
              <Button @click="handleCopy">
                <Copy v-if="!copied" class="size-4" />
                <Check v-else class="size-4" />
                {{ copied ? t('common.copyToClipboard.copied') : t('common.copyToClipboard.copy') }}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <pre class="whitespace-pre-wrap text-sm font-mono bg-muted p-4 rounded-md border overflow-x-auto max-h-[600px] overflow-y-auto">{{ aiContextMarkdown }}</pre>
          </CardContent>
        </Card>
      </section>
    </div>
  </AuthenticatedLayout>
</template>

