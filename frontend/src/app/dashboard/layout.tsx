import TopBar from "@/components/layout/TopBar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen bg-slate-200">
        <TopBar />
        <div className="flex-1">{children}</div>
    </div>
  );
}