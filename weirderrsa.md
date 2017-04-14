# WeirderRSA

Some idiot spoiled this problem on stack exchange.

We know that `e * d = 1 (mod (p - 1)(q - 1))`, so we also have `e * d = 1 (mod p - 1)`
, or `e * dp = 1 (mod p - 1)`. This means `a ^ (e * dp) = a (mod p)` for
some arbitrary choice of `a`. Now that we have two multiples of `p`, we can
compute their GCD to get `p`.

    p = gcd(pow(a, e * dp, n) - a, n)

As long as the exponentiation doesn't give us precisely `a`, we are a winner.
