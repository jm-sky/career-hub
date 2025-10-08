'use client';

import LogoTextLink from "./LogoTextLink";
import { ProfileDropdown } from "./ProfileDropdown";

export default function TopBar() {
    return (
        <div className="flex flex-row justify-between items-center gap-2 border-b py-2 px-4 shadow-sm bg-background/50 backdrop-blur-sm">
            <LogoTextLink href="/dashboard" />
            <ProfileDropdown />
        </div>
    );
}