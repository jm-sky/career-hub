import Link from "next/link";

export default function LogoTextLink({ href = '/' }: { href: string }) {
    return (
        <Link href={href} className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-500 hover:scale-105 transition-all duration-300">CareerHub</Link>
    );
}