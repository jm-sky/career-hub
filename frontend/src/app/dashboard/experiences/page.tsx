import { ProtectedRoute } from '@/components/auth/protected-route';
import { ExperienceManagement } from '@/components/experience/ExperienceManagement';

export default function ExperiencesPage() {
  return (
    <ProtectedRoute>
      <ExperienceManagement />
    </ProtectedRoute>
  );
}

