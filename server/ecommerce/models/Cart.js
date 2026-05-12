const mongoose = require('mongoose')

CartSchema = mongoose.Schema({
  items: { type: Object },
  totalQty: { type: Number },
  totalPrice: { type: Number },
  userId: { type: String }
})

var Cart = module.exports = mongoose.model('Cart', CartSchema)

module.exports.getCartByUserId = function (uid) {
  return Cart.find({ userId: uid })
}

module.exports.getCartById = function (id) {
  return Cart.findById(id)
}

module.exports.updateCartByUserId = async function (userId, newCart) {
  const existing = await Cart.find({ userId: userId })
  if (existing.length > 0) {
    return Cart.findOneAndUpdate(
      { userId: userId },
      {
        $set: {
          items: newCart.items,
          totalQty: newCart.totalQty,
          totalPrice: newCart.totalPrice,
          userId: userId
        }
      },
      { new: true }
    )
  } else {
    return newCart.save()
  }
}

module.exports.updateCartByCartId = async function (cartId, newCart) {
  return Cart.findByIdAndUpdate(cartId, { $set: newCart }, { new: true })
}

module.exports.createCart = function (newCart) {
  return newCart.save()
}