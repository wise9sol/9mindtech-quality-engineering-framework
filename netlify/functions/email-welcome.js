const { Resend } = require("resend");
const { logger } = require("./logger");

const resend = new Resend(process.env.RESEND_API_KEY);

const sendWelcomeEmail = async (email, company, apiKey, trialEndsAt) => {
  const trialEnd = new Date(trialEndsAt).toLocaleDateString("en-US", {
    month: "long", day: "numeric", year: "numeric"
  });

  try {
    await resend.emails.send({
      from: "QualiOps AI <onboarding@9mindtech.com>",
      to: email,
      subject: "Your QualiOps AI API key is ready",
      html: `
        <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:2rem;background:#080C12;color:#F5F7FA;">
          <div style="margin-bottom:1.5rem;">
            <span style="color:#0E7DFF;font-weight:700;font-size:1.1rem;">9MindTech AI</span>
          </div>
          <h1 style="font-size:1.5rem;font-weight:600;margin-bottom:1rem;color:#F5F7FA;">Your API key is ready, ${company}</h1>
          <p style="color:#8899AA;line-height:1.6;margin-bottom:1.5rem;">Your 14-day free trial of QualiOps AI starts now. Here is your API key ? save it somewhere safe. It will not be shown again.</p>
          <div style="background:#0F1923;border:1px solid #1A2535;border-radius:8px;padding:1rem;margin-bottom:1.5rem;font-family:monospace;font-size:0.9rem;color:#0E7DFF;word-break:break-all;">
            ${apiKey}
          </div>
          <p style="color:#8899AA;font-size:0.85rem;margin-bottom:1.5rem;">Your trial expires on <strong style="color:#F5F7FA;">${trialEnd}</strong>.</p>
          <div style="margin-bottom:1.5rem;">
            <p style="color:#F5F7FA;font-weight:600;margin-bottom:0.75rem;">Quick Start</p>
            <p style="color:#8899AA;line-height:1.6;">1. Copy your API key above<br>2. Make your first API call<br>3. Run your first NIST 800-53 compliance scan<br>4. View your Allure report</p>
          </div>
          <a href="https://9mindtech.com" style="display:inline-block;background:#0E7DFF;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:500;">View Quick Start Guide</a>
          <p style="color:#5F6B7A;font-size:0.8rem;margin-top:2rem;">Questions? Reply to this email or book a call at calendly.com/9mindtech_qa-automation-call</p>
        </div>
      `
    });
    logger.info("Welcome email sent", { email, company });
  } catch (err) {
    logger.error("Welcome email failed", err, { email });
  }
};

module.exports = { sendWelcomeEmail };
