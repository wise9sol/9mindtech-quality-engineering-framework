const { createClient } = require("@supabase/supabase-js");
const crypto = require("crypto");
const bcrypt = require("bcryptjs");
const { checkRateLimit } = require("./rate-limit");
const { logger } = require("./logger");

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
    return { statusCode: 405, headers: CORS_HEADERS, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  const ip = event.headers["x-forwarded-for"] || "unknown";
  const { success } = await checkRateLimit(ip, "signup");
  if (!success) {
    logger.warn("Rate limit hit on signup", { ip });
    return { statusCode: 429, headers: CORS_HEADERS, body: JSON.stringify({ error: "Too many requests. Try again later." }) };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Invalid JSON body" }) };
  }

  const { email, company, password } = payload;

  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Invalid email address" }) };
  }
  if (!company || company.trim().length < 2) {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Company name is required" }) };
  }
  if (!password || password.length < 8) {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Password must be at least 8 characters" }) };
  }

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

  const { data: existing } = await supabase
    .from("trial_users")
    .select("id")
    .eq("email", email.toLowerCase())
    .maybeSingle();

  if (existing) {
    return { statusCode: 409, headers: CORS_HEADERS, body: JSON.stringify({ error: "This email is already registered" }) };
  }

  const passwordHash = await bcrypt.hash(password, 12);
  const rawKey = crypto.randomBytes(24).toString("hex");
  const apiKey = `qai_live_${rawKey}`;
  const keyHash = crypto.createHash("sha256").update(apiKey).digest("hex");
  const keyPrefix = apiKey.slice(0, 12);

  const trialEndsAt = new Date();
  trialEndsAt.setDate(trialEndsAt.getDate() + 14);

  const { error: insertError } = await supabase.from("trial_users").insert({
    email: email.toLowerCase(),
    company: company.trim(),
    password_hash: passwordHash,
    api_key_hash: keyHash,
    api_key_prefix: keyPrefix,
    trial_ends_at: trialEndsAt.toISOString(),
  });

  if (insertError) {
    logger.error("Supabase insert error", insertError, { email, company });
    return { statusCode: 500, headers: CORS_HEADERS, body: JSON.stringify({ error: "Account creation failed. Please try again." }) };
  }

  logger.info("User signed up", { email, company, trialEndsAt });

  return {
    statusCode: 200,
    headers: CORS_HEADERS,
    body: JSON.stringify({ apiKey, keyPrefix, trialEndsAt: trialEndsAt.toISOString(), message: "Account created successfully" }),
  };
};
