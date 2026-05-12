// ============================================================================
// FC-001 | Fashion Cube QA Automation - k6 Performance Test
// Requirement: Full e-commerce user journey performance validation
// Thresholds: p95 < 500ms, error rate < 1%
// ============================================================================

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// ---- Custom Metrics ----
const errorRate = new Rate('errors');
const productListTrend = new Trend('product_list_duration');
const productDetailTrend = new Trend('product_detail_duration');
const loginTrend = new Trend('login_duration');
const cartTrend = new Trend('cart_duration');
const searchTrend = new Trend('search_duration');

// ---- Configuration ----
const BASE_URL = __ENV.API_BASE_URL || 'http://localhost:3000';
const TEST_EMAIL = __ENV.TEST_USER_EMAIL || 'testuser@fashioncube.com';
const TEST_PASSWORD = __ENV.TEST_USER_PASSWORD || 'Test@12345';

// ---- Load Stages (Ramp-up / Steady / Ramp-down) ----
export const options = {
    stages: [
        { duration: '1m', target: 10 },   // Ramp-up to 10 VUs
        { duration: '3m', target: 25 },   // Ramp-up to 25 VUs
        { duration: '5m', target: 50 },   // Peak: 50 VUs steady
        { duration: '3m', target: 25 },   // Ramp-down to 25 VUs
        { duration: '1m', target: 0 },    // Ramp-down to 0
    ],
    thresholds: {
        'http_req_duration': ['p(95)<500', 'p(99)<1000'],
        'http_req_failed': ['rate<0.01'],
        'errors': ['rate<0.01'],
        'product_list_duration': ['p(95)<400'],
        'product_detail_duration': ['p(95)<300'],
        'login_duration': ['p(95)<500'],
        'cart_duration': ['p(95)<500'],
        'search_duration': ['p(95)<500'],
    },
};

// ---- Helper: Make authenticated request ----
function getAuthToken() {
    const loginPayload = JSON.stringify({
        credential: {
            email: TEST_EMAIL,
            password: TEST_PASSWORD,
        },
    });

    const loginRes = http.post(`${BASE_URL}/users/login`, loginPayload, {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'FC-001_LOGIN' },
    });

    loginTrend.add(loginRes.timings.duration);

    if (loginRes.status === 201) {
        try {
            const body = JSON.parse(loginRes.body);
            return {
                token: body.user_token.token,
                userId: body.user_token.user_id,
            };
        } catch (e) {
            errorRate.add(1);
            return null;
        }
    }
    errorRate.add(1);
    return null;
}

// ---- Main Test Scenario ----
export default function () {
    // FC-001: Scenario 1 – Browse Products (All Users)
    group('FC-001_PERF_browse_products', function () {
        const res = http.get(`${BASE_URL}/products`, {
            tags: { name: 'FC-001_GET_PRODUCTS' },
        });

        productListTrend.add(res.timings.duration);

        const success = check(res, {
            'FC-001: products status is 200': (r) => r.status === 200,
            'FC-001: products response time < 500ms': (r) => r.timings.duration < 500,
            'FC-001: products body contains array': (r) => {
                try {
                    return JSON.parse(r.body).products.length > 0;
                } catch (e) {
                    return false;
                }
            },
        });

        if (!success) errorRate.add(1);
        else errorRate.add(0);

        // Get product detail for first product
        if (res.status === 200) {
            try {
                const products = JSON.parse(res.body).products;
                if (products.length > 0) {
                    const productId = products[Math.floor(Math.random() * products.length)]._id;
                    const detailRes = http.get(`${BASE_URL}/products/${productId}`, {
                        tags: { name: 'FC-001_GET_PRODUCT_DETAIL' },
                    });

                    productDetailTrend.add(detailRes.timings.duration);

                    check(detailRes, {
                        'FC-001: product detail status is 200': (r) => r.status === 200,
                        'FC-001: product detail response time < 300ms': (r) => r.timings.duration < 300,
                    });
                }
            } catch (e) {
                errorRate.add(1);
            }
        }
    });

    sleep(1);

    // FC-001: Scenario 2 – Search Products
    group('FC-001_PERF_search_products', function () {
        const searchTerms = ['shirt', 'Men', 'Women', 'dress', 'jacket'];
        const term = searchTerms[Math.floor(Math.random() * searchTerms.length)];

        const res = http.get(`${BASE_URL}/search?query=${term}`, {
            tags: { name: 'FC-001_SEARCH' },
        });

        searchTrend.add(res.timings.duration);

        check(res, {
            'FC-001: search status is 200 or 404': (r) => r.status === 200 || r.status === 404,
            'FC-001: search response time < 500ms': (r) => r.timings.duration < 500,
        });
    });

    sleep(1);

    // FC-001: Scenario 3 – Get Categories & Departments
    group('FC-001_PERF_navigation_data', function () {
        const catRes = http.get(`${BASE_URL}/categories`, {
            tags: { name: 'FC-001_GET_CATEGORIES' },
        });

        check(catRes, {
            'FC-001: categories status is 200': (r) => r.status === 200,
            'FC-001: categories response time < 300ms': (r) => r.timings.duration < 300,
        });

        const deptRes = http.get(`${BASE_URL}/departments`, {
            tags: { name: 'FC-001_GET_DEPARTMENTS' },
        });

        check(deptRes, {
            'FC-001: departments status is 200': (r) => r.status === 200,
            'FC-001: departments response time < 300ms': (r) => r.timings.duration < 300,
        });
    });

    sleep(1);

    // FC-001: Scenario 4 – Login & Cart Operations (Authenticated)
    group('FC-001_PERF_authenticated_flow', function () {
        const auth = getAuthToken();

        if (auth) {
            // Get cart
            const cartRes = http.get(`${BASE_URL}/users/${auth.userId}/cart`, {
                headers: { authorization: auth.token },
                tags: { name: 'FC-001_GET_CART' },
            });

            cartTrend.add(cartRes.timings.duration);

            check(cartRes, {
                'FC-001: cart status is 200 or 404': (r) => r.status === 200 || r.status === 404,
                'FC-001: cart response time < 500ms': (r) => r.timings.duration < 500,
            });

            // Add product to cart
            const productsRes = http.get(`${BASE_URL}/products`, {
                tags: { name: 'FC-001_GET_PRODUCTS_FOR_CART' },
            });

            if (productsRes.status === 200) {
                try {
                    const products = JSON.parse(productsRes.body).products;
                    if (products.length > 0) {
                        const productId = products[Math.floor(Math.random() * products.length)]._id;
                        const addCartRes = http.post(
                            `${BASE_URL}/users/${auth.userId}/cart`,
                            JSON.stringify({
                                userId: auth.userId,
                                productId: productId,
                            }),
                            {
                                headers: {
                                    'Content-Type': 'application/json',
                                    authorization: auth.token,
                                },
                                tags: { name: 'FC-001_ADD_TO_CART' },
                            }
                        );

                        check(addCartRes, {
                            'FC-001: add to cart status is 200/201': (r) => r.status === 200 || r.status === 201,
                            'FC-001: add to cart response time < 500ms': (r) => r.timings.duration < 500,
                        });
                    }
                } catch (e) {
                    errorRate.add(1);
                }
            }
        }
    });

    sleep(2);
}

// ---- Summary Handler ----
export function handleSummary(data) {
    return {
        'reports/k6_summary.json': JSON.stringify(data, null, 2),
    };
}
