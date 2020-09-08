module.exports = (sequelize, Sequelize) => {
  const Bet = sequelize.define("bet", {
    date: {
      type: Sequelize.DATEONLY,
      required: true,
    },
    home: {
      type: Sequelize.STRING,
      required: true,
    },
    away: {
      type: Sequelize.STRING,
      required: true,
    },
    odds: {
      type: Sequelize.REAL,
      required: true,
    },
    home_bet: {
      type: Sequelize.REAL,
    },
    kick_off: {
      type: Sequelize.REAL,
      required: true,
    },
    unbet: {
      type: Sequelize.BOOLEAN,
    },
  });

  return Bet;
};
