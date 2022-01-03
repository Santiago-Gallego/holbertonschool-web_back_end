const readDatabase = require("../utils");

class StudentsController {
  static async getAllStudents(req, res) {
    try {
      const data = await readDatabase();
      return res.send(data.join(""));
    } catch (error) {
      return res.status(500).send(error.message);
    }
  }

  static async getAllStudentsByMajor(req, res) {
    const { major } = req.params;
    let data, msg;
    try {
      data = await readDatabase();
    } catch (error) {
      return res.status(500).send(error.message);
    }
    switch (major) {
      case "CS":
        msg = data[1].split("List");
        return res.send(`List${msg[1].slice(0, -1)}`);

      case "SWE":
        msg = data[2].split("List");
        return res.send(`List${msg[1].slice(0, -1)}`);

      default:
        return res.status(500).send("Major parameter must be CS or SWE");
    }
  }
}
module.exports = StudentsController;
