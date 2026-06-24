const logger = {
  info: (msg, meta = {}) => console.log(JSON.stringify({
    level: "info",
    msg,
    meta,
    timestamp: new Date().toISOString()
  })),
  error: (msg, err = {}, meta = {}) => console.error(JSON.stringify({
    level: "error",
    msg,
    error: err.stack || err.message || err,
    meta,
    timestamp: new Date().toISOString()
  })),
  warn: (msg, meta = {}) => console.warn(JSON.stringify({
    level: "warn",
    msg,
    meta,
    timestamp: new Date().toISOString()
  }))
};

module.exports = { logger };
