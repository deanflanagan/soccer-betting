const fs = require("fs");
const path = require("path");
const db = require("../models");

module.exports = () => {
  Object.keys(db).forEach((element) => {
    if (element.toLowerCase() != "sequelize") {
      console.log(element);

      db[element].bulkCreate(
        JSON.parse(
          fs.readFileSync(path.join("data", `${element.toLowerCase()}.json`))
        )
      );
      console.log(`${element} data has been added!`);
    }
  });
  return;
};
