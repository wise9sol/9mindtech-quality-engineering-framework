const { createClient } = require("@supabase/supabase-js");
const { Redis } = require("@upstash/redis");
const { logger } = require("./logger");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": process.env.ALLOWED_ORIGIN || "*",
  "Content-Type": "application/json",
  "X-Content-Type-Options": "nosniff",
};

exports.handler = async () => {
  const services = { supabase: "ok", redis: "ok" };
  let healthy = true;

  try {
    const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
    const { error } = await supabase.from("trial_users").select("id").limit(1);
    if (error) throw error;
  } catch (err) {
    logger.error("Health check ? Supabase failed", err);
    services.supabase = "error";
    healthy = false;
  }

  try {
    const redis = new Redis({
      url: process.env.UPSTASH_REDIS_REST_URL,
      token: process.env.UPSTASH_REDIS_REST_TOKEN,
    });
    await redis.ping();
  } catch (err) {
    logger.error("Health check ? Redis failed", err);
    services.redis = "error";
    healthy = false;
  }

  logger.info("Health check", { services, healthy });

  return {
    statusCode: healthy ? 200 : 503,
    headers: CORS_HEADERS,
    body: JSON.stringify({
      status: healthy ? "healthy" : "degraded",
      services,
      version: process.env.RELEASE_VERSION || "1.0.0",
      timestamp: new Date().toISOString(),
    }),
  };
};

