import { redirect } from "next/navigation";

import { logout } from "@/app/auth/actions";
import { createClient } from "@/lib/supabase/server";

export default async function DashboardPage() {
  const supabase = await createClient();

  const { data: claimsData, error: claimsError } =
    await supabase.auth.getClaims();

  if (claimsError || !claimsData?.claims?.sub) {
    redirect("/login");
  }

  const userId = claimsData.claims.sub;

  const { data: profile } = await supabase
    .from("profiles")
    .select("full_name, role, created_at")
    .eq("id", userId)
    .single();

  const email =
    typeof claimsData.claims.email === "string"
      ? claimsData.claims.email
      : "No email available";

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-white">
      <div className="mx-auto max-w-6xl">
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
          <div>
            <p className="text-sm font-medium text-emerald-400">
              EnerWise AI
            </p>

            <h1 className="mt-1 text-3xl font-semibold">
              Dashboard
            </h1>
          </div>

          <form action={logout}>
            <button
              type="submit"
              className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500 hover:bg-slate-900"
            >
              Sign out
            </button>
          </form>
        </header>

        <section className="mt-10 grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 md:col-span-2">
            <p className="text-sm text-slate-400">
              Welcome
            </p>

            <h2 className="mt-2 text-2xl font-semibold">
              {profile?.full_name ?? "EnerWise User"}
            </h2>

            <p className="mt-2 text-slate-400">
              Start a renewable-energy feasibility assessment and receive
              evidence-grounded recommendations.
            </p>

            <button
              type="button"
              disabled
              className="mt-6 rounded-lg bg-emerald-500 px-5 py-3 font-semibold text-slate-950 opacity-60"
            >
              New Assessment
            </button>

            <p className="mt-2 text-xs text-slate-500">
              Assessment creation will be added in the next phase.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-lg font-semibold">
              Account
            </h2>

            <dl className="mt-5 space-y-4 text-sm">
              <div>
                <dt className="text-slate-500">Email</dt>
                <dd className="mt-1 break-all text-slate-200">
                  {email}
                </dd>
              </div>

              <div>
                <dt className="text-slate-500">Role</dt>
                <dd className="mt-1 text-slate-200">
                  {profile?.role ?? "USER"}
                </dd>
              </div>
            </dl>
          </div>
        </section>

        <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold">
            Your assessments
          </h2>

          <p className="mt-2 text-sm text-slate-400">
            You have not created any assessments yet.
          </p>
        </section>
      </div>
    </main>
  );
}