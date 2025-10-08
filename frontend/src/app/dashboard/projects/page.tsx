import { ProtectedRoute } from '@/components/auth/protected-route';
import { ProjectManagement } from '@/components/project/ProjectManagement';

export default function ProjectsPage() {
  return (
    <ProtectedRoute>
      <ProjectManagement />
    </ProtectedRoute>
  );
}
