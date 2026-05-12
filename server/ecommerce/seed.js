/**
 * FC-001 | Fashion Cube - Database Seed Script
 * Seeds products, variants, departments, and categories into local MongoDB.
 * Run: node seed.js
 */

const mongoose = require('mongoose');
const Product = require('./models/Product');
const Variant = require('./models/Variant');
const Department = require('./models/Department');
const Category = require('./models/Category');
const User = require('./models/User');

const MONGO_URI = 'mongodb://127.0.0.1:27017/fashion-cube';

const departments = [
  { departmentName: 'Men', categories: 'Shirts,Pants,Jackets' },
  { departmentName: 'Women', categories: 'Dresses,Tops,Skirts' },
  { departmentName: 'Kids', categories: 'Boys,Girls,Babies' },
];

const categories = [
  { categoryName: 'Shirts' },
  { categoryName: 'Pants' },
  { categoryName: 'Jackets' },
  { categoryName: 'Dresses' },
  { categoryName: 'Tops' },
];

const products = [
  { title: 'Classic White Shirt', description: 'A clean white dress shirt', department: 'Men', category: 'Shirts', price: 29.99, color: 'White', size: 'M', quantity: 50, imagePath: '/images/white-shirt.jpg', date: Date.now() },
  { title: 'Blue Denim Shirt', description: 'Casual blue denim shirt', department: 'Men', category: 'Shirts', price: 39.99, color: 'Blue', size: 'L', quantity: 30, imagePath: '/images/denim-shirt.jpg', date: Date.now() },
  { title: 'Black Slim Pants', description: 'Slim fit black trousers', department: 'Men', category: 'Pants', price: 49.99, color: 'Black', size: 'M', quantity: 25, imagePath: '/images/black-pants.jpg', date: Date.now() },
  { title: 'Summer Floral Dress', description: 'Light floral summer dress', department: 'Women', category: 'Dresses', price: 59.99, color: 'Multicolor', size: 'S', quantity: 40, imagePath: '/images/floral-dress.jpg', date: Date.now() },
  { title: 'Red Evening Dress', description: 'Elegant red evening dress', department: 'Women', category: 'Dresses', price: 89.99, color: 'Red', size: 'M', quantity: 15, imagePath: '/images/red-dress.jpg', date: Date.now() },
  { title: 'Grey Casual Top', description: 'Comfortable grey casual top', department: 'Women', category: 'Tops', price: 24.99, color: 'Grey', size: 'S', quantity: 60, imagePath: '/images/grey-top.jpg', date: Date.now() },
  { title: 'Winter Jacket', description: 'Warm winter jacket', department: 'Men', category: 'Jackets', price: 129.99, color: 'Navy', size: 'L', quantity: 20, imagePath: '/images/winter-jacket.jpg', date: Date.now() },
  { title: 'Kids Blue Shirt', description: 'Comfortable kids blue shirt', department: 'Kids', category: 'Shirts', price: 14.99, color: 'Blue', size: 'XS', quantity: 45, imagePath: '/images/kids-shirt.jpg', date: Date.now() },
];

async function seed() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log('✅ Connected to MongoDB');

    // Clear existing data
    await Promise.all([
      Product.deleteMany({}),
      Variant.deleteMany({}),
      Department.deleteMany({}),
      Category.deleteMany({}),
    ]);
    console.log('🧹 Cleared existing data');

    // Seed departments & categories
    await Department.insertMany(departments);
    await Category.insertMany(categories);
    console.log(`✅ Seeded ${departments.length} departments, ${categories.length} categories`);

    // Seed products
    const insertedProducts = await Product.insertMany(products);
    console.log(`✅ Seeded ${insertedProducts.length} products`);

    // Seed variants for first 2 products
    const variants = [
      { productID: insertedProducts[0]._id.toString(), color: 'White', size: 'S', quantity: 10, imagePath: '/images/white-shirt-s.jpg' },
      { productID: insertedProducts[0]._id.toString(), color: 'White', size: 'L', quantity: 10, imagePath: '/images/white-shirt-l.jpg' },
      { productID: insertedProducts[1]._id.toString(), color: 'Blue', size: 'M', quantity: 15, imagePath: '/images/denim-shirt-m.jpg' },
    ];
    await Variant.insertMany(variants);
    console.log(`✅ Seeded ${variants.length} variants`);

    // Seed test user
    const existingUser = await User.getUserByEmail('testuser@fashioncube.com');
    if (!existingUser) {
      const newUser = new User({ fullname: 'Test User', email: 'testuser@fashioncube.com', password: 'Test@12345' });
      await User.createUser(newUser);
      console.log('✅ Seeded test user: testuser@fashioncube.com / Test@12345');
    } else {
      console.log('ℹ️  Test user already exists');
    }

    console.log('\n🎉 Database seeded successfully!');
    console.log(`\nTest credentials:\n  Email:    testuser@fashioncube.com\n  Password: Test@12345`);
  } catch (err) {
    console.error('❌ Seed error:', err.message);
  } finally {
    await mongoose.disconnect();
    process.exit(0);
  }
}

seed();
