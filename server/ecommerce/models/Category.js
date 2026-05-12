var mongoose = require('mongoose');

var categorySchema = mongoose.Schema({
  categoryName: { type: String, index: true }
});

var Category = module.exports = mongoose.model('Categories', categorySchema);

module.exports.getAllCategories = function () {
  return Category.find();
}

module.exports.getCategoryById = function (id) {
  return Category.findById(id);
}