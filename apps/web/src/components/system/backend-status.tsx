"use client";

import { useEffect, useState } from "react";

import {
  getBackendHealth,
  type BackendHealth,
} from "@/lib/api";

type StatusState =
  | {
      state: "loading";
      health: null;
    }
  | {
      state: "online";
      health: BackendHealth;
    }
  | {
      state: "offline";
      health: null;
    };

export function BackendStatus() {
  const [status, setStatus] = useState<StatusState>({
    state: "loading",
    health: null,
  });

  useEffect(() => {
    const controller = new AbortController();

    const loadHealth = async () => {
      try {
        const health = await getBackendHealth(controller.signal);

        setStatus({
          state: "online",
          health,
        });
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        console.error("Unable to reach EnerWise AI backend:", error);

        setStatus({
          state: "offline",
          health: null,
        });
      }
    };

    void loadHealth();

    return () => {
      controller.abort();
    };
  }, []);

  if (status.state === "loading") {
    return (
      <div className="mt-10 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
        <p className="text-sm text-slate-500">Platform status</p>

        <p className="mt-2 font-medium text-slate-300">
          Checking backend connection...
        </p>
      </div>
    );
  }

  if (status.state === "offline") {
    return (
      <div className="mt-10 rounded-2xl border border-amber-500/30 bg-amber-500/10 p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm text-amber-300">Platform status</p>

            <p className="mt-1 font-medium text-slate-100">
              Backend connection unavailable
            </p>
          </div>

          <span className="inline-flex items-center gap-2 rounded-full border border-amber-400/30 px-3 py-1 text-sm text-amber-300">
            <span className="h-2 w-2 rounded-full bg-amber-400" />
            API offline
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-10 rounded-2xl border border-emerald-400/20 bg-emerald-400/5 p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm text-slate-500">Platform status</p>

          <p className="mt-1 font-medium text-slate-200">
            {status.health.service}
          </p>

          <p className="mt-1 text-sm text-slate-500">
            Version {status.health.version} · {status.health.environment}
          </p>
        </div>

        <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-sm text-emerald-300">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          API connected
        </span>
      </div>
    </div>
  );
}