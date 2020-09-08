module.exports = (sequelize, Sequelize) => {
  const Bet = sequelize.define("bet", {
    date: {
      type: Sequelize.DATEONLY,
      required: true,
    },
    home: {
      type: Sequelize.STRING,
      required: true,
      allowNull: false,
    },
    away: {
      type: Sequelize.STRING,
      required: true,
      allowNull: false,
    },
    odds: {
      type: Sequelize.REAL,
      required: true,
      allowNull: false,
    },
    home_bet: {
      type: Sequelize.REAL,
    },
    kick_off: {
      type: Sequelize.STRING,
      required: true,
      allowNull: false,
    },
    unbet: {
      type: Sequelize.BOOLEAN,
    },
  });

  return Bet;
};
