module.exports = (app) => {
  const bets = require("../controllers/betController.js");

  var router = require("express").Router();

  router.post("/", bets.create);
  router.get("/", bets.findAll);
  router.get("/unbet", bets.findAllNewBets);
  router.get("/:id", bets.findOne);
  router.put("/:id", bets.update);
  router.delete("/:id", bets.delete);
  router.delete("/", bets.deleteAll);

  app.use("/api/bets", router);
};
