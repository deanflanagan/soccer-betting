const request = require("request-promise");
const dotenv = require("dotenv");
dotenv.config({ path: "./config.env" });

// const getOdds = function () {
//   console.log("Got the odds");
const res = request({
  method: "GET",
  uri:
    "https://api.pinnacle.com/v1/odds/special?sportId=24&specialId=1122578687&oddsFormat=Decimal",
  json: true,
  headers: {
    Authorization:
      "Basic " + new Buffer(process.env.PINNACLE_TOKEN).toString("base64"),
  },
}).then((r) => console.log(r));

// console.log(getOdds());
