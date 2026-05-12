var mongoose = require('mongoose');
var bcrypt = require('bcryptjs');

var userSchema = mongoose.Schema({
    email: { type: String, index: true },
    password: { type: String },
    fullname: { type: String },
    admin: { type: String },
    cart: { type: Object }
});

var User = module.exports = mongoose.model('User', userSchema);

module.exports.createUser = async function (newUser) {
    const salt = await bcrypt.genSalt(10);
    const hash = await bcrypt.hash(newUser.password, salt);
    newUser.password = hash;
    return newUser.save();
}

module.exports.getUserByEmail = function (email) {
    return User.findOne({ email: email });
}

module.exports.getUserById = function (id) {
    return User.findById(id);
}

module.exports.comparePassword = function (givenPassword, hash) {
    return bcrypt.compare(givenPassword, hash);
}

module.exports.getAllUsers = function () {
    return User.find();
}