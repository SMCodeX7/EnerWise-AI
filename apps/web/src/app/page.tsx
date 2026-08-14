export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col justify-center px-6 py-20 lg:px-8">
        <div className="max-w-4xl">
          <span className="inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-sm font-medium text-emerald-300">
            Evidence-Grounded Renewable Energy Intelligence
          </span>

          <h1 className="mt-8 text-5xl font-semibold tracking-tight sm:text-6xl lg:text-7xl">
            EnerWise AI
          </h1>

          <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300 sm:text-xl">
            A multi-agent renewable-energy feasibility and decision-support
            platform combining NLP, hybrid information retrieval, RAG,
            deterministic analysis, security, and Responsible AI.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <button
              type="button"
              className="rounded-xl bg-emerald-400 px-6 py-3 font-semibold text-slate-950 transition hover:bg-emerald-300"
            >
              Start Assessment
            </button>

            <button
              type="button"
              className="rounded-xl border border-slate-700 px-6 py-3 font-semibold text-slate-200 transition hover:border-slate-500 hover:bg-slate-900"
            >
              How It Works
            </button>
          </div>
        </div>

        <div className="mt-20 grid gap-6 md:grid-cols-3">
          <article className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm font-medium text-emerald-300">
              Agentic Intelligence
            </p>
            <h2 className="mt-3 text-xl font-semibold">
              Coordinated AI Analysis
            </h2>
            <p className="mt-3 leading-7 text-slate-400">
              Specialized agents collaborate to understand requirements,
              retrieve evidence, evaluate feasibility, analyse scenarios, and
              verify recommendations.
            </p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm font-medium text-emerald-300">
              Evidence Grounding
            </p>
            <h2 className="mt-3 text-xl font-semibold">
              Hybrid Information Retrieval
            </h2>
            <p className="mt-3 leading-7 text-slate-400">
              Technical recommendations are grounded using trusted renewable
              energy documents, semantic retrieval, lexical search, ranking,
              and source citations.
            </p>
          </article>

          <article className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
            <p className="text-sm font-medium text-emerald-300">
              Responsible AI
            </p>
            <h2 className="mt-3 text-xl font-semibold">
              Explainable Recommendations
            </h2>
            <p className="mt-3 leading-7 text-slate-400">
              Results distinguish evidence, calculations, assumptions,
              uncertainty, missing information, limitations, and confidence.
            </p>
          </article>
        </div>

        <div className="mt-10 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">Platform status</p>
              <p className="mt-1 font-medium text-slate-200">
                Frontend foundation operational
              </p>
            </div>

            <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-sm text-emerald-300">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              Web application online
            </span>
          </div>
        </div>

        <p className="mt-8 max-w-3xl text-sm leading-6 text-slate-500">
          EnerWise AI provides preliminary AI-assisted renewable-energy
          decision support. Final engineering, installation, regulatory, and
          investment decisions should be reviewed by appropriately qualified
          professionals.
        </p>
      </section>
    </main>
  );
}