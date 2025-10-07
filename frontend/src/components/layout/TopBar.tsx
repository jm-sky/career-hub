'use client';

import { Button } from "../ui/button";
import LogoTextLink from "./LogoTextLink";
import { useAuth } from '@/contexts/auth-context';

export default function TopBar() {
    const { logout } = useAuth();

    return (
        <div className="flex flex-row justify-between items-center gap-2 border-b py-2 px-4 shadow-sm bg-background/50 backdrop-blur-sm">
            <LogoTextLink />
            <Button onClick={logout}>Logout</Button>
        </div>
    );
}