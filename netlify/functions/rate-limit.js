const { Ratelimit } = require("@upstash/ratelimit");
const { Redis } = require("@upstash/redis");

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

const limiters = {
  signup: new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(3, "1 h") }),
  "validate-key": new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(100, "1 h") }),
  "submit-config": new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(20, "1 h") }),
  "trigger-scan": new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(10, "1 h") }),
};

const checkRateLimit = async (identifier, endpoint) => {
  const limiter = limiters[endpoint] || limiters["validate-key"];
  const { success, remaining, reset } = await limiter.limit(identifier);
  return { success, remaining, reset };
};

module.exports = { checkRateLimit };
