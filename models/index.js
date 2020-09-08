const dbConfig = require("../config/db.config.js");

const Sequelize = require("sequelize");
const sequelize = new Sequelize(dbConfig.URI, {
  dialect: dbConfig.dialect,
  dialectOptions: dbConfig.dialectOptions,
});

const db = {};

db.Sequelize = Sequelize;
db.sequelize = sequelize;

db.bets = require("./bets.js")(sequelize, Sequelize);

module.exports = db;
