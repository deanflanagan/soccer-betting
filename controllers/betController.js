const db = require("../models");
const Bet = db.bets;
const Op = db.Sequelize.Op;

exports.create = (req, res) => {
  // Validate request
  if (!req.body.date) {
    res.status(400).send({
      message: "Content can not be empty!",
    });
    return;
  }

  // Create a bet
  const bet = {
    date: req.body.date,
    home: req.body.home,
    away: req.body.away,
    odds: req.body.odds,
    home_bet: -1,
    unbet: true,
    kick_off: req.body.kick_off,
  };

  // Save Tutorial in the database
  Bet.create(bet)
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: err.message || "Some error occurred while creating the Bet.",
      });
    });
};

exports.findAll = (req, res) => {
  // get all bets on a certain day
  Bet.findAll()
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving tutorials.",
      });
    });
};

exports.findOne = (req, res) => {
  const id = req.params.id;

  Bet.findByPk(id)
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message: "Error retrieving bet with id=" + id,
      });
    });
};

exports.update = (req, res) => {
  const id = req.params.id;

  Bet.update(req.body, {
    where: { id: id },
  })
    .then((num) => {
      if (num == 1) {
        res.send({
          message: "Bet was updated successfully.",
        });
      } else {
        res.send({
          message: `Cannot update Bet with id=${id}. Maybe Bet was not found or req.body is empty!`,
        });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: `Error updating Bet with id=${id}`,
      });
    });
};

exports.delete = (req, res) => {
  const id = req.params.id;

  Bet.destroy({
    where: { id: id },
  })
    .then((num) => {
      if (num == 1) {
        res.send({
          message: "Bet was deleted successfully!",
        });
      } else {
        res.send({
          message: `Cannot delete bet with id=${id}. Maybe bet was not found?`,
        });
      }
    })
    .catch((err) => {
      res.status(500).send({
        message: `Could not delete bet with id=${id}`,
      });
    });
};

exports.deleteAll = (req, res) => {
  Bet.destroy({
    where: {},
    truncate: false,
  })
    .then((nums) => {
      res.send({ message: `${nums} Bets were deleted successfully!` });
    })
    .catch((err) => {
      res.status(500).send({
        message: err.message || "Some error occurred while removing all bets.",
      });
    });
};

exports.findAllNewBets = (req, res) => {
  Bet.findAll({ where: { unbet: true } })
    .then((data) => {
      res.send(data);
    })
    .catch((err) => {
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving new bets.",
      });
    });
};
