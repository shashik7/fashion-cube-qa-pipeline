var express = require('express');
var router = express.Router();
const ensureAuthenticated = require('../modules/ensureAuthenticated')
const Product = require('../models/Product')
const Variant = require('../models/Variant')
const Department = require('../models/Department')
const Category = require('../models/Category')
const TypedError = require('../modules/ErrorHandler')
const Cart = require('../models/Cart');
const CartClass = require('../modules/Cart')
const paypal_config = require('../configs/paypal-config')
const paypal = require('paypal-rest-sdk')


//GET /products
router.get('/products', async function (req, res, next) {
  try {
    const { query, order } = categorizeQueryString(req.query)
    const products = await Product.getAllProducts(query, order)
    if (products.length < 1) {
      return res.status(404).json({ message: "products not found" })
    }
    res.json({ products })
  } catch (e) { e.status = 406; return next(e) }
});

//GET /products/:id
router.get('/products/:id', async function (req, res, next) {
  try {
    const item = await Product.getProductByID(req.params.id)
    if (!item) {
      let err = new TypedError('product', 404, 'not_found', { message: 'product not found' })
      return next(err)
    }
    res.json({ product: item })
  } catch (e) { e.status = 404; return next(e) }
});

//GET /variants
router.get('/variants', async function (req, res, next) {
  try {
    let { productId } = req.query
    const variants = productId
      ? await Variant.getVariantProductByID(productId)
      : await Variant.getAllVariants()
    return res.json({ variants })
  } catch (e) { return next(e) }
})

//GET /variants/:id
router.get('/variants/:id', ensureAuthenticated, async function (req, res, next) {
  try {
    const variants = await Variant.getVariantByID(req.params.id)
    res.json({ variants })
  } catch (e) { return next(e) }
})

//GET /departments
router.get('/departments', async function (req, res, next) {
  try {
    const departments = await Department.getAllDepartments(req.query)
    res.status(200).json({ departments })
  } catch (e) { return next(e) }
})

//GET /categories
router.get('/categories', async function (req, res, next) {
  try {
    const categories = await Category.getAllCategories()
    res.json({ categories })
  } catch (e) { return next(e) }
})

//GET /search?
router.get('/search', async function (req, res, next) {
  try {
    const { query, order } = categorizeQueryString(req.query)

    // Search by department
    query['department'] = query['query']
    delete query['query']
    let p = await Product.getProductByDepartment(query, order)
    if (p.length > 0) return res.json({ products: p })

    // Search by category
    query['category'] = query['department']
    delete query['department']
    p = await Product.getProductByCategory(query, order)
    if (p.length > 0) return res.json({ products: p })

    // Search by title
    query['title'] = query['category']
    delete query['category']
    p = await Product.getProductByTitle(query, order)
    if (p.length > 0) return res.json({ products: p })

    // Search by ID
    const id = query['title']
    const item = await Product.getProductByID(id).catch(() => null)
    if (item) return res.json({ products: item })

    let error = new TypedError('search', 404, 'not_found', { message: "no product exist" })
    return next(error)
  } catch (e) { return next(e) }
})

// GET filter
router.get('/filter', async function (req, res, next) {
  try {
    let result = {}
    let query = req.query.query

    const byDept = await Product.filterProductByDepartment(query)
    if (byDept.length > 0) result['department'] = generateFilterResultArray(byDept, 'department')

    const byCat = await Product.filterProductByCategory(query)
    if (byCat.length > 0) result['category'] = generateFilterResultArray(byCat, 'category')

    const byTitle = await Product.filterProductByTitle(query)
    if (byTitle.length > 0) result['title'] = generateFilterResultArray(byTitle, 'title')

    if (Object.keys(result).length > 0) return res.json({ filter: result })

    let error = new TypedError('search', 404, 'not_found', { message: "no product exist" })
    return next(error)
  } catch (e) { return next(e) }
})

//GET /checkout
router.get('/checkout/:cartId', ensureAuthenticated, async function (req, res, next) {
  try {
    const cartId = req.params.cartId
    const frontURL = 'https://zack-ecommerce-reactjs.herokuapp.com'

    const c = await Cart.getCartById(cartId)
    if (!c) {
      let err = new TypedError('/checkout', 400, 'invalid_field', { message: 'cart not found' })
      return next(err)
    }

    const items_arr = new CartClass(c).generateArray()
    const paypal_list = items_arr.map(i => ({
      name: i.item.title,
      price: i.item.price,
      currency: "CAD",
      quantity: i.qty
    }))

    const create_payment_json = {
      intent: "sale",
      payer: { payment_method: "paypal" },
      redirect_urls: {
        return_url: frontURL + '/success_page',
        cancel_url: frontURL + '/cancel_page'
      },
      transactions: [{
        item_list: { items: paypal_list },
        amount: { currency: "CAD", total: c.totalPrice },
        description: "This is the payment description."
      }]
    }

    paypal.configure(paypal_config)
    paypal.payment.create(create_payment_json, function (error, payment) {
      if (error) { console.log(JSON.stringify(error)); return next(error) }
      for (const link of payment.links) {
        if (link.rel === 'approval_url') res.json(link.href)
      }
    })
  } catch (e) { return next(e) }
})

//GET /payment/success
router.get('/payment/success', ensureAuthenticated, function (req, res, next) {
  var paymentId = req.query.paymentId;
  var payerId = { payer_id: req.query.PayerID };
  paypal.payment.execute(paymentId, payerId, function (error, payment) {
    if (error) { console.error(JSON.stringify(error)); return next(error) }
    if (payment.state == 'approved') {
      console.log('payment completed successfully')
      res.json({ payment })
    } else {
      console.log('payment not successful')
    }
  })
})

function generateFilterResultArray(products, targetProp) {
  let result_set = new Set()
  for (const p of products) result_set.add(p[targetProp])
  return Array.from(result_set)
}

function categorizeQueryString(queryObj) {
  let query = {}
  let order = {}
  for (const i in queryObj) {
    if (queryObj[i]) {
      if (i === 'order') { order['sort'] = queryObj[i]; continue }
      if (i === 'range') {
        let range_arr = [], query_arr = []
        if (queryObj[i].constructor === Array) {
          for (const r of queryObj[i]) {
            range_arr = r.split('-')
            query_arr.push({ price: { $gt: range_arr[0], $lt: range_arr[1] } })
          }
        }
        if (queryObj[i].constructor === String) {
          range_arr = queryObj[i].split('-')
          query_arr.push({ price: { $gt: range_arr[0], $lt: range_arr[1] } })
        }
        Object.assign(query, { $or: query_arr })
        delete query[i]
        continue
      }
      query[i] = queryObj[i]
    }
  }
  return { query, order }
}

module.exports = router;
