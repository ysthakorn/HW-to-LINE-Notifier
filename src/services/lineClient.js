const axios = require("axios");
const env = require("../config/env");

const LINE_PUSH_API_URL = "https://api.line.me/v2/bot/message/push";

async function pushTextMessage(messageText) {
  return axios.post(
    LINE_PUSH_API_URL,
    {
      to: env.lineGroupId,
      messages: [{ type: "text", text: messageText }],
    },
    {
      headers: {
        Authorization: `Bearer ${env.lineAccessToken}`,
        "Content-Type": "application/json",
      },
      timeout: env.lineRequestTimeoutMs,
    }
  );
}

module.exports = {
  pushTextMessage,
};
