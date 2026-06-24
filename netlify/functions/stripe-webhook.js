const stripe = require("stripe")(process.env.STRIPE_SECRET_KEY);
const { createClient } = require("@supabase/supabase-js");
const { logger } = require("./logger");

exports.handler = async (event) => {
  const sig = event.headers["stripe-signature"];
  let stripeEvent;

  try {
    stripeEvent = stripe.webhooks.constructEvent(
      event.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    logger.error("Webhook signature verification failed", err);
    return { statusCode: 400, body: JSON.stringify({ error: "Invalid signature" }) };
  }

  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

  try {
    switch (stripeEvent.type) {

      case "checkout.session.completed": {
        const session = stripeEvent.data.object;
        const email = session.customer_email || session.metadata?.email;
        const plan = session.metadata?.plan;

        if (email && plan) {
          const { error } = await supabase
            .from("trial_users")
            .update({ plan })
            .eq("email", email.toLowerCase());

          if (error) {
            logger.error("Failed to update plan on checkout", error, { email, plan });
          } else {
            logger.info("Plan upgraded on checkout", { email, plan });
          }
        }
        break;
      }

      case "customer.subscription.deleted": {
        const subscription = stripeEvent.data.object;
        const customerId = subscription.customer;

        const customer = await stripe.customers.retrieve(customerId);
        const email = customer.email;

        if (email) {
          const { error } = await supabase
            .from("trial_users")
            .update({ plan: "expired" })
            .eq("email", email.toLowerCase());

          if (error) {
            logger.error("Failed to downgrade plan", error, { email });
          } else {
            logger.info("Subscription cancelled ? plan set to expired", { email });
          }
        }
        break;
      }

      default:
        logger.info("Unhandled Stripe event", { type: stripeEvent.type });
    }

    return { statusCode: 200, body: JSON.stringify({ received: true }) };

  } catch (err) {
    logger.error("Webhook handler error", err);
    return { statusCode: 500, body: JSON.stringify({ error: "Webhook processing failed" }) };
  }
};
