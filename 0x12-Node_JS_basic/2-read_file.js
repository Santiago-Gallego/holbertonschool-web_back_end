const fs = require('fs');

const countStudents = (path) => {
  const fields = {};
  let data;

  try {
    data = fs.readFileSync(path);
  } catch (error) {
    throw new Error('Cannot load the database');
  }

  data = data.toString().split('\n');
  data = data.filter((element) => element.length > 0);
  data.shift();

  data.forEach((element) => {
    if (element.length > 0) {
      const row = element.split(',');
      if (row[3] in fields) {
        fields[row[3]].push(row[0]);
      } else {
        fields[row[3]] = [row[0]];
      }
    }
  });
  console.log(`Number of students: ${data.length}`);
  for (const field in fields) {
    if (field) {
      const list = fields[field];
      console.log(`Number of students in ${field}: ${list.length}. List: ${list.toString().replace(/,/g, ', ')}`);
    }
  }
};

module.exports = countStudents;
