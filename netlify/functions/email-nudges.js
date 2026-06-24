const { createClient } = require("@supabase/supabase-js");
const { Resend } = require("resend");
const { logger } = require("./logger");

const resend = new Resend(process.env.RESEND_API_KEY);

exports.handler = async () => {
  const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
  const now = new Date();

  // Day 7 nudge — trial started 7 days ago
  const day7Start = new Date(now); day7Start.setDate(day7Start.getDate() - 7);
  day7Start.setHours(0,0,0,0);
  const day7End = new Date(day7Start); day7End.setHours(23,59,59,999);

  // Day 13 upgrade prompt — trial ends tomorrow
  const day13Start = new Date(now); day13Start.setDate(day13Start.getDate() - 13);
  day13Start.setHours(0,0,0,0);
  const day13End = new Date(day13Start); day13End.setHours(23,59,59,999);

  // Fetch Day 7 users
  const { data: day7Users } = await supabase
    .from("trial_users")
    .select("email, company")
    .gte("created_at", day7Start.toISOString())
    .lte("created_at", day7End.toISOString())
    .eq("plan", "trial");

  for (const user of day7Users || []) {
    try {
      await resend.emails.send({
        from: "QualiOps AI <onboarding@9mindtech.com>",
        to: user.email,
        subject: "You are halfway through your QualiOps AI trial",
        html: `
          <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:2rem;background:#080C12;color:#F5F7FA;">
            <div style="margin-bottom:1.5rem;"><span style="color:#0E7DFF;font-weight:700;">9MindTech AI</span></div>
            <h1 style="font-size:1.5rem;font-weight:600;margin-bottom:1rem;">7 days in — have you run your first scan?</h1>
            <p style="color:#8899AA;line-height:1.6;margin-bottom:1.5rem;">Hi ${user.company}, you are halfway through your 14-day QualiOps AI trial. If you have not run your first NIST 800-53 compliance scan yet, now is the time.</p>
            <a href="https://9mindtech.com" style="display:inline-block;background:#0E7DFF;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:500;">Run your first scan</a>
            <p style="color:#5F6B7A;font-size:0.8rem;margin-top:2rem;">Need help? Book a call at calendly.com/9mindtech_qa-automation-call</p>
          </div>
        `
      });
      logger.info("Day 7 nudge sent", { email: user.email });
    } catch (err) {
      logger.error("Day 7 nudge failed", err, { email: user.email });
    }
  }

  // Fetch Day 13 users
  const { data: day13Users } = await supabase
    .from("trial_users")
    .select("email, company, trial_ends_at")
    .gte("created_at", day13Start.toISOString())
    .lte("created_at", day13End.toISOString())
    .eq("plan", "trial");

  for (const user of day13Users || []) {
    try {
      await resend.emails.send({
        from: "QualiOps AI <onboarding@9mindtech.com>",
        to: user.email,
        subject: "Your QualiOps AI trial ends tomorrow",
        html: `
          <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:2rem;background:#080C12;color:#F5F7FA;">
            <div style="margin-bottom:1.5rem;"><span style="color:#0E7DFF;font-weight:700;">9MindTech AI</span></div>
            <h1 style="font-size:1.5rem;font-weight:600;margin-bottom:1rem;">Your trial ends tomorrow</h1>
            <p style="color:#8899AA;line-height:1.6;margin-bottom:1.5rem;">Hi ${user.company}, your QualiOps AI trial expires tomorrow. Upgrade now to keep your API access, scan history, and Allure reports.</p>
            <a href="https://9mindtech.com/#pricing" style="display:inline-block;background:#0E7DFF;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:500;">Upgrade now</a>
            <p style="color:#5F6B7A;font-size:0.8rem;margin-top:2rem;">Questions? Reply to this email or call (240) 269-8965</p>
          </div>
        `
      });
      logger.info("Day 13 upgrade prompt sent", { email: user.email });
    } catch (err) {
      logger.error("Day 13 prompt failed", err, { email: user.email });
    }
  }

  return { statusCode: 200, body: JSON.stringify({ message: "Nudges sent" }) };
};
