# FC-001 | Fashion Cube E-Commerce – Full User Journey

## Jira ID: FC-001

## Summary
As a user, I can browse products, view product details, register/login,
manage my shopping cart, filter/search products by category/department,
and checkout via PayPal.

## Acceptance Criteria

### User Registration (AC-01)
- User can register with fullname, email, password, and confirm password
- Email must be valid format
- Password and confirm password must match
- Duplicate email registration is rejected (HTTP 409)
- All fields are required (HTTP 400 on missing)

### User Login (AC-02)
- User can login with valid email and password
- JWT token is returned on success (expires in 7 days)
- Invalid credentials return HTTP 403
- Missing fields return HTTP 400

### Product Browsing (AC-03)
- Home page displays all products
- User can view single product details by clicking a product
- Products display: image, title, description, price, department, category

### Product Search & Filter (AC-04)
- User can search products by query string
- Search cascades: department → category → title → id
- User can filter products by department, category, title
- Products can be sorted by price range

### Category Navigation (AC-05)
- User can navigate to shop pages by department/category
- Navigation menu displays all departments with their categories

### Shopping Cart (AC-06)
- Authenticated user can add products to cart
- User can increase/decrease item quantities
- User can add product variants (color, size) to cart
- Cart displays subtotal, taxes, shipping, and total
- Empty cart shows empty cart image
- Cart is persisted per user in database

### Checkout (AC-07)
- Authenticated user can initiate PayPal checkout
- Payment redirects to PayPal approval URL
- Successful payment returns payment confirmation

## Technical Notes
- Frontend: React 16, Redux, React-Router v5, Bootstrap 4, Axios
- Backend: Express.js, MongoDB (Mongoose), JWT, bcrypt, PayPal REST SDK
- Auth: JWT token passed via `authorization` header
