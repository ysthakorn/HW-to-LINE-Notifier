const express = require("express");
const notifyRoutes = require("./routes/notifyRoutes");

function createApp() {
  const app = express();

  app.use(express.json());
  app.use(notifyRoutes);

  return app;
}

module.exports = createApp;
