const fs = require("fs");

exports.readDatabase = (path) =>
  new Promise((resolve, reject) => {
    fs.readFile(path, { encoding: "utf-8" }, (err, data) => {
      try {
        if (err) reject(Error("Cannot load the database"));
        const studentsInfo = data
          .split("\n")
          .filter((line) => line)
          .slice(1);
        return resolve({
          studentsInfo,
        });
      } catch (err) {
        return reject(Error("Cannot load the database"));
      }
    });
  });
