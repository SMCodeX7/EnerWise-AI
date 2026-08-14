import type { EmailOtpType } from "@supabase/supabase-js";
import { NextRequest, NextResponse } from "next/server";

import { createClient } from "@/lib/supabase/server";

export async function GET(request: NextRequest) {
  const tokenHash = request.nextUrl.searchParams.get("token_hash");
  const type = request.nextUrl.searchParams.get(
    "type",
  ) as EmailOtpType | null;

  const redirectTo = request.nextUrl.clone();

  redirectTo.pathname = "/login";
  redirectTo.searchParams.delete("token_hash");
  redirectTo.searchParams.delete("type");

  if (tokenHash && type) {
    const supabase = await createClient();

    const { error } = await supabase.auth.verifyOtp({
      token_hash: tokenHash,
      type,
    });

    if (!error) {
      redirectTo.searchParams.set(
        "message",
        "Email confirmed successfully. You can now sign in.",
      );

      return NextResponse.redirect(redirectTo);
    }
  }

  redirectTo.searchParams.set(
    "error",
    "Email confirmation failed or the link has expired.",
  );

  return NextResponse.redirect(redirectTo);
}