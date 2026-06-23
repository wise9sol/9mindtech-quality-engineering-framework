const { createClient } = require("@supabase/supabase-js");
const crypto = require("crypto");
const bcrypt = require("bcryptjs");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": process.env.ALLOWED_ORIGIN || "*",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Content-Type": "application/json",
};

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: CORS_HEADERS, body: "" };
  }

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Method not allowed" }),
    };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch {
    return {
      statusCode: 400,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Invalid JSON body" }),
    };
  }

  const { email, company, password } = payload;

  // --- Input validation ---
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return {
      statusCode: 400,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Invalid email address" }),
    };
  }
  if (!company || company.trim().length < 2) {
    return {
      statusCode: 400,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Company name is required" }),
    };
  }
  if (!password || password.length < 8) {
    return {
      statusCode: 400,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Password must be at least 8 characters" }),
    };
  }

  // --- Supabase client (service role — never expose this key client-side) ---
  const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_KEY
  );

  // --- Duplicate email check ---
  const { data: existing } = await supabase
    .from("trial_users")
    .select("id")
    .eq("email", email.toLowerCase())
    .maybeSingle();

  if (existing) {
    return {
      statusCode: 409,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "This email is already registered" }),
    };
  }

  // --- Hash password ---
  const passwordHash = await bcrypt.hash(password, 12);

  // --- Generate API key ---
  // Format: qai_live_<48 hex chars> — 60 chars total, easy to identify in logs
  const rawKey = crypto.randomBytes(24).toString("hex");
  const apiKey = `qai_live_${rawKey}`;

  // We store only a SHA-256 hash of the full key (never the plaintext)
  const keyHash = crypto.createHash("sha256").update(apiKey).digest("hex");
  // Store the first 12 chars so users can identify which key is which in the dashboard
  const keyPrefix = apiKey.slice(0, 12);

  // --- Trial expiry ---
  const trialEndsAt = new Date();
  trialEndsAt.setDate(trialEndsAt.getDate() + 14);

  // --- Insert user ---
  const { error: insertError } = await supabase.from("trial_users").insert({
    email: email.toLowerCase(),
    company: company.trim(),
    password_hash: passwordHash,
    api_key_hash: keyHash,
    api_key_prefix: keyPrefix,
    trial_ends_at: trialEndsAt.toISOString(),
  });

  if (insertError) {
    console.error("Supabase insert error:", insertError);
    return {
      statusCode: 500,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Account creation failed. Please try again." }),
    };
  }

  // --- Return the plaintext key ONCE — never stored, never logged ---
  return {
    statusCode: 200,
    headers: CORS_HEADERS,
    body: JSON.stringify({
      apiKey,
      keyPrefix,
      trialEndsAt: trialEndsAt.toISOString(),
      message: "Account created successfully",
    }),
  };
};
