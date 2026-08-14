"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { createClient } from "@/lib/supabase/server";

function getValue(formData: FormData, key: string) {
  const value = formData.get(key);
  return typeof value === "string" ? value.trim() : "";
}

export async function login(formData: FormData) {
  const email = getValue(formData, "email").toLowerCase();
  const password = getValue(formData, "password");

  if (!email || !password) {
    redirect("/login?error=Email%20and%20password%20are%20required");
  }

  const supabase = await createClient();

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    redirect(
      "/login?error=Unable%20to%20sign%20in.%20Check%20your%20credentials%20and%20email%20confirmation.",
    );
  }

  revalidatePath("/", "layout");
  redirect("/dashboard");
}

export async function signup(formData: FormData) {
  const fullName = getValue(formData, "fullName");
  const email = getValue(formData, "email").toLowerCase();
  const password = getValue(formData, "password");

  if (fullName.length < 2 || fullName.length > 150) {
    redirect("/signup?error=Enter%20a%20valid%20full%20name");
  }

  if (!email || !email.includes("@")) {
    redirect("/signup?error=Enter%20a%20valid%20email%20address");
  }

  if (password.length < 8) {
    redirect(
      "/signup?error=Password%20must%20contain%20at%20least%208%20characters",
    );
  }

  const supabase = await createClient();

  const { error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName,
      },
    },
  });

  if (error) {
    redirect(
      "/signup?error=Unable%20to%20create%20your%20account.%20Please%20try%20again.",
    );
  }

  redirect(
    "/login?message=Account%20created%20successfully.%20You%20can%20now%20sign%20in.",
  );
}

export async function logout() {
  const supabase = await createClient();

  await supabase.auth.signOut({
    scope: "local",
  });

  revalidatePath("/", "layout");
  redirect("/login");
}