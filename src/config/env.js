const dotenv = require("dotenv");

dotenv.config();

const env = {
  lineAccessToken: process.env.LINE_ACCESS_TOKEN || "YOUR_TOKEN_HERE",
  lineGroupId: process.env.LINE_GROUP_ID || "YOUR_GROUP_ID_HERE",
  port: Number(process.env.PORT || 8080),
  lineRequestTimeoutMs: Number(process.env.LINE_REQUEST_TIMEOUT_SEC || 10) * 1000,
  googleSheetCsvUrl: process.env.GOOGLE_SHEET_CSV_URL || "",
};

module.exports = env;
