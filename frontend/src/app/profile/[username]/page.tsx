'use client';

// Public profile page - displays user's public profile

import { useParams } from 'next/navigation';
import { PublicProfile } from '@/components/profile/PublicProfile';

export default function PublicProfilePage() {
  const params = useParams();
  const username = params.username as string;

  return <PublicProfile username={username} />;
}
