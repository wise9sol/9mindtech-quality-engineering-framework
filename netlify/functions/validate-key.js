const { createClient } = require("@supabase/supabase-js");
const crypto = require("crypto");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": process.env.ALLOWED_ORIGIN || "*",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Content-Type": "application/json",
};

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: CORS_HEADERS, body: "" };
  }

  // Accept key from Authorization: Bearer <key> OR X-API-Key: <key> header
  const authHeader = event.headers["authorization"] || "";
  const xApiKey = event.headers["x-api-key"] || "";
  const rawKey = authHeader.startsWith("Bearer ")
    ? authHeader.slice(7).trim()
    : xApiKey.trim();

  if (!rawKey) {
    return {
      statusCode: 401,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "API key required. Pass via Authorization: Bearer <key> or X-API-Key header." }),
    };
  }

  // Quick format sanity check before hitting the DB
  if (!rawKey.startsWith("qai_live_") || rawKey.length < 40) {
    return {
      statusCode: 401,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Invalid API key format" }),
    };
  }

  const keyHash = crypto.createHash("sha256").update(rawKey).digest("hex");

  const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_KEY
  );

  const { data: user, error } = await supabase
    .from("trial_users")
    .select("id, email, company, trial_ends_at, is_active")
    .eq("api_key_hash", keyHash)
    .maybeSingle();

  if (error || !user) {
    return {
      statusCode: 401,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "API key not recognised" }),
    };
  }

  if (!user.is_active) {
    return {
      statusCode: 403,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Account suspended. Contact support@9mindtech.com" }),
    };
  }

  const now = new Date();
  const trialEnd = new Date(user.trial_ends_at);
  if (now > trialEnd) {
    return {
      statusCode: 403,
      headers: CORS_HEADERS,
      body: JSON.stringify({
        error: "Trial expired",
        trialEndedAt: trialEnd.toISOString(),
        upgradeUrl: "https://9mindtech.com/#pricing",
      }),
    };
  }

  const daysLeft = Math.ceil((trialEnd - now) / (1000 * 60 * 60 * 24));

  return {
    statusCode: 200,
    headers: CORS_HEADERS,
    body: JSON.stringify({
      valid: true,
      userId: user.id,
      company: user.company,
      trialEndsAt: trialEnd.toISOString(),
      daysRemaining: daysLeft,
    }),
  };
};
