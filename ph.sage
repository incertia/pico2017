def PH(P, Q):
    n = P.order()
    fl = n.factor()
    rl = list()
    ml = list()

    print "{} = {}".format(n, fl)

    for p, e in fl:
        pe = p ^ e
        # print "solving {} = {}^{}".format(pe, p, e)

        # generator and point for subgroup of order di
        gi = (n // pe) * P
        hi = (n // pe) * Q

        # solve li * gi = hi

        x = list()
        x.append(0)
        y = (p ^ (e - 1)) * gi    # this should have order p

        # print "y has order {}".format(y.order())

        for k in xrange(e):
            hk = (p ^ (e - 1 - k)) * (-x[k] * gi + hi)
            # print "hk has order {}".format(hk.order())

            # perform bsgs to solve dk * y = hk
            dk = discrete_log(hk, y, operation='+')
            x.append(x[k] + (p ^ k) * dk)

        print "l = {} (mod {})".format(x[e], pe)
        rl.append(x[e])
        ml.append(pe)
    return crt(rl, ml)

F = FiniteField(93556643250795678718734474880013829509320385402690660619699653921022012489089)
E = EllipticCurve(F, [66001598144012865876674115570268990806314506711104521036747533612798434904785, 25255205054024371783896605039267101837972419055969636393425590261926131199030])
P = E.point((56027910981442853390816693056740903416379421186644480759538594137486160388926, 65533262933617146434438829354623658858649726233622196512439589744498050226926))
Q = E.point((23587034938374768786301222539991586253242655515915989431307599794801199763403, 58594847963665471409425852843336835079537055974819057000500246625851308476858))

print PH(P, Q)
