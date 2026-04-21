const express = require("express");
const path = require("path");

const { buildHomeworkMessage } = require("../services/messageBuilder");
const { pushTextMessage } = require("../services/lineClient");

const router = express.Router();

router.get("/", (req, res) => {
  res.sendFile(path.resolve(__dirname, "../views/index.html"));
});

router.get("/health", (req, res) => {
  res.json({ ok: true });
});

router.post("/notify", async (req, res) => {
  const payload = req.body || {};
  const message = buildHomeworkMessage(payload);

  try {
    await pushTextMessage(message);
    return res.json({ ok: true });
  } catch (error) {
    const status = error.response?.status || 502;
    const errorMessage =
      error.response?.data || error.message || "line_request_failed";

    return res.status(status).json({ error: errorMessage });
  }
});

module.exports = router;
