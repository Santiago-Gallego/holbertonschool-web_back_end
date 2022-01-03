const express = require("express");
const router = require("./routes/index");

const app = express();
const PORT = 12345;

app.use("/", router);

app.listen(PORT);

module.exports = app;
