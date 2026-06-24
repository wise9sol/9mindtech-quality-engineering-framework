const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);
const { logger } = require("./logger");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": process.env.ALLOWED_ORIGIN || "*",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Content-Type": "application/json",
};

const PRICE_MAP = {
  audit: process.env.STRIPE_PRICE_AUDIT,
  setup: process.env.STRIPE_PRICE_SETUP,
  qaas:  process.env.STRIPE_PRICE_QAAS,
};

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers: CORS_HEADERS, body: "" };
  }
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, headers: CORS_HEADERS, body: JSON.stringify({ error: "Method not allowed" }) };
  }

  let payload;
  try {
    payload = JSON.parse(event.body || "{}");
  } catch {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Invalid JSON body" }) };
  }

  const { plan, email, idempotencyKey } = payload;

  if (!PRICE_MAP[plan]) {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Invalid plan. Choose: audit, setup, or qaas" }) };
  }

  if (!email) {
    return { statusCode: 400, headers: CORS_HEADERS, body: JSON.stringify({ error: "Email is required" }) };
  }

  try {
    const isRecurring = plan === "qaas";

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      customer_email: email,
      line_items: [{ price: PRICE_MAP[plan], quantity: 1 }],
      mode: isRecurring ? "subscription" : "payment",
      success_url: "https://9mindtech.com/success?session_id={CHECKOUT_SESSION_ID}",
      cancel_url: "https://9mindtech.com/#pricing",
      metadata: { plan, email },
    }, {
      idempotencyKey: idempotencyKey || undefined,
    });

    logger.info("Checkout session created", { email, plan, sessionId: session.id });

    return {
      statusCode: 200,
      headers: CORS_HEADERS,
      body: JSON.stringify({ url: session.url, sessionId: session.id }),
    };

  } catch (err) {
    logger.error("Stripe checkout error", err, { email, plan });
    return { statusCode: 500, headers: CORS_HEADERS, body: JSON.stringify({ error: "Failed to create checkout session" }) };
  }
};
