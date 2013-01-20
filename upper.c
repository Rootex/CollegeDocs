#include <stdio.h>
void capt(char array[100]){
int i, big=0, small=0;
  
for(i=0; array[i] != '\0'; i++){
if(array[i] >= 'A' && array[i] <= 'Z') big++; 
else
small++;
}
if(big > small)
printf("True\n");
else
printf("False\n");
}

int main()
{
int i;
char string[100];


printf("Enter a line: ");
gets(string);


capt(string);

return 0;
}
