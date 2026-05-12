var mongoose = require('mongoose');

var variantSchema = mongoose.Schema({
  productID: { type: String },
  imagePath: { type: String },
  color:     { type: String },
  size:      { type: String },
  quantity:  { type: Number },
  title:     { type: String },
  price:     { type: Number }
});

var Variant = module.exports = mongoose.model('Variant', variantSchema);

module.exports.getVariantByID = function (id) {
  return Variant.findById(id);
}

module.exports.getVariantProductByID = function (id) {
  return Variant.find({ productID: id });
}

module.exports.getAllVariants = function () {
  return Variant.find();
}