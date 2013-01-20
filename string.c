#include <stdio.h>

int main()
{
int i;
char str1[10], str2[10];

printf("Enter a word: ");
scanf("%s", str1);
for(i=0; str1[i]; i++)
str2[i] = str1[i];

printf("The second string is: %s\n", str2);

printf("Enter another word: ");
scanf("%s", str1);

printf("First string is: %s, Second string is: %s\n", str1, str2);

return 0;



}
