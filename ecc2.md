# ECC2

We exploit the almost smoothness of the order of the elliptic curve group. When
we run Pohlig-Hellman, using the results from CRT on the small primes produces a
solution with a modulus larger than our bound, so it must be our desired
solution.

For my challenge, I had the following parameters.

    M  = 93556643250795678718734474880013829509320385402690660619699653921022012489089
    A  = 66001598144012865876674115570268990806314506711104521036747533612798434904785
    B  = 25255205054024371783896605039267101837972419055969636393425590261926131199030
    P  = (56027910981442853390816693056740903416379421186644480759538594137486160388926, 65533262933617146434438829354623658858649726233622196512439589744498050226926)
    nP = (23587034938374768786301222539991586253242655515915989431307599794801199763403, 58594847963665471409425852843336835079537055974819057000500246625851308476858)

Under Pohlig-Hellman, we acquire the following modular equations.

    n = 2 (mod 4)
    n = 0 (mod 3)
    n = 0 (mod 5)
    n = 0 (mod 7)
    n = 130 (mod 137)
    n = 530 (mod 593)
    n = 5173 (mod 24337)
    n = 24401 (mod 25589)
    n = 1403911 (mod 3637793)
    n = 2087121 (mod 5733569)

I would also like to point out that for my particular problem, when we compare
the orders of P and nP, we obtain |P| = 210 * |nP|, which immediately gives us
the first 4 modular equations.
