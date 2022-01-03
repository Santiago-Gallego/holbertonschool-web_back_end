const { Router } = require("express");
const AppController = require("../controllers/AppController");
const StudentsController = require("../controllers/StudentsController");

const router = Router();

router.get("/", AppController.getHome);
router.get("/students", StudentsController.getAllStudents);
router.get("/students/:major", StudentsController.getAllStudentsByMajor);

module.exports = router;
