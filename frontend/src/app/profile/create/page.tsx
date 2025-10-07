import { ProfileWizard } from '@/components/profile/profile-wizard';
import { ProtectedRoute } from '@/components/auth/protected-route';

export default function CreateProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileWizard />
    </ProtectedRoute>
  );
}
