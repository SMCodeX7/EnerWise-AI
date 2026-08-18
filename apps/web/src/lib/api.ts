export interface BackendHealth {
  status: string;
  service: string;
  version: string;
  environment: string;
}

export interface BackendAuthenticatedUser {
  id: string;
  email: string | null;
  full_name: string | null;
  role: "USER" | "ADMIN";
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ??
  "http://127.0.0.1:8000";

export async function getBackendHealth(
  signal?: AbortSignal,
): Promise<BackendHealth> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error(
      `Backend health request failed with status ${response.status}`,
    );
  }

  return response.json() as Promise<BackendHealth>;
}

export async function getBackendCurrentUser(
  accessToken: string,
): Promise<BackendAuthenticatedUser> {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
    method: "GET",
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(
      `Backend authentication request failed with status ${response.status}`,
    );
  }

  return response.json() as Promise<BackendAuthenticatedUser>;
}