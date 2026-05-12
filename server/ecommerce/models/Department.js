var mongoose = require('mongoose');

var departmentSchema = mongoose.Schema({
  departmentName: { type: String, index: true },
  categories:     { type: String }
});

var Department = module.exports = mongoose.model('Department', departmentSchema);

module.exports.getAllDepartments = function (query) {
  return Department.find(query);
}

module.exports.getDepartmentById = function (id) {
  return Department.findById(id);
}