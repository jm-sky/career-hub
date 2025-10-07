import { ProtectedRoute } from '@/components/auth/protected-route';
import { ProfileWizardSteps } from '@/components/profile/ProfileWizardSteps';

export default function EditProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileWizardSteps />
    </ProtectedRoute>
  );
}
