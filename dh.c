#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>

typedef struct pair_t {
  size_t j;
  mpz_t z;
} pair_t;

int pcmp(pair_t *a, pair_t *b)
{
  return mpz_cmp(a->z, b->z);
}

int pcmp2(mpz_t *a, pair_t *b)
{
  return mpz_cmp(*a, b->z);
}

void f(mpz_t g, mpz_t h, mpz_t p, mpz_t n, mpz_t x)
{
   unsigned long int i;
   size_t j;
   mpz_t N;
   pair_t* set;
   mpz_t y;
   mpz_t inv;
   mpz_init(N);
   mpz_sqrt(N, n);
   // mpz_add_ui(N, N, 1);

   printf("m = %s\n", mpz_get_str(NULL, 10, N));

   set = malloc(mpz_get_ui(N) * sizeof(pair_t));

   puts("gen");

   /* compute {(j, g^j)} */
   set[0].j = 0;
   mpz_init_set_ui(set[0].z, 1);
   for (j = 1 ; j < mpz_get_ui(N); j++) {
      set[j].j = j;
      mpz_init(set[j].z);
      mpz_mul(set[j].z, set[j - 1].z, g);
      mpz_mod(set[j].z, set[j].z, p);
      // printf("g^%lu %% p = %s\n", j, mpz_get_str(NULL, 10, set[j].z));
   }

   /* sort the values (j , g^j) with respect to g^j */
   puts("sort");
   qsort(set, mpz_get_ui(N), sizeof(pair_t), pcmp);

   /* compute g^(-N) */
   mpz_init_set(inv, g);
   mpz_powm(inv, inv, N, p);
   mpz_invert(inv, inv, p);

   // printf("g^(-N) %% p = %s\n", mpz_get_str(NULL, 10, inv));

   mpz_init_set(y, h);

   puts("search");
   /* find the elements in the two sequences */
   for (i = 0; i < mpz_get_ui(N); i++) {
      pair_t *_;
      /* find y in the set */
      _ = bsearch(y, set, mpz_get_ui(N), sizeof(pair_t), pcmp2);
      if (_) {
         mpz_mul_ui(N, N, i);
         mpz_add_ui(N, N, _->j);
         /* return i * N + j */
         mpz_set(x, N) ;
         puts("found");
         printf("i = %lu\n", i);
         printf("j = %lu\n", _->j);
         break;
      } else {
        /* y = y * g^(-N) */
        mpz_mul(y, y, inv);
        mpz_mod(y, y, p);
      }
   }
}

int main()
{
  mpz_t g, A, p, n, a;
  mpz_init_set_str(g, "41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977", 10);
  mpz_init_set_str(A, "118273972112639120186970068947944724773714770611796145560317038505039351377800437911584090954295445815108415228076067419564334318734103894856428799576147989726840111816497674618324630523684004675727128364154281009934628997112127793757633331795515579928803348552388657916707518365689221161578522942036857923828", 10);
  mpz_init_set_str(p, "174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843", 10);
  mpz_init_set_str(n, "70368744177664", 10);
  // mpz_init_set_str(g, "10", 10);
  // mpz_init_set_str(A, "522", 10);
  // mpz_init_set_str(p, "541", 10);
  // mpz_init_set_str(n, "256", 10);
  mpz_init_set_str(a, "0", 10);
  f(g, A, p, n, a);
  printf("a = %s\n", mpz_get_str(NULL, 10, a));
  return 0;
}
