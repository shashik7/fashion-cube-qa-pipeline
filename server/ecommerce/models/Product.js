var mongoose = require('mongoose');

var productSchema = mongoose.Schema({
  imagePath: { type: String },
  title: { type: String },
  description: { type: String },
  department: { type: String },
  category: { type: String },
  price: { type: Number },
  color: { type: String },
  size: { type: String },
  quantity: { type: Number },
  date: { type: Number }
});

var Product = module.exports = mongoose.model('Product', productSchema);

module.exports.getAllProducts = function (query, sort) {
  return Product.find(query).sort(sort);
}

module.exports.getProductByDepartment = function (query, sort) {
  return Product.find(query).sort(sort);
}

module.exports.getProductByCategory = function (query, sort) {
  return Product.find(query).sort(sort);
}

module.exports.getProductByTitle = function (query, sort) {
  return Product.find(query).sort(sort);
}

module.exports.filterProductByDepartment = function (department) {
  let regexp = new RegExp(`${department}`, 'i');
  var query = { department: { $regex: regexp } };
  return Product.find(query);
}

module.exports.filterProductByCategory = function (category) {
  let regexp = new RegExp(`${category}`, 'i');
  var query = { category: { $regex: regexp } };
  return Product.find(query);
}

module.exports.filterProductByTitle = function (title) {
  let regexp = new RegExp(`${title}`, 'i');
  var query = { title: { $regex: regexp } };
  return Product.find(query);
}

module.exports.getProductByID = function (id) {
  return Product.findById(id);
}
