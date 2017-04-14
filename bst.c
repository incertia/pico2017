#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct bst {
  struct bst *left;
  struct bst *right;
  char c;
} bst;

char _[] = "yuoteavpxqgrlsdhwfjkzi_cmbn";

bst *bst_make(bst *root, char c) {
  if (root) {
    if (c <= root->c) root->left = bst_make(root->left, c);
    else root->right = bst_make(root->right, c);
  } else {
    root = malloc(sizeof(bst));
    root->left = NULL;
    root->right = NULL;
    root->c = c;
  }
  return root;
}

int main() {
  bst *v = NULL;
  char *s = "DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD";
  int i = 0;

  for (; i < strlen(_); i++) v = bst_make(v, _[i]);

  while (*s) {
    bst *r = v;
    while (*s != 'D') {
      if (*s == 'L') r = r->left;
      else if (*s == 'R') r = r->right;
      s++;
    }
    putchar(r->c);
    s++;
  }
  putchar('\n');
  return 0;
}
