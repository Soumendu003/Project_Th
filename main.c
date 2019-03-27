#include "example.h"
int main() {
/* Test the gcd() function */
{
printf("%d\n", gcd(128,72));
printf("%d\n", gcd(37,42));
}
/* Test the replace() function */
{
char s[] = "Skipping along unaware of the unspeakable peril.";
int nrep;
nrep = replace(s,' ','-');
printf("%d\n", nrep);
printf("%s\n",s);
}
/* Test the distance() function */
{
Point a = { 10.0, 15.0 };
Point b = { 13.0, 11.0 };
printf("%0.2f\n", distance(&a,&b));
}
}
