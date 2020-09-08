const morgan = require("morgan");
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const db = require("./models");
const logger = require("./logger");
const seedData = require("./utils/seeder");

const app = express();

db.sequelize.sync({ force: true }).then(() => {
  seedData();
  console.log("Drop and re-sync db.");
});

var corsOptions = {
  origin: "http://localhost:8081",
};

app.use(cors(corsOptions));
app.use(morgan("dev", { stream: logger.stream }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// set port, listen for requests
const PORT = process.env.PORT || 3000;

require("./routes/betRoutes")(app);

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
