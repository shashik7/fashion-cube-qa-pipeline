const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken')
const config = require('../configs/jwt-config')
const ensureAuthenticated = require('../modules/ensureAuthenticated')
const User = require('../models/User');
const Cart = require('../models/Cart');
const CartClass = require('../modules/Cart')
const Product = require('../models/Product')
const Variant = require('../models/Variant')
const TypedError = require('../modules/ErrorHandler')


//POST /signin  (registration)
router.post('/signin', async function (req, res, next) {
  const { fullname, email, password, verifyPassword } = req.body
  req.checkBody('fullname', 'fullname is required').notEmpty();
  req.checkBody('email', 'Email is required').notEmpty();
  req.checkBody('password', 'Password is required').notEmpty();
  req.checkBody('verifyPassword', 'verifyPassword is required').notEmpty();
  let missingFieldErrors = req.validationErrors();
  if (missingFieldErrors) {
    let err = new TypedError('signin error', 400, 'missing_field', { errors: missingFieldErrors })
    return next(err)
  }
  req.checkBody('email', 'Email is not valid').isEmail();
  req.checkBody('password', 'Passwords have to match').equals(req.body.verifyPassword);
  let invalidFieldErrors = req.validationErrors()
  if (invalidFieldErrors) {
    let err = new TypedError('signin error', 400, 'invalid_field', { errors: invalidFieldErrors })
    return next(err)
  }

  try {
    const existingUser = await User.getUserByEmail(email)
    if (existingUser) {
      let err = new TypedError('signin error', 409, 'invalid_field', { message: "user is existed" })
      return next(err)
    }
    var newUser = new User({ fullname, password, email })
    await User.createUser(newUser)
    res.json({ message: 'user created' })
  } catch (err) { return next(err) }
});

//POST /login
router.post('/login', async function (req, res, next) {
  const { email, password } = req.body.credential || {}
  if (!email || !password) {
    let err = new TypedError('login error', 400, 'missing_field', { message: "missing username or password" })
    return next(err)
  }

  try {
    const user = await User.getUserByEmail(email)
    if (!user) {
      let err = new TypedError('login error', 403, 'invalid_field', { message: "Incorrect email or password" })
      return next(err)
    }
    const isMatch = await User.comparePassword(password, user.password)
    if (isMatch) {
      let token = jwt.sign({ email }, config.secret, { expiresIn: '7d' })
      res.status(201).json({
        user_token: {
          user_id: user.id,
          user_name: user.fullname,
          token,
          expire_in: '7d'
        }
      })
    } else {
      let err = new TypedError('login error', 403, 'invalid_field', { message: "Incorrect email or password" })
      return next(err)
    }
  } catch (err) { return next(err) }
})

//GET cart
router.get('/:userId/cart', ensureAuthenticated, async function (req, res, next) {
  try {
    const cart = await Cart.getCartByUserId(req.params.userId)
    if (cart.length < 1) {
      let err = new TypedError('cart error', 404, 'not_found', { message: "create a cart first" })
      return next(err)
    }
    return res.json({ cart: cart[0] })
  } catch (err) { return next(err) }
})

//POST cart
router.post('/:userId/cart', ensureAuthenticated, async function (req, res, next) {
  try {
    const userId = req.params.userId
    const { productId, increase, decrease } = req.body

    const c = await Cart.getCartByUserId(userId)
    let oldCart = new CartClass(c[0] || { userId })

    // no cart, no product — create empty cart
    if (c.length < 1 && !productId) {
      const resultCart = await Cart.createCart(oldCart.generateModel())
      return res.status(201).json({ cart: resultCart })
    }

    // Try to find product
    const product = await Product.findById(productId).catch(() => null)
    if (product) {
      if (decrease) oldCart.decreaseQty(product.id)
      else if (increase) oldCart.increaseQty(product.id)
      else oldCart.add(product, product.id)
      const newCart = oldCart.generateModel()
      const result = await Cart.updateCartByUserId(userId, newCart)
      return res.status(200).json({ cart: result })
    }

    // Try variant
    const variant = await Variant.getVariantByID(productId).catch(() => null)
    if (variant) {
      const p = await Product.getProductByID(variant.productID)
      let color = variant.color ? "- " + variant.color : ""
      let size = variant.size ? "- " + variant.size : ""
      variant.title = p.title + " " + color + size
      variant.price = p.price
      if (decrease) oldCart.decreaseQty(variant.id)
      else if (increase) oldCart.increaseQty(variant.id)
      else oldCart.add(variant, variant.id)
      const newCart = oldCart.generateModel()
      const result = await Cart.updateCartByUserId(userId, newCart)
      return res.status(200).json({ cart: result })
    }

    // Neither product nor variant found
    let err = new TypedError('/cart', 400, 'invalid_field', { message: "invalid request body" })
    return next(err)
  } catch (err) { return next(err) }
})

//PUT cart
router.put('/:userId/cart', ensureAuthenticated, async function (req, res, next) {
  try {
    const userId = req.params.userId
    const { productId, color, size } = req.body.product

    const c = await Cart.getCartByUserId(userId)
    let oldCart = new CartClass(c[0] || {})
    const p = await Product.getProductByID(productId)
    let newCart = oldCart.add(p, productId, { color, size })

    if (c.length > 0) {
      const result = await Cart.updateCartByUserId(userId, {
        items: newCart.items,
        totalQty: newCart.totalQty,
        totalPrice: newCart.totalPrice,
        userId
      })
      return res.json(result)
    } else {
      const cartDoc = new Cart({
        items: newCart.items,
        totalQty: newCart.totalQty,
        totalPrice: newCart.totalPrice,
        userId
      })
      const resultCart = await Cart.createCart(cartDoc)
      return res.status(201).json(resultCart)
    }
  } catch (err) { return next(err) }
})

module.exports = router;